# -*- coding: utf-8 -*-
"""
Created on Mon May 24 11:48:21 2021

@author: fedir
"""


import pandas as pd
from datetime import datetime


data = pd.read_csv('results_file0.csv')
reaction = pd.read_csv('reactions.csv')

data = pd.read_csv('results_file_processed00.csv')
reaction = pd.read_csv('results_file_processed.csv')

l = range(104)
data = data.iloc[l]
reaction = reaction.iloc[l]

data.columns
data.info()
reaction.columns
reaction.info()

data = data.drop(['duration','experience','location'],axis = 1)
data.info()
data.sort_values("linkedin_url", inplace = True)
data.drop_duplicates(subset = 'linkedin_url',keep = False, inplace = True)

resutls = pd.concat([data,reaction])
resutls = resutls.drop(['duration','experience','location'],axis = 1)
resutls.sort_values("name_x", inplace = True)
resutls.drop_duplicates(subset = 'name_x',keep = False, inplace = True)
resutls.info()

resutls.to_csv('results_file_processed2.csv', encoding = 'utf-8-sig',index = False,sep = ',')


df = pd.merge(data,reaction,on='linkedin_url')


df.columns
df = df.drop(columns=['Unnamed: 0_x','Unnamed: 0_y','name_y','education'])




def calc_time(str_time):
    if str_time=='0':
        return 0
    if str_time == '-':
        return 0
    dates = str_time.split('–')
    for i in range(len(dates)):
        dates[i] = dates[i].strip()
    print(dates)
    try:   
        if dates[-1] == 'Present' or dates[-1] == '' :
            last = datetime.now()
        else:
            if len(dates[-1].split(' '))>1:
                last = datetime.strptime(dates[-1], "%b %Y")
            else:
                print(dates[-1])
                last = datetime.strptime(dates[-1], "%Y")
        if len(dates[0].split(' '))>1:
            first  = datetime.strptime(dates[0], "%b %Y")
        else:
            first  = datetime.strptime(dates[0], "%Y")
        d_time = last - first
        return d_time.days
    except ValueError:
        print(dates[-1])
        return 'sorry'

def match_reg(loc):
    switcher = {
        'Ariana':'Grand -Tunis',
        'Ben Arous':'Grand -Tunis',
        'Manouba':'Grand -Tunis',
        'Nabeul': 'Nord-Est',
        'Zaghouan':'Nord-Est',
        'Bizerte':'Nord-Est',
        'Beja':'Nord-Ouest',
        'Jendouba':'Nord-Ouest',
        'Le Kef':'Nord-Ouest',
        'Siliana':'Nord-Ouest',
        'Sousse':'Centre-Est',
        'Monastir':'Centre-Est',
        'Mahdia':'Centre-Est',
        'Sfax':'Centre-Est',
        'Kairouan':'Centre-Ouest',
        'Kasserine':'Centre-Ouest',
        'Sidi Bouzid':'Centre-Ouest',
        'Gabes':'Sud-Est',
        'Medenine':'Sud-Est',
        'Tataouine':'Sud-Est',
        'Gafsa':'Sud-Ouest',
        'Tozeur': 'Sud-Ouest',
        'Kebili':'Sud-Ouest'
        }
    return switcher.get(loc,"unknown")

def region_class(location):
    if location == 'Tunisia':
        return 'Grand -Tunis'
    c = location.split(',')
    if c[-1].strip() != 'Tunisia':
        return 'Other'
    elif c[0].strip() =='Tunis':
        return 'Grand -Tunis' 
    else:
        loc = c[-2].split(' ')
        if loc[-1].strip()=='Governorate':
            return match_reg(loc[0].strip())
        else:
            return 'unknown'
        
def data_process(df):
    df['experience'] = df['experience'].fillna('0')
    df['duration'] = df['duration'].fillna('0')
    df['location'] = df['location'].fillna('unknown')
    df['nbr_employees'] = df['nbr_employees'].fillna(0)
    df.loc[df.duration == '0', 'work_field'] = "unemployed"
    df['work_field'] = df['work_field'].fillna('unknown')
    df = df.dropna()
            
    l = df['location']
    reg = []
    for i in l:
        reg.append(region_class(i))
    df['region'] = reg
                   
    t1 = df['duration']
    dur1 = []
    for i in t1:
        dur1.append(calc_time(i))
    df['current_job_duration'] = dur1
    
    t2 = df['experience']
    dur2 = []
    for i in t2:
        dur2.append(calc_time(i))
    df['total_experience'] = dur2
    
    if 'reaction' in df.columns:
        df = df.drop(columns=['duration','experience','location'])
        df.loc[df.reaction == 'INTEREST', 'reaction'] = 'PRAISE'
        df.loc[df.reaction == 'MAYBE', 'reaction'] = 'EMPATHY'
    return df

df = data_process(df)

df.to_csv('results_file_processed00.csv', encoding = 'utf-8-sig',index = False,sep = ',')
