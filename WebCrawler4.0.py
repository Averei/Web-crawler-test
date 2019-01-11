import requests
from bs4 import BeautifulSoup, SoupStrainer
from itertools import islice
import pandas as pd
from time import sleep

SESSION = requests.Session()


def get_table_rows(base_url, posts_per_page=30):
    """Continously yield rows from the posts table.

    Requests a new page only when needed.
    """
    start_at = 0
    while True:
        print(f'current page index is: {start_at // posts_per_page + 1}')
        response = SESSION.get(base_url + f"/+{start_at}")
        print(response)
        soup = BeautifulSoup(response.text, 'lxml',
                             parse_only=SoupStrainer("table", {"cellspacing": "1"}))
        yield from soup.find_all("tr")
        start_at += posts_per_page


def parse_row(row):
    """Get info from a row"""
    columns = row.select("td")
    try:
        if not columns or columns[0]["class"] in (["darkrow1"], ["nopad"]):
            return
    except KeyError:  # first column has no class
        return
    try:
        title = row.select_one(
            "td.row1 a[href^=/topic/]").text.strip() or "No Data"
        description = row.select_one(
            "td.row1 div.desc").text.strip() or "No Data"
        replies = row.select_one("td:nth-of-type(4)").text.strip() or "No Data"
        topic_starter = row.select_one(
            'td:nth-of-type(5)').text.strip() or "No Data"
        total_views = row.select_one(
            'td:nth-of-type(6)').text.strip() or "No Data"
        print(title)
        sleep(0.3)
    except AttributeError:  # something is None
        return
    return {"Title": title,
            "Description": description,
            "Replies": replies,
            "Topic Starter": topic_starter,
            "Total Views": total_views}


def parse_rows(url):
    """Filter out rows that could not be parsed"""
    yield from filter(None, (parse_row(row) for row in get_table_rows(url)))


if __name__ == "__main__":
    url = 'https://forum.lowyat.net/ReviewsandGuides'
    max_posts = 1770
    df = pd.DataFrame.from_records(islice(parse_rows(url), max_posts))
    print(df)
