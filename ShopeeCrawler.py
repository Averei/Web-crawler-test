from requests import get
import requests
import json
from time import sleep
import pandas as pd
from multiprocessing import Process


url = 'https://shopee.com.my/api/v2/recommendation/trending_searches_v2?limit=20&offset=0'
url2 = 'https://shopee.com.my/api/v2/flash_sale/get_items?offset=0&limit=16&filter_soldout=true'
url3 = 'https://shopee.com.my/api/v2/recommendation/top_products/meta_lite'
url4 = 'https://shopee.com.my/api/v2/recommend_items/get?recommend_type=5&limit=60&offset=0'
#headers = {'User-Agent': 'Googlebot/2.1 (+http://www.google.com/bot.html)'}
# getTrendingItems
list_keyword = []
list_score = []

# getShockingSales
list_name = []
list_price = []
list_discount = []
list_stock = []

# getTopProduct
list_ProductName = []

# getDailyDiscoveries
list_dailyName = []
list_dailyDiscount = []
list_dailyLikes = []
list_dailyStock = []


def response(_url):
    try:
        response = get(_url)
        return response
    except Exception as e:
        print('Error.getContentFromURL:', e)
        return None


def getDailyDiscoveries():
    index = 0
    if response(url4).status_code is 200:
        print('Api Status: ' + 'Response Daily_Discoveries : [200]')
    else:
        print('API unable to access')
    json_data = response(url4).json()
    total_flashsale = len(json_data['data']['items'])
    total_flashsale -= 1
    for i in range(index, total_flashsale):
        print('Getting data from TopProducts... please wait a few seconds')
        while i <= total_flashsale:
            daily_name = json_data['data']['items'][i]['name']
            daily_discount = json_data['data']['items'][i]['discount']
            daily_likes = json_data['data']['items'][i]['liked_count']
            daily_stock = json_data['data']['items'][i]['stock']
            print(daily_name)
            list_dailyName.append(daily_name)
            list_dailyDiscount.append(daily_discount)
            list_dailyLikes.append(daily_likes)
            list_dailyStock.append(daily_stock)
            sleep(0.5)
            i += 1
        if i > total_flashsale:
            print('Daily Discoveries.... Task completed')
            return


def getTopProducts():
    index = 0
    if response(url3).status_code is 200:
        print('Api Status: ' + 'Response Top_Product : [200]')
    else:
        print('API unable to access')
    json_data = response(url3).json()
    total_flashsale = len(json_data['data']['categories'])
    total_flashsale -= 1
    for i in range(index, total_flashsale):
        print('Getting data from TopProducts... please wait a few seconds')
        while i <= total_flashsale:
            topProduct_name = json_data['data']['categories'][i]['name']
            print(topProduct_name)
            list_ProductName.append(topProduct_name)
            sleep(0.5)
            i += 1
        if i > total_flashsale:
            print('Top Products.... Task completed')
            return


def getShockingSales():
    index = 0
    if response(url2).status_code is 200:
        print('Api Status: ' + 'Response Shocking_Sales : [200]')
    else:
        print('API unable to access')
    json_data = response(url2).json()
    total_flashsale = len(json_data['data']['items'])
    total_flashsale -= 1
    for i in range(index, total_flashsale):
        print('Getting data from ShockingSales... please wait a few seconds')
        while i <= total_flashsale:
            flash_name = json_data['data']['items'][i]['name']
            flash_price = json_data['data']['items'][i]['price']
            flash_discount = json_data['data']['items'][i]['discount']
            flash_stock = json_data['data']['items'][i]['stock']
            print(flash_name)
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
        print('API Status: ' + 'Response Trending_Items : [200]')
    else:
        print('API unable to access')
        return
    json_data = response(url).json()
    total_trending = json_data['data']['total']-1
    for i in range(index, total_trending):
        print('Getting data from TrendingItems... please wait a few seconds')
        while i <= total_trending:
            keyword_trending = json_data['data']['items'][i]['keyword']
            print(keyword_trending)
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

processTopProducts = Process(target=getTopProducts())
processTopProducts.start()

processDailyDiscoveries = Process(target=getDailyDiscoveries())
processDailyDiscoveries.start()

process_ShockingSales.join()
processTrendingItems.join()
processTopProducts.join()
processDailyDiscoveries.join()

# getShockingSales()
toPandaShockingSales = pd.DataFrame({'Name': list_name, 'Price': list_price,
                                     'Discount': list_discount, 'Stock Available': list_stock})

toPandaTrendingItems = pd.DataFrame(
    {'Trending Topic': list_keyword, 'Trending Score': list_score})

toPanadaProcessTopProducts = pd.DataFrame({'Top Product': list_ProductName})

toPandaDailyDiscoveries = pd.DataFrame(
    {'Name': list_dailyName, 'Likes': list_dailyLikes, 'Discount': list_dailyDiscount, 'Stock': list_dailyStock})

print('Converting to Panda Frame....')
sleep(5)
print(toPandaShockingSales)
sleep(2)
# toPandaShockingSales.to_csv("toPandaShockingSales.csv")
print('Saving to CSV file as /toPandaShockingSales.csv')
sleep(2)
print('/n')
print(toPandaTrendingItems)
# toPandaTrendingItems.to_csv("toPandaTrendingItems.csv")
print('Saving to CSV file as /toPandaTrendingItems.csv')
sleep(2)
print(toPanadaProcessTopProducts)
print('/n')
# toPanadaProcessTopProducts.to_csv("toPanadaProcessTopProducts.csv")
print('Saving to CSV file as /toPanadaProcessTopProducts.csv')
sleep(2)
print('/n')
print(toPandaDailyDiscoveries)
# toPandaTrendingItems.to_csv("toPandaDailyDiscoveries.csv")
print('Saving to CSV file as /toPandaDailyDiscoveries.csv')
