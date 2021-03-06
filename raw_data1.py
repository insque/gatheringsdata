# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import os
import requests
import sys
import code
#from _pytest._code.code import Code
reload(sys)
sys.setdefaultencoding('utf-8')

import sqlite3
import numpy as np
import pandas as pd
from pandas.io import sql
import datetime
import re


def del_duplicated(code):
    code='A'+code
    conn = sqlite3.connect('kospi_minute.db')
    c=conn.cursor()
    cmd='DELETE FROM %s WHERE rowid NOT IN (SELECT rowid FROM %s group by [index] )'%(code,code)
    c.execute(cmd)
    print("Sanitized DB")
    conn.commit()
    conn.close()
    pass


def db_write(code,data):
    code="A"+code
    conn = sqlite3.connect('kospi_minute.db')
    print("DB connected table for %s"%code)
    #c = conn.cursor()
    #cmd='CREATE TABLE %s (date text, time text, price text, perLastday text, sellprice text, buyprice text, volume text)'%code
    #c.execute(cmd)
    data.to_sql(code,conn,flavor=None,schema=None,if_exists='append',index=True,index_label=None)
    conn.commit()
    conn.close()
'''
df = pd.DataFrame(data.items(), columns=['Date', 'DateValue'])
df['Date'] = pd.to_datetime(df['Date'])
'''
def read_db(code):
    code='A'+code
    conn = sqlite3.connect('kospi_minute.db')
    print("Read: DB connected table for %s"%code)
    cmd='SELECT * from %s'%code
    read_data=pd.read_sql(cmd,conn)
    print(read_data)
    return read_data
    
    
def get_sise_daily(code):
    day_data={}
    for page in range(1,41):
        print page
        page=str(page)
        
        thisday=datetime.datetime.now().strftime("%Y%m%d")
        
        #######test##########
        thisday='20180314' #This is for test 
        #####################
        thistime=thisday+"180000"
        url="http://finance.naver.com/item/sise_time.nhn?code=%s&thistime=%s&page=%s"%(code,thistime,page)
        html_doc=requests.get(url)
        data=html_doc.text
        soup = BeautifulSoup(data,"lxml")
        
        print("page address= %s"%url)
        #print(soup.find_all('td'))
        soup_tds=soup.find_all('span')
        i=7
        data=[]
        for item in soup_tds:
            if item.text=='시간별':
                pass
            else:
                data.append(item.text.strip())
                #print(item.text.strip())
        print(len(data))
        if len(data)==70 and page!='40':
            print('Parsing sucess')
        else:
            if (len(data)!=0 or len(data)==42 or len(data)==35) and (page=='40':
                print('Parsing sucess')
            
            else:
                print("ERROR: Parsing failed")
                #sys.exit()
                break
        min_data=[]
        min_data_tmp=[]
            
        a=1
        #print(data)
        for item in data:
            tmp=item
            #print(tmp)
            min_data_tmp.append(tmp)
            if a==7:
                timestamp=thisday+min_data_tmp[0].replace(':','')
                #print(timestamp)
                a=1
                day_data[timestamp]=min_data_tmp
                min_data_tmp=[]
            else:
                a=a+1
        
    print(day_data)
    df=pd.DataFrame.from_dict(day_data)
    df=df.T
    print(df)
    db_write(code,df)
    del_duplicated(code)

def kospi_code():
    code=[]
    page=1
    while(True):
        print(page)
        try:
            page=str(page)
            url='http://finance.naver.com/sise/sise_market_sum.nhn?sosok=0&page=%s'%page
            html_doc=requests.get(url)
            data=html_doc.text
            soup = BeautifulSoup(data,"lxml")
            #print("page address= %s"%url)
            #print(soup)
            #print(soup.find_all(href=re.compile("/item/main.nhn?code")  ))    
            tmp=[]
            tmp=soup.find_all('a', attrs={'href':re.compile("[:[:/item/main.nhn?code=:][0-9]{6}$"), 'class':'tltle'})
            #print(len(tmp))
            if len(tmp)==0:
                break
            for item in tmp:
                code.append(item.get('href').split("=")[1])
            #print(code)
        except:
            pass
        page=int(page)
        page=page+1
        
    print("Kospi code= ",code)
    f=open("kospi.txt",'w')
    f.writelines(["%s\n"%item for item in code])
    return code
def kosdak_code():
    code=[]
    page=1
    while(True):
        print(page)
        try:
            page=str(page)
            url='http://finance.naver.com/sise/sise_market_sum.nhn?sosok=1&page=%s'%page
            html_doc=requests.get(url)
            data=html_doc.text
            soup = BeautifulSoup(data,"lxml")
            #print("page address= %s"%url)
            #print(soup)
            #print(soup.find_all(href=re.compile("/item/main.nhn?code")  ))    
            tmp=[]
            tmp=soup.find_all('a', attrs={'href':re.compile("[:[:/item/main.nhn?code=:][0-9]{6}$"), 'class':'tltle'})
            #print(len(tmp))
            if len(tmp)==0:
                break
            for item in tmp:
                code.append(item.get('href').split("=")[1])
            #print(code)
        except:
            pass
        page=int(page)
        page=page+1
        
    print("Kosdak code= ",code)
    f=open("kosdak.txt",'w')
    f.writelines(["%s\n"%item for item in code])
    return code

def data_get():
    kospi=kospi_code()
    kosdak=kosdak_code()
    for code in kospi:
        print("data_get:)",code)
        get_sise_daily(code)

    for code in kosdak():
        print("data_get:)",code)
        get_sise_daily(code)
    

if __name__ == '__main__':
    code = '215600'
    #get_sise_daily(code)
    #read_db(code)
    #kospi_code()
    #kosdak_code()
    data_get()
