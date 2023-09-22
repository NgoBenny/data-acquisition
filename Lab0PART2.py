import requests
from bs4 import BeautifulSoup
from collections import defaultdict

class WikipediaScraper:
    def __init__(self, url):
        self.url = url
        response = requests.get(url)
        self.html = BeautifulSoup(response.text, "html.parser")
        self.data = defaultdict(dict)

    def children(self):
        [print(child.name) for child in self.html.recursiveChildGenerator() if child.name is not None]

    def findAll(self, tags):
        dict = {}
        for tag in self.html.find_all(tags):
            print("{0}: {1}".format(tag.name, tag.text))
            if ':' in tag.text:
                s = tag.text.split(':')
                dict[s[0]] = s[1]
            else:
                dict[tag.text] = None
        for k,v in dict.items():
            print('key= ',k,'\tvalue= ', v)


    def appendTag(self, tag, nustr):
        newtag = self.html.new_tag(tag)
        newtag.string = nustr
        ultag = self.html.ul
        ultag.append(newtag)
        print(ultag.prettify())

    def insertAt(self,tag,nustr,index):
        newtag = self.html.new_tag(tag)
        newtag.string = nustr
        ultag = self.html.ul
        ultag.insert(index, newtag)
        print(ultag.prettify())

    def selectIndex(self,index):
        sel = "li:nth-of-type("+str(index)+")"
        print(self.html.select(sel))

    def scrape(self):
        table = self.html.find("table", {"class": "wikitable"})
        for row in table.find_all("tr")[1:]:
            cells = row.find_all("td")
            if len(cells) > 2:
                country_name = cells[0].find("a")
                if country_name:
                    country_name = country_name.get("title")
                    self.data[country_name]["1980"] = cells[1].get_text().strip()
                    self.data[country_name]["2018"] = cells[2].get_text().strip()

    def get_data(self):
        return self.data


url = "https://en.wikipedia.org/wiki/List_of_countries_by_carbon_dioxide_emissions_per_capita"
scraper = WikipediaScraper(url)
scraper.scrape()
'''
scraper.children()
scraper.findAll('li')
scraper.appendTag('li','new item')
scraper.insertAt('li', 'new item', 2)
scraper.selectIndex(2)
'''

data = scraper.get_data()
for country, values in data.items():
    print(f"{country} - 1980: {values['1980']} - 2018: {values['2018']}")
