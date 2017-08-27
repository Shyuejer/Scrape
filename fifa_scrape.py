# -*- coding: utf-8 -*-
"""
Created on Sun Aug 27 10:45:05 2017

@author: sj
"""

import csv
import requests
from bs4 import BeautifulSoup
import pandas as pd

MAIN = 'https://www.fifaindex.com'
DIRECTORY = 'https://www.fifaindex.com/team/1370/brazil'

print("accesing " + DIRECTORY + "...")

response = requests.get(DIRECTORY)
html = response.content
soup = BeautifulSoup(html, "lxml")

starting_eleven = []
team_kits = []

'''
for count, info_panel in enumerate(soup.findAll('div',class_="panel panel-info")):
    # info_panel no.1 is 
    if count == 1:
        for div in info_panel.find_all('div', class_='name'):
            for a in div.find_all('a'):
                a = a.text
                starting_eleven.append(a)
    if count == 6:
        for link in info_panel.find_all('img'):
            link = link.get('src')
            team_kits.append(link)
    else:
        for span in info_panel.findAll('span'):
            pass            
'''
class Player(object):
    def __init__(self, kit_no, position, ovr, pot, name, preferred_pos, age):
            
        self.kit_no = kit_no
        self.position = position
        self.over = ovr
        self.pot = pot
        self.name = name 
        self.preferred_pos = preferred_pos
        self.age = age 
        
header_cells = ["jersey_number","position",'ovr','potential','url','Name',"Preferred Positions","Age"]        
players = []

table = soup.find('table',class_='table table-striped')
tbody = table.find('tbody')

td_to_avoid = [2,3] 

for player in tbody.find_all('tr'):
    temp = []
    for count, values in enumerate(player.find_all('td')):
        if count in td_to_avoid:
            pass
        elif count == 4:
            for span in values.find_all('span'):
                temp.append(span.get_text())
        elif count == 5:
            a = values.find('a')
            subdirectory = a.get('href')
            temp.append(MAIN+subdirectory)
            values = values.get_text()
            temp.append(values)
            
        elif count == 6:
            temp_whenmulti =[]
            for span in values.find_all('span'):
                temp_whenmulti.append(span.get_text())
            temp.append(temp_whenmulti)
        else:
            values = values.get_text()
            temp.append(values)
    
    players.append(temp)

with open("C:\\Users\\sj\\Dropbox\\%s.csv" % DIRECTORY[36:], "w", newline='') as outfile:
    writer = csv.writer(outfile)
    writer.writerow(header_cells)
    writer.writerows(players)
