#This will not run on online IDE
import requests
from bs4 import BeautifulSoup


class CovidDataCollector:
    def __init__(self, url):
        self.URL = url


    def getData(self):
        """ Get the COVID cases Count data"""
        r = requests.get(self.URL)
        soup = BeautifulSoup(r.content, 'html5lib')
        return self.scrapData(soup)

    def scrapData(self, data):
        divData = data.find("div", id="maincounter-wrap")
        divInner = divData.find("div",class_='maincounter-number')
        countText = divInner.find("span").text
        count = int(countText.replace(',',''))
        return count