import urllib.request
from bs4 import BeautifulSoup
import csv

class entry:
    def __init__(self, title, order, comments, points):
        self.title = title
        self.order = order
        self.comments = comments
        self.points = points

def fillEntries(entries):
    urlpage =  'https://news.ycombinator.com/news?p=2'
    page = urllib.request.urlopen(urlpage)
    soup = BeautifulSoup(page, 'html.parser')
    
    
    table=soup.find('table')
    results = table.find_all('tr')[3].find_all('tr')
    
    for i in range (0, len(results), 3):
    
        indexStart = results[i].text.find('.') + 2
        indexEnd = results[i].text.find('(')-1
        title = results[i].text[indexStart:indexEnd]
        order = results[i].text[1:indexStart-2]
        idx = results[i+1].text.find(' ')
        points = results[i+1].text[1:idx]
        indexStart = results[i+1].text.find(' | hide | ') + 10
        indexEnd = results[i+1].text.find(' comments')
        comments = results[i+1].text[indexStart:indexEnd]
        entries.append(entry(title, order, comments, points))
                
entries = []
fillEntries(entries)


print()
    
    

