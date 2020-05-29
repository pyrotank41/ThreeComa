import alpaca_trade_api as tradeapi

# A class implimentation for using Alpaca API
# this class is dependent on alpaca_traded_api module as 
# to implement certain functions for our use and work past the 
# implementation of the alpaca api itself.
# Following are current known limitation of Alpaca API: 
#   - The rate limit is 200 requests per every minute per API key.
#   - One or more (max 200) symbol names split by commas (",").
#   - The maximum number of bars to be returned for each symbol. It can be between 1 and 1000. Default is 100 if parameter is unspecified or 0.

# get_barsets() doesnt return accurate barsets pre-market, even during the pre-market hrs supported my alpaca trading. 

class Alpaca:
    
    # protected data members
    _live_url  = 'https://api.alpaca.markets'
    _paper_url = 'https://paper-api.alpaca.markets'
    _live  = False

    # if live = True, you will get live rest api instance.
    def __init__(self, key, secret, live=False, api_verison='v2'):
        if live: self._api = tradeapi.REST(key, secret, self._live_url,  api_version='v2')
        else   : self._api =  tradeapi.REST(key, secret, self._paper_url, api_version='v2')
        self._live = live
    
    # public data members and functions.

    # getApi ------------------------------------------------------------------------
    # returns the REST API instance of alpaca. 
    # It is intended to use whenever there is a function that is not supported my this class yet.
    def getApi(self):
        return self._api

    # getGappersInPercent------------------------------------------------------------
    # A function to return percentage gap price and volume in a timeframe of a stocks 
    # it takes alpaca api instance, list of tickers, time frame(size of a candle) and
    # No of candels(number of time interval we are looking for a gap) 
    def getGappersInPercent(self, tickers, gap_percent=0.0, time_frame='minute', no_of_candles=3):

        barset = self._api.get_barset(tickers, time_frame, no_of_candles)
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


    