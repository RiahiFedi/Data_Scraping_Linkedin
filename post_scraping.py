# -*- coding: utf-8 -*-
"""
@author: fedir
"""

from selenium import webdriver
import csv
from time import sleep
import parameters 
from bs4 import BeautifulSoup
from login import scroll_down,login_sequence



driver = webdriver.Chrome('C:/Users/fedir/Data_Scraping_Linkedin/chromedriver')

login_sequence()

driver.get('https://www.linkedin.com/posts/attijari-bank-tunisie_attijari-bank-espace-libre-service-bancaire-activity-6769179416443547648-N-K0/')
sleep(1)
scroll_down()

# locate the reactions pannel
react_pannel = driver.find_element_by_id('ember83').ul.li.click()

