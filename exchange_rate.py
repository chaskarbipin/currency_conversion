#!/usr/bin/env python

import requests
import json
import os
import csv
from datetime import datetime, timedelta
import pandas as pd
import matplotlib.pyplot as plt
from dotenv import load_dotenv

def input_validation(currency_code, currency_list):
    if currency_code not in currency_list:
        return 1
    elif currency_code.isalpha() != True:
        return 1
    elif len(currency_code) != 3:
        return 1
    else:
        return 0
    
def get_url(url):
    """
    This function makes a call to the APILAYER and returns the API response
    """
    try:
        load_dotenv()
        payload = {}
        headers= {
          "apikey": os.getenv("API_KEY")
            }
        response = requests.request("GET", url, headers=headers, data = payload)
        status_code = response.status_code
        content = response.text
        return status_code, content
    except requests.exceptions.RequestException as e:
        print(f"Error making GET request: {e}")
        return None, None

def get_currencies_list(target=None):
    baseurl = "https://api.apilayer.com/fixer"
    url = f"{baseurl}/symbols"
    #print('URL', url)
    status_code, content = get_url(url)
    currencies = json.loads(content)
    currency_list = list(currencies['symbols'].keys())
    return currency_list


def load_currency_history(from_currency, to_currency, target=None):
    """
    This function receive API response and store in JSON format
    """
    #baseurl = "https://api.apilayer.com/exchangerates_data/timeseries"
    baseurl = "https://api.apilayer.com/fixer/"
    end_date = datetime. today().strftime("%Y-%m-%d")         #returns 2020-01-01
    start_date = (datetime.today() - timedelta(days=30)).strftime("%Y-%m-%d")
    base_currency = ''''''+from_currency+''''''
    symbols = from_currency.upper() + "," + to_currency.upper()

    url = "{0}timeseries?start_date={1}&end_date={2}&base={3}&symbols={4}".format(baseurl,start_date,end_date,base_currency,symbols)
    #print('URL', url)
    status_code, content = get_url(url)
    #print(status_code, content)
    
    if status_code == 200:
        with open("currency_history.json", 'w', encoding='utf-8') as f:
            f.write(content)  
            print("JSON file created here '",os.path.realpath(f.name),"'")
    else:
        return None

def pre_process_history(from_currency, to_currency, target=None):
    """
    This function read JSON format and process into CSV format
    """
    with open('currency_history.json') as json_file: 
        data_set = json.load(json_file)
        rates = data_set['rates']

        with open('temp.csv', 'w', newline='') as csv_file:
            for items in rates:
                writer = csv.writer(csv_file)
                writer.writerow([items, rates[items][''''''+from_currency+''''''], rates[items][''''''+to_currency+'''''']]) 

    file = pd.read_csv("temp.csv")
    processed_file = "currency_history.csv"
    headerList = ['CURRENCY_DATE', 'FROM_CURRENCY', 'TO_CURRENCY']
    file.to_csv("currency_history.csv", header=headerList, index=False) 
    os.remove("temp.csv")
    print("CSV file created here '",os.path.realpath(processed_file),"'")

    
def perform_data_analysis(target=None):
    """
    This function read CSV content and show some trends
    """
    csv_file =  pd.read_csv("currency_history.csv")
    min_rate = csv_file.min()
    print("\n#################################################################################")
    print(f"Lowest {to_currency} in the month (base currency={from_currency}) =>\n\tRATE = {min_rate['TO_CURRENCY']} \n\tDATE = {min_rate['CURRENCY_DATE']}")
    print("#################################################################################")
    max_rate = csv_file.max()
    print(f"Highest {to_currency} in the month (base currency={from_currency}) =>\n\tRATE = {max_rate['TO_CURRENCY']} \n\tDATE = {max_rate['CURRENCY_DATE']}")
    print("#################################################################################")
    average_rate = csv_file['TO_CURRENCY'].mean()
    print("Mean => ", average_rate)
    print("#################################################################################")
    plt.plot(csv_file['CURRENCY_DATE'], csv_file['TO_CURRENCY'])
    plt.xlabel("DATE")  # add X-axis label
    plt.ylabel(to_currency)  # add Y-axis label
    plt.title("CURRENCY GRAPH")  # add title
    plt.grid(True)
    plt.xticks(rotation=90)
    plt.show()


from_currency = input("Enter from currency code:")
to_currency = input("Enter to currency code:")
currency_list = get_currencies_list()

if input_validation(from_currency.upper(), currency_list) == 0 & input_validation(to_currency.upper(), currency_list) == 0:
    load_currency_history(from_currency, to_currency)
    pre_process_history(from_currency, to_currency)
    perform_data_analysis()
else:
    raise Exception("Currency code exception occurred")
