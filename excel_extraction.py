# -*- coding: utf-8 -*-
"""
Created on Tue Jun  9 00:03:59 2020

@author: yangy
"""
import pandas as pd
import glob
import xlsxwriter 


workbook = xlsxwriter.Workbook('Report.xlsx') 

excel_dic = "excel_files/"


# Function to extract file name from a path
def file_name_extr(file_path):
     return file_path.split('\\')[1].split('.')[0]   

# Function to generate a list of tests based on the file name
def generate_test_list(file_name):
    if file_name == "直流充电连接控制时序":
        list = ["chm_id", "crm_id", "bcl_i", "bcl_u", "ccs_i", "ccs_u",	"cc1_12v", "uaux_h", "uaux_l", "uz", "uzo_umed", "izo", "uz_stop"]
    
    else:
        list = []  
    return list

# Function to Create a dictionary for storing empty and zero tests
def generate_test_result_dict(test_list, row):
    # Create a dictionary
    test_dict = {}
    
    for test in test_list:
        value = row[test]
        
        # 值为空
        if value == "Empty Cell":
            test_dict[test] = "EMPTY"
        # 值为零
        elif value == 0:
            test_dict[test] = "ZERO"
        
    return test_dict      
        



# For each excel file in the folder
for excel_file in glob.glob(excel_dic + "*.xlsx"):
    # Variable for the file name
    file_name = file_name_extr(excel_file)
    
    # excel READING: Load data frame and fill the empty cell with text
    df = pd.read_excel(excel_file).fillna("Empty Cell")
    # Count number of stations/设备数量
    num_of_stations = len(df.index - 1)
    # Operators/生产厂家
    operators = df.operator.unique()
    # Stations/站点
    stations = df.station_name.unique()
    
    print(operators)
    print(stations)
    
    
    # excel WRITING 
    worksheet = workbook.add_worksheet(file_name) 
    
    worksheet.write('A1', '设备数量') 
    worksheet.write('A2', '生产厂家') 
    worksheet.write('A3', '站点') 

    worksheet.write('B1', num_of_stations) 
    
    operator_col_i = 1
    for operator in operators:
        worksheet.write(1, operator_col_i, operator)
        operator_col_i+=1
    
    station_col_i = 1   
    for station in stations:    
        worksheet.write(2, station_col_i, station)
        station_col_i+=1
        
  
    
    worksheet.write('A6', '设备编码') 
    worksheet.write('B6', '检测信息') 
    worksheet.write('C6', '备注') 
    
    # List of tests
    test_list = generate_test_list(file_name)
    
    #Read through each row of excel
    for i, row in df.iterrows():
        row_index = i+6
        
        # Varibles
        asset_code = str(row['asset_code'])
        check_date = row['check_date']
        
        # Write asset code at column 0
        worksheet.write(row_index, 0, asset_code)
        
        
        # 未检测
        if check_date == "Empty Cell":
            # Write result at column 1
            worksheet.write(row_index, 1, "未检测")
            print(asset_code + " has NOT been tested")
        
        else:
            test_result_dict = generate_test_result_dict(test_list, row)
            
            # 有效检测-Dictionary size is 0. 
            if len(test_result_dict) == 0:
                # Write result at column 1
                worksheet.write(row_index, 1, "有效检测")
                print(asset_code + " has NO EMPTY or ZERO")
            # 无效检测
            else:
                # Write result at column 1
                worksheet.write(row_index, 1, "无效检测")
                print(asset_code + " has EMPTY or ZERO")

                # Index variable for the comment colum
                comment_col_i = 2
                
                # Loop through all values in the dictionary
                for test in test_result_dict:
                    value = test_result_dict[test]
                    
                    # 缺失数据
                    if value == "EMPTY":
                        # Write comment
                        worksheet.write(row_index, comment_col_i, "空值-" + test)
                        print(test + " is EMPTY")
                    # 零数据
                    else:
                        # Write comment
                        worksheet.write(row_index, comment_col_i, "零数据-" + test)
                        print(test + " is ZERO")
                        
                    comment_col_i += 1
                        
workbook.close()
print("Excel file saved!")        
    


'''





# Count number of stations
# 多少台设备
num_of_stations = len(df.index - 1)

# Operators
# 生产厂家
operators = df.operator.unique()

# Stations
# 站点
stations = df.station_name.unique()


 
wbkName = 'result.xls'
wbk = xlwings.Book(wbkName)
ws = wbk.sheets[1]

ws.range(1, 1).value = '设备数量'
wbk.save(wbkName)


rb = xlrd.open_workbook('result.xls')

summary_sheet = rb.get_sheet(0)
summary_sheet.write(0, 0, '设备数量')
summary_sheet.write(0, 1, num_of_stations)
summary_sheet.write(1, 0, '生产厂家')
summary_sheet.write(1, 1, operators)
summary_sheet.write(2, 0, '站点')
summary_sheet.write(2, 1, stations)

wb.save('result.xls')
'''