#!/usr/bin/env python

import requests
import json
import os
import csv
from datetime import datetime, timedelta
import pandas as pd
import matplotlib.pyplot as plt


def get_url(url):
    """
    This function makes a call to the APILAYER and returns the API response
    """
    try:
        payload = {}
        headers= {
          "apikey": "G53JIyJhFpqlj1Km9r08bwTUkOWyFbYC"
            }
        response = requests.request("GET", url, headers=headers, data = payload)
        status_code = response.status_code
        content = response.text
        return status_code, content
    except requests.exceptions.RequestException as e:
        print(f"Error making GET request: {e}")
        return None, None
    
def load_currency_history(target=None):
    """
    This function receive API response and store in JSON format
    """
    #baseurl = "https://api.apilayer.com/exchangerates_data/timeseries"
    baseurl = "https://api.apilayer.com/fixer/timeseries"
    end_date = datetime. today().strftime("%Y-%m-%d")         #returns 2020-01-01
    start_date = (datetime.today() - timedelta(days=30)).strftime("%Y-%m-%d")
    base_currency = 'AUD'
    symbols = 'AUD,NZD'

    url = "{0}?start_date={1}&end_date={2}&base={3}&symbols={4}".format(baseurl,start_date,end_date,base_currency,symbols)
    print('URL', url)
    status_code, content = get_url(url)
    print(status_code, content)
    
    if status_code == 200:
        with open("currency_history.json", 'w', encoding='utf-8') as f:
            f.write(content)  
            print("JSON file created here '",os.path.realpath(f.name),"'")
    else:
        return None

def pre_process_history(target=None):
    """
    This function read JSON format and process into CSV format
    """
    with open('currency_history.json') as json_file: 
        data_set = json.load(json_file)
        rates = data_set['rates']

        with open('temp.csv', 'w', newline='') as csv_file:
            for items in rates:
                writer = csv.writer(csv_file)
                writer.writerow([items, rates[items]['AUD'], rates[items]['NZD']]) 

    file = pd.read_csv("temp.csv")
    processed_file = "currency_history.csv"
    headerList = ['CURRENCY_DATE', 'AUD_RATE', 'NZD_RATE']
    file.to_csv("currency_history.csv", header=headerList, index=False) 
    os.remove("temp.csv")
    print("CSV file created here '",os.path.realpath(processed_file),"'")

    
def perform_data_analysis(target=None):
    """
    This function read CSV content and show some trends
    """
    csv_file =  pd.read_csv("currency_history.csv")
    min_rate = csv_file.min()
    print("\nLowest in the month =>\nNZD = ", min_rate['NZD_RATE'], "\nDATE = ", min_rate['CURRENCY_DATE'])
    max_rate = csv_file.max()
    print("\nHighest in the month =>\nNZD = ", max_rate['NZD_RATE'], "\nDATE = ", max_rate['CURRENCY_DATE'])
    average_rate = csv_file['NZD_RATE'].mean()
    print("\nMean => ", average_rate)
    plt.plot(csv_file['CURRENCY_DATE'], csv_file['NZD_RATE'])
    plt.xlabel("DATE")  # add X-axis label
    plt.ylabel("NZD")  # add Y-axis label
    plt.title("CURRENCY GRAPH")  # add title
    plt.grid(True)
    plt.xticks(rotation=90)
    plt.show()

    
#load_currency_history()
pre_process_history()
perform_data_analysis()
