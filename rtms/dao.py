# !/user/bin/python3
# coding=utf-8
import datetime

from django.db.models import Max

import rtms.models as rtms_models


# r_patient_rtms表相关：
# 新增病人的rTMS治疗信息
def insert_patient_rtms(rPatientRtms_object):
    rPatientRtms_object.save()


# 通过病人id获取最大治疗顺序号
def get_treatment_num_byPatientId(patient_id):
    max_treatment_num = rtms_models.rPatientRtms.objects.filter(delete=0, patient_id=patient_id).aggregate(
        max_treatment_num=Max('treatment_num'))['max_treatment_num']
    return max_treatment_num

# 通过病人id和session_id查询治疗次数
def get_rtms_num_byPatientIdSessionId(patient_id, session_id):
    rtms_num = rtms_models.rPatientRtms.objects.filter(delete=0, patient_id=patient_id, session_id=session_id).count()
    return rtms_num

# 通过病人id和session_id查询治疗方案id，单一方案返回治疗方案id，多个方案返回None
def get_rtms_treatment_id_byPatientIdSessionId(patient_id,session_id):
    rtms_treatment_id_list = rtms_models.rPatientRtms.objects.filter(delete=0, patient_id=patient_id, session_id=session_id).values('treatment_id').distinct()
    if rtms_treatment_id_list==None:
        treatment_id = None
    if rtms_treatment_id_list!=None:
        num_treatment_id = len(list(rtms_treatment_id_list))
        if num_treatment_id==1:
            treatment_id = rtms_treatment_id_list[0]['treatment_id']
        else:
            treatment_id= None
    return treatment_id


# t_treatment_rtms表相关
# 查询所有治疗方案
def get_treatment_rtms():
    treatment_rtms_list = rtms_models.tTreatmentRtms.objects.filter(delete=0)
    return treatment_rtms_list


# 通过病人id获取最大治疗顺序号
def get_max_treatmentId():
    max_treatment_id = rtms_models.tTreatmentRtms.objects.filter(delete=0).aggregate(max_treatment_id=Max('treatment_id'))[
        'max_treatment_id']
    return max_treatment_id


# 通过治疗方案id查询治疗方案名称
def get_treatment_name_byTreatmentId(treatment_id):
    treatment_obj = rtms_models.tTreatmentRtms.objects.filter(treatment_id=treatment_id, delete=0)
    if treatment_obj == None or treatment_id == None:
        treatment_name = None
    else:
        treatment_name = treatment_obj[0].treatment_name
    return treatment_name


# 新增治疗方案
def insert_tTreatmentRtms(treatment_name, therapeutic_target, frequency, pulses, stimulation_time,
                          inter_train_intervals, pulse_trains, total_pulses, total_time_minute, total_time_second, note,
                          doctor_id):
    max_treatmentId = get_max_treatmentId()
    if max_treatmentId!=None:
        tTreatmentRtms_obj = rtms_models.tTreatmentRtms(
            treatment_id=int(str(max_treatmentId)) + 1,
            treatment_name=treatment_name,
            therapeutic_target=therapeutic_target,
            frequency=frequency,
            pulses=pulses,
            stimulation_time=stimulation_time,
            inter_train_intervals=inter_train_intervals,
            pulse_trains=pulse_trains,
            total_pulses=total_pulses,
            total_time_minute=total_time_minute,
            total_time_second=total_time_second,
            note=note,
            doctor_id=doctor_id,
            create_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"),
            update_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"),
            delete=0
        )
        tTreatmentRtms_obj.save()
