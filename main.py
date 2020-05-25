'''
Author: pyrotank
description: TODO
'''


# regular imports --------------------------------------------------------------
import alpaca_trade_api as tradeapi
import datetime

#user defined imports ----------------------------------------------------------
import tickers  
import config # FIXME use config_api, this import is for development only



print("*****************************************************************")
print("** Hello Money Makers, Welcome to the best tool to make money! **")
print("*****************************************************************\n")

# TODO: this bit needs to be update a few times a day
# hence will be putting it elsewhere later
# tickers.downloadNasdaqListed()
# tickers.downloadOtherListed()

# getAlpacaApiInstance ----------------------------------------------------------
# generates returns REST API instance takes in a parameter for live account.
# if live = True, you will get live rest api instance.
def getAlpacaApiInstance(live=False):
    url = ''
    if live: url = 'https://api.alpaca.markets'
    else   : url = 'https://paper-api.alpaca.markets'

    if live: return tradeapi.REST(config.ALPACA_LIVE_API_KEY,  config.ALPACA_LIVE_SECRET,  url, api_version='v2')
    else   : return tradeapi.REST(config.ALPACA_PAPER_API_KEY, config.ALPACA_PAPER_SECRET, url, api_version='v2')

# getGappersInPercent------------------------------------------------------------
# A function to return percentage gap price and volume in a timeframe of a stocks 
# it takes alpaca api instance, list of tickers, time frame(size of a candle) and
# No of candels(number of time interval we are looking for a gap)          
def getGappersInPercent(api, tickers, time_frame='minute', no_of_candles=3):

    barset = api.get_barset(tickers, time_frame, no_of_candles)
    change = {}
    for ticker in barset:
        bars = barset[ticker]
        if bars == []:
            print(f'ticker "{ticker}" doesnt exist')
            continue
            
        try:
            # See how much ticker moved in that timeframe.
            range_open = bars[0].c
            range_close = bars[-1].o
            percent_change = round((range_close - range_open)/range_open * 100 , 2) 
            
            vol_start = bars[0].v
            vol_end = bars[-1].v
            percent_vol_change = round((vol_end - vol_start)/vol_start * 100, 2)

            change[ticker] = (percent_change, percent_vol_change)
            print(f'{ticker} moved {percent_change}% with {percent_vol_change}% volume change over the last {no_of_candles} {time_frame} on {bars[-1].t}'.format(percent_change))
        except Exception as e:
            print(e)

    return change
    

api = getAlpacaApiInstance()
print(getGappersInPercent(api, ['DRAD','AAPL', 'TSLA']))