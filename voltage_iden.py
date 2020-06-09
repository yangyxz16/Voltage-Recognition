# -*- coding: utf-8 -*-
"""
Created on Tue Jun  2 23:07:11 2020

@author: yangy
"""

import requests 
import glob
import base64


host = ''
request_url = ""
input_folder = "image/p1/"
access_token = ''

# Retrieving Access Token
# 获取Access Token
AK = ''
SK = ''
response = requests.get(host + AK + '&client_secret=' + SK).json()
if response:
    access_token = response['access_token']
    
for img_file in glob.glob(input_folder + "*.jpg"):
    with open(img_file, "rb") as imageFile:
        # Convert image to base64
        # 将图片转换为base64编码
        img_str = base64.b64encode(imageFile.read())
        # Convert from bytes to string
        # 将bytes转换为string格式
        img_str = img_str.decode("utf-8") 
    
    params = {"image": img_str}
    request_url = request_url + "?access_token=" + access_token
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    # POST request
    response = requests.post(request_url, json = params, headers=headers)
    response_Json = response.json()

    print(response_Json)

    

