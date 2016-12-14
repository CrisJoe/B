# -*- coding: utf-8 -*-
"""
Created on Wed Dec 14 10:03:29 2016

@author: CrisJoe


Barra main program

"""


import mysql.connector

from WindPy import *

import numpy as np

import pandas as pd

from pandas import Series, DataFrame

# import barra_main_fun as bmf





conn = mysql.connector.connect(user='root', password='password',  
                               database='ffactors', use_unicode=True)
cursor = conn.cursor()

BegT = '2009-01-01'
EndT = '2016-09-30'

factor_names = ['ETOP', 'ETP5', 'EXTE', 'VFLO', 'VERN', 'PAYO', 'VCAP', 'AGRO',
                'EGRO', 'DELE', 'S_SalseG', 'C_SalseG', 'T_SalseG', 'S_ProfitG',
                'C_ProfitG', 'T_ProfitG', 'S_CFOG', 'C_CFOG', 'T_CFOG', 'S_ROEG', 
                'C_ROEG', 'T_ROEG', 'S_ROAG', 'C_ROAG', 'T_ROAG', 'MLEV', 'BLEV', 
                'DTOA', 'STO_1M', 'STO_3M', 'STO_6M', 'STO_12M', 'STO_60M', 
                'HALPHA', 'RSTR_1M', 'RSTR_3M', 'RSTR_6M', 'RSTR_12M', 'LNCAP',
                'LNCAPCB', 'BTOP', 'STOP', 'EBITDAvsEV', 'HILO', 'BTSG', 'DASTD', 
                'LPRI', 'CMRA', 'VOLBT', 'SERDP', 'BETA', 'SIGMA', 'YLD', 'YLD3', 
                'S_GPM', 'C_GPM', 'T_GPM', 'S_NPM', 'C_NPM', 'T_NPM', 'S_CTP', 
                'C_CTP', 'T_CTP', 'S_ROE', 'C_ROE', 'T_ROE', 'S_ROA', 'C_ROA', 
                'T_ROA']
                
'''factor data prepare'''
temp_endT = '20090123'
temp_str = 'select * from '+'A股_因子载荷_' + temp_endT +';'  
cursor.execute(temp_str)
data_factor = cursor.fetchall()
temp_data = DataFrame(data_factor)
temp_index = temp_data[1]   # 股票代码
temp_data1 = temp_data.ix[:,4:]
data_factor = DataFrame(temp_data1.values, index = temp_index, 
                         columns=factor_names)
data_code1 = [x[2:] + '.' + x[:2] for x in temp_index]


w.start()
# delete stocks which IPO < 1 year
IPO_date = w.wss(data_code1, "ipo_date").Data[0]
delta_days = [(datetime.strptime(temp_endT, '%Y%m%d') - x).days 
              for x in IPO_date]
data_code = [data_code1[x] for x, y in enumerate(delta_days) if y > 365]        # 1 year
temp_data_code = [x[-2:] + x[:6] for x in data_code]
data_factor = data_factor.loc[temp_data_code]

# delete ST PT stocks



# delete 


# data from Wind
temp_begT2 = '20090131'
temp_endT2 = '20090228'
temp_prepare = w.wss(data_code, "pct_chg_per,ev,industry_citic",
                     "startDate="+temp_begT2+";endDate="+temp_endT2
                     +";tradeDate="+temp_endT+";industryType=1").Data
temp_index = data_factor.index
'''stock future return prepare'''
temp_data = temp_prepare[0]
data_return = DataFrame(temp_data, index = temp_index, columns=['return'])
data_return = data_return / 100.

'''stock cap and industry prepare'''
temp_data = temp_prepare[1]
data_cap = DataFrame(temp_data, index = temp_index, columns=['cap'])
temp_data = temp_prepare[2]
data_ind = DataFrame(temp_data, index = temp_index, columns=['ind_citic'])
