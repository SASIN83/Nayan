from datetime import datetime, time
import pandas as pd
import os
from pathlib import Path
import requests
import csv
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
#create report csv file date-wise if doesnot exist
def ReportFileCreate():
    NameList=[]
    now= datetime.now()
    dstr,tstr=now.date(),now.time()
    #info=,'Date':dstr,'Month':dstr.strftime("%B"),'Year':dstr.strftime("%Y"),'Time':tstr.strftime("%X")}
    train_data= pd.DataFrame()
    train_data['Name'] = NameList
    train_data['Type'] = []
    train_data['Location']=[]
    train_data['Time'] = tstr.strftime("%X")
    train_data['Date'] = dstr
    train_data['Month'] = dstr.strftime("%B")
    train_data['Year'] = dstr.strftime("%Y")
    
    if os.path.exists(os.path.join(BASE_DIR,'/Recognize/Records/Records-{}.csv'.format(dstr))):
        pass
    else:
        train_data.to_csv(os.path.join(BASE_DIR,'Recognize/Records/Records-{}.csv'.format(dstr)),header=True, index=False,encoding='utf-8',sep=';')

#Enter details to csv of case
def ReportFileEdit(name,category):
    x = os.path.isfile(os.path.join(BASE_DIR,'Recognize/Records/Records-{}.csv'.format(datetime.now().date())))
    if x==False:
        ReportFileCreate()
    
    with open(os.path.join(BASE_DIR,'Recognize/Records/Records-{}.csv'.format(datetime.now().date())),'r+',encoding='utf-8') as f:
        loc = requests.get('https://ipinfo.io/json').json()
        info=pd.read_csv(os.path.join(BASE_DIR,'Recognize/Records/Records-{}.csv'.format(datetime.now().date())),delimiter=';')
        NameList = []
        now= datetime.now()
        dstr,tstr=now.date(),now.time()
        location = [loc['city'],loc['region'],loc['country']]
        print(info.values)
        for line in info:
            entry = line.split(';')
            NameList.append(entry[0])  
            f.writelines(f'{name},{category},{location},{tstr.strftime("%X")},{dstr},{dstr.strftime("%B")},{dstr.strftime("%Y")}\n')
        
#data = {'Name':name,'Type':category,'Location':location,'Time':tstr.strftime("%X"),'Date':dstr,'Month':dstr.strftime("%B"),'Year':dstr.strftime("%Y")}
ReportFileEdit('Sasin','Red')
pd.read_csv(os.path.join(BASE_DIR,'Recognize/Records/Records-{}.csv'.format(datetime.now().date()))).drop_duplicates(subset=['Name','Location'],keep='last')
