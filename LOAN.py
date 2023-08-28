import pandas as pd
import re, os
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options

# Function to convert
def listToString(s):
    # initialize an empty string
    str1 = ""
    # traverse in the string
    for ele in s:
        str1 += ele
        # return string
    return str1

# Headless driver configuration
opts = Options()
opts.headless = True
driver = webdriver.Firefox(executable_path=r'C:\Users\19788\Desktop\Archive\Path Drags\geckodriver.exe', options=opts)
driver.get('https://www.protonscan.io/supply/#loan')

try:
    element = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CLASS_NAME, "tabs-component-tab-a"))
    )
    WebDriverWait(driver, 10)
    results = []
    content = driver.page_source
    soup = BeautifulSoup(content, features='lxml')
    a1 = soup.find('b', text='Issued:').find_previous().text
    a2 = soup.find('b', text='Vesting:').find_previous().text
    a3 = soup.find('b', text='Staked:').find_previous().text
    a4 = soup.find('b', text='Farming and Staking Rewards:').find_previous().text
    a5 = soup.find('b', text='Pooled Liquidity:').find_previous().text
    a6 = soup.find('b', text='Undistributed Exchanges:').find_previous().text
    a7 = soup.find('b', text='Circulating:').find_previous().text
    raw = [a1, a2, a3, a4, a5, a6, a7]

finally:
    driver.quit()

buk = []
for i in raw:
    z = re.findall(r'-?\d{1,3},?\d{1,3},?\d{1,3},?\d{1,3}', i)
    z = listToString(z)
    z = int(str.replace(z, ',', ''))
    buk.append(z)

# Load dataframe
now = datetime.now()
date = now.strftime("%d/%m/%Y %H:%M:%S")
data = {'Date': [date], 'Issued': [buk[0]], 'Vesting': [buk[1]], 'Staked': [buk[2]], 'Farming and Staking Rewards': [buk[3]], 'Pooled Liquidity': [buk[4]], 'Undistributed Exchanges': [buk[5]], 'Circulating': [buk[6]]}
df = pd.DataFrame(data)

# .csv processing
df.to_csv(r'C:\Users\19788\Desktop\Archive\Scripts\Incoming\loan.csv', mode='a', index=False, header=False)
dxy = pd.read_csv(r'C:\Users\19788\Desktop\Archive\Scripts\Incoming\loan.csv')
print(dxy)