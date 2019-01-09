from requests import get
import requests
import json
from time import sleep
import pandas as pd
from multiprocessing import Process


url = 'https://shopee.com.my/api/v2/recommendation/trending_searches_v2?limit=20&offset=0'
url2 = 'https://shopee.com.my/api/v2/flash_sale/get_items?offset=0&limit=16&filter_soldout=true'
#headers = {'User-Agent': 'Googlebot/2.1 (+http://www.google.com/bot.html)'}
list_keyword = []
list_score = []

list_name = []
list_price = []
list_discount = []
list_stock = []


def response(_url):
    try:
        response = get(_url)
        return response
    except Exception as e:
        print('Error.getContentFromURL:', e)
        return None


def getShockingSales():
    index = 0
    if response(url2).status_code is 200:
        print('Api Satus: ' + 'OK')
    else:
        print('API unable to access')
    json_data = response(url2).json()
    total_flashsale = 15
    for i in range(index, total_flashsale):
        print('Getting data from requested API... please wait a few seconds')
        while i <= total_flashsale:
            flash_name = json_data['data']['items'][i]['name']
            flash_price = json_data['data']['items'][i]['price']
            flash_discount = json_data['data']['items'][i]['discount']
            flash_stock = json_data['data']['items'][i]['stock']
            list_name.append(flash_name)
            list_price.append(flash_price)
            list_discount.append(flash_discount)
            list_stock.append(flash_stock)
            sleep(0.5)
            i += 1
        if i > total_flashsale:
            print('Shocking Sales.... Task completed')
            return


def getTrendingItems():
    index = 0
    if response(url).status_code is 200:
        print('API Status: ' + 'OK')
    else:
        print('API unable to access')
        return
    json_data = response(url).json()
    total_trending = json_data['data']['total']-1
    for i in range(index, total_trending):
        print('Getting data from requested API... please wait a few seconds')
        while i <= total_trending:
            keyword_trending = json_data['data']['items'][i]['keyword']
            trending_score = json_data['data']['items'][i]['score']
            list_keyword.append(keyword_trending)
            list_score.append(trending_score)
            sleep(0.5)
            i += 1
        if i > total_trending:
            print('Trending Items..... Task Completed')
            return


process_ShockingSales = Process(target=getShockingSales())
process_ShockingSales.start()

processTrendingItems = Process(target=getTrendingItems())
processTrendingItems.start()

process_ShockingSales.join()
processTrendingItems.join()

# getShockingSales()
toPandaShockingSales = pd.DataFrame({'Name': list_name, 'Price': list_price,
                                     'Discount': list_discount, 'Stock Available': list_stock})

toPandaTrendingItems = pd.DataFrame(
    {'Trending Topic': list_keyword, 'Trending Score': list_score})

print('Converting to Panda Frame....')
sleep(5)
print(toPandaShockingSales)
sleep(2)
toPandaShockingSales.to_csv("toPandaShockingSales.csv")
print('Saving to CSV file as /toPandaShockingSales.csv')
sleep(2)
print('/n')
print(toPandaTrendingItems)
toPandaTrendingItems.to_csv("toPandaTrendingItems.csv")
print('Saving to CSV file as /toPandaTrendingItems.csv')
