from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
import pandas as pd

search_term = "data+science+books"
my_url = "https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2380057.m570.l1313&_nkw={}&_sacat=0".format(search_term)
client = uReq(my_url)
page_html = client.read()
page_soup = soup(page_html, features="html.parser")
span_tags = page_soup.findAll('span', {"class": "s-item__price"})

prices = []
for item in span_tags:
    prices.append(item.text.replace(",", "").strip("$HKD"))

numeric_array = pd.to_numeric(prices, errors='coerce')
df = pd.DataFrame(numeric_array)
df = df.dropna()
df.to_csv("{}_prices.csv".format(search_term))
