from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from . import dao as statistics_dao
from tools.layuiPage import paginator
from tools.Scale_tools import *

def getPatients(request):
    search_condition = {}
    count = 0
    data = request.GET
    if data.get('name'):
        search_condition['patient__name__contains'] = data['name']
    if data.get('session_id'):
        search_condition['session_id'] = data.get('session_id')
    if data.get('gender'):
        search_condition['patient__sex'] = data.get('gender')
    if data.get('age_min') and data.get('age_max'):
        if not (data.get('age_min') == '0' and data.get('age_max') == '0'):
            search_condition['age__range'] = (data.get('age_min'), data.get('age_max'))
    if data.getlist('source'):
        search_condition['source__in'] = data.getlist('source')
    if data.getlist('diagnosis'):
        search_condition['patient__diagnosis__in'] = data.getlist('diagnosis', [])
    if data.get('is_blood'):
        search_condition['blood'] = data['is_blood']
    if data.get('is_cognitive'):
        search_condition['cognitive'] = data['is_cognitive']
    if data.get('is_sound'):
        search_condition['sound'] = data['is_sound']
    if data.get('is_hairs'):
        search_condition['hairs'] = data['is_hairs']
    if data.get('is_manure'):
        search_condition['manure'] = data['is_manure']
    if data.get('is_first'):
        search_condition['first'] = data['is_first']
    if data.get('is_mri_check'):
        search_condition['mri_examination'] = data['is_mri_check']
    if data.getlist('handy'):
        search_condition['handy__in'] = data.getlist('handy')
    if data.get('is_ghr'):
        search_condition['patient__is_ghr'] = data['is_ghr']
    if data.getlist('impatient_state'):
        search_condition['patient__impatient_state__in'] = data.getlist('impatient_state')
    if data.get('scan_start_date') or data.get('scan_end_date'):
        search_condition['scan_date__range'] = (data['scan_start_date'], data['scan_end_date'])

    scales_id_models = {
        '8': 'RPatientHama',
        '7': 'RPatientHamd17',
        '9': 'RPatientYmrs',
        '10': 'RPatientbprs',

        '18': 'RPatientAdolescentEvents',
        '20': 'RPatientAtq',
        '17': 'RPatientCognitiveEmotion',
        '14': 'RPatientHappiness',
        '13': 'RPatientManicsymptom',
        '15': 'RPatientPleasure',
        '12': 'RPatientSuicidal',
        '11': 'RPatientYbobsessiontable',
        '19': 'RPatientSembu',
        '30': 'RPatientGad',
        '29': 'RPatientPhq',
        '32': 'RPatientPss',
        '31': 'RPatientInsomnia',
        '16': 'RPatientGrowth',

        '24': 'RPatientVept',
        '21': 'RPatientWcst',
        '22': 'RPatientRbans',
        '23': 'RPatientFept',
        '33': 'RPatientSuicideBehavior'
    }

    if data.getlist('scale_id') and data.getlist('scale_total_score_name') and data.getlist('scale_total_score') \
                and data.getlist('scales_total_score_compare'):
        score_name_list = data.getlist('scale_total_score_name')
        score_list = data.getlist('scale_total_score')
        score_compare_list = data.getlist('scales_total_score_compare')
        print(list(zip(score_name_list, score_list, score_compare_list)))

        for i, s_id in enumerate(data.getlist('scale_id')):
            model_name = scales_id_models.get(str(s_id))
            model_name = model_name.lower()
            search_content = model_name + '__' + score_name_list[i]
            if score_compare_list[i] == '0':
                search_condition[search_content] = score_list[i]
            if score_compare_list[i] == '1':
                search_condition[search_content + '__gte'] = score_list[i]

            if score_compare_list[i] == '2':
                search_condition[search_content + '__lte'] = score_list[i]
    print(search_condition)

    patients, count = statistics_dao.get_all_patientID_and_sessionID_by_filter(search_condition)

    res = {
            'code': 200,
            'msg': 'ok',
            'count': count,
            'data': patients
    }
    return JsonResponse(res)


def get_patient_data(request):
    patients = ''
    search_dict = {}

    if request.is_ajax():
        if request.method == 'GET':
            data = request.GET

            # 以下为基本筛选条件的组合
            if data.getlist('name[]') or data.getlist('patient_id[]'):
                search_dict['patient__name__in'] = data.getlist('name[]', [])
                search_dict['patient_id__in'] = data.getlist('patient_id[]', [])
            if data.getlist('session_id[]'):
                search_dict['session_id__in'] = data.getlist('session_id[]')
            if data.get('age_min') and data.get('age_max'):
                if not (data.get('age_min') == '0' and data.get('age_max') == '0'):
                    search_dict['age__range'] = (data.get('age_min'), data.get('age_max'))
            if data.get('sex'):
                search_dict['patient__sex__contains'] = data['sex']
            if data.get('source'):
                search_dict['source'] = data['source']
            if data.get('blood'):
                search_dict['blood'] = data['blood']
            if data.get('cognitive'):
                search_dict['cognitive'] = data['cognitive']
            if data.get('sound'):
                search_dict['sound'] = data['sound']
            if data.getlist('diagnosis[]'):
                search_dict['patient__diagnosis__in'] = data.getlist('diagnosis[]')
            if data.get('startDate') or data.get('endDate'):
                search_dict['scan_date__range'] = (data['startDate'], data['endDate'])

            # 以下为量表分数的条件筛选（封装成函数）
            scales_models = {
                'hama': 'RPatientHama',
                'hamd17': 'RPatientHamd17',
                'ymrs': 'RPatientYmrs',
                'bprs': 'RPatientbprs'
            }
            for raw_name, models_name in scales_models.items():
                scales_condition_alloc(data, raw_name, search_dict, models_name)

            patients = ''
            count = 0
            fact_data_list = []

            # 前台table设置中的page设置为true后渲染会自动传给后台page和limit值
            page_num = int(data.get('page', 1))
            page_limit = int(data.get('limit', 30))
            print(search_dict)
            scales_scores = []

            patients, count = statistics_dao.get_all_patient_by_filter(search_dict)
            if not data.get('all'):
                patients = paginator(patients, page_num, page_limit)

            # 把每条复扫记录基本信息与量表完成情况与得分情况组合
            for patient_detail in patients:
                scales_do = statistics_dao.get_one_patient_scales(patient_detail['id'])
                scales_scores = statistics_dao.get_scales_score(patient_detail['id'])

                new_self_rating_scores = statistics_dao.get_restructured_self_total_score_by_session_id(
                    patient_detail['id']
                )
                patient_detail.update(scales_do)
                patient_detail.update(scales_scores)
                patient_detail.update(new_self_rating_scores)
                fact_data_list.append(patient_detail)

            # 这里返回格式最好保持一致（是指res的key一致，不一致也可以前台parseData处理），data的值为字典列表
            res = {
                'code': 0,
                'msg': 'ok',
                'count': count,
                'data': fact_data_list
            }
            return JsonResponse(res)
        else:
            # TODO ajax的POST请求可以写在这里
            return HttpResponse("ok")


def show_page(request):
    username = request.session.get('username')
    session = statistics_dao.get_all_session()
    return render(request, 'statistics/index.html', {
        # 'patients': patients,
        'username': username,
        'session_all_list': session
    })


# ajax请求所有被试姓名与ID
def get_names(request):
    import patients.models as pm
    data = request.GET
    if data.get('keyword'):
        kw = data.get('keyword')
        if kw.isdigit():
            id_list = pm.BPatientBaseInfo.objects.filter(id=kw).values('id', 'name')
            return JsonResponse({'code': 0, 'msg': 'ok', 'data': list(id_list)})
        else:
            name_list = pm.BPatientBaseInfo.objects.filter(name__contains=data.get('keyword')).values('id', 'name')
            return JsonResponse({'code': 0, 'msg': 'ok', 'data': list(name_list)})
    else:
        return JsonResponse({
            'code': 1,
            'msg': 'nothing',
            'data': []
        })


# ajax请求所有扫描编号
def get_sessions(request):
    session = statistics_dao.get_all_session()
    for s in session:
        s['session_id_standard'] = 'S' + str(s['session_id']).zfill(3)
    return JsonResponse({'code': 0, 'msg': 'ok', 'data': list(session)})


def get_restructured_self_rating(request):
    result = statistics_dao.get_restructured_self_total_score(1871, 12)
    return JsonResponse({
        'code': 0,
        'msg': 'ok',
        'data': list(result)
    })
