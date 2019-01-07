from requests import get
from bs4 import BeautifulSoup
from pprint import pprint
import pandas as pd
from time import sleep


url = 'https://forum.lowyat.net/ReviewsandGuides'

list_topic = []
list_description = []
list_replies = []
list_topicStarted = []
list_totalViews = []


def getContentFromURL(_url):
    try:
        response = get(_url)
        html_soup = BeautifulSoup(response.text, 'lxml')
        return html_soup
    except Exception as e:
        print('Error.getContentFromURL:', e)
        return None


def iterateThroughPages(_lastindexpost, _postperpage, _url):
    indices = '/+'
    index = 0
    for i in range(index, _lastindexpost):
        print('Getting data from ' + url)
        try:
            extractDataFromRow1(getContentFromURL(
                _url), 'td', 'row1', 'valign', 'middle')
            extractDataFromRow2(getContentFromURL(_url))
            print('current page index is: ' + str(index))
            print(_url)
            while i <= _lastindexpost:
                for table in get(_url):
                    if table != None:
                        new_getPostPerPage = i + _postperpage
                        newlink = f'{url}{indices}{new_getPostPerPage}'
                        print(newlink)
                        bs_link = getContentFromURL(newlink)
                        extractDataFromRow1(
                            bs_link, 'td', 'row1', 'valign', 'middle')
                        extractDataFromRow2(bs_link)
                        # threading to prevent crash. Waits 0.5 secs before executing
                        sleep(0.5)
                    i += _postperpage
                    print('current page index is: ' + str(i))
                    if i > _lastindexpost:
                        # If i gets more than the input page(etc 1770) halts
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
                'a[href^="/topic/"]').text.replace("\n", "")
            description = container.select_one(
                'div.desc').text.replace("\n", "")
            if topic or description is not None:
                dict_topic = topic
                dict_description = description
                if dict_description is '':
                    dict_description = 'No Data'
                    # list_description.append(dict_description)
                    #so no empty string#
                list_topic.append(dict_topic)
                list_description.append(dict_description)
            else:
                None
    except Exception as e:
        print('Error.extractDataFromRow1:', e)
        return None


def extractDataFromRow2(_url):
    try:
        for container in _url.select('table[cellspacing="1"] > tr')[2:32]:
            replies = container.select_one('td:nth-of-type(4)').text.strip()
            topic_started = container.select_one(
                'td:nth-of-type(5)').text.strip()
            total_views = container.select_one(
                'td:nth-of-type(6)').text.strip()
            if replies or topic_started or total_views is not None:
                dict_replies = replies
                dict_topicStarted = topic_started
                dict_totalViews = total_views
                if dict_replies is '':
                    dict_replies = 'No Data'
                elif dict_topicStarted is '':
                    dict_topicStarted = 'No Data'
                elif dict_totalViews is '':
                    dict_totalViews = 'No Data'
                list_replies.append(dict_replies)
                list_topicStarted.append(dict_topicStarted)
                list_totalViews.append(dict_totalViews)
            else:
                print('no data')
                None
    except Exception as e:
        print('Error.extractDataFromRow2:', e)
        return None


# limit to 1740
print(iterateThroughPages(1740, 30, url))
new_panda = pd.DataFrame(
    {'Title': list_topic, 'Description': list_description,
     'Replies': list_replies, 'Topic Starter': list_topicStarted, 'Total Views': list_totalViews})
pprint(new_panda)
new_panda.to_csv("output.csv")
