# -*- coding: utf-8 -*-
"""
Created on Thu Sep 23 16:05:24 2021

@author: 10628
"""

import re
import pandas as pd

# 从纯文本检测信息中提取所需信息
def extract_required_information(test_information):
    
    # 创建所需信息的正则表达式匹配模式
    medical_record_pattern = re.compile(r'病 历 号：([a-zA-Z0-9]*)')
    bar_code_pattern = re.compile(r'条 码 号：([0-9]*)')
    name_pattern = re.compile(r'姓    名: ([^ ]+)')
    date_pattern = re.compile(r'检验时间：([0-9-]*)')
    
    # 匹配
    try:                        
        medical_record_num = medical_record_pattern.findall(test_information)[0]
        bar_code_num = bar_code_pattern.findall(test_information)[0]
        name = name_pattern.findall(test_information)[0]
        date = date_pattern.findall(test_information)[0]
    except:
        print("没有匹配到部分所需信息")
        
    test_information_table = pd.DataFrame([name, medical_record_num, bar_code_num, date], 
                                          index = ["姓名",
                                                   "病历号",
                                                   "条码号",
                                                   "检测日期"])
    
    return test_information_table

# 在匹配对象的两位字符之间加空格
def split_word_num(str):
    str = str.group()
    return str[0] + " " + str[1]

# 将纯文本检测结果格式化为表格
def format_test_result(test_result):
    
    test_result = re.sub('抗“ O” 试验', '抗“O”试验', test_result)
    # 将连在一起的汉字和数字之间加空格
    test_result = re.sub('[\u4e00-\u9fa5][0-9]', split_word_num, test_result)
    
    # 删除"↑""↓"
    test_result = test_result.replace("↑", "")
    test_result = test_result.replace("↓", "")
    test_result_list = test_result.split('\n')
    
    flag = 0
    for i in test_result_list:
        test_result_list[flag] = i.split(' ')
        test_result_list[flag] = list(filter(None, test_result_list[flag]))
        flag = flag + 1
        
    try:
        if len(test_result_list[0]) == 5:
            test_result_df = pd.DataFrame(test_result_list, 
                                           columns = ["序号",
                                                      "项目名称",
                                                      "结果",
                                                      "参考范围",
                                                      "单位"])
        elif len(test_result_list[0]) == 3:
            test_result_df = pd.DataFrame(test_result_list, 
                                           columns = ["项目名称",
                                                      "结果",
                                                      "参考范围",])
        else:
            print("请检查此表格列数")
            
    except:
        print("文本处理错误，请检查得到的检测结果文本")
    
    return test_result_df


# 对于中间分栏的pdf，提取检测结果
def crop_pdf_with_two_column(page):
    
    crop_parameter1 = (0, 
                       page.lines[1]['top'],
                       page.lines[2]['x0'],
                       page.rects[0]['bottom'])
    crop_parameter2 = (page.lines[2]['x0'],
                       page.lines[1]['top'],
                       page.width,
                       page.rects[0]['bottom'])
    
    croped_test_result_page1 = page.crop(crop_parameter1)
    croped_test_result_page2 = page.crop(crop_parameter2)
    
    croped_test_result_text1 = croped_test_result_page1.extract_text()
    croped_test_result_text2 = croped_test_result_page2.extract_text()
    
    croped_test_result_text = croped_test_result_text1 + '\n' + croped_test_result_text2
    
    return croped_test_result_text

# 对于中间未分栏的pdf，提取检测结果
def crop_pdf_with_single_column(page):
    
    crop_parameter = (0, 
                      page.lines[1]['top'],
                      page.width,
                      page.rects[0]['bottom'])
    
    croped_test_result_page = page.crop(crop_parameter)
    
    croped_test_result_text = croped_test_result_page.extract_text()
    
    return croped_test_result_text
    
# 对于含有图表的pdf，提取检测结果
def crop_pdf_with_image(page):
    
    crop_parameter = (0, 
                      page.lines[1]['top'],
                      page.width,
                      page.images[0]['top'])
    
    croped_test_result_page = page.crop(crop_parameter)
    
    croped_test_result_text = croped_test_result_page.extract_text()
    
    return croped_test_result_text

# 分割pdf中除检测结果外的部分
def crop_pdf_test_information(page):
    
    crop_parameter1 = (0,
                       0,
                       page.width,
                       page.lines[1]['top'])
    crop_parameter2 = (0,
                       page.rects[0]['bottom'],
                       page.width,
                       page.height)
    
    # 分割
    croped_patient_page = page.crop(crop_parameter1)
    croped_test_information_page = page.crop(crop_parameter2)
    
    # 提取文本信息
    croped_patient_text = croped_patient_page.extract_text()
    croped_test_information_text = croped_test_information_page.extract_text()
    
    test_information_text = croped_patient_text + '\n' + croped_test_information_text
    
    return test_information_text

