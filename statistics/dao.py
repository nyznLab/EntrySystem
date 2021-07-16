import json

import patients.models as patients_models
import scales.models as scales_models
import users.models as users_models
from django.forms import model_to_dict


# 获取每位病人的一条复扫记录的所做量表情况
def get_one_patient_scales(patient_session_id):
    done_list = []
    not_done_list = []
    no_need_list = []
    one_patient_scales = scales_models.RPatientScales.objects.filter(patient_session_id=patient_session_id)
    scale_count = scales_models.DScales.objects.all().count()

    if one_patient_scales.exists():
        for i in one_patient_scales:

            # 检出患者已完成量表与未完成量表
            if i.state:
                done_list.append(i.scale_id)
            else:
                not_done_list.append(i.scale_id)
        # 检出哪些量表该患者不需要做
        for n in range(1, scale_count + 1):
            if n not in done_list + not_done_list:
                no_need_list.append(n)

    else:
        print(patient_session_id + '的量表数据不存在！')

    done = scales_models.DScales.objects.filter(id__in=done_list).values()
    not_done = scales_models.DScales.objects.filter(id__in=not_done_list).values()
    no_need = scales_models.DScales.objects.filter(id__in=no_need_list).values()
    scales_dict = {}
    s_dict = {
        # 'done': done_list,
        'done': list(done),
        # 'not_done': not_done_list,
        'not_done': list(not_done),
        # 'no_need': no_need_list,
        'no_need': list(no_need)
    }
    scales_dict['scales'] = s_dict
    return scales_dict


# 按条件筛选患者信息
def get_all_patient_by_filter(condition):

    print(patients_models.DPatientDetail.__class__.__name__)
    results = ''
    count = 0

    if condition:
        results = patients_models.DPatientDetail.objects.filter(**condition).order_by('patient_id')
        count = results.count()

    else:
        results = patients_models.DPatientDetail.objects.all().order_by('patient_id')
        count = results.count()

        # results = patients_models.DPatientDetail.objects.filter(patient__name__contains=value)

    info_list = list(results.values())
    n = 0
    for i in results:
        info_list[n]['name'] = i.patient.name
        info_list[n]['sex'] = i.patient.sex
        info_list[n]['nation'] = i.patient.nation
        info_list[n]['diagnosis'] = i.patient.diagnosis
        info_list[n]['other_diagnosis'] = i.patient.other_diagnosis
        info_list[n]['inpatient_state'] = i.patient.inpatient_state
        user = users_models.SUser.objects.get(pk=i.doctor_id)
        if user:
            info_list[n]['doctor'] = user.name
        n += 1
    return info_list, count


# 获取量表单项得分与总分
def get_scales_score(patient_session_id):

    # 他评量表

    res_hama = scales_models.RPatientHama.objects.filter(patient_session_id=patient_session_id).values()
    res_hamd17 = scales_models.RPatientHamd17.objects.filter(patient_session_id=patient_session_id).values()
    res_ymrs = scales_models.RPatientYmrs.objects.filter(patient_session_id=patient_session_id).values()
    res_bprs = scales_models.RPatientBprs.objects.filter(patient_session_id=patient_session_id).values()
    hama, hamd17, ymrs, bprs = '', '', '', ''
    if res_hama:
        hama = res_hama[0]
    if res_hamd17:
        hamd17 = res_hamd17[0]
    if res_ymrs:
        ymrs = res_ymrs[0]
    if res_bprs:
        bprs = res_bprs[0]

    scales_score = {
        'HAMA': hama,
        'HAMD17': hamd17,
        'YMRS': ymrs,
        'BPRS': bprs,
    }
    return scales_score

