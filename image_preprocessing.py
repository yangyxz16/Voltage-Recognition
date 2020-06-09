# -*- coding: utf-8 -*-
"""
Created on Sun May 24 16:24:05 2020

@author: yangy
"""

import cv2
import numpy as np
import glob

i = 1
# Lower and upper range of green
# 绿色的区间
lower_range = np.array([40, 40,40])
upper_range = np.array([70, 255,255])

load_from_folder = "image/pre_processed/"
save_to_folder = "image/processed/"

# Loop through every jpg file in the folder
# 读取文件夹中的每个jpg文件
for img_file in glob.glob(load_from_folder + "*.jpg"):
    img = cv2.imread(img_file)
    height, width = img.shape[:2]
    start_height = int(height * .5)
    end_width = int(width * .5)
    
    # Crop image
    # 剪切图片
    cropped_img = img[start_height:height , 0:end_width]

    # Convert to HSV
    # 转换成HSV
    hsv = cv2.cvtColor(cropped_img, cv2.COLOR_BGR2HSV)

    # Show only the green range
    # 只显示绿色
    mask = cv2.inRange(hsv, lower_range, upper_range)

    # Show the image
    # 显示图片
    cv2.imshow("Mask", mask)
    filename = "C:/User/yangy/Desktop/aaaaaa.jpg"

    # Save the image
    # 保存图片
    cv2.imwrite(save_to_folder + str(i) + ".jpg", cropped_img)
    
    print(i)

    i += 1
    
#cv2.waitKey(0)
cv2.destroyAllWindows()