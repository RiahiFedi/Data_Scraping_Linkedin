# -*- coding: utf-8 -*-
"""
@author: fedir
"""

from selenium import webdriver
import csv
from time import sleep
import parameters 
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import random
import pandas as pd


def scroll_down():
    SCROLL_PAUSE_TIME=4
    #height=driver.execute_script("return document.body.scrollHeight")
    driver.execute_script("window.scrollTo({top: document.body.scrollHeight,left: 0,behavior: 'smooth'});")
    sleep(SCROLL_PAUSE_TIME)
    '''while True:
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
        sleep(SCROLL_PAUSE_TIME)
        max_height=driver.execute_script("return document.body.scrollHeight")
        if max_height == height:
            break
        height=max_height'''


driver = webdriver.Chrome('C:/Users/fedir/Data_Scraping_Linkedin/chromedriver')
driver.get('https://www.linkedin.com')
username = driver.find_element_by_id('session_key')
username.send_keys(parameters.linkedin_username)
sleep(random.randint(500,1000)/1000)
password = driver.find_element_by_id('session_password')
password.send_keys(parameters.linkedin_password)
sleep(random.randint(500,1000)/1000)
sign_in_button = driver.find_element_by_class_name('sign-in-form__submit-button')
sign_in_button.click()


driver.get('https://www.linkedin.com/posts/attijari-bank-tunisie_attijari-bank-espace-libre-service-bancaire-activity-6769179416443547648-N-K0/')
sleep(random.randint(500,1000)/1000)

# locate the reactions pannel
react_pannel = driver.find_element(By.XPATH, '//*[@id="ember77"]/ul/li[1]/button')
actions = ActionChains(driver)
actions.move_to_element(react_pannel).perform()
react_pannel.click()

react_pannel = driver.find_element(By.XPATH, '//*[@class="artdeco-modal__content social-details-reactors-modal__content ember-view"]')
allfoll=int(driver.find_element_by_xpath('//*[@class="ml0 p3 artdeco-tab active artdeco-tab--selected ember-view"]/div/span[2]').text)
for i in range(int(allfoll//6)):
    driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", react_pannel)
    sleep(random.randint(500,1000)/1000)
    
sel = driver.page_source
soup = BeautifulSoup(sel, 'lxml')
place_holder = soup.find('div',{'class' : 'artdeco-modal__content social-details-reactors-modal__content ember-view'})
profile_elements = place_holder.find_all('li',{'class' : 'artdeco-list__item'})

info = {'name' : [], 'profile_link' : [], 'reaction' : []}



for el in profile_elements:
    url = el.a['href']
    name = el.find('div',{'class' : 'artdeco-entity-lockup__title ember-view'}).span.text.strip()
    reaction = el.find('img',{'class' : 'reactions-icon social-details-reactors-tab-body__icon reactions-icon__consumption--small'})['alt']
    
    info['name'].append(name)
    info['profile_link'].append(url)
    info['reaction'].append(reaction)
    
df = pd.DataFrame(data=info)
df.to_csv('reactions.csv')
