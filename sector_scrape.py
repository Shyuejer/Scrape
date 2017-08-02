import csv
import requests
from bs4 import BeautifulSoup

url = 'http://www.isaham.my/all-sectors'

# want to better show that I'm accessing the SUBSECTION.
print "accesing " + url + "..."
response = requests.get(url)
html = response.content
soup = BeautifulSoup(html, "html.parser")

# Because there are some annoying numbers within the cell, I'll have to get rid of them. Potentially have to just take [:-1] to remove the ending white space.
external_span = soup.find('span')
unwanted = external_span.find('span')
unwanted.soup.extract()

list_sectors = []
for cell in soup.findAll("a", class_="list-group-item"):
    # .text is needed or we'll have the stupid tag.
    cell = cell.text
    cell = cell.replace(u'\xa0', u' ')
    list_sectors.append(cell)

print list_sectors
'''
for row in soup.findAll('tr')[1:]:
    data_cells = []
    for cell in row.findAll('td'):
        text = cell.text.replace('&nbsp;', '')
        data_cells.append(text)
    data_rows.append(data_cells)
'''    
