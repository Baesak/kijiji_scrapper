"""Scrapper for Kijiji Property Rent"""

from time import sleep
from datetime import datetime as dtime
from alchemy import session
from model import Property
from logger import logging
import requests
from bs4 import BeautifulSoup


class KijijiScrapper:
    """Scraps all data from page and make records in db"""

    def __init__(self, link: str):
        self.link = link
        self.page = 1
        self._create_link()

    def _create_link(self):
        """Creates link with specified page"""

        link_list = self.link.split("/")
        link_list.insert(-1, f"page-{self.page}")

        self.link = "/".join(link_list)

    def parse_page(self):
        """Scraps page (including pagination)"""

        while True:
            print(f"Processing page {self.page}...")

            r = self._get_page()
            soup = BeautifulSoup(r.content, "html.parser")
            elements = soup.select("div[class=clearfix]")

            if len(elements) == 0:
                sleep(50)
            else:
                self._write_in_db(elements)

                if not soup.find("a", title="Next"):
                    break

                self.page += 1
                self._create_link()

        print("Done!")

    def _get_page(self):
        """Connects to page"""

        try:
            return requests.get(self.link)

        except requests.exceptions.RequestException as error:
            print("Connection problems!")
            logging.error(str(error))
            exit()

    def _write_in_db(self, elements):
        """Makes records in db """

        for element in elements:
            new_property = Property(**self._get_attrs(element))
            session.add(new_property)

            session.commit()

    def _get_attrs(self, element) -> dict:
        """Selects the attributes that are
         needed for the SQLAlchemy model"""

        location_spans = element.find("div", class_="location").find_all("span")
        location, date = [span.text for span in location_spans]
        currency, price = self._get_price_and_currency(
            element.find("div", class_="price").contents[0])

        attrs_dict = {
            "title": element.a.text,
            "description": element.find("div", class_="description").contents[0],
            "price": price,
            "currency": currency,
            "beds": element.find("span", class_="bedrooms").text.lstrip("\nBeds: "),
            "picture": element.find("picture").img["data-src"]
            if element.find("picture") else '',
            "location": location,
            "date": date if "ago" not in date
            else str(dtime.strftime(dtime.now().date(), "%d-%m-%Y"))
        }

        for key, value in attrs_dict.items():
            attrs_dict[key] = value.strip(" \n ") if value else None

        return attrs_dict

    @staticmethod
    def _get_price_and_currency(price: str) -> tuple:
        """Handles the price and returns the price and currency attribute"""

        currency_dict = {
            "$": "dollar",
            "€": "euro",
            "£": "pound"
        }
        price = price.strip(" \n ")

        if price[0] in currency_dict.keys():
            number = price[1:].replace(",", "")
            return currency_dict[price[0]], number
        if price == "Free":
            return None, '0'

        # if "Please Contact"
        return None, None
