import urllib.request
from bs4 import BeautifulSoup
from datetime import datetime
import time

def print_to_file(output):
    """Helper Method to overwrite a file with a given string"""
    file = open('log.txt', 'w+')
    file.write(output)

def main():
    """ Helper varibles"""
    freshEntries = []
    notPastEightDays = True 
    currLink = "http://www.reddit.com/r/hiphopheads/search?q=[FRESH]&sort=new&restrict_sr=on&count=0&after=t3_304u7x"

    while notPastEightDays: # while the current posts are not more than a week old

        """ Make a request to the page, if it fails, wait 5 seconds and try again """
        requestWorked = False
        while not requestWorked:
            try:
                request = urllib.request.Request(currLink) # stores the request
                soup = BeautifulSoup(urllib.request.urlopen(request)) # make the request and use BS4 to store it
                requestWorked = True # it worked so carry on.
            except  Exception  as e:
                print(e)
                print("Too many requests, sleeping for 5 seconds")
                requestWorked = False
                time.sleep(5) # something went wrong, wait 5 seconds and try again
                print("awake")


        """ reddit logic """

        entries = soup.find_all('div', attrs={'class':'entry'}) # find all thread posts on page

        for entry in entries:

            """ extract the post date and convert to Datetime object """
            dateDiv = entry.find('time')
            date = dateDiv.attrs['datetime']
            oldDate = datetime.strptime(date[:date.index("T")], '%Y-%m-%d')

            """ caculate the date difference """
            currDate = datetime.utcnow()
            dateDiff = currDate - oldDate

            if dateDiff.days > 7: # if the diff is 8 days, break and stop
                notPastEightDays = False
                break
            else:

                # extracting the wanted info
                title = entry.find('p',attrs={'class':'title'})
                title = title.getText()
                if '[fresh]' in title.lower():
                    link = entry.find('a',attrs={'class','title'})
                    freshEntries.append((title,link.get('href'),oldDate)) 

        print("finished page")
        currLink = soup.find('span', attrs={'class':'nextprev'}).find('a',attrs={'rel':'next'}).attrs['href'] # next page
        time.sleep(1)

    outputText = '---------------list of Fresh Hip Hop--------------\n'
    for entry in freshEntries:
        outputText += '--------------------------------------------------\n'
        outputText += 'title: ' + entry[0] + '\n'
        outputText += 'link: ' + entry[1] + '\n'
        outputText += 'date: ' + str(entry[2]) + '\n'
        outputText += '--------------------------------------------------\n'

    print_to_file(outputText)

if __name__ == '__main__':
    main()