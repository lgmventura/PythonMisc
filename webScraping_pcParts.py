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
csv_path = '/home/luiz/Documents/pc.csv'

# dict
d = {}

def getIdealoLowestPrice(url: str):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'}
    r=requests.get(url, headers=headers)
    soup1 = BeautifulSoup(r.content, 'lxml')
    
    # specific from idealo.de
    text_success = soup1.find('span', attrs={'class':'oopStage-conditionButton-wrapper-text-price-prefix'}).next_element.next_element.next_element
    price_str = text_success.string
    price_str_dotdec = price_str.replace(',', '.')
    price_str_dotdec = price_str_dotdec.replace('€', '')
    price = float(price_str_dotdec)
    return price
    

# intel i7 12700K
url = "https://www.idealo.de/preisvergleich/OffersOfProduct/201660528_-core-i7-12700k-intel.html"
price = getIdealoLowestPrice(url)
d['i7-12700K'] = price

# RAM
url = "https://www.idealo.de/preisvergleich/OffersOfProduct/201656031_-fury-beast-32gb-kit-ddr5-4800-cl38-kf548c38bbk2-32-kingston.html"
price = getIdealoLowestPrice(url)
d['Kingston32 KF548C38BBK2-32'] = price

# RAM 2
url = "https://www.idealo.de/preisvergleich/OffersOfProduct/201656965_-valueram-32gb-kit-ddr5-4800-cl40-kvr48u40bs8k2-32-kingston.html"
price = getIdealoLowestPrice(url)
d['Kingston32 KVR48U40BS8K2-32'] = price

# tower
url = "https://www.idealo.de/preisvergleich/OffersOfProduct/200988159_-quantum-v2-aerocool.html"
price = getIdealoLowestPrice(url)
d['Aerocool Quantum v2'] = price

# video card
url = "https://www.idealo.de/preisvergleich/OffersOfProduct/201413370_-geforce-rtx-3070-ti-msi.html"
price = getIdealoLowestPrice(url)
d['MSI GeForce RTX 3070 Ti'] = price

# video card 2
url = "https://www.idealo.de/preisvergleich/OffersOfProduct/200622613_-geforce-rtx-3080-asus.html"
price = getIdealoLowestPrice(url)
d['Asus GeForce RTX 3080'] = price

# HDD
url = "https://www.idealo.de/preisvergleich/OffersOfProduct/5430648_-p300-2tb-bulk-hdwd120uzsva-toshiba.html"
price = getIdealoLowestPrice(url)
d['HD Toshiba 2TB HDWD120UZSVA'] = price

# SSD
url = "https://www.idealo.de/preisvergleich/OffersOfProduct/200682744_-980-pro-1tb-m-2-samsung.html"
price = getIdealoLowestPrice(url)
d['SSD Samsung 1TB 980'] = price

# SSD 2
url = "https://www.idealo.de/preisvergleich/OffersOfProduct/200746059_-black-sn850-1tb-western-digital.html"
price = getIdealoLowestPrice(url)
d['SSD WD 1TB SN850'] = price

# Motherboard


# PSU
url = "https://www.idealo.de/preisvergleich/OffersOfProduct/201466860_-rm850-850w-2021-corsair.html"
price = getIdealoLowestPrice(url)
d['PSU Corsair RM850 850W'] = price


# creating a table file
if not os.path.isfile(csv_path):
    df = pd.DataFrame()
else:
    df = pd.read_csv(csv_path, index_col=0)

# checking last values
values_last = df.iloc[-1].values[1:] # exclude first, which is the datatime

values = np.array([*d.values()])

if values.shape != values_last.shape: # new element added into the observation list
    updDf = True
elif np.any(values != values_last): # some price changed
    updDf = True
else: # nothing changed, no need to insert a new row with everything unchanged
    updDf = False
    
if updDf == True:    
    now = datetime.datetime.now()
    now_str = now.isoformat()
    
    iData = {}
    iData['time'] = now_str
    iData.update(d)
    iDf = pd.DataFrame([iData])
    
    df = pd.concat([df, iDf], ignore_index=True)
    
    df.to_csv(csv_path)

# Plotting graph
if df.shape[0] > 1:
    dts = list(map(datetime.datetime.fromisoformat, df.time))
    dts = np.array(dts)
    total_price = df.sum(axis=1)
    plt.plot(dts, total_price)
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
