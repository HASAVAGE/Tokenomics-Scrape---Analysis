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
driver.get('https://www.protonscan.io/tokens/LOAN-proton-loan.token')

try:
    element = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CLASS_NAME, "token-price"))
    )
    WebDriverWait(driver, 10)
    results = []
    content = driver.page_source
    soup = BeautifulSoup(content, features='lxml')
    b1 = soup.find('b', text='Market Cap').find_next().text
    b2 = soup.find('b', text='Daily Volume').find_next().text
    b3 = soup.find('b', text='Token Holders').find_next().text
    b4 = soup.find('b', text='Issued Supply').find_next().text
    grp = [b1, b2, b3, b4]

finally:
    driver.quit()

bute = []
for i in grp:
    z = re.findall(r'-?\d{1,3}.?,?\d{1,3}.?,?\d{1,3}.?,?\d{1,3}.?', i)
    z = listToString(z)
    z = str.replace(z, ',', '')
    bute.append(z)

# Load dataframe
now = datetime.now()
date = now.strftime("%d/%m/%Y %H:%M:%S")
data = {'Date': [date], 'Market Cap': [bute[0]], 'Daily Volume': [bute[1]],
        'Token Holders': [bute[2]], 'Issued Supply': [bute[3]]}
df = pd.DataFrame(data)
df['Price'] = float(df['Market Cap']) / float(df['Issued Supply'])
print(df)

# .csv processing
df.to_csv(r'C:\Users\19788\Desktop\Archive\Scripts\Incoming\loan2.csv', mode='a', index=False, header=False)
dxy = pd.read_csv(r'C:\Users\19788\Desktop\Archive\Scripts\Incoming\loan2.csv')
print(dxy)