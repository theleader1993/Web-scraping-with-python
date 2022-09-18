#!/usr/bin/env python
# coding: utf-8

# - Mục tiêu : Crawl toàn bộ giá của tất cả mã cổ phiếu trong lịch sử từ website được cty VNDIRECT lưu trữ sử dụng API

# In[17]:


from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import requests
import pandas as pd
import json

def convert_to_datetime(string):
    format = "%Y-%m-%d"
    return datetime.strptime(string,format)


def craw_data_vndirect(str_start_date):
    url = "https://finfo-api.vndirect.com.vn/v4/stock_prices"
    HEADERS = {'content-type': 'application/x-www-form-urlencoded', 'User-Agent': 'Mozilla'}
    
    start_date = convert_to_datetime(str_start_date)
    destination_date = start_date + relativedelta(months= 12)
    str_destination_date = destination_date.strftime("%Y-%m-%d")
    
    query = '~date:gte:' + str_start_date + '~date:lte:' + str_destination_date
    param_1 = {"q" : query , 'size': 5}
    response_1 = requests.get(url, params = param_1, headers = HEADERS)
    
    totalElements =  response_1.json()['totalElements']
    totalPages = (totalElements // 200000) + 1
    
    list_temp = []
    for i in range(1,totalPages +1):
        params_2 = {"q" : query , 'size': 200000, 'page': i}
        response_2 = requests.get(url,params = params_2, headers = HEADERS)
        df = pd.DataFrame(response_2.json()['data'])
        list_temp.append(df)
    return pd.concat(list_temp, ignore_index = True)

list_result = []
for i in range(2013, 2023):
    list_result.append(craw_data_vndirect(f"{i}-01-01"))
    print('complete năm: ', i)
print('successfull')


# In[18]:


df_result = pd.concat(list_result,ignore_index = True)
print(df_result.shape)
df_result.head()


# In[19]:


df_result.duplicated().value_counts()


# In[20]:


data_vndirect = df_result.drop_duplicates()
data_vndirect.shape


# In[21]:


data_vndirect.info(show_counts=True)


# In[22]:


#cuối cùng convert sang file csv để lưu trữ
data_vndirect.to_csv(r'C:\Users\daodq\Desktop\Đồ án cuối khóa\vndirect.csv', index =False)
print('complete')


# In[2]:


import pandas as pd
df = pd.read_csv("vndirect.csv")
df.head()


# In[ ]:




