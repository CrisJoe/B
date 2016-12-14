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
    
    
    

