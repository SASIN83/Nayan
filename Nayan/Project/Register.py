from datetime import datetime, time
import pandas as pd
import os
from pathlib import Path
import requests
import csv
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
#create report csv file date-wise if doesnot exist
path = os.path.join(BASE_DIR,'Recognize/Records/Records-{}.csv'.format(datetime.now().date()))
def ReportFileCreate():
    now= datetime.now()
    dstr,tstr=now.date(),now.time()
    train = {'Name':[],
    'Type':[],
    'ID':[],
    'Location':[],
    'Time':[],
    'Date':[],
    'Month':[],
    'Year':[]}
    df = pd.DataFrame(train)
    if os.path.exists(os.path.join(BASE_DIR,'/Recognize/Records/Records-{}.csv'.format(dstr))):
        pass
    else:
        df.to_csv(path,header=True,index=False,encoding='utf-8')

#Enter details to csv of case
def ReportFileEdit(name,category,ids):
    x = os.path.isfile(path)
    if x==False:
        ReportFileCreate()
    
    loc = requests.get('https://ipinfo.io/json').json()
    NameList = []
    now= datetime.now()
    dstr,tstr=now.date(),now.time()
    location = [loc['city'],loc['region'],loc['country']]
    pf = {'Name':[name],
            'Type':[category],
            'ID':[ids],
            'Location':[location],
            'Time':[str(tstr.strftime("%X"))],
            'Date':[str(dstr)],
            'Month':[str(dstr.strftime("%B"))],
            'Year':[str(dstr.strftime("%Y"))]}
    df = pd.DataFrame(pf)
    df.to_csv(path,index=False,header = False,mode = 'a')
    pd.read_csv(path).drop_duplicates(subset=['ID','Location'],keep='last').to_csv(path,header=True,index=False)

#data = {'Name':name,'Type':category,'Location':location,'Time':tstr.strftime("%X"),'Date':dstr,'Month':dstr.strftime("%B"),'Year':dstr.strftime("%Y")}


