import json

import patients.models as patients_models
import scales.models as scales_models
import users.models as users_models
from django.apps import apps
from django.db.models import Max,Count


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

    scales_dict = {
        'HAMA': 'RPatientHama',
        'HAMD17': 'RPatientHamd17',
        'YMRS': 'RPatientYmrs',
        'BPRS': 'RPatientBprs',

        'adolescent_events': 'RPatientAdolescentEvents',
        'atq': 'RPatientAtq',
        'cognitive_emotion': 'RPatientCognitiveEmotion',
        'happiness': 'RPatientHappiness',
        'manicsymptom': 'RPatientManicsymptom',
        'pleasure': 'RPatientPleasure',
        'suicidal': 'RPatientSuicidal',
        'ybobsessiontable': 'RPatientYbobsessiontable',
        'sembu': 'RPatientSembu',
        'gad': 'RPatientGad',
        'phq': 'RPatientPhq',
        'pss': 'RPatientPss',
        'insomnia': 'RPatientInsomnia',
        'growth': 'RPatientGrowth',

        'vept': 'RPatientVept',
        'wcst': 'RPatientWcst',
        'rbans': 'RPatientRbans',
        'fept': 'RPatientFept'
    }
    scales_score = {}
    for scale_name, model_name in scales_dict.items():
        model = apps.get_model('scales', model_name)
        res = model.objects.filter(patient_session_id=patient_session_id).values()
        if res.exists():
            scales_score[scale_name] = res[0]
        else:
            scales_score[scale_name] = {}
    return scales_score


def get_all_session():
    session = patients_models.DPatientDetail.objects.values('session_id').annotate(Count('session_id')).order_by()
    return session
