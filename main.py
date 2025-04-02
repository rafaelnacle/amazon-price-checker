import os
import smtplib

from bs4 import BeautifulSoup
from dotenv import load_dotenv
import requests

load_dotenv()

practice_url = "https://appbrewery.github.io/instant_pot/"
live_url = "https://www.amazon.com/dp/B075CYMYK6?psc=1&ref_=cm_sw_r_cp_ud_ct_FM9M699VKHTT47YD50Q6"

response = requests.get(practice_url)
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