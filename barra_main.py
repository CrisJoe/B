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
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 14 10:03:29 2016
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
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 14 10:03:29 2016

@author: CrisJoe


Barra main program

"""


# import mysql.connector

from WindPy import *

import numpy as np

import pandas as pd

from pandas import Series, DataFrame

import barra_main_fun as bmf


'''
conn = mysql.connector.connect(user='joe', password='password',  host='192.168.1.101', \
    database='ffactors', use_unicode=True)
'''
'''
conn = mysql.connector.connect(user='root', password='password',  
                               database='ffactors', use_unicode=True)
'''
'''
cursor = conn.cursor()
'''

window = 6

BegT = '2009-01-01'
EndT = '2016-09-30'

w.start()
Date2 = w.tdays(BegT, EndT, "Period=M").Data[0]
Date = [datetime.strftime(x, '%Y%m%d') for x in Date2]

single_factor_b = DataFrame()
single_factor_t = DataFrame()
seri_factor = []
seri_return = []
seri_ind = []
date_i = 0
#while date_i < len(Date) - 1:
while date_i < window:
    endT = Date[date_i]
    temp_start = w.tdaysoffset(1, endT).Data[0]
    begT2 = datetime.strftime(temp_start[0], '%Y%m%d')
    endT2 = Date[date_i + 1]
    [data_factor, data_return, data_ind, data_cap] = bmf.data_prepare(
                                                        endT, begT2, endT2)         # 因子截止日，下期收益起始日， 下期收益截止日

    [factor_expose, ind_matrix] = bmf.data_for_reg(data_factor, data_cap, 
                                                   data_ind)
    seri_factor.append(factor_expose)
    seri_ind.append(ind_matrix)
    seri_return.append(data_return)
    print '单因子检验- ' + endT + ' :'
    [single_factor_b2, single_factor_t2] = bmf.single_factor_reg(
                                        factor_expose, ind_matrix, data_return)
    single_factor_b = pd.concat([single_factor_b, DataFrame(single_factor_b2,
                                index=[endT], columns=factor_expose.columns)], 
                                axis=0)
    single_factor_t = pd.concat([single_factor_t, DataFrame(single_factor_t2,
                                index=[endT], columns=factor_expose.columns)], 
                                axis=0)    
    date_i += 1


factor_selected = bmf.select_single_factor(single_factor_b, single_factor_t)



date_i = 0
#while date_i < len(Date) - 1:
while date_i < window:
    a = bmf.combine_factor_b(factor_selected['risk_factor'], 
                             seri_factor[date_i], seri_return[date_i],
                             seri_ind[date_i])
