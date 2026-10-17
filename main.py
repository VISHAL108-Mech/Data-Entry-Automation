"""Scrape property listings and submit each one to a Google Form."""

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from dotenv import load_dotenv
import os

load_dotenv()

URL = os.getenv("SITE_URL")
FORM_URL = os.getenv("FORM_URL")


def main():
    """Fetch listings, then submit each row to the form."""

    # Pull the page HTML and parse the listing data.
    try:
        r = requests.get(url=URL)
        data = r.text
        soup = BeautifulSoup(data, "html.parser")
    except Exception as e:
        print(f"Error fetching the webpage: {e}")
        return

    # Collect the price, address, and listing link for each property.
    prices = soup.find_all(name="span", class_="PropertyCardWrapper__StyledPriceLine")
    price_list = [price.text.replace("+", "/").split("/")[0] for price in prices]

    addresses = soup.find_all(name="address")
    address_list = [
        address.getText().replace(" | ", "").strip() for address in addresses
    ]

    links = soup.find_all(name="a", class_="StyledPropertyCardDataArea-anchor")
    link_list = [link.get("href") for link in links]

    # Start the browser and fill out one form per listing.
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=chrome_options)

    for i in range(len(price_list)):
        try:
            driver.get(url=FORM_URL)
        except Exception as e:
            print(f"Error occurred while navigating to the form: {e}")
            continue
        sleep(2)

        address_input = driver.find_element(
            By.XPATH,
            "//*[@id='mG61Hd']/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input",
        )
        price_input = driver.find_element(
            By.XPATH,
            "//*[@id='mG61Hd']/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input",
        )
        link_input = driver.find_element(
            By.XPATH,
            "//*[@id='mG61Hd']/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input",
        )
        button = driver.find_element(
            By.XPATH, "//*[@id='mG61Hd']/div[2]/div/div[3]/div[1]/div[1]/div/span/span"
        )

        address_input.send_keys(address_list[i])
        price_input.send_keys(price_list[i])
        link_input.send_keys(link_list[i])
        try:
            button.click()
        except Exception as e:
            print(f"Error occurred while clicking the submit button: {e}")


if __name__ == "__main__":
    main()
