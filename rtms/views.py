import datetime
import json
import logging
import os
import random
import re

import pandas as pd
from django.conf import settings
from django.core.paginator import Paginator
from django.db import transaction
from django.shortcuts import render, HttpResponse

import patients.dao as patients_dao
import rtms.dao as rtms_dao
import rtms.models as rtms_models


class rtmsExcelError(Exception):
    def __init__(self, ErrorInfo):
        super().__init__(self)  # 初始化父类
        self.errorinfo = ErrorInfo

    def __str__(self):
        return self.errorinfo


def logger_config(log_path, logging_name):
    '''
    配置log
    :param log_path: 输出log路径
    :param logging_name: 记录中name，可随意
    :return:logger对象
    '''
    logger = logging.getLogger(logging_name)
    logger.setLevel(level=logging.DEBUG)
    handler = logging.FileHandler(log_path, encoding='UTF-8')
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    logger.addHandler(console)
    return logger


logger = logger_config(log_path='rtms/log/rtms_log.txt', logging_name="user")


def read_index_data_notnull(data_pd, colum_label):
    '''
    获取一列数据中非空数据和索引
    :param data_pd [ndarray]：rTMS治疗信息sheet的ndarray
    :return [list]: 索引+非空数据
    '''
    data_raw = pd.DataFrame(list(data_pd[colum_label]), columns=[colum_label])
    data_pd_notnull = data_raw[data_raw[colum_label] != ""]

    index_notnull = []
    for m in data_pd.index:
        m_value = data_pd[colum_label].loc[m]
        if len(m_value) != 0:
            index_notnull.append(m)
    data_pd_notnull.index = index_notnull
    return data_pd_notnull


def read_rtms_excel(doctor_id, filename):
    # 1.检查传入的excel是否正确
    insert_patient_session_list = []
    flag_rtms_excel = 0

    # 格式错误汇总
    # 0-写入成功；1-没有数据更新；2-rtms格式错误；3-excel文件后缀错误；4-excel中缺少相应字段；
    # 5-没有”治疗具体信息汇总“这个sheet;6-其他error;7-没有获取到文件
    error_info = '0'
    check_rtms_excel = {}

    # 被试号(格式正确)；扫描号(格式正确)；治疗日期(格式正确、非空)；运动阈值(非空)；能量强度(非空)；治疗方案(非空、已有方案)
    # 扫描号不连续（写入成功，但提示）
    check_patient_id = []
    check_session_id = []
    check_date = []
    check_resting_motor_threshold = []
    check_intensity = []
    check_treatment_str = []
    check_treatment_num = []
    tip_session_id=[]

    treatment_data = list(rtms_dao.get_treatment_rtms().values_list('treatment_id', 'treatment_name'))

    # 1.2 读excel
    excel_path = settings.UPLOAD_ROOT + "/" + filename
    sheet_name = '治疗具体信息汇总'
    # 1.2.1 不读空行(扫描次数+扫描备注(日期)不为空)
    data_raw_pd = pd.read_excel(excel_path, sheet_name=sheet_name, dtype=str,
                                usecols=['编号', '扫描次数', '扫描备注（日期）', '运动阈值', '能量强度（%）', '方案', '备注'])
    data_pd = data_raw_pd.dropna(axis=0,how='all',inplace=False)
    data_pd = data_pd.reset_index(drop=True)
    data_pd.fillna("", inplace=True)

    patient_pd = read_index_data_notnull(data_pd, '编号')
    patient_id_list = patient_pd['编号'].to_list()
    patient_index_list = list(patient_pd.index)

    pattern_space = re.compile(r'\s+')
    pattern_treatment_num = re.compile(r'第(.*?)次', re.S)

    try:
        with transaction.atomic():
            insert_patient_rtms_obj_list = []
            idx_insert_patient_rtms_obj_list = 0

            # excel字段数据提取与检查
            for i in range(len(patient_index_list)):
                patient_id = ""
                treatment_num_add = 0
                patient_id_str = re.sub('\D', '', (patient_id_list[i]).split("_")[1])
                if patient_id_str != '':
                    patient_id = str(int(patient_id_str))
                else:
                    flag_rtms_excel = 1
                    check_patient_id.append(str(patient_id_list[i]))

                # 病人的最大治疗顺序号,没有病人相关信息None
                max_treatment_num = None
                if patient_id != "":
                    max_treatment_num = rtms_dao.get_treatment_num_byPatientId(patient_id)

                # 1.2.2 获取patient_id对应的的行索引范围 [p_range1,p_range2）
                p_range1 = patient_index_list[i]
                if i != (len(patient_index_list) - 1):
                    p_range2 = patient_index_list[i + 1] - 1
                else:
                    p_range2 = len(data_pd.index) - 1

                if p_range1 != p_range2:
                    # 在行索引范围内找这个patient_id对应的session_id的索引和数值
                    session_data = data_pd.loc[p_range1:p_range2, :]
                    session_pd = read_index_data_notnull(session_data, '扫描次数')
                    session_id_list = session_pd['扫描次数'].to_list()
                    session_index_list = list(session_pd.index)

                    session_id = ""
                    for j in range(len(session_index_list)):
                        # 1.2.3 获取session_id的行索引范围
                        session_id_str = re.sub("\D", "", session_id_list[j])
                        if session_id_str != "":
                            session_id = int(session_id_str)
                            if j!=0:
                                if (pre_session_id+1)!=session_id:
                                    tip_session_id.append(str(patient_id_list[i]))
                            pre_session_id = session_id
                        else:
                            flag_rtms_excel = 1
                            check_session_id.append(str(session_id_list[j]))

                        if j != (len(session_index_list) - 1):
                            s_range1 = session_index_list[j]
                            s_range2 = session_index_list[j + 1] - 1
                        else:
                            s_range1 = session_index_list[j]
                            if i != (len(patient_index_list) - 1):
                                s_range2 = patient_index_list[i + 1] - 1
                            if i == len(patient_index_list) - 1:
                                s_range2 = len(data_pd) - 1

                        if s_range1 < s_range2:
                            pre_treatment_date = 'a'
                            pre_pre_treatment_date = 'b'

                            # 扫描信息从s_range1_index +1开始,一直读完s_range2_index行
                            for x in range(s_range1 + 1, s_range2 + 1):
                                flag_treatment_date = 0  # 当治疗日期格式不正确时，treatment_num的计算跳过

                                # treatment_date
                                date_str = data_pd['扫描备注（日期）'].loc[x]
                                date_str = re.sub(pattern_space, "", date_str)

                                if str(date_str) != '' and str(date_str)[0] == "第":
                                    if j == 0 and x == s_range1 + 1:
                                        first_treatment_num = int(
                                            str((re.findall(pattern_treatment_num, date_str))[0])) - 1
                                    compile_s = re.compile(r'[(（](.*?)[）)]', re.S)
                                    if (re.search(compile_s, str(date_str)) != None):
                                        treatment_date = (re.findall(compile_s, str(date_str)))[0]
                                        if (
                                        re.search(re.compile(r'(.*?)/(.*?)/(.*?)', re.S), str(treatment_date))) != None:
                                            if (len(treatment_date.split("/")[0]) <= 4) and (
                                                    len(treatment_date.split("/")[1]) <= 2) and (
                                                    len(treatment_date.split("/")[2]) <= 2):
                                                treatment_date = treatment_date.split("/")[0] + '-' + (
                                                treatment_date.split("/")[1]).zfill(2) + '-' + (
                                                                 treatment_date.split("/")[2]).zfill(2)
                                            else:
                                                flag_treatment_date = 1
                                                flag_rtms_excel = 1
                                                check_date.append(
                                                    "NN_" + str(patient_id).zfill(8) + "_S" + str(session_id).zfill(
                                                        3) + '_' + str(x - s_range1))
                                        else:
                                            flag_treatment_date = 1
                                            flag_rtms_excel = 1
                                            check_date.append(
                                                "NN_" + str(patient_id).zfill(8) + "_S" + str(session_id).zfill(
                                                    3) + '_' + str(x - s_range1))
                                    else:
                                        flag_treatment_date = 1
                                        flag_rtms_excel = 1
                                        check_date.append(
                                            "NN_" + str(patient_id).zfill(8) + "_S" + str(session_id).zfill(
                                                3) + '_' + str(x - s_range1))

                                    # resting_motor_threshold
                                    resting_motor_threshold = str(data_pd['运动阈值'].loc[x])
                                    resting_motor_threshold = re.sub("\D", "",
                                                                     resting_motor_threshold)  # 兼容cell里填了其他文字或单位的情况
                                    if resting_motor_threshold == "":
                                        flag_rtms_excel = 1
                                        check_resting_motor_threshold.append(
                                            "NN_" + str(patient_id).zfill(8) + "_S" + str(session_id).zfill(
                                                3) + '_' + str(x - s_range1))

                                    # intensity
                                    intensity = str(data_pd['能量强度（%）'].loc[x])
                                    intensity = re.sub(pattern_space, "", intensity)  # 兼容cell里填了其他文字或单位的情况
                                    if intensity != "":
                                        if float(intensity) <= 2:
                                            intensity = str(int(100 * float(intensity)))
                                    else:
                                        flag_rtms_excel = 1
                                        check_intensity.append(
                                            "NN_" + str(patient_id).zfill(8) + "_S" + str(session_id).zfill(
                                                3) + '_' + str(x - s_range1))

                                    # treatment_num
                                    treatment_num_str = re.sub("\D", "",
                                                               str(re.findall(pattern_treatment_num, date_str)[0]))
                                    if treatment_num_str != "":
                                        treatment_num_add = treatment_num_add + 1
                                        treatment_num = int(treatment_num_str)
                                        if treatment_num != first_treatment_num + treatment_num_add:
                                            flag_rtms_excel = 1
                                            check_treatment_num.append(
                                                "NN_" + str(patient_id).zfill(8) + "_S" + str(session_id).zfill(
                                                    3) + '_' + str(x - s_range1))
                                    else:
                                        flag_rtms_excel = 1
                                        check_treatment_num.append(
                                            "NN_" + str(patient_id).zfill(8) + "_S" + str(session_id).zfill(
                                                3) + '_' + str(x - s_range1))

                                    # times_per_day
                                    times_per_day = 1
                                    if flag_treatment_date == 1:
                                        treatment_date = "wrong date" + str(random.randint(1, 10))
                                    else:
                                        if pre_pre_treatment_date != pre_treatment_date == treatment_date:
                                            times_per_day = 2
                                            if idx_insert_patient_rtms_obj_list >= 1:
                                                update_obj = insert_patient_rtms_obj_list[
                                                    idx_insert_patient_rtms_obj_list - 1]
                                                update_obj.update_times_per_day(2)
                                                insert_patient_rtms_obj_list[
                                                    idx_insert_patient_rtms_obj_list - 1] = update_obj
                                        if pre_pre_treatment_date == pre_treatment_date == treatment_date:
                                            times_per_day = 3
                                            if idx_insert_patient_rtms_obj_list >= 2:
                                                update_obj = insert_patient_rtms_obj_list[
                                                    idx_insert_patient_rtms_obj_list - 1]
                                                update_obj.update_times_per_day(2)
                                                insert_patient_rtms_obj_list[
                                                    idx_insert_patient_rtms_obj_list - 1] = update_obj

                                                update_obj2 = insert_patient_rtms_obj_list[
                                                    idx_insert_patient_rtms_obj_list - 1 - 1]
                                                update_obj2.update_times_per_day(3)
                                                insert_patient_rtms_obj_list[
                                                    idx_insert_patient_rtms_obj_list - 1 - 1] = update_obj2
                                        if pre_treatment_date!='a':
                                            pre_treatment_datetime = datetime.datetime.strptime(str(pre_treatment_date)+' 00:00:00','%Y-%m-%d %H:%M:%S')
                                            treatment_datetime = datetime.datetime.strptime(str(treatment_date)+' 00:00:00','%Y-%m-%d %H:%M:%S')
                                            compare_day = (pre_treatment_datetime - treatment_datetime).days
                                            if (compare_day >0):
                                                flag_treatment_date = 1
                                                flag_rtms_excel = 1
                                                check_date.append(
                                                    "NN_" + str(patient_id).zfill(8) + "_S" + str(session_id).zfill(
                                                        3) + '_' + str(x - s_range1))
                                        pre_pre_treatment_date = pre_treatment_date
                                        pre_treatment_date = treatment_date

                                    # note
                                    note = data_pd['备注'].loc[x]

                                    # treatment_id
                                    treatment_str = data_pd['方案'].loc[x]
                                    if treatment_str == "":
                                        flag_rtms_excel = 1
                                        check_treatment_str.append(
                                            "NN_" + str(patient_id).zfill(8) + "_S" + str(session_id).zfill(
                                                3) + '_' + str(x - s_range1))
                                    else:
                                        treatment_str = re.sub(pattern_space, "", treatment_str)
                                        treatment_id = 999
                                        for t in range(len(treatment_data)):
                                            if treatment_data[t][1] == treatment_str:
                                                treatment_id = treatment_data[t][0]
                                        if treatment_id == 999:
                                            flag_rtms_excel = 1
                                            check_treatment_str.append(
                                                "NN_" + str(patient_id).zfill(8) + "_S" + str(session_id).zfill(
                                                    3) + '_' + str(x - s_range1))

                                    create_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
                                    update_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")

                                    if max_treatment_num == None or treatment_num > max_treatment_num:
                                        if (flag_rtms_excel == 0):
                                            rPatientRtms_object = rtms_models.rPatientRtms(
                                                patient_id=patient_id,
                                                session_id=str(session_id),
                                                treatment_id=str(treatment_id),
                                                resting_motor_threshold=resting_motor_threshold,
                                                intensity=intensity,
                                                treatment_date=treatment_date,
                                                treatment_num=str(treatment_num),
                                                times_per_day=str(times_per_day),
                                                note=note,
                                                doctor_id=str(doctor_id),
                                                create_time=create_time,
                                                update_time=update_time,
                                                delete=str(0)
                                            )
                                            try:
                                                insert_patient_rtms_obj_list.append(rPatientRtms_object)
                                                idx_insert_patient_rtms_obj_list = idx_insert_patient_rtms_obj_list + 1

                                                if [patient_id, session_id] not in insert_patient_session_list:
                                                    insert_patient_session_list.append([patient_id, session_id])

                                            except Exception as e:
                                                logging.error("Failed to collect rPatientRtms_object: %s"%e)
                                else:
                                    flag_rtms_excel = 1
                                    check_treatment_num.append(
                                        "NN_" + str(patient_id).zfill(8) + "_S" + str(session_id).zfill(
                                            3) + '_' + str(x - s_range1))

            # 批量写入数据库
            if (flag_rtms_excel == 0):
                try:
                    rtms_models.rPatientRtms.objects.bulk_create(insert_patient_rtms_obj_list)
                except Exception as e:
                    error_info = '6'
                    logging.error("Failed to write to database: %s"%e)
                if len(insert_patient_rtms_obj_list) == 0:
                    error_info = '1'
            else:
                error_info = '2'

            for patient_session in insert_patient_session_list:
                rtms_num = rtms_dao.get_rtms_num_byPatientIdSessionId(patient_id=patient_session[0],
                                                                      session_id=patient_session[1])
                rtms_treatment_id = rtms_dao.get_rtms_treatment_id_byPatientIdSessionId(patient_id=patient_session[0],
                                                                                        session_id=patient_session[1])

                update_dpatient_detail_obj = patients_dao.get_patient_detail_byPatientIdAndSessionId(patient_session[0],
                                                                                                     patient_session[1])
                if update_dpatient_detail_obj != None:
                    update_dpatient_detail_obj.update_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    update_dpatient_detail_obj.tms = rtms_num
                    update_dpatient_detail_obj.tms_treatment_id = rtms_treatment_id
                    update_dpatient_detail_obj.save()

    except Exception as e:
        error_info = '6'
        if flag_rtms_excel == 1:
            logger.error("excel格式错误: %s"%e)
        else:
            logger.error("非excel格式错误: %s"%e)

    check_rtms_excel = {
        'error_info': error_info,
        'check_patient_id': check_patient_id,
        'check_session_id': check_session_id,
        'check_date': check_date,
        'check_resting_motor_threshold': check_resting_motor_threshold,
        'check_intensity': check_intensity,
        'check_treatment_str': check_treatment_str,
        'check_treatment_num': check_treatment_num,
        'tip_session_id':tip_session_id
    }

    return check_rtms_excel


def get_rtms_by_search(request):
    treatment_rtms_list = rtms_models.tTreatmentRtms.objects.filter(delete=0).values \
        ('treatment_name', 'therapeutic_target', 'frequency',
         'pulses', 'stimulation_time', 'inter_train_intervals',
         'pulse_trains', 'total_pulses', 'total_time_minute',
         'total_time_second')
    return render(request, 'upload_rtms.html', {'treatment_rtms_list': treatment_rtms_list})


def pagination_function(paginator, page, is_paginated=True):
    # 分页实现
    if not is_paginated:
        return {}
    left = []
    right = []
    left_has_more = False
    right_has_more = False

    # 标示是否需要显示第 1 页、最后1页的页码号
    first = False
    last = False

    page_number = page.number
    total_pages = paginator.num_pages
    page_range = paginator.page_range

    if page_number == 1:
        right = page_range[page_number:page_number + 2]
        if right[-1] < total_pages - 1:
            right_has_more = True
        if right[-1] < total_pages:
            last = True
    elif page_number == total_pages:
        left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]
        if left[0] > 2:
            left_has_more = True
        if left[0] > 1:
            first = True
    else:
        left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]
        right = page_range[page_number:page_number + 2]

        if right[-1] < total_pages - 1:
            right_has_more = True
        if right[-1] < total_pages:
            last = True

        if left[0] > 2:
            left_has_more = True
        if left[0] > 1:
            first = True

    data = {
        'left': left,
        'right': right,
        'left_has_more': left_has_more,
        'right_has_more': right_has_more,
        'first': first,
        'last': last,
    }

    return data


def get_all_rtms_data(request):
    rtms_data_list = rtms_models.rPatientRtms.objects.filter(delete=0).values \
        ('patient_id', 'session_id', 'treatment_num', 'treatment_id', 'resting_motor_threshold',
         'intensity', 'times_per_day', 'treatment_date').order_by("patient_id", 'treatment_num')

    paginator = Paginator(rtms_data_list, 10)
    page_num = request.GET.get('page', 1)
    try:
        page_num = int(page_num)
    except:
        page_num = 1
    if page_num < 1 or page_num > paginator.num_pages:
        page_num = 1
    is_paginated = True
    rtms_data_list_page = paginator.get_page(page_num)
    for rtms_data in rtms_data_list_page:
        rtms_data['patient_id'] = 'NN_' + str(rtms_data['patient_id']).zfill(8)
        rtms_data['session_id'] = 'S' + str(rtms_data['session_id']).zfill(3)
        rtms_data['treatment_id'] = rtms_dao.get_treatment_name_byTreatmentId(rtms_data['treatment_id'])

    paginator_data = pagination_function(paginator, rtms_data_list_page, is_paginated)

    return render(request, 'manage_rtms.html', locals())


def files_upload(request):
    if request.method == "POST":
        doctor_id = request.session.get('doctor_id')

        file_object = request.FILES.get('files')
        if file_object != None:
            if file_object.name.split('.')[-1] == 'xlsx':
                logger.info('uplaod:%s' % file_object)
                # 创建upload文件夹
                if not os.path.exists(settings.UPLOAD_ROOT):
                    os.makedirs(settings.UPLOAD_ROOT)
                try:
                    if file_object is None:
                        return HttpResponse('请选择要上传的文件')
                    # 循环二进制写入
                    with open(settings.UPLOAD_ROOT + "/" + file_object.name, 'wb') as f:
                        for i in file_object.readlines():
                            f.write(i)
                    excel_path = settings.UPLOAD_ROOT + "/" + file_object.name
                    sheetnames = list(pd.read_excel(excel_path, sheet_name=None))
                    if "治疗具体信息汇总" in sheetnames:
                        # 读取rtms文件并写入数据库
                        sheet_columns = (pd.read_excel(excel_path, sheet_name="治疗具体信息汇总", dtype=str)).columns.tolist()
                        required_columns = ['编号', '扫描次数', '扫描备注（日期）', '运动阈值', '能量强度（%）', '方案', '备注']
                        flag_column = True
                        for c in required_columns:
                            if c not in sheet_columns:
                                flag_column = False
                        if flag_column:
                            check_rtms_excel = read_rtms_excel(doctor_id, file_object.name)
                        else:
                            check_rtms_excel = {'error_info': 4}
                    else:
                        check_rtms_excel = {'error_info': 5}
                except Exception as e:
                    logger.error('异常:%s' % e)
            else:
                check_rtms_excel = {'error_info': 3}
        else:
            check_rtms_excel = {'error_info': 7}
        return HttpResponse(json.dumps(check_rtms_excel, indent=4, ensure_ascii=False))


def add_rtms_treatment(request):
    if request.is_ajax():
        check_new_treatment = {"check_new_treatment": 0}
        treatment_name = request.POST.get("treatment_name")
        therapeutic_target = request.POST.get("therapeutic_target")
        frequency = request.POST.get("frequency")
        pulses = request.POST.get("pulses")
        stimulation_time = request.POST.get("stimulation_time")
        inter_train_intervals = request.POST.get("inter_train_intervals")
        pulse_trains = request.POST.get("pulse_trains")
        total_pulses = request.POST.get("total_pulses")
        total_time_minute = request.POST.get("total_time_minute")
        total_time_second = request.POST.get("total_time_second")
        note = request.POST.get("note")
        doctor_id = request.session.get('doctor_id')

        treatment_name_list = list(rtms_dao.get_treatment_rtms().values('treatment_name'))
        if {'treatment_name':str(treatment_name)} not in treatment_name_list:
            rtms_dao.insert_tTreatmentRtms(treatment_name, therapeutic_target, frequency, pulses, stimulation_time,
                                           inter_train_intervals, pulse_trains, total_pulses, total_time_minute,
                                           total_time_second, note,
                                           doctor_id)
        else:
            check_new_treatment = {"check_new_treatment": 1}
        if check_new_treatment['check_new_treatment']==1:
            return HttpResponse("方案名称重复！提交失败!")
        if check_new_treatment['check_new_treatment']==0:
            return HttpResponse("提交成功！")
