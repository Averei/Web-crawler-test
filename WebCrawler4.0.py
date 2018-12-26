from requests import get
from bs4 import BeautifulSoup
from pprint import pprint
import pandas as pd
import numpy as np
from pprint import pprint
import itertools
import operator
from time import sleep
from tabulate import tabulate
from threading import Event


url = 'https://forum.lowyat.net/ReviewsandGuides'

l1 = []
l2 = []
l3 = []
l4 = []
l5 = []


def getContentFromURL(_url):
    try:
        response = get(_url)
        html_soup = BeautifulSoup(response.text, 'lxml')
        # type(html_soup)
        return html_soup
    except Exception as e:
        print('Error.getContentFromURL:', e)
        return None


def iterateThroughPages(_lastindexpost, _postperpage, _url):
    indices = '/+'
    index = 0
    for i in range(index, _lastindexpost):
        try:
            while i <= _lastindexpost:
                print(2)
                print(i)
                for table in get(_url):
                    print(3)
                    if table != None:
                        print(4)
                        new_getPostPerPage = i + _postperpage
                        print('value is: ' + str(new_getPostPerPage))
                        newlink = f'{url}{indices}{new_getPostPerPage}'
                        print(5)
                        # print(newlink)
                        bs_link = getContentFromURL(newlink)
                        # print(bs_link)
                        print(6)
                        extractDataFromRow1(
                            bs_link, 'td', 'row1', 'valign', 'middle')
                        sleep(0.5)
                        print(7)
                    i += _postperpage
                    print('current index is: ' + str(i))
                    if i > _lastindexpost:
                        # print(l)
                        print('No more available post to retrieve')
                        return
        except Exception as e:
            print('Error.iterateThroughPages:', e)
            return None


def extractDataFromRow1(_url, _tag, _classname, _alignment, _position):
    try:
        for container in _url.find_all(_tag, {'class': _classname, _alignment: _position}):
            # get data from topic title in table cell
            topic = container.select_one(
                'a[href^="/topic/]"').text.replace("\n", "")
            description = container.select_one(
                'div.desc').text.replace("\n", "")
            if topic and description is not None:
                d1 = topic
                d2 = description
                if description is '':
                    d2 = 'No Data'
                l1.append(d1)
                l2.append(d2)
                # print(d)
            else:
                None
    except Exception as e:
        print('Error.extractDataFromRow1:', e)
        return None


def extractDataFromRow2(_url, _tag, _classname, _alignment, _position):
    try:
        for container in _url.find_all(_tag, {'class': _classname, _alignment: _position}):
            # print(container)
            # get data from topic title in table cell
            print(0)
            # pprint(container)
            replies = container.select_one(
                'a[href^="javascript:]"').text
            print(1)
            print('there are ' + replies + ' replies')
            print(2)
            topic_starter = container.next_sibling.text
            print(3)
            print('the owner of this topic is ' + topic_starter)
            for total_view in container.find('a', href=True, style=True):
                #total_view = container.select_one(style="background-color:").text
                #total_view = container.find(("td")["style"])
                #total_view = container.next_sibling.find_next_sibling/next_sibling
                print(4)
                print(total_view)
            if replies and topic_starter is not None:
                d1 = replies
                d2 = topic_starter
                l4.append(d2)
                l3.append(d1)
            else:
                print('no data')
                None
    except Exception as e:
        print('Error.extractDataFromRow2:', e)
        return None


# extractDataFromRow1(getContentFromURL(url), 'td')
# pprint(l1)
# def finalOutputPandas(_data):
# print(extractDataFromRow2(getContentFromURL(
#   url), 'td', 'row2', 'align', 'center'))
# pprint(extractDataFromRow1(getContentFromURL(
#    url), 'td', 'row1', 'valign', 'middle'))
print(extractDataFromRow2(getContentFromURL(
    url), 'td', 'row2', 'align', 'center'))
# print(iterateThroughPages(300, 30, url))
# test_pd=pd.DataFrame({'Title': l1, 'Description': l2})
# pprint(test_pd)
# test_pd.to_csv('out.csv')
# # print(len(board_array))
# df = pd.DataFrame(l)
# df.columns = ['Description', 'Title']
# pprint(df.head(90))
