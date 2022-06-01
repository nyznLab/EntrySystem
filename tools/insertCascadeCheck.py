import patients.models as patients_models
import scales.models as scales_models
import users.models as users_models
import tools.Utils as tools_utils

"""##############表插入前的外键表检验接口#############"""
'''##############表插入前的外键表检验接口#############'''
'''##############表插入前的外键表检验接口#############'''
'''##############表插入前的外键表检验接口#############'''


# patient_medical_history 表插入前的外键检验
def insert_patient_medical_history_check(rPatientMedicalHistory_object):
    # 空值判断
    if rPatientMedicalHistory_object is None \
            or rPatientMedicalHistory_object.patient_session_id is None \
            or rPatientMedicalHistory_object.scale_id is None \
            or rPatientMedicalHistory_object.doctor_id is None:
        tools_utils.object_judgment(True)
    else:
        # 非空时外键判断
        dPatientDetail = \
            patients_models.DPatientDetail.objects.filter(pk=rPatientMedicalHistory_object.patient_session_id)[0]
        dScales = scales_models.DScales.objects.filter(pk=rPatientMedicalHistory_object.scale_id)[0]
        doctor = users_models.SUser.objects.filter(pk=rPatientMedicalHistory_object.doctor_id)[0]
        if dPatientDetail is None or dScales is None or doctor is None:
            object_flag = True
        else:
            object_flag = False
        tools_utils.object_judgment(object_flag)


# patient_drug_information 表插入前的外键检验
def insert_patient_drug_information_check(rPatientDrugInformation_object):
    # 空值判断
    if rPatientDrugInformation_object is None \
            or rPatientDrugInformation_object.patient_session_id is None \
            or rPatientDrugInformation_object.scale_id is None \
            or rPatientDrugInformation_object.doctor_id is None:
        tools_utils.object_judgment(True)
    else:
        # 非空时外键判断
        dPatientDetail = \
            patients_models.DPatientDetail.objects.filter(pk=rPatientDrugInformation_object.patient_session_id)[0]
        dScales = scales_models.DScales.objects.filter(pk=rPatientDrugInformation_object.scale_id)[0]
        doctor = users_models.SUser.objects.filter(pk=rPatientDrugInformation_object.doctor_id)[0]
        if dPatientDetail is None or dScales is None or doctor is None:
            object_flag = True
        else:
            object_flag = False
        tools_utils.object_judgment(object_flag)


# patient_detail 表插入前的外键检验
def insert_patient_detail_check(patient_detail_objct):
    # 空值判断
    if patient_detail_objct is None \
            or patient_detail_objct.patient_id is None \
            or patient_detail_objct.doctor_id is None:
        tools_utils.object_judgment(True)
    else:
        # 非空时的外键判断
        doctor = users_models.SUser.objects.filter(pk=patient_detail_objct.doctor_id)[0]
        patient = patients_models.BPatientBaseInfo.objects.filter(pk=patient_detail_objct.patient_id)[0]
        if doctor is None or patient is None:
            object_flag = True
        else:
            object_flag = False
        tools_utils.object_judgment(object_flag)


# base info 表插入前的外键检验
def insert_patient_base_info_check(bPatientBaseInfo_object):
    # 空值判断
    if bPatientBaseInfo_object is None \
            or bPatientBaseInfo_object.doctor_id is None:
        tools_utils.object_judgment(True)
    else:
        # 非空时外键判断
        doctor = users_models.SUser.objects.filter(pk=bPatientBaseInfo_object.doctor_id)[0]
        if doctor is None:
            object_flag = True
        else:
            object_flag = False
        tools_utils.object_judgment(object_flag)


# 汉密尔顿抑郁量表插入前的外键检验
def insert_hamd_check(rPatientHAMD17_object):
    # 空值判断
    if rPatientHAMD17_object is None \
            or rPatientHAMD17_object.patient_session_id is None \
            or rPatientHAMD17_object.scale_id is None \
            or rPatientHAMD17_object.doctor_id is None:
        tools_utils.object_judgment(True)
    else:
        # 非空时外键判断
        dPatientDetail = patients_models.DPatientDetail.objects.filter(pk=rPatientHAMD17_object.patient_session_id)[0]
        dScales = scales_models.DScales.objects.filter(pk=rPatientHAMD17_object.scale_id)[0]
        doctor = users_models.SUser.objects.filter(pk=rPatientHAMD17_object.doctor_id)[0]
        if dPatientDetail is None or dScales is None or doctor is None:
            object_flag = True
        else:
            object_flag = False
        tools_utils.object_judgment(object_flag)


# 33项轻躁狂量表插入前的外键检验
def insert_mainicsymptom_check(rPatientManicsymptom_object):
    # 空值判断
    if rPatientManicsymptom_object is None \
            or rPatientManicsymptom_object.patient_session_id is None \
            or rPatientManicsymptom_object.scale_id is None \
            or rPatientManicsymptom_object.doctor_id is None:
        tools_utils.object_judgment(True)
    else:
        # 非空时外键判断
        dPatientDetail = \
            patients_models.DPatientDetail.objects.filter(pk=rPatientManicsymptom_object.patient_session_id)[0]
        dScales = scales_models.DScales.objects.filter(pk=rPatientManicsymptom_object.scale_id)[0]
        doctor = users_models.SUser.objects.filter(pk=rPatientManicsymptom_object.doctor_id)[0]
        if dPatientDetail is None or dScales is None or doctor is None:
            object_flag = True
        else:
            object_flag = False
        tools_utils.object_judgment(object_flag)


# 斯奈斯和汉密尔顿快乐量表插入前的外键检验
def insert_hapiness_check(rPatienthappiness_object):
    # 空值判断
    if rPatienthappiness_object is None \
            or rPatienthappiness_object.patient_session_id is None \
            or rPatienthappiness_object.scale_id is None \
            or rPatienthappiness_object.doctor_id is None:
        tools_utils.object_judgment(True)
    else:
        # 非空时外键判断
        dPatientDetail = patients_models.DPatientDetail.objects.filter(pk=rPatienthappiness_object.patient_session_id)[
            0]
        dScales = scales_models.DScales.objects.filter(pk=rPatienthappiness_object.scale_id)[0]
        doctor = users_models.SUser.objects.filter(pk=rPatienthappiness_object.doctor_id)[0]
        if dPatientDetail is None or dScales is None or doctor is None:
            object_flag = True
        else:
            object_flag = False
        tools_utils.object_judgment(object_flag)


# 利手量表插入前的外键检验
def insert_handle_check(rPatientChineseHandy_object):
    # 空值判断
    if rPatientChineseHandy_object is None \
            or rPatientChineseHandy_object.patient_session_id is None \
            or rPatientChineseHandy_object.scale_id is None \
            or rPatientChineseHandy_object.doctor_id is None:
        tools_utils.object_judgment(True)
    else:
        # 非空时外键判断
        dPatientDetail = \
            patients_models.DPatientDetail.objects.filter(pk=rPatientChineseHandy_object.patient_session_id)[0]
        dScales = scales_models.DScales.objects.filter(pk=rPatientChineseHandy_object.scale_id)[0]
        doctor = users_models.SUser.objects.filter(pk=rPatientChineseHandy_object.doctor_id)[0]
        if dPatientDetail is None or dScales is None or doctor is None:
            object_flag = True
        else:
            object_flag = False
        tools_utils.object_judgment(object_flag)


# 一般资料_学习情况插入前的外键检验
def insert_information_study_check(rPatientBasicInformationStudy_object):
    # 空值判断
    if rPatientBasicInformationStudy_object is None \
            or rPatientBasicInformationStudy_object.patient_session_id is None \
            or rPatientBasicInformationStudy_object.scale_id is None \
            or rPatientBasicInformationStudy_object.doctor_id is None:
        tools_utils.object_judgment(True)
    else:
        # 非空时外键判断
        dPatientDetail = \
            patients_models.DPatientDetail.objects.filter(pk=rPatientBasicInformationStudy_object.patient_session_id)[0]
        dScales = scales_models.DScales.objects.filter(pk=rPatientBasicInformationStudy_object.scale_id)[0]
        doctor = users_models.SUser.objects.filter(pk=rPatientBasicInformationStudy_object.doctor_id)[0]
        if dPatientDetail is None or dScales is None or doctor is None:
            object_flag = True
        else:
            object_flag = False
        tools_utils.object_judgment(object_flag)


# 认知情绪调节插入前的外键检验
def insert_cognitive_emotion_check(rPatientCognitiveEmotion_object):
    # 空值判断
    if rPatientCognitiveEmotion_object is None \
            or rPatientCognitiveEmotion_object.patient_session_id is None \
            or rPatientCognitiveEmotion_object.scale_id is None \
            or rPatientCognitiveEmotion_object.doctor_id is None:
        tools_utils.object_judgment(True)
    else:
        # 非空时外键判断
        dPatientDetail = \
            patients_models.DPatientDetail.objects.filter(pk=rPatientCognitiveEmotion_object.patient_session_id)[0]
        dScales = scales_models.DScales.objects.filter(pk=rPatientCognitiveEmotion_object.scale_id)[0]
        doctor = users_models.SUser.objects.filter(pk=rPatientCognitiveEmotion_object.doctor_id)[0]
        if dPatientDetail is None or dScales is None or doctor is None:
            object_flag = True
        else:
            object_flag = False
        tools_utils.object_judgment(object_flag)


# 快感体验能力量表插入前的外键检验
def insert_pleasure_check(rPatientPleasure_object):
    # 空值判断
    if rPatientPleasure_object is None \
            or rPatientPleasure_object.patient_session_id is None \
            or rPatientPleasure_object.scale_id is None \
            or rPatientPleasure_object.doctor_id is None:
        tools_utils.object_judgment(True)
    else:
        # 非空时外键判断
        dPatientDetail = patients_models.DPatientDetail.objects.filter(pk=rPatientPleasure_object.patient_session_id)[0]
        dScales = scales_models.DScales.objects.filter(pk=rPatientPleasure_object.scale_id)[0]
        doctor = users_models.SUser.objects.filter(pk=rPatientPleasure_object.doctor_id)[0]
        if dPatientDetail is None or dScales is None or doctor is None:
            object_flag = True
        else:
            object_flag = False
        tools_utils.object_judgment(object_flag)


# 简明精神量表插入前的外键检验
def insert_bprs_check(rPatientbprs_object):
    # 空值判断
    if rPatientbprs_object is None \
            or rPatientbprs_object.patient_session_id is None \
            or rPatientbprs_object.scale_id is None \
            or rPatientbprs_object.doctor_id is None:
        tools_utils.object_judgment(True)
    else:
        # 非空时外键判断
        dPatientDetail = patients_models.DPatientDetail.objects.filter(pk=rPatientbprs_object.patient_session_id)[0]
        dScales = scales_models.DScales.objects.filter(pk=rPatientbprs_object.scale_id)[0]
        doctor = users_models.SUser.objects.filter(pk=rPatientbprs_object.doctor_id)[0]
        if dPatientDetail is None or dScales is None or doctor is None:
            object_flag = True
        else:
            object_flag = False
        tools_utils.object_judgment(object_flag)


# 重复成套性神经心理状态测验结果表
def insert_rbans_check(rPatientrbans_object):
    # 空值判断
    if rPatientrbans_object is None \
            or rPatientrbans_object.patient_session_id is None \
            or rPatientrbans_object.scale_id is None \
            or rPatientrbans_object.doctor_id is None:
        tools_utils.object_judgment(True)
    else:
        # 非空时外键判断
        dPatientDetail = patients_models.DPatientDetail.objects.filter(pk=rPatientrbans_object.patient_session_id)[0]
        dScales = scales_models.DScales.objects.filter(pk=rPatientrbans_object.scale_id)[0]
        doctor = users_models.SUser.objects.filter(pk=rPatientrbans_object.doctor_id)[0]
        if dPatientDetail is None or dScales is None or doctor is None:
            object_flag = True
        else:
            object_flag = False
        tools_utils.object_judgment(object_flag)


# 一般信息_家族及疾病史
def insert_information_health_check(rPatientBasicInformationHealth_object):
    # 空值判断
    if rPatientBasicInformationHealth_object is None \
            or rPatientBasicInformationHealth_object.patient_session_id is None \
            or rPatientBasicInformationHealth_object.scale_id is None \
            or rPatientBasicInformationHealth_object.doctor_id is None:
        tools_utils.object_judgment(True)
    else:
        # 非空时外键判断
        dPatientDetail = \
            patients_models.DPatientDetail.objects.filter(pk=rPatientBasicInformationHealth_object.patient_session_id)[
                0]
        dScales = scales_models.DScales.objects.filter(pk=rPatientBasicInformationHealth_object.scale_id)[0]
        doctor = users_models.SUser.objects.filter(pk=rPatientBasicInformationHealth_object.doctor_id)[0]
        if dPatientDetail is None or dScales is None or doctor is None:
            object_flag = True
        else:
            object_flag = False
        tools_utils.object_judgment(object_flag)


# 汉密尔顿焦虑量表
def insert_hama_check(rPatientHama_object):
    # 空值判断
    if rPatientHama_object is None \
            or rPatientHama_object.patient_session_id is None \
            or rPatientHama_object.scale_id is None \
            or rPatientHama_object.doctor_id is None:
        tools_utils.object_judgment(True)
    else:
        # 非空时外键判断
        dPatientDetail = patients_models.DPatientDetail.objects.filter(pk=rPatientHama_object.patient_session_id)[0]
        dScales = scales_models.DScales.objects.filter(pk=rPatientHama_object.scale_id)[0]
        doctor = users_models.SUser.objects.filter(pk=rPatientHama_object.doctor_id)[0]
        if dPatientDetail is None or dScales is None or doctor is None:
            object_flag = True
        else:
            object_flag = False
        tools_utils.object_judgment(object_flag)

# 蒙哥马利抑郁评定量表（MADRS）
def insert_madrs_check(rPatientMadrs_object):
    if rPatientMadrs_object is None \
        or rPatientMadrs_object.patient_session_id is None \
        or rPatientMadrs_object.scale_id is None \
        or rPatientMadrs_object.doctor_id is None:
        tools_utils.object_judgment(True)
    else:
        # 非空时外键判断
        dPatientDetail = patients_models.DPatientDetail.objects.filter(pk=rPatientMadrs_object.patient_session_id)[0]
        dScales = scales_models.DScales.objects.filter(pk=rPatientMadrs_object.scale_id)[0]
        doctor = users_models.SUser.objects.filter(pk=rPatientMadrs_object.doctor_id)[0]
        if dPatientDetail is None or dScales is None or doctor is None:
            object_flag = True
        else:
            object_flag = False
        tools_utils.object_judgment(object_flag)


# 临床疗效总评量表（CGI）
def insert_cgi_check(rPatientCgi_object):
    if rPatientCgi_object is None \
        or rPatientCgi_object.patient_session_id is None \
        or rPatientCgi_object.scale_id is None \
        or rPatientCgi_object.doctor_id is None:
        tools_utils.object_judgment(True)
    else:
        # 非空时外键判断
        dPatientDetail = patients_models.DPatientDetail.objects.filter(pk=rPatientCgi_object.patient_session_id)[0]
        dScales = scales_models.DScales.objects.filter(pk=rPatientCgi_object.scale_id)[0]
        doctor = users_models.SUser.objects.filter(pk=rPatientCgi_object.doctor_id)[0]
        if dPatientDetail is None or dScales is None or doctor is None:
            object_flag = True
        else:
            object_flag = False
        tools_utils.object_judgment(object_flag)



# 一般资料_物质依赖
def insert_information_abuse_check(rPatientBasicInformationAbuse_object):
    # 空值判断
    if rPatientBasicInformationAbuse_object is None \
            or rPatientBasicInformationAbuse_object.patient_session_id is None \
            or rPatientBasicInformationAbuse_object.scale_id is None \
            or rPatientBasicInformationAbuse_object.doctor_id is None:
        tools_utils.object_judgment(True)
    else:
        # 非空时外键判断
        dPatientDetail = \
            patients_models.DPatientDetail.objects.filter(pk=rPatientBasicInformationAbuse_object.patient_session_id)[0]
        dScales = scales_models.DScales.objects.filter(pk=rPatientBasicInformationAbuse_object.scale_id)[0]
        doctor = users_models.SUser.objects.filter(pk=rPatientBasicInformationAbuse_object.doctor_id)[0]
        if dPatientDetail is None or dScales is None or doctor is None:
            object_flag = True
        else:
            object_flag = False
        tools_utils.object_judgment(object_flag)


# 儿童成长经历
def insert_growth_check(rPatientGrowth_object):
    # 空值判断
    if rPatientGrowth_object is None \
            or rPatientGrowth_object.patient_session_id is None \
            or rPatientGrowth_object.scale_id is None \
            or rPatientGrowth_object.doctor_id is None:
        tools_utils.object_judgment(True)
    else:
        # 非空时外键判断
        dPatientDetail = patients_models.DPatientDetail.objects.filter(pk=rPatientGrowth_object.patient_session_id)[0]
        dScales = scales_models.DScales.objects.filter(pk=rPatientGrowth_object.scale_id)[0]
        doctor = users_models.SUser.objects.filter(pk=rPatientGrowth_object.doctor_id)[0]
        if dPatientDetail is None or dScales is None or doctor is None:
            object_flag = True
        else:
            object_flag = False
        tools_utils.object_judgment(object_flag)


# 青少年生活事件量表
def insert_adolescnet_event_check(rPatientAdolescentEvents_object):
    # 空值判断
    if rPatientAdolescentEvents_object is None \
            or rPatientAdolescentEvents_object.patient_session_id is None \
            or rPatientAdolescentEvents_object.scale_id is None \
            or rPatientAdolescentEvents_object.doctor_id is None:
        tools_utils.object_judgment(True)
    else:
        # 非空时外键判断
        dPatientDetail = \
            patients_models.DPatientDetail.objects.filter(pk=rPatientAdolescentEvents_object.patient_session_id)[0]
        dScales = scales_models.DScales.objects.filter(pk=rPatientAdolescentEvents_object.scale_id)[0]
        doctor = users_models.SUser.objects.filter(pk=rPatientAdolescentEvents_object.doctor_id)[0]
        if dPatientDetail is None or dScales is None or doctor is None:
            object_flag = True
        else:
            object_flag = False
        tools_utils.object_judgment(object_flag)


# 面孔情绪感知能力测试
def insert_fept_check(rPatientFept_object):
    # 空值判断
    if rPatientFept_object is None \
            or rPatientFept_object.patient_session_id is None \
            or rPatientFept_object.scale_id is None \
            or rPatientFept_object.doctor_id is None:
        tools_utils.object_judgment(True)
    else:
        # 非空时外键判断
        dPatientDetail = patients_models.DPatientDetail.objects.filter(pk=rPatientFept_object.patient_session_id)[0]
        dScales = scales_models.DScales.objects.filter(pk=rPatientFept_object.scale_id)[0]
        doctor = users_models.SUser.objects.filter(pk=rPatientFept_object.doctor_id)[0]
        if dPatientDetail is None or dScales is None or doctor is None:
            object_flag = True
        else:
            object_flag = False
        tools_utils.object_judgment(object_flag)


# 音频情绪感知能力测试
def insert_vept_check(rPatientVept_object):
    # 空值判断
    if rPatientVept_object is None \
            or rPatientVept_object.patient_session_id is None \
            or rPatientVept_object.scale_id is None \
            or rPatientVept_object.doctor_id is None:
        tools_utils.object_judgment(True)
    else:
        # 非空时外键判断
        dPatientDetail = patients_models.DPatientDetail.objects.filter(pk=rPatientVept_object.patient_session_id)[0]
        dScales = scales_models.DScales.objects.filter(pk=rPatientVept_object.scale_id)[0]
        doctor = users_models.SUser.objects.filter(pk=rPatientVept_object.doctor_id)[0]
        if dPatientDetail is None or dScales is None or doctor is None:
            object_flag = True
        else:
            object_flag = False
        tools_utils.object_judgment(object_flag)


# 杨氏躁狂量表
def insert_ymrs_check(rPatientYmrs_object):
    # 空值判断
    if rPatientYmrs_object is None \
            or rPatientYmrs_object.patient_session_id is None \
            or rPatientYmrs_object.scale_id is None \
            or rPatientYmrs_object.doctor_id is None:
        tools_utils.object_judgment(True)
    else:
        # 非空时外键判断
        dPatientDetail = patients_models.DPatientDetail.objects.filter(pk=rPatientYmrs_object.patient_session_id)[0]
        dScales = scales_models.DScales.objects.filter(pk=rPatientYmrs_object.scale_id)[0]
        doctor = users_models.SUser.objects.filter(pk=rPatientYmrs_object.doctor_id)[0]
        if dPatientDetail is None or dScales is None or doctor is None:
            object_flag = True
        else:
            object_flag = False
        tools_utils.object_judgment(object_flag)


# 简式父母养育方式问卷表
def insert_sembu_check(rPatientSembu_object):
    # 空值判断
    if rPatientSembu_object is None \
            or rPatientSembu_object.patient_session_id is None \
            or rPatientSembu_object.scale_id is None \
            or rPatientSembu_object.doctor_id is None:
        tools_utils.object_judgment(True)
    else:
        # 非空时外键判断
        dPatientDetail = patients_models.DPatientDetail.objects.filter(pk=rPatientSembu_object.patient_session_id)[0]
        dScales = scales_models.DScales.objects.filter(pk=rPatientSembu_object.scale_id)[0]
        doctor = users_models.SUser.objects.filter(pk=rPatientSembu_object.doctor_id)[0]
        if dPatientDetail is None or dScales is None or doctor is None:
            object_flag = True
        else:
            object_flag = False
        tools_utils.object_judgment(object_flag)


# 一般学习_家庭信息
def insert_information_family_check(patient_basic_info_family_object):
    # 空值判断
    if patient_basic_info_family_object is None \
            or patient_basic_info_family_object.patient_session_id is None \
            or patient_basic_info_family_object.scale_id is None \
            or patient_basic_info_family_object.doctor_id is None:
        tools_utils.object_judgment(True)
    else:
        # 非空时外键判断
        dPatientDetail = \
            patients_models.DPatientDetail.objects.filter(pk=patient_basic_info_family_object.patient_session_id)[0]
        dScales = scales_models.DScales.objects.filter(pk=patient_basic_info_family_object.scale_id)[0]
        doctor = users_models.SUser.objects.filter(pk=patient_basic_info_family_object.doctor_id)[0]
        if dPatientDetail is None or dScales is None or doctor is None:
            object_flag = True
        else:
            object_flag = False
        tools_utils.object_judgment(object_flag)


# 自杀量表
def insert_suicide_check(rpatientsuicidal_object):
    # 空值判断
    if rpatientsuicidal_object is None \
            or rpatientsuicidal_object.patient_session_id is None \
            or rpatientsuicidal_object.scale_id is None \
            or rpatientsuicidal_object.doctor_id is None:
        tools_utils.object_judgment(True)
    else:
        # 非空时外键判断
        dPatientDetail = patients_models.DPatientDetail.objects.filter(pk=rpatientsuicidal_object.patient_session_id)[0]
        dScales = scales_models.DScales.objects.filter(pk=rpatientsuicidal_object.scale_id)[0]
        doctor = users_models.SUser.objects.filter(pk=rpatientsuicidal_object.doctor_id)[0]
        if dPatientDetail is None or dScales is None or doctor is None:
            object_flag = True
        else:
            object_flag = False
        tools_utils.object_judgment(object_flag)


# 耶鲁布朗
def insert_YBO_check(rpatientybobsessiontable_object):
    # 空值判断
    if rpatientybobsessiontable_object is None \
            or rpatientybobsessiontable_object.patient_session_id is None \
            or rpatientybobsessiontable_object.scale_id is None \
            or rpatientybobsessiontable_object.doctor_id is None:
        tools_utils.object_judgment(True)
    else:
        # 非空时外键判断
        dPatientDetail = \
            patients_models.DPatientDetail.objects.filter(pk=rpatientybobsessiontable_object.patient_session_id)[0]
        dScales = scales_models.DScales.objects.filter(pk=rpatientybobsessiontable_object.scale_id)[0]
        doctor = users_models.SUser.objects.filter(pk=rpatientybobsessiontable_object.doctor_id)[0]
        if dPatientDetail is None or dScales is None or doctor is None:
            object_flag = True
        else:
            object_flag = False
        tools_utils.object_judgment(object_flag)


# 自动思维问卷
def insert_ATQ_check(rPatientAtq_object):
    # 空值判断
    if rPatientAtq_object is None \
            or rPatientAtq_object.patient_session_id is None \
            or rPatientAtq_object.scale_id is None \
            or rPatientAtq_object.doctor_id is None:
        tools_utils.object_judgment(True)
    else:
        # 非空时外键判断
        dPatientDetail = patients_models.DPatientDetail.objects.filter(pk=rPatientAtq_object.patient_session_id)[0]
        dScales = scales_models.DScales.objects.filter(pk=rPatientAtq_object.scale_id)[0]
        doctor = users_models.SUser.objects.filter(pk=rPatientAtq_object.doctor_id)[0]
        if dPatientDetail is None or dScales is None or doctor is None:
            object_flag = True
        else:
            object_flag = False
        tools_utils.object_judgment(object_flag)


# 一般资料_其他信息
def insert_information_other_check(rPatientBasicInformationOther_object):
    # 空值判断
    if rPatientBasicInformationOther_object is None \
            or rPatientBasicInformationOther_object.patient_session_id is None \
            or rPatientBasicInformationOther_object.scale_id is None \
            or rPatientBasicInformationOther_object.doctor_id is None:
        tools_utils.object_judgment(True)
    else:
        # 非空时外键判断
        dPatientDetail = \
            patients_models.DPatientDetail.objects.filter(pk=rPatientBasicInformationOther_object.patient_session_id)[0]
        dScales = scales_models.DScales.objects.filter(pk=rPatientBasicInformationOther_object.scale_id)[0]
        doctor = users_models.SUser.objects.filter(pk=rPatientBasicInformationOther_object.doctor_id)[0]
        if dPatientDetail is None or dScales is None or doctor is None:
            object_flag = True
        else:
            object_flag = False
        tools_utils.object_judgment(object_flag)


# 威斯康星
def insert_wcst_check(rPatientWcst_object):
    tools_utils.object_judgment(False)


def insert_Pss_check(rPatientPss_object):
    # 空值判断
    if rPatientPss_object is None \
            or rPatientPss_object.patient_session_id is None \
            or rPatientPss_object.scale_id is None \
            or rPatientPss_object.doctor_id is None:
        tools_utils.object_judgment(True)
    else:
        # 非空时外键判断
        dPatientDetail = patients_models.DPatientDetail.objects.filter(pk=rPatientPss_object.patient_session_id)[0]
        dScales = scales_models.DScales.objects.filter(pk=rPatientPss_object.scale_id)[0]
        doctor = users_models.SUser.objects.filter(pk=rPatientPss_object.doctor_id)[0]
        if dPatientDetail is None or dScales is None or doctor is None:
            object_flag = True
        else:
            object_flag = False
        tools_utils.object_judgment(object_flag)

def insert_Insomnia_check(rPatientInsomnia_object):
    # 空值判断
    if rPatientInsomnia_object is None \
            or rPatientInsomnia_object.patient_session_id is None \
            or rPatientInsomnia_object.scale_id is None \
            or rPatientInsomnia_object.doctor_id is None:
        tools_utils.object_judgment(True)
    else:
        # 非空时外键判断
        dPatientDetail = patients_models.DPatientDetail.objects.filter(pk=rPatientInsomnia_object.patient_session_id)[0]
        dScales = scales_models.DScales.objects.filter(pk=rPatientInsomnia_object.scale_id)[0]
        doctor = users_models.SUser.objects.filter(pk=rPatientInsomnia_object.doctor_id)[0]
        if dPatientDetail is None or dScales is None or doctor is None:
            object_flag = True
        else:
            object_flag = False
        tools_utils.object_judgment(object_flag)

def insert_Gad_check(rPatientGad_object):
    # 空值判断
    if rPatientGad_object is None \
            or rPatientGad_object.patient_session_id is None \
            or rPatientGad_object.scale_id is None \
            or rPatientGad_object.doctor_id is None:
        tools_utils.object_judgment(True)
    else:
        # 非空时外键判断
        dPatientDetail = patients_models.DPatientDetail.objects.filter(pk=rPatientGad_object.patient_session_id)[0]
        dScales = scales_models.DScales.objects.filter(pk=rPatientGad_object.scale_id)[0]
        doctor = users_models.SUser.objects.filter(pk=rPatientGad_object.doctor_id)[0]
        if dPatientDetail is None or dScales is None or doctor is None:
            object_flag = True
        else:
            object_flag = False
        tools_utils.object_judgment(object_flag)


def insert_Phq_check(rPatientPhq_object):
    # 空值判断
    if rPatientPhq_object is None \
            or rPatientPhq_object.patient_session_id is None \
            or rPatientPhq_object.scale_id is None \
            or rPatientPhq_object.doctor_id is None:
        tools_utils.object_judgment(True)
    else:
        # 非空时外键判断
        dPatientDetail = patients_models.DPatientDetail.objects.filter(pk=rPatientPhq_object.patient_session_id)[0]
        dScales = scales_models.DScales.objects.filter(pk=rPatientPhq_object.scale_id)[0]
        doctor = users_models.SUser.objects.filter(pk=rPatientPhq_object.doctor_id)[0]
        if dPatientDetail is None or dScales is None or doctor is None:
            object_flag = True
        else:
            object_flag = False
        tools_utils.object_judgment(object_flag)

def insert_suibe_check(rPatientSuicideBehavior_object):
    # 空值判断
    if rPatientSuicideBehavior_object is None \
            or rPatientSuicideBehavior_object.patient_session_id is None \
            or rPatientSuicideBehavior_object.scale_id is None \
            or rPatientSuicideBehavior_object.doctor_id is None:
        tools_utils.object_judgment(True)
    else:
        # 非空时外键判断
        dPatientDetail = patients_models.DPatientDetail.objects.filter(pk=rPatientSuicideBehavior_object.patient_session_id)[0]
        dScales = scales_models.DScales.objects.filter(pk=rPatientSuicideBehavior_object.scale_id)[0]
        doctor = users_models.SUser.objects.filter(pk=rPatientSuicideBehavior_object.doctor_id)[0]
        if dPatientDetail is None or dScales is None or doctor is None:
            object_flag = True
        else:
            object_flag = False
        tools_utils.object_judgment(object_flag)