import requests
import pandas as pd


URL1 = 'https://shopee.com.my/api/v2/recommendation/trending_searches_v2?limit=20&offset=0'
URL2 = 'https://shopee.com.my/api/v2/flash_sale/get_items?offset=0&limit=16&filter_soldout=true'
URL3 = 'https://shopee.com.my/api/v2/recommendation/top_products/meta_lite'
URL4 = 'https://shopee.com.my/api/v2/recommend_items/get?recommend_type=5&limit=60&offset=0'

SESSION = requests.Session()


def get_response(_url):
    response = SESSION.get(_url)
    return response


def get_daily_discoveries(response):
    response.raise_for_status()
    return[
        (item['name'], item['discount'], item['liked_count'], item['stock'])
        for item in response.json()['data']['items']
    ]


def get_trending_items(response):
    response.raise_for_status()
    return[
        (item['keyword'], item['score'])
        for item in response.json()['data']['items']
    ]


def get_shocking_sales(response):
    response.raise_for_status()
    return [
        (item['name'], item['price'], item['discount'], item['stock'])
        for item in response.json()['data']['items']
    ]


def get_top_products(response):
    response.raise_for_status()
    return[
        (item['name'])
        for item in response.json()['data']['categories']
    ]

# Trending Items


def create_pdTI():
    return pd.DataFrame(
        get_trending_items(get_response(URL1)),
        columns=['TI_Name', 'TI_Score']
    )
# Shocking Sales


def create_pdSS():
    return pd.DataFrame(
        get_shocking_sales(get_response(URL2)),
        columns=['SS_Name', 'SS_Price', 'SS_Discount', 'SS_Stock']
    )

# Top Product


def create_pdTP():
    return pd.DataFrame(
        get_top_products(get_response(URL3)),
        columns=['TP_Name']
    )


# Daily Discoveries


def create_pdDD():
    return pd.DataFrame(
        get_daily_discoveries(get_response(URL4)),
        columns=['DD_Name', 'DD_Discount', 'DD_Likes', 'DD_Stock']
    )


def create_CSV():
    ShockingSales = create_pdSS()
    DailyDiscoveries = create_pdDD()
    TrendingItems = create_pdTI()
    TopProduct = create_pdTP()
    return (ShockingSales.to_csv("ShockingSales.csv"),
            DailyDiscoveries.to_csv("DailyDiscoveries.csv"),
            TrendingItems.to_csv("TrendingItems.csv"),
            TopProduct.to_csv("TopProduct.csv"))


if __name__ == '__main__':
    create_CSV()
