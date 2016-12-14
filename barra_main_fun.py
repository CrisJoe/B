# -*- coding: utf-8 -*-
"""
Created on Wed Dec 14 10:04:17 2016

@author: CrisJoe


main function for barra

"""
from WindPy import *

import numpy as np

import pandas as pd

from pandas import Series, DataFrame

import statsmodels.api as sm

import scipy.stats as stats

import barra_app_fun as baf

import mysql.connector
conn = mysql.connector.connect(user='joe', password='password',  host='192.168.1.101', \
    database='ffactors', use_unicode=True)

'''
conn = mysql.connector.connect(user='root', password='password',  
                               database='ffactors', use_unicode=True)
'''
cursor = conn.cursor()

def data_prepare(endT, begT2, endT2):
    
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
    temp_endT = endT
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

    
    # delete '停牌'                                         ??????是否需要剔除
    
    # delete 财务数据异常
    
    # data from Wind
    temp_begT2 = begT2
    temp_endT2 = endT2
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
    return [data_factor, data_return, data_ind, data_cap]

def data_for_reg(data_factor, data_cap, data_ind):
    data_del_extreme = baf.del_extreme(data_factor.values, 'median')
    data_standard = baf.standard_data(data_del_extreme)                         # 部分因子为负时失去意义，应如何标准化
    factor_expose = baf.get_factor_exposure(data_standard, data_cap.values)
    factor_expose = DataFrame(factor_expose, index=data_factor.index, 
                              columns=data_factor.columns)
    ind_matrix = baf.get_industry_matrix(data_ind, 'ZX')
        
    return [factor_expose, ind_matrix]

def single_factor_reg(factor_expose, ind_matrix, data_return):

    factor_test = list(factor_expose.columns)
    single_factor_t = np.zeros([1, len(factor_test)])
    single_factor_b = np.zeros([1, len(factor_test)])
    for factor_i in range(len(factor_test)):
        temp_factor = factor_expose[factor_test[factor_i]]
        temp_row = np.isnan(temp_factor)
        code_remain = temp_row[temp_row == False].index
        len1 = len(temp_row)
        len2 = len(code_remain)
        print("单因子检验：有效占比" +str(round((float(len2) / len1) * 100.,2)) 
              +"%; 缺失" + str(len1-len2) + '个数据, ' + str(len1) + "个因子" + 
              factor_test[factor_i])
        X1 = temp_factor.loc[code_remain].values
        X2 = ind_matrix.loc[code_remain].values
        if np.sum(np.sum(X2, axis=0) == 0) > 0:
            print '######### 因子' + factor_test[factor_i] + '行业不全 ########'
            # exit()
            single_factor_b[0, factor_i] = 0
            single_factor_t[0, factor_i] = 0
        else:
            Y = data_return.loc[code_remain].values
            X1.shape = (len(X1), 1)
            X_ones = np.ones_like(X1)
            X = np.hstack([X_ones, X1, X2])
            model = sm.OLS(Y, X, missing='drop')
            results = model.fit()
            single_factor_b[0, factor_i] = results.params[1]
            single_factor_t[0, factor_i] = results.tvalues[1]
    return [single_factor_b, single_factor_t]
        
def select_single_factor(single_factor_b, single_factor_t):        # 复杂的筛选条件，有待完善
    # 1 
    t_mean = np.mean(np.abs(single_factor_t))
    temp1 = t_mean >= 1.96                              ############# param 1.96
    temp_temp1 = temp1.values
    temp_temp1.shape = (len(temp_temp1), 1)
    
    # 2
    t_percent = np.abs(single_factor_t) >= 1.96         ############# param 1.96
    temp_temp2 = np.sum(t_percent, 0) / float(t_percent.shape[0])
    temp2 = temp_temp2 >= 0.2                           ############# param 20%
    temp_temp2 = temp2.values
    temp_temp2.shape = (len(temp_temp2), 1)
    
    # 3
    temp_b = single_factor_b.values
    b_tvalue = np.zeros([len(temp2), 1])
    for j in range(len(temp2)):
        temp_temp_b = temp_b[:, j]
        temp_b_tvalue, a = stats.ttest_1samp(temp_temp_b, 0)
        b_tvalue[j] = temp_b_tvalue
    temp_temp3 = np.abs(b_tvalue) >= 1.96               ############# param 1.96
    

    data1 = DataFrame(np.hstack([temp_temp1 * temp_temp2, 
                      temp_temp1 * temp_temp2 * temp_temp3]), 
                      columns=['risk_factor', 'alpha_factor'], 
                      index=temp2.index)
    return data1
    
