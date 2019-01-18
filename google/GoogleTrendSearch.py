import re
from functools import partial

import requests
import pandas as pd
from bs4 import BeautifulSoup, SoupStrainer


class GoogleAnalysis:
    def __init__(self, url):
        session = requests.Session()
        self.get_url = partial(session.get, url)

    def _fetch_xml(self, country_code):
        response = self.get_url(params={'geo': country_code})
        return BeautifulSoup(
            response.content, 'xml',
            parse_only=SoupStrainer('channel'))

    def _retrieve_trends(self, country_code):
        soup = self._fetch_xml(country_code)
        titles = soup.find_all('title')[1:]
        traffics = soup.find_all('ht:approx_traffic')
        return [
            (title.text, re.sub("[+,]", "", traffic.text))
            for title, traffic in zip(titles, traffics)
        ]

    def trends(self, country_code):
        df = pd.DataFrame(
            self._retrieve_trends(country_code),
            columns=['Title', 'Score'],
        )
        df['Country Code'] = country_code
        return df


def country_codes(url='https://countrycode.org/'):
    response = requests.get(url)
    soup = BeautifulSoup(
        response.text, 'lxml',
        parse_only=SoupStrainer('table'))
    return [
        cell.string[:2]
        for row in soup.find_all(['td', 'tr'])
        # Some rows don't define row.find_all('td')[2] so filter out
        for cell in row.find_all('td')[2:3]
    ]


def main(url):
    google = GoogleAnalysis(url)
    codes = country_codes()
    return pd.concat([
        google.trends(country_code)
        # Country codes are repeated twice, we only need them once
        for country_code in codes[:len(codes) // 2]
    ])


if __name__ == '__main__':
    import time
    start = time.perf_counter()
    print('Hello!')
    trends = main(
        'https://trends.google.com/trends/trendingsearches/daily/rss')
    print(trends.to_string(index=False))
    print(time.perf_counter() - start)
