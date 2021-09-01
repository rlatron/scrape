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
    urlpage =  'https://news.ycombinator.com/news'
    page = urllib.request.urlopen(urlpage)
    soup = BeautifulSoup(page, 'html.parser')
    
    
    table=soup.find('table')
    results = table.find_all('tr')[3].find_all('tr')
    
    for i in range (0, len(results)-2, 3):
    
        indexStart = results[i].text.find('.') + 2
        indexEnd = results[i].text.find('(')-1
        title = results[i].text[indexStart:indexEnd]
        order = int(results[i].text[1:indexStart-2])
        idx = results[i+1].text.find(' ')
        points = int(results[i+1].text[1:idx])
        indexStart = results[i+1].text.find(' | hide | ') + 10
        indexEnd = results[i+1].text.find(' comments')
        #if the comments string wasn't found then there is no comments
        if indexEnd == -1:
            comments=0
        else:
            comments = int(results[i+1].text[indexStart:indexEnd])
        entries.append(entry(title, order, comments, points))

def moreThanFiveWordsFilter(entries):
    returnedEntries = []
    for entry in entries:
        if len(entry.title.split()) > 5:
            returnedEntries.append(entry)  
    returnedEntries.sort(key=lambda x: x.comments)
    return returnedEntries     

def lessThanFiveWordsFilter(entries):
    returnedEntries = []
    for entry in entries:
        if len(entry.title.split()) <= 5:
            returnedEntries.append(entry)  
    returnedEntries.sort(key=lambda x: x.points)
    return returnedEntries  

                
def main():
    entries = []
    fillEntries(entries)
    filteredEntriesFiveMore = moreThanFiveWordsFilter(entries)
    filteredEntriesFiveLess = lessThanFiveWordsFilter(entries)
    assert len(filteredEntriesFiveMore) + len(filteredEntriesFiveLess) == len(entries)
    
if __name__ == "__main__":
    main()
    
