import scales.models as scale_models
from .models import DPatientDetail, DEthnicity

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
import tools.Utils as tools_utils
import tools.idAssignments as tools_idAssignments
import patients.models as patients_models
import scales.models as scales_models
import scales.views as scale_views
import patients.dao as patients_dao
import followup.dao as followup_dao
import followup.views as followup_views
import tools.config as tools_config
from tools.Utils import Paginator
import json
import scales.dao as scales_dao
import time

scale_class_dict = {7: [scales_models.RPatientHamd17, [8, 21, 35], ['正常', '可能有抑郁症', '可能是轻或中度抑郁', '可能为严重抑郁']], \
                    8: [scales_models.RPatientHama, [7, 14, 21, 29], ['没有焦虑', '可能有焦虑', '肯定有焦虑', '肯定有明显焦虑', '可能为严重焦虑']], \
                    9: [scales_models.RPatientYmrs, [5, 13, 20, 30], ['正常', '轻度', '中度', '重度', '极重度']], \
                    10: [scales_models.RPatientBprs, [36], ['正常', '偏高']]}


def get_patient_by_search(request):
    search_dict = {}
    name = request.POST.get('name')
    sex = request.POST.get('sex')
    id = request.POST.get('patient_id')
    diagnosis = request.POST.get('diagnosis')
    if name and name.strip()!='':
        search_dict['name'] = name
    if sex and sex.strip()!='':
        search_dict['sex'] = sex
    if id and id.strip()!='':
        search_dict['id'] = int(id)
    if diagnosis and diagnosis.strip()!='':
        search_dict['diagnosis'] = diagnosis
    patients = patients_models.BPatientBaseInfo.objects.filter(**search_dict).all().order_by('-id')
    all_patients=patients_models.BPatientBaseInfo.objects.all().order_by('id')
    username = request.session.get('username')
    nations = DEthnicity.objects.all()
    obj_count = len(patients)
    obj_perpage = 10
    pagetag_current = request.POST.get('page',1)
    pagetag_dsp_count = 6
    paginator = Paginator(obj_count, obj_perpage, pagetag_current, pagetag_dsp_count)
    patients = patients[paginator.obj_slice_start:paginator.obj_slice_end]
    return render(request, 'manage_patients.html', {"patients": patients,
                                                    "all_patients":all_patients,
                                                    'username': username,
                                                    'nations': nations,
                                                    'paginator': paginator})

# 被试基本信息录入，需要生成id的信息，需要向patient_detail进行信息插入(session==1的信息)
# todo 在进行病人或者复扫创建的时候，需要创建ｒ_patients_scales创建量表完成信息，默认应该是未完成的，需要根据青少年这些去做
# 被试基本信息录入，需要生成id的信息，需要向patient_detail进行信息插入(session==1的信息)
# todo 在进行病人或者复扫创建的时候，需要创建ｒ_patients_scales创建量表完成信息，默认应该是未完成的，需要根据青少年这些去做
def add_patient_baseinfo(request):
    name = request.POST.get("name")
    birth_date = request.POST.get("birth_date")
    sex = request.POST.get("sex")
    nation = request.POST.get("nation")
    doctor_id = request.session.get('doctor_id')
    diagnosis = request.POST.get("diagnosis")
    other_diagnosis = request.POST.get("other_diagnosis")
    scan_date = request.POST.get('scan_date')
    age = tools_utils.calculate_age_by_scandate(str(birth_date), str(scan_date))
    ########################
    # 手动输入id
    patient_id = request.POST.get('patient_id')
    ########################

    # 自动分配id
    # patient_id = tools_idAssignments.patient_Id_assignment()
    patient_id, session_id, standard_id = tools_idAssignments.patient_session_id_assignment(patient_id)
    #rtms:  state:0

    # 插入高危信息表:需要在b_patient_base_info之前创建
    rPatientGhr = patients_models.RPatientGhr(ghr_id=patient_id, doctor_id=doctor_id)

    for key in request.POST.keys():
        pos = key.rfind('_')
        st = key[:pos]
        print("st:   " + st)
        if hasattr(rPatientGhr, st) and key != 'diagnosis':
            val = request.POST.get(key)
            if val == '':
                val = None
            setattr(rPatientGhr, st, val)
            if st == 'kinship':
                patients_dao.add_patient_ghr(rPatientGhr)
                rPatientGhr = patients_models.RPatientGhr(ghr_id=patient_id, doctor_id=doctor_id)
        if st=='kin_patient_id':
            kin_patient_id=request.POST.get(key)
            if kin_patient_id != '0':
                # rPatientGhr.diagnosis = patients_models.BPatientBaseInfo.objects.filter(
                #     pk=kin_patient_id).first().diagnosis
                diagnosis_val=patients_models.BPatientBaseInfo.objects.filter(
                    pk=kin_patient_id).first().diagnosis
                setattr(rPatientGhr, 'diagnosis', diagnosis_val)
                print(diagnosis_val)



    # 基本信息创建
    patient_base_info = patients_models.BPatientBaseInfo(id=patient_id, name=name, sex=sex, birth_date=birth_date,
                                                         nation=nation,
                                                         doctor_id=doctor_id,
                                                         diagnosis=diagnosis,
                                                         other_diagnosis=other_diagnosis)
    patients_dao.add_base_info(patient_base_info)


    # 创建一条复扫记录
    # age = tools_utils.calculate_age(birth_date)
    patient_detail = patients_models.DPatientDetail(patient_id=patient_id, session_id=session_id,
                                                    standard_id=standard_id,
                                                    age=age, doctor_id=doctor_id,
                                                    scan_date=scan_date,tms=None)
    patients_dao.add_patient_detail(patient_detail)
    # 查询需要做的量表,并在r_patient_scales中插入需要做的量表
    scales_list = patients_dao.judgment_scales(patient_detail.id)
    # 为初扫/复扫的病人预先在r_patient_scales中插入多条记录，依据被试需要做的scales_list
    patients_dao.add_rscales(scales_list, patient_detail.id)
    # 更新随访表
    # followup_dao.add_followup(patient_id, session_id, patient_detail.id, scan_date)
    # 页面跳转，select_scales页面
    patient_detail_id = patients_dao.get_patient_detail_byPatientIdAndSessionId(patient_id, session_id).id

    redirect_url = '/scales/select_scales?patient_session_id={}&patient_id={}'.format(str(patient_detail_id),
                                                                                      str(patient_id))
    return redirect(redirect_url)





# 添加复扫信息,需要获取到上次扫描的病人详细信息
def add_patient_followup(request):
    patient_id = request.GET.get('patient_id')
    doctor_id = request.session.get('doctor_id')
    scan_date = request.POST.get('scan_date')
    patient_baseinfo = patients_dao.get_base_info_byPK(patient_id)
    patient_id, session_id, standard_id = tools_idAssignments.patient_session_id_assignment(patient_baseinfo.id)
    patient_detail_last = patients_dao.get_patient_detail_last_byPatientId(patient_id)

    # 插入前的准备工作，这里需要预先进行处理，将上次的值赋进去
    patient_detail = patient_detail_last
    patient_detail.id = None
    patient_detail.tms = None
    patient_detail.patient_id = patient_id
    patient_detail.session_id = session_id
    patient_detail.standard_id = standard_id
    patient_detail.age = tools_utils.calculate_age_by_scandate(str(patient_baseinfo.birth_date), str(scan_date))
    patient_detail.scan_date=scan_date
    patient_detail.doctor_id = doctor_id

    patients_dao.add_patient_detail(patient_detail)
    # 获取创建的复扫信息自增id
    patient_detail_id = patients_dao.get_patient_detail_byPatientIdAndSessionId(patient_id, session_id).id
    # 查询需要做的量表,并在r_patient_scales中插入需要做的量表
    scales_list = patients_dao.judgment_scales(patient_detail_id)
    #更新随访表
    # followup_dao.add_followup(patient_id, session_id, patient_detail_id, scan_date)
    # 为初扫/复扫的病人预先在r_patient_scales中插入多条记录，依据被试需要做的scales_list
    patients_dao.add_rscales(scales_list, patient_detail.id)
    redirect_url = '/scales/select_scales?patient_session_id={}&patient_id={}'.format(str(patient_detail_id),
                                                                                      str(patient_id))
    return redirect(redirect_url)


# def get_selected_scales_with_lastsession(request):
#     patient_id = request.GET.get('patient_id')
#     last_patient_session_id = request.GET.get('last_patient_session_id')
#     # 获取上一次的复扫详情信息
#     last_patient_detail = patients_dao.get_patient_detail_byPK(last_patient_session_id)
#     # 获取这一次复扫信息
#     patient_baseinfo = patients_dao.get_base_info_byPK(patient_id)
#     patient_detail = patients_dao.get_patient_detail_last_byPatientId(patient_id)
#     generalinfo_scale_list, other_test_scale_list, self_test_scale_list, cognition_scale_list = scales_dao.get_uodo_scales(patient_detail.id)
#     return render(request, 'select_scales.html', {
#                                                   'patient_id': patient_baseinfo.id,
#                                                   'patient_baseinfo': patient_baseinfo,
#                                                   'patient_session_id': patient_detail.id,
#                                                   'standard_id':patient_detail.standard_id,
#                                                   "username": request.session.get('username'),
#                                                   'patient_detail': last_patient_detail,
#                                                   "todo_generalinfo_scale_size": len(generalinfo_scale_list),
#                                                   "todo_other_test_scale_size": len(other_test_scale_list),
#                                                   "todo_self_test_scale_size": len(self_test_scale_list),
#                                                   "todo_cognition_scale_size": len(cognition_scale_list),
#                                                   })

# 获取病人详细信息

# 获取病人详细信息

def get_patient_detail(request):
    if request.GET:
        patient_id = request.GET.get("patient_id")

        patient_baseinfo = patients_dao.get_base_info_byPK(patient_id)
        patient_detail_list = DPatientDetail.objects.all().select_related('patient__doctor').filter(
            patient_id=patient_id).values('id', 'patient_id', 'session_id', 'standard_id', 'create_time','update_time',
                                          'cognitive','sound','blood','hairs','manure','drugs_information',
                                          'mri_examination','first','tms','age','occupation','education','years',
                                          'emotional_state','phone','source','height','weight','waist','hip','handy','note','scan_date',
                                          'patient_id__diagnosis','patient_id__other_diagnosis', 'doctor__name','doctor__id')
        test_states = scales_models.RPatientScales.objects.all().select_related('patient_session_id__scale'). \
            filter(patient_session_id__patient=patient_baseinfo).values(
            'patient_session_id','patient_session_id__session_id','patient_session_id__patient_id',
            'scale_id','scale__scale_name', 'scale__do_scale_type','state','end_time'
        )
        for patient_detail in patient_detail_list:
            patient_session_id = patient_detail['id']
            patient_rtms_info = patients_models.BPatientRtms.objects.all().filter(patient_session_id=patient_session_id)
            count = patient_rtms_info.count()
            patient_detail['rtms_count'] = count
        ordered_dic = {}
        for test_state in test_states:
            if test_state['patient_session_id__session_id'] not in ordered_dic:
                ordered_dic[test_state['patient_session_id__session_id']] = {test_state['scale_id']: test_state}
            else:
                ordered_dic[test_state['patient_session_id__session_id']][test_state['scale_id']] = test_state
        nation_list = patients_dao.get_DEthnicity_all()
        ghr_list = patients_models.RPatientGhr.objects.filter(ghr_id=patient_id)
        ghr_diagnosis = []
        ghr_kinship = []
        for i in ghr_list:
            ghr_diagnosis.append(i.diagnosis)
            ghr_kinship.append(i.kinship)
        num_ghr = ghr_list.count()
        patients = patients_dao.get_base_info_all()
        return render(request, 'patient_detail.html',
                      {
                          'patient_id': patient_id,
                          'name': patient_baseinfo.name,
                          'birth_date': patient_baseinfo.birth_date.strftime('%Y-%m-%d'),
                          'sex': patient_baseinfo.sex,
                          'nation': patient_baseinfo.nation,
                          "patient_detail_res": patient_detail_list,
                          "username": request.session.get('username'),
                          "patients_states": ordered_dic,
                          'test': ordered_dic,
                          'nation_list': nation_list,
                          'diagnosis': patient_baseinfo.diagnosis,
                          'other_diagnosis': patient_baseinfo.other_diagnosis,
                          'ghr_diagnosis': ghr_diagnosis,
                          'ghr_kinship': ghr_kinship,
                          'num_ghr': num_ghr,
                          'patients':patients,
                          'doctor_id':request.session.get('doctor_id')
                      })
    else:
        return render(request, 'patient_detail.html', {"username": request.session.get("username")})

# 删除病人信息
def del_patient(request):
    if request.GET:
        patient_id = request.GET.get("patient_id")
        patients_dao.del_patient_base_info_byPK(patient_id)
        # followup_dao.del_followup_by_patient_id(patient_id)
        # 后续添加删除成功的展示页面，然后自动跳转回subjectmanage页面
        return redirect('/patients/get_all_patients_baseinfo')
    else:
        return redirect('/patients/get_all_patients_baseinfo')


# 删除一条复扫记录
def del_followup(request):
    patient_id = request.GET.get("patient_id")
    patient_session_id = request.GET.get("patient_session_id")
    print('session:   ',patient_session_id,"-----------pid",patient_id)
    patient_detail = DPatientDetail.objects.all().select_related('doctor').filter(pk=patient_session_id)
    # patient_detail_id=patient_detail.id

    all_list_tms = patients_models.BPatientRtms.objects.filter(patient_session_id=patient_session_id)
    for list in all_list_tms:
        list.delete()

    if patient_detail.count() == 1:
        # 只有创建该条记录的用户才能够删除本条记录
        if patient_detail.first().doctor.username == request.session.get('username'):
            patient_detail.first().delete()
            # followup_dao.del_followup_by_patient_detail_id(patient_detail_id)

    return redirect('/patients/get_patient_detail?patient_id=' + patient_id)




# 更新patient_detail以及patient_base_info
def update_patient_detail(request):
    patient_session_id = request.GET.get('patient_session_id')
    patient_id = request.GET.get('patient_id')
    session_id = request.GET.get('session_id')
    patient_detail = patients_dao.get_patient_detail_byPK(patient_session_id)
    # patient_base_info = patients_dao.get_base_info_byPK(patient_id)
    # 通过field的方式进行数据的传递，注意，需要保证form表单中各项的名称与数据库中字段名称是名称相同
    fields_data = DPatientDetail._meta.fields
    data_dict = patient_detail.__dict__
    for ele in fields_data:
        if request.POST.get(ele.name) is not None and request.POST.get(ele.name) is not '':
            data_dict[ele.name] = request.POST.get(ele.name)
    patients_dao.add_patient_detail(patient_detail)
    # patient_base_info.diagnosis = request.POST.get('diagnosis')
    # patient_base_info.other_diagnosis = request.POST.get('other_diagnosis')
    # patients_dao.add_base_info(patient_base_info)
    redirect_url = '/scales/select_scales?patient_session_id={}&patient_id={}'.format(str(patient_session_id), str(patient_id))

    return redirect(redirect_url)


# 更新base_info,同时更新高危
def update_base_info(request):
    patient_id = request.GET.get("patient_id")
    print("#################" + str(request.POST.get('nation')))
    patient_base_info = patients_dao.get_base_info_byPK(patient_id)
    print("################" + str(patient_base_info.nation))
    ori_diagnosis=patient_base_info.diagnosis #获取之前的诊断
    patient_base_info = scale_views.set_attr_by_post(request, patient_base_info)
    print("################" + str(patient_base_info.nation))
    new_diagnosis=patient_base_info.diagnosis

    patients_dao.add_base_info(patient_base_info)

    #更新高危信息
    set_ghr_by_post(request, patient_id)  #如果高危信息页面没有变化，函数不会保存新的内容
    if ori_diagnosis==7 and new_diagnosis!='7': #从高危改成其他患病类型，要把原先的高危信息删除
        #print("del_ghr------------------------------------")
        all_list_ghr = patients_models.RPatientGhr.objects.filter(ghr_id=patient_id)
        for list in all_list_ghr:
            list.delete()
    #添加高危信息
    if  new_diagnosis=='7' and ori_diagnosis!=7:
        #print('add_ghr----------------------------')
        add_ghr_by_post(request,patient_id)

    return redirect('/patients/get_patient_detail?patient_id=' + patient_id)


# 新建被试获取自动生成的id
@csrf_exempt
def get_generateId(id):
    patient_id = tools_idAssignments.patient_Id_assignment()
    standard_id = tools_idAssignments.generate_standard_id(patient_id, 1)
    data = {}
    data['standard_id'] = standard_id
    return JsonResponse(data)


# 被试详细信息显示
def subjectDetailInfo(request):
    return render(request, 'forms_general_info.html', {"username": request.session.get("username")})


def patient_statistics(request):
    patients_n = 0
    hc_n = 0
    mdd_n = 0
    bd_n = 0
    sz_n = 0
    man_age_list = []
    woman_age_list = []
    man_education_list = []
    woman_education_list = []
    all_patient_base_info = patients_dao.get_base_info_all()
    for patient_base_info in all_patient_base_info:
        patient_id = patient_base_info.__getattribute__('id')
        sex = patient_base_info.__getattribute__('sex')
        patient_detail_info = DPatientDetail.objects.filter(patient_id=patient_id)
        if len(patient_detail_info) > 0:
            age = patient_detail_info[0].__getattribute__('age')
            education = patient_detail_info[0].__getattribute__('education')
            if sex == 0:
                if age is not None:
                    woman_age_list.append(age)
                if education is not None:
                    woman_education_list.append(education)
            elif sex == 1:
                if age is not None:
                    man_age_list.append(age)
                if education is not None:
                    man_education_list.append(education)

            # diagnosis = patient_detail_info[0].__getattribute__('diagnosis')
            diagnosis = patient_detail_info[0].patient.diagnosis
            if diagnosis == 'HC':
                hc_n += 1
            else:
                patients_n += 1
                # 0：未诊断
                # 1：健康者
                # 2：重性抑郁障碍
                # 3：焦虑障碍
                # 4：双相障碍
                # 5：精神分裂症
                # 6：强迫症
                # 7：高危遗传
                # 8：临床高危
                # 9：抑郁症状
                if diagnosis == 2:
                    mdd_n += 1
                elif diagnosis == 4:
                    bd_n += 1
                elif diagnosis == 5:
                    sz_n += 1
        else:
            continue

    man_age_list = [12, 15, 32, 44, 56, 21, 16, 18]
    woman_age_list = [23, 14, 17, 29, 56, 44, 32, 45, 36, 65]
    man_education_list = [12, 15, 32, 44, 56, 21, 16, 18, 22, 5, 2, 4, 8]
    woman_education_list = [23, 14, 17, 29, 56, 44, 32, 45, 36, 33, 2, 1, 17, 44, 2]
    patients_n = 123
    hc_n = 65
    mdd_n = 65
    bd_n = 35
    sz_n = 23

    subject_n = patients_n + hc_n
    woman_n = len(woman_age_list)
    man_n = len(man_age_list)

    # age
    man_age_num_list = []
    woman_age_num_list = []
    age_labels_list = []
    for i in range(1, 8):
        age_index = (i + 1) * 10
        man_age_num = 0
        woman_age_num = 0
        for age in man_age_list:
            if age_index > age >= i * 10:
                man_age_num += 1
        for age in woman_age_list:
            if age_index > age >= i * 10:
                woman_age_num += 1
        man_age_num_list.append(man_age_num)
        woman_age_num_list.append(woman_age_num)
        age_labels_list.append('%d-%d' % (i * 10, age_index))

    # education
    man_education_num_list = []
    woman_education_num_list = []
    education_labels_list = []
    for i in range(0, 5):
        education_index = (i + 1) * 10
        man_education_num = 0
        woman_education_num = 0
        for education in man_education_list:
            if education_index > education >= i * 10:
                man_education_num += 1
        for education in woman_education_list:
            if education_index > education >= i * 10:
                woman_education_num += 1
        man_education_num_list.append(man_education_num)
        woman_education_num_list.append(woman_education_num)
        education_labels_list.append('%d-%d' % (i * 10, education_index))

    patients = patients_dao.get_patient_detail_all()
    for patient in patients:
        doctor = patients_dao.get_user_byPK(patient.doctor_id)
        search_scales = scales_dao.get_scales_by_patientAndtype(patient.id,tools_config.other_test_type)
        base_info = patients_dao.get_base_info_byPK(patient.patient_id)

        # patient.name = base_info['name']
        # patient.sex = base_info['sex']
        # patient.doctor_id = doctor['username']
        patient.name = base_info.name
        patient.sex = base_info.sex
        print("###########", doctor)
        patient.doctor_id = doctor.name

        # if patient.diagnosis == 1:
        #     patient.diagnosis = 'MDD'
        # elif patient.diagnosis == 2:
        #     patient.diagnosis = 'BD'
        # elif patient.diagnosis == 3:
        #     patient.diagnosis = 'SZ'
        patient.patient.diagnosis = tools_config.disease_type_dict[patient.patient.diagnosis]

        scale_id_list = []
        scale_score_list = []
        if len(search_scales) > 0:
            for scale in search_scales:
                if scale.state == 0:
                    continue
                scale_id_list.append(scale.scale_id)

                scale_class = scale_class_dict[scale.scale_id][0]
                if len(scale_class.objects.filter(patient_session_id=patient.id).values()) > 0:
                    scale_info = scale_class.objects.filter(patient_session_id=patient.id).values()[0]
                    scale_score_list.append(scale_info['total_score'])

        patient.scale_id_list = scale_id_list
        patient.scale_score_list = scale_score_list

    scales = scales_dao.get_scale_by_doscaletype(tools_config.other_test_type)
    all_scale_id_list = []
    all_scale_name_list = []
    all_scale_value_range_list = []
    all_scale_value_str_range_list = []
    for scale in scales:
        all_scale_id_list.append(scale.id)
        all_scale_name_list.append(scale.scale_name)
        if scale.id in scale_class_dict.keys():
            all_scale_value_range_list.append(scale_class_dict[scale.id][1])
            all_scale_value_str_range_list.append(scale_class_dict[scale.id][2])

    print('-' * 100)
    print(scale_score_list)
    return render(request, 'patient_statistics.html', {
        'username': request.session.get('username'),
        'man_age_num_list': json.dumps(man_age_num_list),
        'woman_age_num_list': json.dumps(woman_age_num_list),
        'age_labels_list': json.dumps(age_labels_list),
        'man_education_num_list': json.dumps(man_education_num_list),
        'woman_education_num_list': json.dumps(woman_education_num_list),
        'education_labels_list': json.dumps(education_labels_list),
        'patients_n': patients_n,
        'hc_n': hc_n,
        'mdd_n': mdd_n,
        'bd_n': bd_n,
        'sz_n': sz_n,
        'subject_n': subject_n,
        'woman_n': woman_n,
        'man_n': man_n,
        'patients': patients,
        'scales': scales,
        'all_scale_id_list': json.dumps(all_scale_id_list),
        'all_scale_name_list': json.dumps(all_scale_name_list),
        'all_scale_value_range_list': json.dumps(all_scale_value_range_list),
        'all_scale_value_str_range_list': json.dumps(all_scale_value_str_range_list)
    })


def test_view(request):
    dic = request.session.get('history')
    return render(request, 'warning.html')


# 根据request post信息设置models的值
def set_attr_by_post(request, _object):
    for key in request.POST.keys():
        if hasattr(_object, key) and request.POST.get(key) != '':
            setattr(_object, key, request.POST.get(key))
    return _object

# 根据request post信息更新高危信息
def set_ghr_by_post(request,id):
    #print('modify_ghr--------------------------')
    #doctor_id=request.session.get('doctor_id')
    rPatientGhr = patients_models.RPatientGhr()
    ghr_kinship_list = []
    ghr_diagnosis_list = []
    for key in request.POST.keys():
        pos = key.rfind('_')
        st = key[:pos]
        print("st:   " + st)
        if hasattr(rPatientGhr, st) and key!='diagnosis':
            val = request.POST.get(key)
            if val == '':
                val = None
            if st == 'kinship':
                ghr_kinship_list.append(val)
            if st=='diagnosis':
                ghr_diagnosis_list.append(val)

    for i in range(len(ghr_diagnosis_list)):
        diagnosis = ghr_diagnosis_list[i]
        kinship = ghr_kinship_list[i]
        patient_ghr=patients_models.RPatientGhr.objects.filter(ghr_id=id, kinship=kinship)[0]
        patient_ghr.diagnosis=diagnosis
        patients_dao.add_patient_ghr(patient_ghr)



def add_ghr_by_post(request,id):
    doctor_id=request.session.get('doctor_id')
    rPatientGhr = patients_models.RPatientGhr(ghr_id=id, doctor_id=doctor_id)
    for key in request.POST.keys():
        #pos = key.rfind('_')-4
        #st = key[:pos]
        end_pos = key.rfind('_') - 1  # 倒数第一个"_"的位置再左移一位
        start_pos = key.rfind('_', 0, end_pos)  # 从开始截至到end_pos的位置，从右往左出现的第一个"_"也就是我们要找的倒数第二个"_"
        st = key[:start_pos]

        if hasattr(rPatientGhr, st) and key != 'diagnosis':
            val = request.POST.get(key)
            if val == '':
                val = None
            setattr(rPatientGhr, st, val)
            if st == 'kinship':
                patients_dao.add_patient_ghr(rPatientGhr)
                rPatientGhr = patients_models.RPatientGhr(ghr_id=id, doctor_id=doctor_id)


def del_blood(request):
    patient_session_id = request.GET.get('patient_session_id')
    patient_id = request.GET.get('patient_id')
    blood_res=patients_models.RPatientBlood.objects.filter(patient_session_id=patient_session_id).first()
    if blood_res is not None:
        blood_res.delete()
    patient_detail_res=patients_models.DPatientDetail.objects.filter(id=patient_session_id).first()
    patient_detail_res.blood=0
    patient_detail_res.save()
    redirect_url = '/scales/select_scales?patient_session_id={}&patient_id={}'.format(str(patient_session_id),str(patient_id))
    return redirect(redirect_url)

def add_blood(request):
    patient_session_id = request.GET.get('patient_session_id')
    patient_id = request.GET.get('patient_id')
    blood_res = patients_models.RPatientBlood.objects.filter(patient_session_id=patient_session_id).first()
    if blood_res is not None:
        blood_res.delete()
    rPatientBlood= patients_models.RPatientBlood(patient_session_id=patient_session_id)
    rPatientBlood=set_attr_by_post(request, rPatientBlood)
    rPatientBlood.save()
    patient_detail_res=patients_models.DPatientDetail.objects.filter(id=patient_session_id).first()
    patient_detail_res.blood=1
    patient_detail_res.save()
    redirect_url = '/scales/select_scales?patient_session_id={}&patient_id={}'.format(str(patient_session_id),str(patient_id))
    return redirect(redirect_url)