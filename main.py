import os
import smtplib

from bs4 import BeautifulSoup
from dotenv import load_dotenv
import requests

load_dotenv()

practice_url = "https://appbrewery.github.io/instant_pot/"
live_url = "https://www.amazon.com/dp/B075CYMYK6?psc=1&ref_=cm_sw_r_cp_ud_ct_FM9M699VKHTT47YD50Q6"

# ------- Add headers to the request -------
header = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
    "Dnt": "1",
    "Priority": "u=1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Sec-Gpc": "1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
}

response = requests.get(practice_url, headers=header)
soup = BeautifulSoup(response.content, "html.parser")
# print(soup.prettify())

# Find the html element with the price
price = soup.find(class_="a-offscreen").get_text()
# print(price)

# Remove dollar sign
price_without_currency = price.split("$")[1]

# Convert to floating point number
price_as_float = float(price_without_currency)

# ------- Send mail -------
title = soup.find(id="productTitle").get_text().strip()

BUY_PRICE = 100
EMAIL = os.getenv("EMAIL")
PASS = os.getenv("PASS")
SMTP_ADDR = os.getenv("SMTP_ADDR")

if price_as_float < BUY_PRICE:
    message = f"{title} is on a sale for {price}!"

    with smtplib.SMTP(SMTP_ADDR, port=587) as connection:
        connection.ehlo()
        connection.starttls()
        result = connection.login(EMAIL, PASS)
        connection.sendmail(
            from_addr=EMAIL,
            to_addrs=EMAIL,
            msg=f"Subject:Amazon Price Alert!\n\n{message}\n{practice_url}".encode("utf-8")
        )