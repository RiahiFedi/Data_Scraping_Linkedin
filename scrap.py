# -*- coding: utf-8 -*-
"""
Created on Mon May 24 21:06:51 2021

@author: fedir
"""

           ''' if len(job_list[-1].find_all('button',{'class':'pv-profile-section__see-more-inline pv-profile-section__text-truncate-toggle artdeco-button artdeco-button--tertiary artdeco-button--muted'})) > 0:
           
                #more_pannel = driver.find_element_by_class_name('pv-experience-section__see-more pv-profile-section__actions-inline ember-view')
                more_pannel = driver.find_element(By.ID,"experience-section")
                more_pannel = more_pannel.find_elements(By.CLASS_NAME, 'pv-entity__position-group-pager pv-profile-section__list-item ember-view')
                more_pannel = more_pannel[-1].find_element(By.XPATH, '//*[@class="pv-experience-section__see-more pv-profile-section__actions-inline ember-view"]')
                actions = ActionChains(driver)
                actions.move_to_element(more_pannel).perform()
                more_pannel = more_pannel.find_elements(By.XPATH, '//*[@class="pv-profile-section__see-more-inline pv-profile-section__text-truncate-toggle artdeco-button artdeco-button--tertiary artdeco-button--muted"]')[-1]
                actions = ActionChains(driver)
                more_pannel.click()
                sel = driver.page_source
                soup = BeautifulSoup(sel, 'lxml') ''' 