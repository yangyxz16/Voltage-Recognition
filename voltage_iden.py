# -*- coding: utf-8 -*-
"""
Created on Tue Jun  2 23:07:11 2020

@author: yangy
"""
import os
import os.path
import requests 
import glob
import base64
from xlwt import Workbook
import time


host = ''
request_url = ""
input_folder = "image/labeled/"

# AK and SK used to retrieve access token
AK = ''
SK = ''


'''
Set up excel output
设置excel输出
'''
# Create a Workbook for writing excel
# 用来编写excel
wb = Workbook()

# Create sheet1: Result Summary
# Sheet1: 分类结果
s1 = wb.add_sheet('Summary') 
# Headers for sheet1
s1.write(0, 0, '分类')
s1.write(0, 1, '准确率')

# Create sheet2: Wrong Prediction
# Sheet2: 错误分类
s2 = wb.add_sheet('Wrong Predict')
# Headers for sheet2
s2.write(0, 0, '图片')
s2.write(0, 1, '分类')
s2.write(0, 2, '预测结果')


''' 
Set up access token and request URL
'''
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


row = 1 # Variable for row index
row_wrong = 1
# All the folders in the "labeled" directory
dirs = next(os.walk(input_folder))[1]
for dir in dirs:
    
    # Variable for counting the correct prediction
    # 正确预测
    correct = 0
    # Variable for counting total prediction
    # 总数
    total = 0
    
    print("--------------------" + dir + "--------------------")
    
    # All the images in the current "labeled" directory
    for img_file in glob.glob(input_folder + dir + "/" + "*.jpg"):
        with open(img_file, "rb") as imageFile:
            print(img_file + " is being processed")
            
            # Convert image to base64
            # 将图片转换为base64编码
            img_str = base64.b64encode(imageFile.read())   
            # Convert from bytes to string
            # 将bytes转换为string格式
            img_str = img_str.decode("utf-8") 
            
            
            params = {"image": img_str}
            
            # POST request
            response = requests.post(request_url, json = params, headers=headers)
            time.sleep(1);
            
            try:
                # Convert response to JSON format
                # 将返回结果转换为JSON
                response_Json = response.json()
                predicted_result = response_Json['results'][0]['name']
                
                # Check if predicted result matches the label
                # 正确分类
                if (predicted_result == dir):
                    correct+=1
                    print("Prediction - CORRECT")
                
                # Predicted result does not match the label
                # 错误分类
                else:
                    # Record in sheet2
                    s2.write(row_wrong, 0, img_file)
                    s2.write(row_wrong, 1, dir)
                    s2.write(row_wrong, 2, predicted_result)
                    print("Prediction - INCORRECT")
                    row_wrong+=1
                    
            except:
                print(response_Json)
                print("ERROR");
            
             
            total+=1
            print("----------------------------------------")
    
    # 计算准确率
    correct_percentage = correct / total
    
    s1.write(row, 0, dir)
    s1.write(row, 1, correct_percentage)
    row+=1
    
wb.save('result.xls')
print("Successfully Saved!")