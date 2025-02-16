from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
from serpapi import GoogleSearch
import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
load_dotenv()

def getRelevantLinks(query: str):
    try:
        params = {
            "engine": "google",
            "location":"India", 
            "q": query,
            "num": "3",
            "api_key": os.environ.get("SERP_API_KEY")
        }

        search = GoogleSearch(params)
        results = search.get_dict()
        organic_results = results["organic_results"]

        return organic_results
        
    except Exception as e:
        print(e)
        return getRelevantLinks(query)


def findMarket(market: str):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920x1080")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--disable-extensions")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)

    url = f"https://www.statista.com/outlook/"
    driver.get(url)
    time.sleep(1)
    accept_cookies_btn = driver.find_element(By.ID, "onetrust-accept-btn-handler")
    accept_cookies_btn.click()
    time.sleep(1)

    search_input = driver.find_element(By.CSS_SELECTOR, "input.marketingHubPageSearch__searchInput")
    search_input.send_keys(f"{market}\n")
    time.sleep(2)
    
    try:
        link_list = driver.find_element(By.CSS_SELECTOR, "ul.outlookSearchResults.scrollBox.pos-static.outlookSearchResults--small")
        search_results = link_list.find_elements(By.TAG_NAME, "a")
        
        for result in search_results:
            href = result.get_attribute("href")
            if href and "http" in href:
                driver.quit()
                print(href)
                return href

    except Exception as e:
        driver.quit()
        print(f"Error finding search results list: {e}")


def pageScrapper(url: str):
    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        return soup.get_text()

    except Exception as e:
        return None

