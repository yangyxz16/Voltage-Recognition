# -*- coding: utf-8 -*-
"""
Created on Fri Jun 12 23:38:29 2020

@author: yangy

Cropping images only
"""

import os
import glob
import cv2

load_from_folder = "image/unprocessed/"
save_to_folder = "image/processed/"

# All the folders in the "labeled" directory
dirs = next(os.walk(load_from_folder))[1]

for dir in dirs:
    
    i = 1
    
    save_path = save_to_folder + dir + "/"
    
    try:
        os.mkdir(save_path)
    except OSError:
        print ("Creation of the directory %s failed" % save_path)
    
    for img_file in glob.glob(load_from_folder  + dir + "/" + "*.jpg"):
        print(load_from_folder  + dir + "/")
        img = cv2.imread(img_file)
        
        height, width = img.shape[:2]
        start_height = int(height * .5)
        end_width = int(width * .5)
        
        # Crop image
        # 剪切图片
        cropped_img = img[start_height:height , 0:end_width]
        
        
        cv2.imwrite(save_path + str(i) + ".jpg", cropped_img)
        #cv2.imwrite(save_to_folder + dir + "/" + str(i) + ".jpg", cropped_img)
        #`print(save_to_folder + dir + "/" + str(i) + ".jpg")
        i+=1