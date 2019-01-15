import requests
from bs4 import BeautifulSoup, SoupStrainer
import pandas as pd

list_topic = []
list_time = []
list_comment = []

SESSION = requests.Session()


def get_response(url):  # Gets the <html> structure from the website #
    response = SESSION.get(url)
    soup = BeautifulSoup(response.text, 'lxml',
                         parse_only=SoupStrainer('ul', {'class': 'posts posts-archive'}))
    return soup


def iteration(url, max_page=52):
    starting_page = 1
    while starting_page <= max_page:
        ## formats the new URL etc (https://paultan.org/topics/test-drive-reviews/page/1) ##
        new_url = url + f"page/{starting_page}"
        data = get_response(new_url)
        get_reviews(data)
        ## iteration starts ##
        starting_page += 1


def get_reviews(response):
    for container in response('article'):
        title = container.h2.a.text
        time = container.time.text
        comment = container.p.a.text
        list_topic.append(title)
        list_time.append(time)
        list_comment.append(comment)
    else:
        None


def create_pdReview():
    return pd.DataFrame({'Title': list_topic, 'Comment': list_comment, 'Time': list_time})


if __name__ == '__main__':
    URL = 'https://paultan.org/topics/test-drive-reviews/'
    iteration(URL)
    df = create_pdReview()
    df.to_csv("PaulTan.csv")
