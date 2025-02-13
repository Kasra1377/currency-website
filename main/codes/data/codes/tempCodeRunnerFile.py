url = "https://www.tgju.org/currency"
cs = scrap.currency_scraper.CurrencyScrapper()
table_headers = cs.scrap_table_headers()
currency_info = cs.scrap_currency_info()
print("Table Headers : ", table_headers)
print("Currency Info : ", currency_info)