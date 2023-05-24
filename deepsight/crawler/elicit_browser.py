from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

import os
import time
from copy import copy
from typing import Dict, Any, List
import sys

from dotenv import load_dotenv
load_dotenv()

class ElicitSearchDriver:
    """A class to interact with elicit.org using Selenium."""

    def __init__(self) -> None:
        self.setup_browser()
        self.login_elicit()
        self.cmd_ctrl = Keys.COMMAND if sys.platform == "darwin" else Keys.CONTROL
        self.first_search: bool = True

    def setup_browser(self) -> None:
        """Sets up the browser with headless mode and opens the elicit.org login page."""
        options = Options()
        options.add_argument("--headless=new")
        self.driver: webdriver.Chrome = webdriver.Chrome(options=options)
        self.driver.get("http://elicit.org/login")

    def login_elicit(self) -> None:
        """Logs into elicit.org using the provided email and password."""
        print("Initiating...", end=" ")

        self._wait_and_click('//button[contains(@class,"firebaseui-idp-button")]')

        self._wait_and_send_keys('//input[@type="email"]', os.environ["ELICIT_EMAIL"])

        self._click_element('//button[@type="submit"]')

        self._wait_and_send_keys('//input[@type="password"]', os.environ["ELICIT_PASSWORD"])

        self._click_element('//button[@type="submit"]')

        print("done!")

    def process_string(self, table_text: str) -> List[Dict[str, Any]]:
        """Parses a string containing article data and returns a list of dictionaries with article information.

        Args:
            input_str: A string containing article data.

        Returns:
            A list of dictionaries containing article information.
        """
        articles: List[Dict[str, Any]] = []
        splited_input = copy(table_text).split("\n")
        splited_input = list(filter(lambda a: a not in ["DOI", "PDF"], splited_input))

        i: int = 0
        while i < len(splited_input):
            (
                title,
                author,
                journal,
                pub_year,
                citations,
                abstract,
                i,
            ) = self._parse_article(splited_input, i)
            assert isinstance(pub_year, int), f"Publication year is not a number: {pub_year}"
            assert isinstance(citations, int), f"Citations is not a number: {citations}"
            article_data: Dict[str, Any] = {
                "title": title,
                "author": author,
                # "journal": journal,       # Disabled due to low priority.
                "publication_year": pub_year,
                "citations": citations,
                "summary": abstract,
            }
            articles.append(article_data)

        return articles

    def _get_results(self) -> List[Dict[str, Any]]:
        """Retrieves search results from the website and processes them.

        Returns:
            A list of dictionaries containing article information.
        """

        self._wait_for_text('//tbody[contains(@class,"cursor-pointer")]', "")

        self._wait_for_element('//div[contains(@class,"whitespace-pre-line")]')

        table = self._wait_for_non_empty_table()

        while True:
            try:
                result = self.process_string(table.text)
                break
            except Exception:
                time.sleep(0.3)
        result = self.process_string(table.text)
        return result

    def search(self, query: str) -> List[Dict[str, Any]]:
        """Searches for a query on elicit.org and returns the results.

        Args:
            query: A string containing the search query.

        Returns:
            A list of dictionaries containing article information.
        """

        print(f'Searching query "{query}"...', end=" ")
        self._wait_for_element('//input[contains(@class,"chakra-input")]')

        # Clear previous search
        self._clear_search_input()

        self.driver.find_element(By.XPATH, '//input[contains(@class,"chakra-input")]').send_keys(query)

        if self.first_search:
            self.first_search = False
            self._click_element('//button[text()="Search"]')
        else:
            self._click_element('//button[contains(@class,"chakra-button")]')

        result = self._get_results()
        print("done!")
        return result

    def _wait_and_click(self, xpath: str) -> None:
        self._wait_for_element(xpath)
        self._click_element(xpath)

    def _wait_and_send_keys(self, xpath: str, keys: str) -> None:
        self._wait_for_element(xpath)
        self.driver.find_element(By.XPATH, xpath).send_keys(keys)

    def _wait_for_element(self, xpath: str) -> None:
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))

    def _wait_for_text(self, xpath: str, text: str) -> None:
        WebDriverWait(self.driver, 10).until(EC.text_to_be_present_in_element((By.XPATH, xpath), text))

    def _click_element(self, xpath: str) -> None:
        self.driver.find_element(By.XPATH, xpath).click()

    def _get_first_two_authors(self, authors_str):
        authors_list = authors_str.split(", ")
        return ", ".join(authors_list[:2]) if len(authors_list) > 2 else authors_str

    def _parse_article(self, data: List[str], i: int) -> tuple:
        title = data[i]
        author = self._get_first_two_authors(data[i + 1])
        if data[i + 2].isdigit():
            i -= 1
            journal = ""
        else:
            journal = data[i + 2]
        pub_year = int(data[i + 3])
        try:
            citations = int(data[i + 4][:-10])
        except Exception:
            i += 1
            citations = int(data[i + 4][:-10])
        abstract = data[i + 5]
        i += 6

        return title, author, journal, pub_year, citations, abstract, i

    def _clear_search_input(self) -> None:
        search_input = self.driver.find_element(By.XPATH, '//input[contains(@class,"chakra-input")]')
        search_input.click()
        search_input.send_keys(self.cmd_ctrl + "a")
        search_input.send_keys(Keys.DELETE)

    def _wait_for_non_empty_table(self) -> webdriver.Chrome:
        while True:
            table = self.driver.find_element(By.XPATH, '//tbody[contains(@class,"cursor-pointer")]')
            if table.text != "":
                break
            time.sleep(0.3)
        return table
