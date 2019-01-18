import requests
from bs4 import BeautifulSoup, SoupStrainer
import pandas as pd

SESSION = requests.Session()

list_a = []


class mySession:

    def fetch_xml(self, URL):  # Gets the <html> structure from the website #
        response = SESSION.get(URL)
        soup = BeautifulSoup(response.text, 'html.parser',
                             parse_only=SoupStrainer('table'))
        return soup


session = mySession()


def parse_row(_row):
    rows = session.fetch_xml(_row)
    _rows = rows.findChildren(['td', 'tr'])
    for row in _rows:
        cells = row.findChildren('td')[2:3]
        for cell in cells:
            value = cell.string
            list_a.append(value[:2])
    return None


def create_pdTrend(url):
    return pd.DataFrame({'Country_Code': list_a})


def iterate_List(data):
    i = 0
    while i < len(data):
        a = get_data_fromList(i)
        print(a)
        i += 1
    else:
        print('Has reach the end of i ' + str(i))


def get_data_fromList(num):
    key_iterate = num-1
    return[(i)
           for i in list_a[key_iterate:num]]


def create_dict(url):
    country_code = create_pdTrend(parse_row(url))
    return dict(country_code.Country_Code)


if __name__ == '__main__':
    URL = "https://countrycode.org/"
    parse_row(URL)
    print(iterate_List(list_a))
