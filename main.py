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

def main():
    # TODO: this bit needs to be update a few times a day.
    # hence will be putting the following line of code elsewhere later during development.
    # updateTickerList()

    alp = alpaca.Alpaca(config.ALPACA_PAPER_API_KEY, config.ALPACA_PAPER_SECRET)
    print(alp.getGappersInPercent(['AAL', 'AAL', 'AAL','AAL','AAPL', 'TSLA', 'LK'], gap_percent=1))
    
main()    