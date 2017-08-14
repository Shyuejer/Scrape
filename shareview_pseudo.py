# script will have to execute selenium on Shareview and 
# store the numbers in an csv file, which will then be launched over Tableau.

# 1: visit the screener site and fill in the form
## my criteria are Dividend Cover (> 2x), ROE, DY, 
## net-cash (not intially filtered), croic (need to compute).
### requires Selenium

#chrome driver at D file.

# 2: save the result in the form of stock codes.
##
 
# 3: visit individual stock infos and fetch them back into pd df

# 4: output to csv
import requests 
from bs4 import BeautifulSoup
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
 
## create a pandas dataframe to store the scraped data
 
## launch the Chrome driver
my_path = "D:\\chromedriver.exe"
driver = webdriver.Chrome(executable_path=my_path)
screener = "http://data.shareview.co.uk/stock-screener/?https=0&hideSearch=0&hideTabs=0&hideTradeNow=0&hideNav=1"
driver.get(screener)
wait = WebDriverWait(driver,10)

url_temp = "http://data.shareview.co.uk/quote/{}/?https=0&hideSearch=0&hideTabs=0&hideTradeNow=0&hideNav=1&xdjs="
text = []
data_tags = []
mega_value_list = []


def find_AS():
    select = Select(driver.find_element_by_name('index[]'))
    select.select_by_visible_text('FTSE All-Share')
    

def send():
    element_dividendYieldMin = wait.until(EC.presence_of_element_located((By.NAME,"dividendYieldMin")))
    element_dividendYieldMax= wait.until(EC.presence_of_element_located((By.NAME,"dividendYieldMax")))
    element_dividendYieldMin.send_keys("0")
    element_dividendYieldMax.send_keys("1000")
    
def get_list():
    all_tds = driver.find_elements_by_tag_name('td')
    for tds in all_tds[::2]:
        text.append(tds.text)
    print (text[:10])

def fetch_data_tags():
    response = requests.get(url_temp.format(text[0]))
    html = response.content
    # soup = Beautiful(html,"html.parser") 
    soup = BeautifulSoup(html,"html.parser")  
    table = soup.find_all('table')[2]
    
    # return a list of the names of 18 attributes of a stock.
    for dt in table.find_all('th'):
        data_tags.append(dt.text)     
        
def fetch_data_values(stock):
    response = requests.get(url_temp.format(stock))
    html = response.content
    # soup = Beautiful(html,"html.parser") 
    soup = BeautifulSoup(html,"html.parser")  
    table = soup.find_all('table')[2]
    
    # initialize a local list to later merge with the mega list
    local_value_list = []
    local_value_list.append(stock)
    
    # complete the local list with 19 entries.
    for value in table.find_all('td'):
        local_value_list.append(value.text)
    
    mega_value_list.append(local_value_list)

def main():
    find_AS()
    # skip send() 
    form_submit = driver.find_element_by_class_name("button")
    form_submit.click()
    time.sleep(3)
    get_list()
    fetch_data_tags()
    progress_counter = 0
    full_bar = len(text)
    for stock in text:
        fetch_data_values(stock)
        progress_counter+=1
        print(progress_counter/full_bar)
        
    df = pd.DataFrame(index=data_tags)
    for local_list in mega_value_list:
        df[local_list[0]] = local_list[1:]
    df.to_csv("yay.csv")
    
if __name__ == "__main__":
    main()