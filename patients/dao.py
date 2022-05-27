import users.models as users_models
import patients.models as patients_models
import scales.models as scales_models
import tools.Utils as tools_utils
import tools.insertCascadeCheck as tools_insertCascadeCheck
import tools.config as tools_config


# 将要做的scales分成个人信息，自评，他评等四类
def judgment_do_scales(scales_list):
    information_list = []
    other_test_list = []
    self_test_list = []
    cognition_list = []
    for scale in scales_list:
        if scale.do_scale_type == 0:
            information_list.append(scale)
        elif scale.do_scale_type == 1:
            other_test_list.append(scale)
        elif scale.do_scale_type == 2:
            self_test_list.append(scale)
        elif scale.do_scale_type == 3:
            cognition_list.append(scale)
    return information_list, other_test_list, self_test_list, cognition_list


# 获取被试需要做的scales的list
def judgment_scales(patient_detail_id):
    patient_detail = get_patient_detail_byPK(patient_detail_id)
    # 判断是初扫还是复扫
    if patient_detail.session_id == 1:
        # 初扫
        # 判断患者年龄
        if patient_detail.age > tools_config.adult_age:
            # 成人
            scales_list = scales_models.DScales.objects.filter(scale_type__in=[0, 2])
        else:
            # 青少年
            scales_list = scales_models.DScales.objects.filter(scale_type__in=[0, 1, 2])
    else:
        # 复扫
        scales_list = scales_models.DScales.objects.filter(scale_type__in=[2])
    return scales_list


# 当初扫和复扫时，依据被试需要做的scales_list，预先插入r_patient_scales表中多条记录
def add_rscales(scales_list, patient_detail_id):
    # 插入r_patient_scales表
    insert_list = []
    for scale in scales_list:
        insert_list.append(scales_models.RPatientScales(patient_session_id=patient_detail_id,
                                                        scale_id=scale.id, state=0))
    scales_models.RPatientScales.objects.bulk_create(insert_list)


################ add 部分 ################
################ add 部分 ################
################ add 部分 ################

# add baseinfo表
def add_base_info(patient_base_info_objct):
    # 插入数据库前的级联检验
    tools_insertCascadeCheck.insert_patient_base_info_check(patient_base_info_objct)
    # 插入数据库
    patient_base_info_objct.save()


# add patient_detail表
def add_patient_detail(patient_detail_objct):
    # 插入数据库前的级联检验
    tools_insertCascadeCheck.insert_patient_detail_check(patient_detail_objct)
    # 插入数据库
    patient_detail_objct.save()

# add BPatientAppointment表
def add_patient_appointment(PatientAppoientment_object):
    PatientAppoientment_object.save()


# add DPatientIsMedicalAdvice表
def add_medical_advice(medical_advice_object):
    medical_advice_object.save()

################ del 部分 ################
################ del 部分 ################
################ del 部分 ################

# patient_detail表
def del_patient_detail_byPK(patient_detail_id):
    patients_models.DPatientDetail.object.filter(id=patient_detail_id)[0].delete()


# del patient_base_info表,同时需要删除高危信息,rtms治疗情况
def del_patient_base_info_byPK(patient_id):
    if patients_models.BPatientBaseInfo.objects.filter(pk=patient_id).count() > 0:
        #删除所有的rtms信息
        patient_detail = patients_models.DPatientDetail.objects.filter(patient_id=patient_id)
        for detail in patient_detail:
            patient_session_id = detail.id
            all_list_tms = patients_models.BPatientRtms.objects.filter(patient_session_id=patient_session_id)
            for list in all_list_tms:
                list.delete()
        patients_models.BPatientBaseInfo.objects.filter(pk=patient_id).first().delete()
        all_list_ghr = patients_models.RPatientGhr.objects.filter(ghr_id=patient_id)
        for list in all_list_ghr:
            list.delete()


#高危信息表
def add_patient_ghr(rPatientGhr):
    # 插入数据库前的级联检验
    tools_insertCascadeCheck.insert_patient_base_info_check(rPatientGhr)
    rPatientGhr.save()

################ get 部分 ################
################ get 部分 ################
################ get 部分 ################
################ get 部分 ################


def get_patient_detail_last_byPatientId(patient_id):
    patient_detail_res = patients_models.DPatientDetail.objects.filter(patient_id=patient_id)
    if patient_detail_res.count() == 0:
        return None
    else:
        return patient_detail_res.last()


def get_patient_detail_byPatientId(patient_session_id):
    patient_detail_res = patients_models.DPatientDetail.objects.filter(id=patient_session_id)[0]
    return patient_detail_res

# get scales表
def get_scales_all():
    scales_list = scales_models.DScales.objects.all()
    return scales_list


# get user表
def get_user_byPK(doctor_id):
    doctor = users_models.SUser.objects.filter(id=doctor_id)[0]
    return doctor


# get 民族表
def get_DEthnicity_all():
    dEthnicity_list = patients_models.DEthnicity.objects.all()
    return dEthnicity_list


# get base info表
def get_base_info_all():
    base_info_list = patients_models.BPatientBaseInfo.objects.all().order_by('-id')
    return base_info_list


def get_base_info_byPK(patient_id):
    patient = patients_models.BPatientBaseInfo.objects.select_related().filter(pk=patient_id)
    if patient.count() == 0:
        return None
    else:
        return patient[0]


# get patient_detail 主体
def get_patient_detail_byPK(patient_detail_id):
    patient_detail = patients_models.DPatientDetail.objects.filter(id=patient_detail_id)
    if patient_detail.count() == 0:
        return None
    else:
        return patient_detail[0]


def get_patient_detail_byPatientIdAndSessionId(patient_id, session_id):
    dPatientDetail = patients_models.DPatientDetail.objects.filter(patient_id=patient_id, session_id=session_id)
    if dPatientDetail.count() == 0:
        return None
    else:
        return dPatientDetail[0]


def get_patient_detail_byForeignPatientId(patient_id):
    patient_detail_list = patients_models.DPatientDetail.objects.filter(patient__id=patient_id)
    if patient_detail_list.count() == 0:
        return None
    else:
        return patient_detail_list


def get_patient_detail_all():
    patient_detail_list = patients_models.DPatientDetail.objects.all()
    return patient_detail_list


def get_patient_detail_lastsession(patient_id):
    patient_detail_list = patients_models.DPatientDetail.objects.filter(patient__id=patient_id).order_by('-session_id')
    if patient_detail_list.count() == 0:
        return None
    return patient_detail_list[0]

# 根据patient_id获取长期医嘱信息表中的相关记录
def get_medical_advice_info(patient_id):
    medical_advice_info = patients_models.DPatientIsMedicalAdvice.objects.filter(patient_id=patient_id)
    if medical_advice_info.count() == 0:
        return None
    return medical_advice_info[0]

# 长期医嘱表中更新备注
def add_medical_adviec_ps(patient_id, postscript):
    medical_adviec_ps = patients_models.DPatientIsMedicalAdvice.objects.filter(patient_id=patient_id)
    medical_adviec_ps.update(postscript=postscript, is_postscript=1)


# 医嘱表更新前清空旧记录的方法
def del_medical_advice_by_patientid(patient_id):
    res = patients_models.BPatientMedicalAdviceDetail.objects.filter(patient_id=patient_id)
    if res.exists():
        res.delete()
# 查询数据库中的用药信息
def get_medical_advice_drug(patient_id):
    medical_advice_drug = patients_models.BPatientMedicalAdviceDetail.objects.filter(patient_id=patient_id)
    if medical_advice_drug.count() == 0:
        return None
    return medical_advice_drug

# 无需长期医嘱、病程记录、备注，设置识别字段为0
def set_dont_need_ma_or_pn(patient_id):
    patient = get_medical_advice_info(patient_id)
    # 若d_patient_is_medical_advice表中无此病人的信息，则先创建一条这个病人的记录
    if patient == None:
        patients_models.DPatientIsMedicalAdvice.objects.create(patient_id=patient_id)
        patient = get_medical_advice_info(patient_id)
    patient.is_medical_advice = 0
    patient.is_progress_note = 0
    patient.is_postscript = 0
    patient.save()

# r_patient_scales表相关：
# get r patient_detail 的自评量表状态
def get_patient_scales_byPatientDetailId_self(patient_detail_id):
    patient_scales_list = scales_models.RPatientScales.objects.filter(patient_session=patient_detail_id,
                                                                      scale__patient_or_doctor_type=0)
    return patient_scales_list


# get r patient_detail 的他评量表状态
def get_patient_scales_byPatientDetailId_other(patient_detail_id):
    patient_scales_list = scales_models.RPatientScales.objects.filter(patient_session=patient_detail_id,
                                                                      scale__patient_or_doctor_type=1)
    return patient_scales_list


# get r patient_detail 的认知表状态
def get_patient_scales_byPatientDetailId_cognition(patient_detail_id):
    patient_scales_list = scales_models.RPatientScales.objects.filter(patient_session=patient_detail_id,
                                                                      cale__patient_or_doctor_type=2)
    return patient_scales_list


# get r patient_detail表
def get_patient_scales_byPatientDetailId(patient_detail_id):
    patient_scales_list = scales_models.RPatientScales.objects.filter(patient_session=patient_detail_id)
    if patient_scales_list.count() == 0:
        return None
    else:
        return patient_scales_list

# d_patient_appointment表
def get_patient_appointment_all():
    patients_models.DPatientAppointment.objects.all()

def set_inpatient_type(patient_id,inpatient_state):
    patient = patients_models.BPatientBaseInfo.objects.filter(pk = patient_id)[0]
    patient.inpatient_state = inpatient_state
    patient.save()

#rtms:
def add_rtms_info(bPatientRtms):
    bPatientRtms.save()