from bs4 import BeautifulSoup
import requests
import sys

sys.path.append("..\codes")
from configuration import config

class CurrencyScrapper:
    english_currency_names = config.ENGLISH_CURRENCY_NAMES
    english_table_headers = config.ENGLISH_TABLE_HEADERS

    def __init__(self, url):
        self.url = url

    def scrap_table_headers(self, parser="html.parser", slice=2, mapping_names=True):
        self.page = requests.get(self.url)
        self.soup = BeautifulSoup(self.page.text, parser)

        self.currency_table = self.soup.find("div", class_="fs-row")
        self.table_headers = self.currency_table.find("thead")
        self.table_headers = self.table_headers.find_all("th")
        self.table_headers = [header.text.strip() for header in self.table_headers]
        self.table_headers = [header for header in self.table_headers if header]
        
        if mapping_names:
            self.table_headers = [self.english_table_headers[header] for header in self.table_headers]
        
        if slice:
            self.table_headers = self.table_headers[:slice]
        
        return self.table_headers
      
    def scrap_currency_info(self, parser="html.parser", slice=12, mapping_names=True):
        self.page = requests.get(self.url)
        self.soup = BeautifulSoup(self.page.text, parser)
        
        # Extracting the names of currencies from the table 
        self.currency_table = self.soup.find("div", class_="fs-row")
        self.currency_indeces = self.currency_table.find("tbody")
        self.currency_names = self.currency_indeces.find_all("th")
        self.currency_names = [name.text.strip() for name in self.currency_names]

        # Extracting the values of currencies from the table 
        self.currency_values = self.currency_indeces.find_all("td", class_="nf")
        self.currency_values = [value.text.strip() for value in self.currency_values]
        # Removing redundant information
        self.currency_values = [int(self.currency_values[i].replace(",", ""))  for i in range(len(self.currency_values)) if i % 2 == 0] 

        if slice:
            self.currency_names, self.currency_values = self.currency_names[:slice], self.currency_values[:slice]

        if mapping_names:
            self.currency_names = [self.english_currency_names[name] for name in self.currency_names]
        
        self.currency_info = [self.currency_names, self.currency_values]
        
        return self.currency_info

    def scrap_currency_table(self):
        self.table_headers = self.scrap_table_headers()
        self.currency_info = self.scrap_currency_info()
        self.currency_data = {k:v for k,v in zip(self.table_headers,self.currency_info)}
        print("Currency table scrapped!")
        return self.currency_data

if __name__ == "__main__":
    url = "https://www.tgju.org/currency"
    cs = CurrencyScrapper(url)
    currency_data = cs.scrap_currency_table()
    print("Currency data: ", currency_data)