# -*- coding: utf-8 -*-
"""
Created on Fri Aug 11 12:20:54 2017

@author: sj
"""

import requests
import pandas as pd
from bs4 import BeautifulSoup

url = 'http://data.shareview.co.uk/quote/{}/?https=0&hideSearch=0&hideTabs=0&hideTradeNow=0&hideNav=1&xdjs='
group_stock = ["azn","pay"]

df = pd.DataFrame()


for stock in group_stock:
    # url.format(stock) returns the functional url
    response = requests.get(url.format(stock))
    html = response.content
    soup = BeautifulSoup(html, "html.parser")
    table = soup.findAll("table")[2]
    table.prettify()

    # the name of stock's attribute and its ratios
    keys = []
    values = []
    counter = 0
    
    for x in table.findAll("td"):
        x = x.get_text()
        x = "".join(x.split(","))
        values.append(x)
    # only need to grab attribute names once        
    if keys == []:
        for x in table.findAll("th"):
            x = x.get_text()
            keys.append(x)

    values = pd.Series(values)
    df["%s" % stock] = values

df = df.set_index(keys=keys)    
df = df.transpose()
print df    
df.to_csv('fuck.csv')

def write():
    with open ("a.txt",'w') as f:
        for stuff in values:
            f.write(stuff + "\n")
'''
list_sectors = []
for cell in soup.findAll("a", class_="list-group-item"):
    # .text is needed or we'll have the stupid tag.
    span_tag = cell.span.extract()
    cell = cell.text
    cell = cell.replace(u'\xa0', u' ')
    list_sectors.append(cell)


# Checking if website links work
def request_count():
    # These are my requests counters. 
    good_counter = 0
    bad_counter = 0  
    for sector in list_sectors:
        sector = sector[:-1].lower()
        sector = sector.split(" ")
        sector = "-".join(sector)
        sector = sector.replace('&','and')
        request = requests.head(url_2 + '/' + sector)
        if request.status_code == 200:
            print('Website exists for %s' %sector)
            good_counter += 1
        else:
            print('Website does not exist for %s' %sector)
            bad_counter += 1


    print "Number of good counters: %i" %good_counter
    print "Number of bad counters: %i" %bad_counter        

# The exciting part: fetching data from 50 pages!
# First I will make a list of websites to visit
list_of_sites = []

for sector in list_sectors:
    sector = sector[:-1].lower()
    sector = sector.split(" ")
    sector = "-".join(sector)
    sector = sector.replace('&','and')
    list_of_sites.append(url_2+'/'+sector)

def fetch():
    for url in list_of_sites:
        print "accesing " + url
        response = requests.get(url)
        if response.status_code == 200:
            html = response.content
            soup = BeautifulSoup(html, "html.parser")
            data_rows = []    
            x_cells = []
            for cell in soup.findAll('th'):
                # .text is needed or we'll have the stupid tag.
                x_cells.append(cell.text)
            
            for row in soup.findAll('tr')[1:]:
                data_cells = []
                for cell in row.findAll('td'):
                    text = cell.text.replace('&nbsp;', '')
                    data_cells.append(text)
                data_rows.append(data_cells)
            
            outfile = open("C:\\Users\\sj\\Dropbox\\Investing\\isaham.data\\%s.csv" % url[27:], "wb")
            writer = csv.writer(outfile)
            writer.writerow(x_cells)
            writer.writerows(data_rows)
'''