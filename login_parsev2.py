# -*- coding: utf-8 -*-
"""
Created on Wed Mar 24 01:29:37 2021

@author: fedir
"""

from selenium import webdriver
import csv
from time import sleep
import parameters 
import requests
from bs4 import BeautifulSoup


# if field is present pass if field:pas if field is not present print text else:
def validate_field(field):
    if type(field) is not str:
       field = 'No results'
    return field

# defining new variable passing two parameters
#writer = csv.writer(open("test_data_frame", 'wb'))

# writerow() method to the write to the file object
#writer.writerow(['Name', 'Job Title', 'Company', 'College', 'Location', 'URL'])

# specifies the path to the chromedriver.exe
driver = webdriver.Chrome('C:/Users/fedir/Data_Scraping_Linkedin/chromedriver')

# driver.get method() will navigate to a page given by the URL address
driver.get('https://www.linkedin.com')

# locate email form by_class_name
username = driver.find_element_by_id('session_key')

# send_keys() to simulate key strokes
username.send_keys(parameters.linkedin_username)

# sleep for 0.5 seconds
sleep(0.5)

# locate password form by_class_name
password = driver.find_element_by_id('session_password')

# send_keys() to simulate key strokes
password.send_keys(parameters.linkedin_password)
sleep(0.5)

# locate submit button by_xpath
sign_in_button = driver.find_element_by_class_name('sign-in-form__submit-button')

# .click() to mimic button click
sign_in_button.click()


#Getting the collected Linkedin urls
url_fl = open(parameters.urls_file_name, "r")
linkedin_urls = []
for line in url_fl:
  stripped_line = line.strip()
  linkedin_urls.append(stripped_line)
url_fl.close()

f = open(parameters.file_name, 'w')
writer = csv.writer(f)

# writerow() method to the write to the file object
writer.writerow(['Name','Job Title','Company','College', 'Location','URL'])

from parsel import Selector
# For loop to iterate over each URL in the list

linkedin_url = linkedin_urls[9]

def extract_profil(linkedin_url):
    
    page = requests.get(linkedin_url)
    soup = BeautifulSoup(page.content, 'html.parser')

    info=[]
    
    try:
        name_div=soup.find('div',{'class' : 'flex-1 mr5'})
        name_loc=name_div.find_all('ul')
        name=name_loc[0].li.text.strip()
        location=name_loc[1].li.text.strip()
        profile_title=name_div.h2.text.strip()
        exp_section=soup.find('section',{'id' : 'experience-section'}).ul.li.div.a
        entreprise_name=exp_section.find('h3').text.strip().replace('Nom de l’entreprise','').strip()
        Duration=exp_section.find('h4').text.strip().replace('Durée totale','').strip()
        job_div=soup.find('div',{'class': 'pv-entity__summary-info-v2 pv-entity__summary-info--background-section pv-entity__summary-info-margin-top'})
        job_title=job_div.find('h3').text.strip().replace('Poste','').strip()
        job_duration=job_div.find('span',{'class':'pv-entity__bullet-item-v2'}).text.strip() 
        
    except AttributeError:
        entreprise_name=''
        Duration=''
        job_title=''
        job_duration=''
        
        
    info.append(linkedin_url)
    info.append(name)
    info.append(location)
    info.append(profile_title)
    info.append(entreprise_name)
    info.append(Duration)
    info.append(job_title)
    info.append(job_duration)
    #info.append(extract_mail())
    #info.append(extract_birthday())

    return info

results = []
for linkedin_url in linkedin_urls:
    results.append(extract_profil(linkedin_url))
    
    
    
for linkedin_url in linkedin_urls:
    
    # get the profile URL 
    driver.get(linkedin_url)
    
    # add a 5 second pause loading each URL
    sleep(12)
    
    # assigning the source code for the webpage to variable sel
    sel = Selector(text=driver.page_source) 
    
    
    # xpath to extract the text from the class containing the name
    name = sel.CLASS_NAME('flex-1 mr5').extract_first()
    if name:
        name = name.strip()
    
    
    # xpath to extract the text from the class containing the job title
    job_title = sel.xpath('//*[@id="ember47"]/div[2]/div[2]/div[1]/h2/text()').extract_first()
    
    if job_title:
        job_title = job_title.strip()
    
    
    # xpath to extract the text from the class containing the company
    company = sel.xpath('//*[@id="ember55"]/text()').extract_first()
    
    if company:
        company = company.strip()
    
    
    # xpath to extract the text from the class containing the college
    college = sel.xpath('//*[@id="ember58"]/text()').extract_first()
    
    if college:
        college = college.strip()
    
    
    # xpath to extract the text from the class containing the location
    location = sel.xpath('//*[@id="ember47"]/div[2]/div[2]/div[1]/ul[2]/li[1]/text()').extract_first()
    
    if location:
        location = location.strip()
    
    sel = None
    
    linkedin_url = driver.current_url
    
    print('\n')
    print(type(name))
    
    print(type(job_title))
    
    print(type(company))
    
    print(type(college))
    
    print(type(location))
    
    print(type(linkedin_url))
    print('\n')
    
    name = validate_field(name)
    job_title = validate_field(job_title)
    company = validate_field(company)
    college = validate_field(college)
    location = validate_field(location)
    linkedin_url = validate_field(linkedin_url)
    
    print('\n')
    print(type(name))
    print('Name: ' + name)
    
    print(type(job_title))
    print('Job Title: ' + job_title)
    
    print(type(company))
    print('Company: ' + company)
    
    print(type(college))
    print('College: ' + college)
    
    print(type(location))
    print('Location: ' + location)
    
    print(type(linkedin_url))
    print('URL: ' + linkedin_url)
    print('\n')
    
    writer.writerow([name.encode('utf-8'),
                 job_title.encode('utf-8'),
                 company.encode('utf-8'),
                 college.encode('utf-8'),
                 location.encode('utf-8'),
                 linkedin_url.encode('utf-8')])
    
    name = None
    job_title = None
    company = None
    college = None
    location = None
    
# terminates the application
# terminates the application
driver.quit()
f.close()