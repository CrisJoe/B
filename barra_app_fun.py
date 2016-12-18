# -*- coding: utf-8 -*-
"""
Created on Wed Dec 14 10:05:15 2016

@author: CrisJoe


application function for barra and other data handle

"""

from WindPy import *

import numpy as np

import pandas as pd

from pandas import Series, DataFrame



def del_extreme(data_factor_values, method):
    data = data_factor_values.copy()
    data1 = np.zeros_like(data)
    if method == 'median':
        ss = 5.2                                            ##### param can be changed in the future
        M = np.nanmedian(data, axis=0)
        Z = np.abs(data - M)
        Zmid = np.nanmedian(Z, axis=0)
        for j in range(len(Zmid)):                          #????? 能不能不用循环实现
            temp_data = data[:,j]
            temp_row = np.where(temp_data > M[j] + ss * Zmid[j])[0]
            temp_data[temp_row] = M[j] + ss * Zmid[j]
            temp_row = np.where(temp_data < M[j] - ss * Zmid[j])[0]
            temp_data[temp_row] = M[j] - ss * Zmid[j]
            data1 [:,j] = temp_data 
    '''
    elif method == 'std':
    
    elif method == 'quarter':
    '''    
    return data1

    
def standard_data(data_del_extreme):
    data = data_del_extreme.copy()
    temp_mean = np.nanmean(data, axis=0)
    temp_std = np.nanstd(data, axis=0)
    data1 = (data - temp_mean) / temp_std
    return data1
    
def get_factor_exposure(data_standard, data_cap):
    data1 = np.zeros_like(data_standard) * np.nan
    for j in range(np.shape(data_standard)[1]):
        temp_row = np.isnan(data_standard[:,j])
        temp_cap = data_cap[~temp_row]
        temp_data = data_standard[~temp_row, j]
        cap_weight = temp_cap / np.sum(temp_cap) 
        temp_data.shape = (len(temp_data), 1)
        temp_sum = np.sum(cap_weight * temp_data)
        temp_data = temp_data - temp_sum
        data1[~temp_row, j] = temp_data[:,0]
    return data1
    
def get_industry_matrix(data_ind, ind_style):
    
    if ind_style == 'ZX':
        temp_name = [u"石油石化",u"煤炭",u"有色金属",u"电力及公用事业",u"钢铁",
                     u"基础化工",u"建筑",u"建材",u"轻工制造",u"机械",u"电力设备",
                     u"国防军工",u"汽车",u"商贸零售",u"餐饮旅游",u"家电",
                     u"纺织服装",u"医药",u"食品饮料",u"农林牧渔",u"银行",
                     u"非银行金融",u"房地产",u"交通运输",u"电子元器件",u"通信",
                     u"计算机",u"传媒",u"综合"]
        ind_matrix = np.zeros([len(data_ind), len(temp_name)])
        for ind_i in range(len(temp_name)):
            temp_row = np.where(data_ind.values == temp_name[ind_i])[0]
            ind_matrix[temp_row, ind_i] = 1
        data1 = DataFrame(ind_matrix, index=data_ind.index, columns=temp_name)
    '''
    elif ind_style == 'SW':
    '''    
    return data1
    
def print_corr(factor):
    temp_corr_matrix = factor.corr()
    temp_len = len(temp_corr_matrix)
    temp_name = temp_corr_matrix.index
    temp_matrix = temp_corr_matrix.values
    temp = {}
    if temp_len == 2:
        temp[temp_name[1] +' & '+ temp_name[0]] = round(temp_matrix[1, 0], 2)
    else:
        for i in range(1,temp_len):
            for j in range(i-1):
                temp[temp_name[i] +' & '+ temp_name[j]] = round(temp_matrix[i, j], 2)
    temp = Series(temp)
    temp_loc = temp[np.abs(temp) >= 0.75].index
    for i in range(len(temp_loc)):
        print '存在共线性: ' + str(temp[temp_loc[i]]) + ', ' + temp_loc[i]
    


