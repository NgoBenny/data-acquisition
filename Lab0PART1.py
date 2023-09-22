import requests
from bs4 import BeautifulSoup
from collections import defaultdict

url = "https://en.wikipedia.org/wiki/List_of_countries_by_carbon_dioxide_emissions_per_capita"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

data = defaultdict(dict)
table = soup.find("table", {"class": "wikitable"})
for row in table.find_all("tr")[1:]:
    cells = row.find_all("td")
    if len(cells) > 2:
        country_name = cells[0].find("a")
        if country_name:
            country_name = country_name.get("title")
            data[country_name]["1980"] = cells[1].get_text().strip()
            data[country_name]["2018"] = cells[2].get_text().strip()

for country, values in data.items():
    print(f"{country} - 1980: {values['1980']} - 2018: {values['2018']}", end='\n')
