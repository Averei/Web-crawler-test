import time
import re
import requests
from bs4 import BeautifulSoup, SoupStrainer
import pandas as pd
import time

SESSION = requests.Session()


""" This is the Google Analytics Selector Section """


class myGoogleSession:

    def fetch_google_xml(self, URL, country_code):
        format_url = f"{URL}{country_code}"
        response = SESSION.get(format_url)
        soup = BeautifulSoup(response.text, 'xml',
                             parse_only=SoupStrainer('channel'))
        return soup


google_session = myGoogleSession()


def google_trends_retriever(URL, country_code):
    xml_soup = google_session.fetch_google_xml(URL, country_code)
    print(country_code)
    return[(title.text, re.sub("[+,]", "", traffic.text))
           for title, traffic in zip(xml_soup.find_all('title')[1:],
                                     xml_soup.find_all('ht:approx_traffic'))]


def create_pdTrend(data):
    check_panda = pd.DataFrame(
        google_trends_retriever(GoogleURL, data),
        columns=['Title', 'Score']
    )
    if len(check_panda) == 0:
        print('No available data')
    else:
        return check_panda


""" This is the Country Code Selector Section """


country_code_list = []


class myCountryCodeSession:
    def fetch_countrycode_html(self, URL):
        response = SESSION.get(URL)
        soup = BeautifulSoup(response.text, 'html.parser',
                             parse_only=SoupStrainer('table'))
        return soup


countryCode_session = myCountryCodeSession()


def parse_row(url):
    rows = countryCode_session.fetch_countrycode_html(url)
    _rows = rows.findChildren(['td', 'tr'])
    for row in _rows:
        cells = row.findChildren('td')[2:3]
        for cell in cells:
            value = cell.string
            country_code_list.append(value[:2])
    return None


def create_pdCountryCode(country_code):
    return pd.DataFrame({'Country_Code': country_code})


def iterate_List(data):
    i = 1
    while i <= 239:
        selected_CountryCode = get_data_fromList(i)
        print(create_pdTrend(selected_CountryCode))
        i += 1
    else:
        print('Has reach the end of i ' + str(i))


def get_data_fromList(num):
    key = num-1
    for i in country_code_list[key:num]:
        return str(i)


if __name__ == '__main__':
    """ URL Section """
    GoogleURL = "https://trends.google.com/trends/trendingsearches/daily/rss?geo="
    CountryCodeURL = "https://countrycode.org/"
    """-------------"""
    start = time.time()
    print("hello")

    """Country Code Section """
    parse_row(CountryCodeURL)
    """---------------------"""

    """Google Analytics Section """
    iterate_List(country_code_list)
    """-------------------------"""
    end = time.time()
    print(end - start)

"""Unused code """


# def create_dict(url):
#     country_code = create_pdCountryCode(parse_row(url))
#     return dict(country_code.Country_Code)


# def iterate_CountryCode(url):
#     key_return = create_dict(url)[:-1]
#     return [(the_key)
#             for the_key in key_return.items()]


"""Unused code """
