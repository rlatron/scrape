import urllib.request
from bs4 import BeautifulSoup
import csv

class entry:
    def __init__(self, title, order, comments, points):
        self.title = title
        self.order = order
        self.comments = comments
        self.points = points

def fill30Entries(entries, url):
    page = urllib.request.urlopen(url)
    soup = BeautifulSoup(page, 'html.parser') 
    
    table = soup.find('table')
    results = table.find_all('tr')[3].find_all('tr')
    
    for i in range (0, len(results)-2, 3):
        #find the title and the order
        indexStart = results[i].text.find('.') + 2
        indexEnd = results[i].text.find('(')-1
        title = results[i].text[indexStart:indexEnd]
        order = int(results[i].text[1:indexStart-2])
        #find the number of points
        index = results[i+1].text.find(' ')
        points = int(results[i+1].text[1:index])
        #find the number of comments
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

def tests(entries, filteredEntriesMoreFive, filteredEntriesLessFive):
    #test that we only took only 30 entries and the consistency between both filters
    assert len(entries) == 30
    assert len(filteredEntriesMoreFive) + len(filteredEntriesLessFive) == len(entries)
    #check that the entries are ordered by number of comments and that the titles have more than five words
    for i in range(1, len(filteredEntriesMoreFive)):
        assert filteredEntriesMoreFive[i].comments >= filteredEntriesMoreFive[i-1].comments 
        assert len(filteredEntriesMoreFive[i].title.split()) > 5 
    #check that the entries are ordered by number of points and that the titles have less or equal to five words
    for i in range(1, len(filteredEntriesLessFive)):
        assert filteredEntriesLessFive[i].points >= filteredEntriesLessFive[i-1].points 
        assert len(filteredEntriesLessFive[i].title.split()) <= 5
    
                
def main():
    entries = []
    fill30Entries(entries, 'https://news.ycombinator.com/news')
    filteredEntriesMoreFive = moreThanFiveWordsFilter(entries)
    filteredEntriesLessFive = lessThanFiveWordsFilter(entries)
    tests(entries, filteredEntriesMoreFive, filteredEntriesLessFive)
    
    #try again with page 2
    entries = []
    fill30Entries(entries, 'https://news.ycombinator.com/news?p=2')
    filteredEntriesMoreFive = moreThanFiveWordsFilter(entries)
    filteredEntriesLessFive = lessThanFiveWordsFilter(entries)
    tests(entries, filteredEntriesMoreFive, filteredEntriesLessFive)
    
if __name__ == "__main__":
    main()
    
