import time
import re
import requests
from bs4 import BeautifulSoup, SoupStrainer
import pandas as pd

SESSION = requests.Session()


class mySession:

    def fetch_xml(self, URL, country_code):  # Gets the <html> structure from the website #
        format_url = f"{URL}{country_code}"
        response = SESSION.get(format_url)
        soup = BeautifulSoup(response.text, 'xml',
                             parse_only=SoupStrainer('channel'))
        return soup


session = mySession()


def trends_retriever(URL, country_code):
    xml_soup = session.fetch_xml(URL, country_code)
    return[(title.text, re.sub("[+,]", "", traffic.text))
           for title, traffic in zip(xml_soup.find_all('title')[1:],
                                     xml_soup.find_all('ht:approx_traffic'))]


def create_pdTrend():
    return pd.DataFrame(
        trends_retriever(URL, 'US'),
        columns=['Title', 'Score']
    )


if __name__ == '__main__':
    URL = "https://trends.google.com/trends/trendingsearches/daily/rss?geo="
    print(create_pdTrend())
