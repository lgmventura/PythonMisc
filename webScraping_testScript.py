#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Testing web scraping

Created on Mon Apr 11 19:13:19 2022

@author: luiz
"""
#from urllib.request import urlopen

from bs4 import BeautifulSoup
import requests
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as md
import os
#from pathlib import Path
import datetime

# initial settings
csv_path = '/home/luiz/Documents/eur_brl.csv'

#url='https://www.accuweather.com/en/in/surat/202441/daily-weather-forecast/202441'
url = "https://wise.com/de/currency-converter/eur-to-brl-rate"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'}
r=requests.get(url, headers=headers)
soup1 = BeautifulSoup(r.content, 'lxml') 
#print(soup1.prettify())

# specific from wise.com
text_success = soup1.find('span', attrs={'class':'text-success'})
rate_str = text_success.string
rate_str_dotdec = rate_str.replace(',', '.')

rate = float(rate_str_dotdec)

# creating a table file
if not os.path.isfile(csv_path):
    df = pd.DataFrame()
else:
    df = pd.read_csv(csv_path, index_col=0)

# checking last rate
rate_last = df.rate.iloc[-1]

if rate != rate_last:
    now = datetime.datetime.now()
    now_str = now.isoformat()
    
    iData = {'time': now_str, 'rate': rate}
    iDf = pd.DataFrame([iData])
    
    df = pd.concat([df, iDf], ignore_index=True)
    
    df.to_csv(csv_path)

# Plotting graph
if df.shape[0] > 1:
    dts = list(map(datetime.datetime.fromisoformat, df.time))
    dts = np.array(dts)
    rates = df.rate
    plt.plot(dts, rates)
    plt.subplots_adjust(bottom=0.2)
    plt.xticks(rotation=25)
    xfmt = md.DateFormatter('%Y-%m-%d %H:%M:%S')
    ax=plt.gca()
    ax.xaxis.set_major_formatter(xfmt)

    plt.grid(True, which='major', color=(0.8, 0.8, 0.8), alpha=0.5)
    plt.grid(True, which='minor', color=(0.8, 0.8, 0.8), alpha=0.1)
    plt.minorticks_on()
    plt.xlabel("Date and time")
    plt.ylabel("Brl / Eur")
