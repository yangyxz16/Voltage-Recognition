# -*- coding: utf-8 -*-
"""
Created on Tue Jun  9 00:03:59 2020

@author: yangy
"""
import pandas as pd
load_from = "excel_files/直流充电连接控制时序.xlsx"
df = pd.read_excel(load_from)

# Count number of stations
# 多少台设备
num_of_stations = len(df.index - 1)

# Operators
# 生产厂家
operators = df.operator.unique()

print(num_of_stations)
print(operators)