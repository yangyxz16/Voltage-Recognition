# -*- coding: utf-8 -*-
"""
Created on Sun Jun 21 19:54:33 2020

Program to read the excel file, download the picture for each ASSET;
call image_preprocessing.py to preprocess the images;
call voltage_iden.py for classification

@author: yangy
"""
import pandas as pd
import urllib.request
import os
import xlsxwriter 
#import runpy
import cv2
import numpy as np
import base64
import requests 
import shutil 

'''
-----Set up excel file-----
'''
workbook = xlsxwriter.Workbook('Report.xlsx') 
worksheet = workbook.add_worksheet() 
worksheet.write('A1', '设备编码') 
worksheet.write('B1', '检测结果') 
worksheet.write('C1', '备注') 



'''
-----File locations-----
'''
excel_location = "excel_files/直流充电连接控制时序.xlsx"
img_location = "image/image_from_excel/"
img_pp_location = "image/processed/"
oper_location = "image/oper/"
uncertain_location = "image/uncertain/"

# Load data frame and fill the empty cell with text
df = pd.read_excel(excel_location).fillna("Empty Cell")



''' 
-----Set up access token and request URL-----
'''
host = ''
request_url = ""
input_folder = "image/processed/"

# AK and SK used to retrieve access token
AK = ''
SK = ''

# Function to Retrieving Access Token
# 获取Access Token
def get_access_token():
    response = requests.get(host + AK + '&client_secret=' + SK).json()
    if response:
        access_token = response['access_token']
        return access_token

access_token = get_access_token()
request_url = request_url + "?access_token=" + access_token
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}



''' 
-----Functions-----
'''
# Function to download image from the given url
def url_to_jpg(asset_code, url):
    filename = str(asset_code) + '.jpg'
    full_path = img_location + filename
    urllib.request.urlretrieve(url, full_path)
    print("Save " + full_path)
    return full_path

'''Function to proprocess images'''
def preprocess_img(path, asset_num):
    # Read image
    # 读取图片
    img = cv2.imread(path)
    
    # Define height and width for cropping
    # 定义用来剪裁的长和宽
    height, width = img.shape[:2]
    start_height = int(height * .5)
    end_height = int(height * .9)
    end_width = int(width * .5)
    
    # Crop image
    # 剪切图片
    cropped_img = img[start_height:end_height , 0:end_width]
    
    # Convert to HSV
    # 转换成HSV
    hsv = cv2.cvtColor(cropped_img, cv2.COLOR_BGR2HSV)

    # Lower and upper range of green
    # 绿色的区间
    lower_range = np.array([40, 40,40])
    upper_range = np.array([70, 255,255])
    
    # Show only the green range
    # 只显示绿色
    mask = cv2.inRange(hsv, lower_range, upper_range)
    
    save_path = img_pp_location + asset_num + ".jpg"
    
    # Save the image
    # 保存图片
    cv2.imwrite(save_path, mask)
    
    return save_path

'''Function to convert image to sting'''
def img_to_str(save_path):
    with open(save_path, "rb") as imageFile:
        # Convert image to base64
        # 将图片转换为base64编码
        img_str = base64.b64encode(imageFile.read())   
        # Convert from bytes to string
        # 将bytes转换为string格式
        img_str = img_str.decode("utf-8") 
    
        return img_str

'''Function to call three functions to :
    1. Download image from the given URL
    2. Preprocess the image
    3. Convert image to String
    AND
    4. HTTP post request'''
def clas(asset_num, img_url):
    image_path = url_to_jpg(asset_num, img_url)
    image_pp_path = preprocess_img(image_path, asset_num)
    img_str = img_to_str(image_pp_path)
    
    params = {"image": img_str}
    
    # POST request
    response = requests.post(request_url, json = params, headers=headers)
    response_Json = response.json()
    
    return (response_Json)

'''Function to copy the image to a location'''
def copy_file(asset_code, destination_location):
    file_name = asset_code + '.jpg'
    copy_path = img_location + file_name
    paste_path = destination_location + file_name
    shutil.copyfile(copy_path, paste_path) 



'''
-----Read through each row of excel-----
'''
for i, row in df.iterrows():
    row_index = i+1
    asset_code = str(row['asset_code'])
    image_url = row['image1_data']
    
    # Write the asset code for each row
    worksheet.write(row_index, 0, asset_code)
    
    # 无图片
    if image_url == "Empty Cell":
        print(asset_code + " has not image")
        worksheet.write(row_index, 1, "未检测")
    
    else:
        response = clas(asset_code, image_url)
        result = response['results'][0]['name']
        percent = float(response['results'][0]['score'])
        
        worksheet.write(row_index, 2, result)
        
        # Only if the result percentage is over 60%
        if percent >= 0.6:
            print("CERTAIN RESULT: " + result)
            
            # 有效检测
            if (result == 'Good_U' or result == 'Burr_U'):    
                worksheet.write(row_index, 1, "有效检测")
            # 无效检测
            else:
                # 检测结果：操作异常
                if (result == 'Oper_U'):
                    # Copy oper images to a seperate folder
                    copy_file(asset_code, oper_location)
                    print("Copied OPER IMAGE-" + asset_code)
                    worksheet.write(row_index, 1, "操作异常")
                # 检测结果：零电压
                else: 
                    worksheet.write(row_index, 1, "零电压")
        
        #  If the percentage is lower than 60%          
        else: 
            print("UNCERTAIN RESULT")
            
            worksheet.write(row_index, 1, "无法判断")
            
            # Copy uncertain images to a seperate folder
            copy_file(asset_code, uncertain_location)
            print("Copied UNCERTAIN IMAGE-" + asset_code)
        
        
workbook.close()
print("Excel file saved!") 

        
        
        
        
        
        
        
        
        
        