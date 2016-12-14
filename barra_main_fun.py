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

import barra_app_fun as baf



def single_factor_reg(data_factor, data_return, data_cap, data_ind):
    data_del_extreme = baf.del_extreme(data_factor.values, 'median')
    data_standard = baf.standard_data(data_del_extreme)                         # 部分因子为负时失去意义，应如何标准化
    factor_expose = baf.get_factor_exposure(data_standard, data_cap.values)
    factor_test = list(data_factor.columns)
    for factor_i in range(len(factor_test)):
        
