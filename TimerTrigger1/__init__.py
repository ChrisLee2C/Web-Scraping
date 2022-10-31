import datetime
import logging

import azure.functions as func #need azure account to install

from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
import pandas as pd

search_term = "data+science+books"
my_url = "https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2380057.m570.l1313&_nkw={}&_sacat=0".format(search_term)

def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    #  Make the client object and read the html into a soup object
    uClient = uReq(my_url)
    page_html = uClient.read()
    uClient.close()

    page_soup = soup(page_html, 'html.parser')
    divs = page_soup.findAll('div',{'class':'s-item__details clearfix'})

    # Extract relevant data from the soup object

    prices = []

    for items in divs: 
        price = items.find('span',{'class':"s-item__price"})
        price = price.text[1:]
        price = price.replace(',','').strip("$HKD")
        prices.append(price)

    # Clean data and save to a file for later use
    
    prices = pd.DataFrame(pd.to_numeric(prices,errors='coerce')).dropna()
    name = search_term + str(utc_timestamp)  +".csv"
    name = "".join( x for x in name if (x.isalnum() or x in "._- "))
    prices.to_csv(name)

    logging.info('Python timer trigger function ran at %s', utc_timestamp)
