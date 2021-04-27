# -*- coding: utf-8 -*-
"""
@author: fedir
"""

# imports
from selenium import webdriver
import csv
from time import sleep
import parameters 
from bs4 import BeautifulSoup

# if field is present pass if field:pas if field is not present print text else:
def validate_field(field):
    if type(field) is not str:
       field = 'No results'
    return field
# defining new variable passing two parameters
writer = csv.writer(open("test_data_frame", 'w'))

# writerow() method to the write to the file object
writer.writerow(['Name', 'Job Title', 'Company', 'Duration', 'Location', 'URL'])

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
writer.writerow(['Name','Job Title','Company','Duration', 'Location','Education','URL'])

# For loop to iterate over each URL in the list

linkedin_url = linkedin_urls[4]


for linkedin_url in linkedin_urls:
  
    # get the profile URL 
    driver.get(linkedin_url)
    
    # add a 5 second pause loading each URL
    sleep(5)
    
    
    scroll_down()
    
    # assigning the source code for the webpage to variable sel
    sel = driver.page_source
    soup = BeautifulSoup(sel, 'lxml')
    
    
    name_div=soup.find('div',{'class' : 'flex-1 mr5'})
    
    info=[]
        
    try:
        name_div=soup.find('div',{'class' : 'flex-1 mr5 pv-top-card__list-container'})
        name_loc=name_div.find_all('ul')
        
        name=name_loc[0].li.text.strip()
        location=name_loc[1].li.text.strip()
        profile_title=name_div.h2.text.strip()
        
        big_div = soup.find('div',{'class' : 'display-flex mt2 pv-top-card--reflow'})
        work_div = big_div.find_all('div')
        place_holder = work_div[1].find_all('a', {'class' : 'pv-top-card--experience-list-item'})
        
        if len(place_holder)>1:
            entreprise_name = place_holder[0].span.text.strip()
            education = place_holder[1].span.text.strip()
        else:
            education = place_holder[0].span.text.strip()
            entreprise_name = 'Currently Unemployed'
            
        exp_section=soup.find('section',{'id' : 'experience-section'}).ul.li
        #place_holder = exp_section.find_all('div',{'class' : 'pv-entity__summary-info pv-entity__summary-info--background-section mb2'})
        place_holder = exp_section.find('h4')
        place_holder = place_holder.find_all('span')
        Duration = place_holder[1].text.strip()
        
        
        #exp_section=soup.find('section',{'id' : 'experience-section'}).ul.li.div.a
        #entreprise_name=exp_section.find('h3').text.strip().replace('Nom de l’entreprise','').strip()
        #Duration=exp_section.find('h4').text.strip().replace('Durée totale','').strip()
        #job_div=soup.find('div',{'class': 'pv-entity__summary-info-v2 pv-entity__summary-info--background-section pv-entity__summary-info-margin-top'})
        #job_title=job_div.find('h3').text.strip().replace('Poste','').strip()
        #job_duration=job_div.find('span',{'class':'pv-entity__bullet-item-v2'}).text.strip() 
        
    except AttributeError:
        print('lol')
        #Duration=''
        #job_title=''
        #job_duration=''
        
        

    info.append(name)
    info.append(profile_title)
    info.append(entreprise_name)
    info.append(Duration)
    info.append(location)
    info.append(education)
    info.append(linkedin_url)
    #info.append(job_title)
    #info.append(job_duration)
    #info.append(extract_mail())
    #info.append(extract_birthday())
    print(info)

    writer.writerow([name.encode('utf-8'),
             profile_title.encode('utf-8'),
             entreprise_name.encode('utf-8'),
             Duration.encode('utf-8'),
             location.encode('utf-8'),
             education.encode('utf-8'),
             linkedin_url.encode('utf-8')])


    name = None
    profile_title = None
    entreprise_name = None
    Duration = None
    location = None

   
# terminates the application
# terminates the application
driver.quit()
f.close()


