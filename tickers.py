import wget
import os
import pandas as pd # we are using pandas to convert Bar seperated values to csv.

base_nasdaq_url = "ftp://ftp.nasdaqtrader.com/symboldirectory/"

# A simple function to download the file from a given url using wget library
def _download_file(url, path):
    try:
        os.remove(path) # removing the exesting file
    except:
        pass # if the path doesnt exists we ignore the error

    # downloading the file and saving it to the path
    r = wget.download(url, path)
    print(f'\n[*] Downloaded file from {url}')

# since we are getting the list of tickers in the form of Bar(|) seperated values,
# we are just cleaning the txt file provided and generating an equivalent CSV file 
def _convert_bar_seperated_txt_to_CSV(from_path, to_path):
    df = pd.read_csv(from_path, sep="|")
    # df = df.set_index('Symbol')
    print(df.head)
    df.to_csv(to_path, index=False)

# a function that retrieves nasdaqlisted stocks and ETFs     
def downloadNasdaqListed():
    
    download_path = 'tickers/nasdaq_listed.txt'
    url = base_nasdaq_url + "nasdaqlisted.txt"
    
    _download_file(url, download_path)
    _convert_bar_seperated_txt_to_CSV(download_path, 'tickers/nasdaq_listed.csv')
    
# a function that retrieves stocks and ETFs which are not listed in nasdaq. 
def downloadOtherListed():
    download_path = 'tickers/other_listed.txt'
    url = base_nasdaq_url + "otherlisted.txt"
    
    _download_file(url, download_path)
    _convert_bar_seperated_txt_to_CSV(download_path, 'tickers/other_listed.csv')

if __name__ == "__main__":
    downloadNasdaqListed()
    downloadOtherListed()