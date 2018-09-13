import requests
import bs4 as bs
import datetime as dt
import os
import time
import pandas as pd
import pandas_datareader.data as web
from django.http import HttpResponse
import pickle
def save_sp500_tickers():
    #parse S&P 500 using BeautifulSoup
    resp = requests.get('http://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    soup = bs.BeautifulSoup(resp.text, 'lxml')
    #Get data from table
    table = soup.find('table', {'class': 'wikitable sortable'})
    #create an empty list to store tickers
    tickers = []
    #iterate throug for loop to load in names of tickers
    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[0].text
        #ticker = ticker.replace('.','-').strip()
        tickers.append(ticker)
        print(tickers)

    #I had problems getting these tickers using the data reader thus I removed them from the list
    with open("sp500tickers.pickle","wb") as f:
        tickers.remove('ANDV')
        tickers.remove('BKNG')
        tickers.remove('BHF')
        tickers.remove('CBRE')
        tickers.remove('DWDP')
        tickers.remove('DXC')
        tickers.remove('TPR')
        tickers.remove('UAA')
        tickers.remove('WELL')
        pickle.dump(tickers,f)

    return tickers

#save_sp500_tickers()

def get_data_from_google(reload_sp500=False):
    #check if you want stock data reloaded or taken from a previously saved pickle file
    if reload_sp500:
        tickers=save_sp500_tickers()
    else:
        with open("sp500tickers.pickle","rb") as f:
            tickers=pickle.load(f)
    # check if stock_dfs folder exists
    if not os.path.exists('stock_dfs'):
        os.makedirs('stock_dfs')
    # initiate date to begin pulling stock data from
    start=dt.datetime(2000,1,1)
    end=dt.datetime.now()
    for ticker in tickers:
        # just in case your connection breaks, we'd like to save our progress!
        if not os.path.exists('stock_dfs/{}.csv'.format(ticker)):
            time.sleep(0.5)
            df = web.DataReader(ticker, 'morningstar', start, end)
            df.reset_index(inplace=True)
            #inplace=True makes changes permanent
            df.set_index("Date", inplace=True)
            #drop the column symbol
            df = df.drop("Symbol", axis=1)
            #conver to csv
            df.to_csv('stock_dfs/{}.csv'.format(ticker))
        else:
            print('Already have {}'.format(ticker))
get_data_from_google(reload_sp500=True)
