import requests 
from bs4 import BeautifulSoup
import pandas as pd

url_temp = "http://data.shareview.co.uk/quote/{}/?https=0&hideSearch=0&hideTabs=0&hideTradeNow=0&hideNav=1&xdjs="
df = pd.DataFrame()

# I'm gonna call the function over a list of urls
def fetch(name):
    response = requests.get(url_temp.format(name))
    html = response.content
    soup = BeautifulSoup(html,"html.parser") 
    table = soup.find_all('table')[2]

    # create a new table, here I know the size is 18, 
    # but I'm not sure if I should create an empty 1 first.

    col_counter = 0
    col_names = []
    values = []
    if col_counter < 1:
        col_counter += 1
        for keys in table.find_all('tr'):
            col_names.append(keys.text)
    for data in table.find_all('td'):
        values.append(data.text)
    df[name] = values
    
def save_to_csv(filename):
    df.to_csv(filename)
    
def main():
    fetch("AZN")
    print(df)
    save_to_csv("AZN.csv")
    
if __name__ == "__main__":
    main()