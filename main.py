'''
Author: pyrotank
Project Name: Three Comas
description: TODO
'''

# regular imports --------------------------------------------------------------
import alpaca_trade_api as tradeapi
import datetime
import time

#user defined imports ----------------------------------------------------------
import tickers  
import alpaca
import config # FIXME use config_api, this import is for development only

print("*****************************************************************")
print("** Hello Money Makers, Welcome to the best tool to make money! **")
print("*****************************************************************\n")

# updateTickerList --------------------------------------------------------------
# A simple function that updates the list of tickers in nasdaq and other exchanges
# its is to be used only once or a few times a day (need to work on the frequency of the usage)
def updateTickerList():
    tickers.downloadNasdaqListed()
    tickers.downloadOtherListed()

# getAlpacaApiInstance ----------------------------------------------------------

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
def getGappersInPercent(api, tickers, gap_percent=0.0, time_frame='minute', no_of_candles=3):

    barset = api.get_barset(tickers, time_frame, no_of_candles)
    change = {}
    for ticker in barset:
        bars = barset[ticker]
        if bars == []:
            print(f'ticker "{ticker}" doesnt exist')
            continue
            
        try:
            # See how much ticker moved in the given timeframe.
            range_open = bars[0].c
            range_close = bars[-1].o
            percent_change = round((range_close - range_open)/range_open * 100 , 2) 
            
            vol_start = bars[0].v
            vol_end = bars[-1].v
            percent_vol_change = round((vol_end - vol_start)/vol_start * 100, 2)
            if gap_percent == 0.0:
                change[ticker] = (percent_change, percent_vol_change, bars[-1].t)
            else:
                if(percent_change >= gap_percent):
                    change[ticker] = (percent_change, percent_vol_change, bars[-1].t)

            print(f'''{ticker} moved {percent_change}% with {percent_vol_change}% volume\
                change over the last {no_of_candles} {time_frame} from {bars[0].t} to {bars[-1].t}''')
        except Exception as e:
            print(e)

    return change

def getGappers(api, tickers, gap_percent, time_frame='minute', no_of_candles=3):
    pass

def tickEvery(func, sec=1, min=0, hr=0):
    cur_time = time.time()
    t = sec + (60 * min) + (60^2)*hr
    while True:
        if time.time() == round(cur_time + t):
            func()
            cur_time = time.time()
def hello():
    print('hello')        

def main():
    # TODO: this bit needs to be update a few times a day.
    # hence will be putting the following line of code elsewhere later during development.
    # updateTickerList()
    # tickEvery(hello)
    alp = alpaca.Alpaca(config.ALPACA_PAPER_API_KEY, config.ALPACA_PAPER_SECRET)
    print(alp.getGappersInPercent(['AAL', 'AAL', 'AAL','AAL','AAPL', 'TSLA', 'LK'], gap_percent=1))


main()    