# -*- coding: utf-8 -*-
# @Time    : 2020/11/30 16:57
# @Author  : Fang Hanzheng
# @File    : SelfDefinedFilter.py
# @Software: PyCharm


from django import template
from tools import idAssignments
from tools import config
import patients.models as patients_models

register = template.Library()


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter(name='calciulateId')
def calciulateId(patient_id):
    return idAssignments.pack_patient_id(patient_id)


@register.filter(name='processNone')
def processNone(value):
    if value is None:
        return ''
    return value

@register.filter(name='processFloat')
def processFloat(value):
    if value is None:
        return ''
    return round(value, 2)

@register.filter(name='processSession')
def processSession(value):
    num = str(value)
    return 'S' + num.zfill(3)


@register.filter(name='get_diagnosis_by_dict')
def get_diagnosis_by_dict(patient):
    if patient['patient_id__diagnosis'] is None:
        return '--'
    if patient['patient_id__diagnosis'] == 99:
        return patient['patient_id__other_diagnosis']
    else:
        return config.disease_type_dict[patient['patient_id__diagnosis']]


@register.filter(name='get_diagnosis_by_object')
def get_diagnosis_by_object(patient):
    if patient.diagnosis is None:
        return '--'
    if patient.diagnosis == 99:
        return patient.other_diagnosis
    else:
        str = config.disease_type_dict[patient.diagnosis]
        if str == '高危遗传':
            s = str
            all_list = patients_models.RPatientGhr.objects.filter(ghr_id=patient.id)
            if all_list.count() != 0:
                s += '('
                for list in all_list:
                    s += config.disease_type_dict[list.diagnosis]
                    s += ";"
                s += ')'

            return s
        else:
            return str


@register.filter(name='get_scale_url')
def get_scale_url(scale_detail):
    scale_id = scale_detail['scale_id']
    patient_session_id = scale_detail['patient_session_id']
    patient_id = scale_detail['patient_session_id__patient_id']
    next_page_url = config.scales_html_dict[int(scale_id)]
    redirect_url = '{}?patient_session_id={}&patient_id={}&enter_page=1'.format(next_page_url, str(patient_session_id),
                                                                                str(patient_id))
    return redirect_url


@register.filter(name='check_scale')
def check_scale(scale_detail):
    scale_id = scale_detail['scale_id']
    patient_session_id = scale_detail['patient_session_id']
    patient_id = scale_detail['patient_session_id__patient_id']
    next_page_url = config.check_scales_html_dict[int(scale_id)]
    redirect_url = '{}?patient_session_id={}&patient_id={}&enter_page=1'.format(next_page_url, str(patient_session_id),
                                                                                str(patient_id))
    return redirect_url


# 进入个人一般信息重做页面
@register.filter(name='get_baseinfo_redo_scale_url')
def get_baseinfo_redo_scale_url(scale_detail):
    scale_id = scale_detail['scale_id']
    patient_session_id = scale_detail['patient_session_id']
    patient_id = scale_detail['patient_session_id__patient_id']
    next_page_url = config.scales_html_dict[int(scale_id)]
    redirect_url = '{}?patient_session_id={}&patient_id={}&do_type=0'.format(next_page_url, str(patient_session_id),
                                                                             str(patient_id))
    return redirect_url


# 进入个人一般信息查看页面
@register.filter(name='get_baseinfo_check_scale_url')
def get_baseinfo_check_scale_url(scale_detail):
    scale_id = scale_detail['scale_id']
    patient_session_id = scale_detail['patient_session_id']
    patient_id = scale_detail['patient_session_id__patient_id']
    next_page_url = config.scales_html_dict[int(scale_id)]
    redirect_url = '{}?patient_session_id={}&patient_id={}&do_type=1'.format(next_page_url, str(patient_session_id),
                                                                             str(patient_id))
    return redirect_url


@register.filter(name='get_self_scale_url')
def get_self_scale_url(scale_detail):
    scale_id = scale_detail['scale_id']
    patient_session_id = scale_detail['patient_session_id']
    # patient_id = scale_detail['patient_session_id__patient_id']
    redirect_url = '/scales/self_test?scale_id={}&patient_session_id={}'.format(str(scale_id), str(patient_session_id))
    return redirect_url


# 进入自评量表查看页面
@register.filter(name='get_self_check_scale_url')
def get_self_check_scale_url(scale_detail):
    try:
        scale_id = scale_detail['scale_id']
        patient_session_id = scale_detail['patient_session_id']
        patient_id = scale_detail['patient_session_id__patient_id']
        next_page_url = config.check_scales_html_dict[int(scale_id)]
        redirect_url = '{}?patient_session_id={}&patient_id={}'.format(next_page_url, str(patient_session_id),
                                                                       str(patient_id))
    except Exception as e:
        print(e)
        return ""
    return redirect_url


@register.filter(name='get_progress_note_url')
def get_progress_note_url(inpatient):
    if inpatient.progress_note.name.strip() == '':
        return '#'
    return inpatient.progress_note.url
