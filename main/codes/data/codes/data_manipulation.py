import sys
import os
import pandas as pd
import numpy as np

sys.path.append("..\codes")
import time_module
from scrap import currency_scraper

class DataCreation:
    tm = time_module.TimeModule()
    def __init__(self, currency_data: currency_scraper.CurrencyScrapper,
            save_path = "..\codes\data\datasets\currency_dataframes"):
        self.currency_data = currency_data.scrap_currency_table()
        self.save_path = save_path

    def create_dataframe(self, dataframe_name ,save_as_csv=True):
        # Must create sigle data frame not batches, and must return sn empty dataframe.
        self.empty_dataframe = pd.DataFrame(data={"Value": [], "Time": [], "Date":[]})
        if save_as_csv:
            self.empty_dataframe.to_csv(self.save_path + '\{}_history.csv'.format(dataframe_name),
                index=False)
        print("{}_history.csv created successfully.".format(dataframe_name))
        return self.empty_dataframe

    def update_dataframes(self):

        for currency, value in zip(self.currency_data["Currency Name"], self.currency_data["Current Value"]):
            self.new_dataframe = pd.DataFrame(data={"Value": [value], "Time": [self.tm.current_time()],
                "Date":[self.tm.today_date()]})
            if os.path.isfile(self.save_path + '\{}_history.csv'.format(currency)):
                self.current_dataframe = pd.read_csv(self.save_path + "\{}_history.csv".format(currency))
                self.updated_dataframe = pd.concat([self.current_dataframe, self.new_dataframe])
            else:
                self.empty_dataframe = self.create_dataframe(currency)
                self.updated_dataframe = pd.concat([self.empty_dataframe, self.new_dataframe])
            
            self.updated_dataframe.to_csv(self.save_path + "\{}_history.csv".format(currency),
                index=False)
            print("{}_history.csv updated successfully.".format(currency))


class DataProcess:
    tm = time_module.TimeModule()
    def __init__(self):
        pass
    
    def convert_to_toman(self, value, put_comma = True):
        value = int(value / 10) 
        if put_comma:
            value = "{:,}".format(value)
        return value

    def calculate_currency_change(self, dataframe):
        try:
            self.yesterday_dataframe = dataframe.loc[dataframe["Date"] == self.tm.yesterday_date()] #DRY
            self.percent_change = round(((dataframe.Value.iloc[-1] - self.yesterday_dataframe.Value.iloc[-1]) / dataframe.Value.iloc[-1] ) * 100, 4)
            self.absolute_change = dataframe.Value.iloc[-1] - self.yesterday_dataframe.Value.iloc[-1]
            self.absolute_change = self.convert_to_toman(self.absolute_change)
        except:
            self.percent_change, self.absolute_change = 0, 0

        return str(self.absolute_change) + "  (" + str(self.percent_change) +"%)"

    def calculate_currency_min_max_value(self, dataframe):
        # add error catching codes if we do not have previous day, week, etc.
        # if len(dataframe.Value) > 1:
        #     # filter dataframe to get the maximum and minimum value of the previous day
        try:
            self.yesterday_dataframe = dataframe.loc[dataframe["Date"] == self.tm.today_date()] #DRY

            self.min_value = self.yesterday_dataframe.Value.min()
            self.max_value = self.yesterday_dataframe.Value.max()
        except:
            self.min_value, self.max_value = dataframe.Value.iloc[-1], dataframe.Value.iloc[-1]

        return self.min_value, self.max_value

    def calculate_currency_indicators(self, dataframe, name):
        self.currency_value_change = self.calculate_currency_change(dataframe)
        self.currency_min_value, self.currency_max_value = self.calculate_currency_min_max_value(dataframe)
        
        self.live_value = self.convert_to_toman(dataframe.Value.iloc[-1])
        self.currency_min_value = self.convert_to_toman(self.currency_min_value)
        self.currency_max_value = self.convert_to_toman(self.currency_max_value)
        
        self.currency_rows = pd.DataFrame(data={"Currency": [name], "Live Value":[self.live_value],
                    "Change":[self.currency_value_change], "Minimum Price":[self.currency_min_value],
                    "Maximum Price":[self.currency_max_value]})
        return self.currency_rows

class CurrencySpecificDataProcess(DataProcess):

    def maximum_oscillation_in_day(self, dataframe):
        try:
            self.today_dataframe = dataframe.loc[dataframe["Date"] == self.tm.today_date()]
            self.today_values =  self.today_dataframe["Value"].to_list()
            self.value_differences = [next_value - current_value for current_value, next_value 
                            in zip(self.today_values, self.today_values[1:])]

            return max(self.value_differences, key=abs)
        except:
            return 0

    def maximum_percentage_oscillation_in_day(self, dataframe):
        try:
            self.today_dataframe = dataframe.loc[dataframe["Date"] == self.tm.today_date()]
            self.today_values =  self.today_dataframe["Value"].to_list()
            self.value_percent_changes = [(next_value - current_value) / current_value for current_value, next_value 
                            in zip(self.today_values, self.today_values[1:])]
            # self.absolute_percent_changes = [abs(next_value - current_value) / 100 for current_value, next_value 
            #                 in zip(self.today_values, self.today_values[1:])]
            
            # self.absolute_percent_changes = np.array(self.absolute_percent_changes)
            # self.maximum_absolute_percent_index = round(self.absolute_percent_changes.argmax(), 3)
            self.maximum_percent_change = max(self.value_percent_changes, key=abs)
            return str(round(self.maximum_percent_change * 100, 2)) + "%"
        except:
            return "0%"
    
    def calculate_currency_indicators(self, dataframe, name):
        self.currency_value_change = self.calculate_currency_change(dataframe)    # This return values must be rewritten
        self.currency_min_value, self.currency_max_value = self.calculate_currency_min_max_value(dataframe)
        self.daily_maximum_oscillation_value = self.maximum_oscillation_in_day(dataframe)
        self.daily_maximum_oscillation_percentage = self.maximum_percentage_oscillation_in_day(dataframe)
        
        #You can write a for loop on functions
        self.live_value = self.convert_to_toman(dataframe.Value.iloc[-1])
        self.currency_min_value = self.convert_to_toman(self.currency_min_value)
        self.currency_max_value = self.convert_to_toman(self.currency_max_value)
        self.daily_maximum_oscillation_value = self.convert_to_toman(self.daily_maximum_oscillation_value)
        
        self.currency_specific_indicator_dataframe = pd.DataFrame(data={"Currency": [name], "Value":[self.live_value],
                    "Change (comparing to yesterdey)":[self.currency_value_change], "Minimum price of the day":[self.currency_min_value],
                    "Maximum price of the day":[self.currency_max_value], "Today's maxumum oscillation":[self.daily_maximum_oscillation_value],
                    "Today's maxumum oscillation (in %)":[self.daily_maximum_oscillation_percentage],
                    "Time":[self.tm.current_time()]})
        
        return self.currency_specific_indicator_dataframe



class MainPageTableCreation:
    
    def __init__(self, root_path, table_folder, dataframes_folder, table_name, headers = [],
                data_processing = DataProcess()):
        
        self.root_path = root_path
        self.table_folder = table_folder
        self.dataframes_folder = dataframes_folder
        self.table_name = table_name
        self.headers = headers
        self.data_processing = data_processing

    def create_empty_table(self, save_as_csv=True):
        self.empty_table = pd.DataFrame(data={header : [] for header in self.headers})
        if save_as_csv:
            self.empty_table.to_csv(self.root_path + self.table_folder + "/" + self.table_name,
            index=False)
        print("{} created successfully.".format(self.table_name))
        return self.empty_table

    def add_to_table(self):
        self.dataframe_names_list = os.listdir(self.root_path + self.dataframes_folder)
        self.main_page_currency_table = self.create_empty_table()
        for dataframe_file in self.dataframe_names_list:
            self.currency_name = dataframe_file.split("_")[0]
            self.dataframe = pd.read_csv(self.root_path + self.dataframes_folder + "/" + dataframe_file)
            self.currency_rows = self.data_processing.calculate_currency_indicators(self.dataframe, self.currency_name)
            self.main_page_currency_table = pd.concat([self.main_page_currency_table, self.currency_rows],
                ignore_index=True)

        self.main_page_currency_table.to_csv(self.root_path + self.table_folder + "/" +self.table_name,
            index=False)
        
        print("{} updated successfully.".format(self.table_name))


class CurrencyIndicatorTableCreation(MainPageTableCreation):
    
    def __init__(self, root_path, table_folder, dataframes_folder, table_name, headers=[],
                data_processing=CurrencySpecificDataProcess()):
        super().__init__(root_path, table_folder, dataframes_folder, table_name, headers,
                data_processing)
        
    def add_to_table(self):
        self.dataframe_names_list = os.listdir(self.root_path + self.dataframes_folder)
        self.currency_indicators_table = self.create_empty_table()
        for dataframe_file in self.dataframe_names_list:
            self.currency_name = dataframe_file.split("_")[0]
            self.dataframe = pd.read_csv(self.root_path + self.dataframes_folder + "/" + dataframe_file)
            self.currency_specific_indicator_dataframe = self.data_processing.calculate_currency_indicators(self.dataframe, self.currency_name)
            self.currency_indicators_table = pd.concat([self.currency_indicators_table, self.currency_specific_indicator_dataframe],
                ignore_index=True)

        self.currency_indicators_table.to_csv(self.root_path + self.table_folder + "/" + self.table_name,
            index=False)
        
        print("{} created successfully.".format(self.table_name))

if __name__ == "__main__":
    url = "https://www.tgju.org/currency"
    cs = currency_scraper.CurrencyScrapper(url)
    dc = DataCreation(cs).update_dataframes()
    
    main_page_table = MainPageTableCreation(root_path = "..\codes\data\datasets", table_folder = "\main_page_table", 
                dataframes_folder = "\currency_dataframes",
                table_name = "main_page_currency_table.csv", data_processing = DataProcess()).add_to_table()
    
    currency_specific_indicator_table = CurrencyIndicatorTableCreation(root_path="..\codes\data\datasets",
                dataframes_folder = "\currency_dataframes", table_folder = "\currency_specific_indicators",
                table_name="currency_indicators_table.csv").add_to_table()

