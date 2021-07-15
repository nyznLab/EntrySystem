'''
@Project ：entry_system
@File ：excelUtils.py
@IDE  ：PyCharm
@Author ：skj
@Date ：1/26/21 8:39 PM
'''
import xlrd
from tools.config import excel_col_dict
import re
import datetime
class ExcelObject():
    def __init__(self,start_time,medical_name,dose_num,dose_unit,
                 group_flag,drug_type,usage_way,start_doctor,start_nurse,
                 end_doctor,end_nurse,end_time):
        self.start_time = start_time
        self.medical_name = medical_name
        self.dose_num = dose_num
        self.dose_unit = dose_unit
        self.group_flag = group_flag
        self.drug_type  = drug_type
        self.usage_way = usage_way
        self.start_doctor = start_doctor
        self.start_nurse = start_nurse
        self.end_doctor = end_doctor
        self.end_nurse = end_nurse
        self.end_time = end_time

def read_excel(file_contents):
    excel_object_list = []
    sheet = xlrd.open_workbook(file_contents=file_contents).sheet_by_index(0)
    for row in sheet.get_rows():
        if is_date(row[excel_col_dict['start_time']].value.strip()):
            # 计算start_time,需要根据tomorrow
            base_start_time = row[excel_col_dict['start_time']].value.strip()
            is_tomorrow = row[excel_col_dict['is_tomorrow']].value.strip()
            start_time = get_start_time(base_start_time,is_tomorrow)
            # 读取名称
            medical_name = row[excel_col_dict['medical_name']].value.strip()
            # dose剂量换算
            base_dose = row[excel_col_dict['dose']].value.strip()
            if base_dose == '':
                dose_num = None
                dose_unit = None
            else:
                dose_num, dose_unit = get_dose(base_dose)
            # 读取组标
            group_flag = row[excel_col_dict['group_flag']].value.strip()
            group_flag = group_flag if group_flag!='' else None
            # 读取药物类型
            drug_type = row[excel_col_dict['drug_type']].value.strip()
            drug_type = drug_type if drug_type!='' else None
            # 使用方式
            usage_way = row[excel_col_dict['usage_way']].value.strip()
            usage_way = usage_way if usage_way!='' else None
            # 开始医生
            start_doctor = row[excel_col_dict['start_doctor']].value.strip()
            start_doctor = start_doctor if start_doctor!='' else None
            # 开始护士
            start_nurse = row[excel_col_dict['start_nurse']].value.strip()
            start_nurse = start_nurse if start_nurse!='' else None
            # 结束医生
            end_doctor = row[excel_col_dict['end_doctor']].value.strip()
            end_doctor = end_doctor if end_doctor!='' else None
            # 结束护士
            end_nurse = row[excel_col_dict['end_nurse']].value.strip()
            end_nurse = end_nurse if end_nurse!='' else None
            # 结束时间
            end_time = row[excel_col_dict['end_time']].value.strip()
            end_time = end_time if end_time!='' else None
            excelObject = ExcelObject(start_time=start_time, medical_name=medical_name,
                                      dose_num = dose_num,dose_unit = dose_unit,
                                      group_flag=group_flag, drug_type=drug_type,
                                      usage_way=usage_way, start_doctor=start_doctor,
                                      start_nurse=start_nurse, end_doctor=end_doctor,
                                      end_nurse=end_nurse, end_time=end_time)
            excel_object_list.append(excelObject)
    return excel_object_list
# 正则表达式匹配,是否是日期类型
def is_date(s):
    pattern = re.compile('\d{4}[-/]\d{2}[-/]\d{2}')
    if pattern.search(s) is None:
        return False
    return True
# 根据'明'判断开始时间
def get_start_time(start_time,is_tommorrow):
    if is_tommorrow != '':
        next_day = datetime.datetime.strptime(start_time.split(' ')[0].strip(), '%Y-%m-%d') + datetime.timedelta(days=1)
        return datetime.datetime.replace(next_day,hour=8,minute=0,second=0)
    return datetime.datetime.strptime(start_time,'%Y-%m-%d %H:%M:%S')

# 计量单位统一换算为ml或者mg,返回剂量数值以及基本单位
def get_dose(base_dose):
    p_number = re.findall(r"\d+\.?\d*", base_dose)
    danwei = re.findall(r'[mg|kg|ml|l|M|g|ug|µg]+', base_dose)
    dose_num = None
    dose_unit = None
    if len(p_number)==1 and len(danwei)==1:
        dose_num = p_number[0]
        dose_unit = danwei[0]
        if dose_unit in  ['l','g']:
            dose_num = float(dose_num) * 1000
            dose_unit = 'm'+dose_unit
    return dose_num,dose_unit

