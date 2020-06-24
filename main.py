'''
Author: pyrotank
Project Name: Three Comas
description: TODO
'''

# regular imports --------------------------------------------------------------
import alpaca_trade_api as tradeapi
import sys
import psycopg2 # for 
import datetime
import time

#user defined imports ----------------------------------------------------------
sys.path.insert(1,'./nasdaq')
import tickers  
import alpaca
import pgsql
import config # FIXME use config_api, this import is for development only

print("*****************************************************************")
print("** Hello Money Makers, Welcome to the best tool to make money! **")
print("*****************************************************************\n")


db = pgsql.Pgsql("postgres", "password", "test", "localhost")
alp = alpaca.Alpaca(config.ALPACA_PAPER_API_KEY, config.ALPACA_PAPER_SECRET)


# updateTickerList --------------------------------------------------------------
# A simple function that updates the list of tickers in nasdaq and other exchanges
# its is to be used only once or a few times a day (need to work on the frequency of the usage)
def updateTickerList():
    tickers.downloadNasdaqListed()
    tickers.downloadOtherListed()

def addAssetsListToDB():
    
    
    asset_list_alpaca = alp.getAssets()
    db_instance = pgsql.Pgsql("postgres", "password", "test", "localhost")
    # deleting previous information and inserting new one.
    # need to change tghis approach in future as we shall not select, just update. 
    db_instance.executeQuery("delete from assets_alpaca;")

    for i in asset_list_alpaca:
        q = f'''INSERT INTO assets_alpaca (ticker, name, exchange, tradable, shortable, marginable) 
            VALUES ('{i[0]}','{i[1]}','{i[2]}','{'T' if i[3] else 'F'}','{'T' if i[4] else 'F'}', '{'T' if i[5] else 'F'}');'''
        db_instance.executeQuery(q)



def getTickers():
    q = "select ticker from assets_alpaca"
    return db.executeQuery(q)

def format_nanos(nanos, timeonly=False, desimal=False):
    dt = datetime.datetime.fromtimestamp(nanos / 1e9)
    
    if   desimal : s = '{}{:09.0f}'.format(dt.strftime('%Y-%m-%d T:%H:%M:%S.%f'), nanos % 1e9)
    elif timeonly: s = '{}'.format(dt.strftime('%H:%M:%S'))
    else:          s = '{}{:09.0f}'.format(dt.strftime('%Y-%m-%d %H:%M:%S'))

    return s

def test(ticker):
    print("{:<10}{:<7}  {:<10}{:<8} {:<8}".format('ticker', '%change',
                    'last', 'last T', 'last TT'))
    while(1):
        all_t = alp.getPoly().all_tickers()
        for i in all_t:
            if(i.ticker == ticker):
                print("{:<10}{:<7}  {:<10}{} {}".format(i.ticker, i.todaysChangePerc, 
                    i.lastQuote['P'], format_nanos(i.lastQuote['t'], timeonly=True), 
                    format_nanos(i.lastTrade['t'], timeonly=True)))
                break


def format_print(i):
    print("{:<10}{:<7}  {:<10}{} {}".format(i.ticker, i.todaysChangePerc, 
        i.lastQuote['P'], format_nanos(i.lastQuote['t'], timeonly=True), 
        format_nanos(i.lastTrade['t'], timeonly=True)))


def gappers(perc_change=5):
    
    print("[*] Running market gappers watchlist...")
    print(f"[*] stocks that are gapping more than {perc_change}% ...\n")
    print("{:<10}{:<7}  {:<10}{:<8} {:<8}".format('ticker', '%change',
                    'last', 'last T', 'last TT'))
    try:
        while(1):
            
            all_t = alp.getPoly().all_tickers()
            # print(all_t[0])
            gappers = []
            print()
            for i in all_t:
                if i.todaysChangePerc > perc_change:
                    
                    gappers.append(i)

                    # format_print(i)

            gappers.sort(key = lambda i: float(i.todaysChangePerc), reverse=True)
            

            for i in gappers:
                print("{:<10}{:<7}  {:<10}{} {}".format(i.ticker, i.todaysChangePerc, 
                i.lastQuote['P'], format_nanos(i.lastQuote['t'], timeonly=True), 
                format_nanos(i.lastTrade['t'], timeonly=True)))
            print("\n\n\n")               

    except KeyboardInterrupt:
        print("\n[x] Stopping market gappers watchlist...\n")

def getSplits(symbol):
    return


def main():

    alp = alpaca.Alpaca(config.ALPACA_PAPER_API_KEY, config.ALPACA_PAPER_SECRET)
    # asset_list_alpaca = alp.getAssets()
    api = alp.getApi()
    # for k,v in api.alpha_vantage.historic_quotes('LK').items():
    #     print(f"{k} :{v}")
    all_tickers = alp.getPoly().all_tickers()
    poly = alp.getPoly()
    
    # print(alp.getPoly().get(f"/reference/splits/{'SFUN'}",version='v2'))
    # polyticker = alp.getPoly().get(f"/reference/tickers?sort=ticker&market=STOCKS&perpage=50&page=715",version='v2')
    # print(polyticker['count']/polyticker['perPage'])
    # for i in polyticker['tickers']:
    #     print(i['ticker'])
    
    gappers(30)     
    
    # tickers.sort()
    # print(tickers[0])
    # print(len(tickers))


   
main()    