# -*- coding: utf-8 -*-
"""
Created on Fri Jun 12 20:05:30 2020

@author: yangy
"""

'''
From the output of "voltage_iden.py", read the "Wrong Predict" sheet and extract only wrong prediction images
从"voltage_iden.py"输出的excel表格中，读取"Wrong Predict"表并且提取出错误分类的图片
'''

import pandas as pd
import os
import shutil 

try:
    os.mkdir("image/wrong_predict/" )
except OSError:
    print ("Creation of the directory failed")

# Read excel file and first column
# 读取excel表格和第一列
df = pd.read_excel('result.xls', sheet_name='Wrong Predict')
images = df['图片']

for img in images:
    '''
    EXAMPLE
    img = 'image/labeled/Burr_U\1110.jpg'
    dir = 'Burr_U\1110.jpg'
    folder_name = 'Burr_U'
    file_name = '1110.jpg'
    '''
    dir = img.split('/')[2]
    dir1 = dir.split('\\')
    folder_name = dir1[0]
    file_name = dir1[1]
    
    try:
        os.mkdir("image/wrong_predict/" + folder_name )
    except OSError:
        print ()
    
    '''
    Copy form source path to destination path
    复制文件
    '''
    source = "image/labeled/" + folder_name + "/" + file_name
    destination = "image/wrong_predict/" + folder_name + "/" + file_name
    shutil.copyfile(source, destination) 