import time

from django.shortcuts import render, redirect
import json
import tools.insertCascadeCheck as tools_insertCascadeCheck
import tools.calculatingScores as tools_calculatingScores
import scales.config as config
import tools.Utils as tools_utils
import scales.models as scales_models
import patients.models as patient_models
import tools.config as tools_config
import patients.dao as patients_dao


################### 自定义update方法 ####################
################### 自定义update方法 ####################
################### 自定义update方法 ####################

# 这里不能使用update方法，django中使用自带update方法无法更新带有auto_now的时间字段
# 更新r_patient_scales中的state状态
def update_rscales_state(patient_session_id, scale_id, state):
    rPatientScales = \
        scales_models.RPatientScales.objects.filter(patient_session_id=patient_session_id, scale_id=scale_id)[0]
    rPatientScales.state = state
    rPatientScales.save()


def update_rscales_skip(patient_session_id, scale_id, state):
    rPatientScales = \
        scales_models.RPatientScales.objects.filter(patient_session_id=patient_session_id, scale_id=scale_id)[0]
    rPatientScales.state = state
    rPatientScales.save()


################### insert方法部分 #####################
################### insert方法部分 #####################
################### insert方法部分 #####################
################### insert方法部分 #####################


#######################################################################################
########################## add_hamd_database 可以作为dao的样例 #########################
#######################################################################################

# 病人病史表
def add_medical_history(rPatientMedicalHistory, state):
    # 插入前的级联检验
    # 存入数据库
    rPatientMedicalHistory.save()
    update_rscales_state(rPatientMedicalHistory.patient_session_id, rPatientMedicalHistory.scale_id, state)


def add_drugs_information(rPatientDrugsInformation):
    rPatientDrugsInformation.save()


# 汉密尔顿焦虑量表
def add_hamd_database(rPatientHAMD17, state):
    # 计算量表得分
    rPatientHAMD17.total_score, object_flag = tools_calculatingScores.HAMD17_total_score(rPatientHAMD17)
    # 量表得分检验
    tools_utils.object_judgment(object_flag)
    # 插入前的级联检验
    tools_insertCascadeCheck.insert_hama_check(rPatientHAMD17)
    # 插入数据库
    rPatientHAMD17.save()
    # 修改r_patient_scales表中state状态
    update_rscales_state(rPatientHAMD17.patient_session_id, rPatientHAMD17.scale_id, state)


# 33 项轻躁狂症状清单
def add_manicsymptom_database(rPatientManicsymptom, state):
    # 存进数据库
    rPatientManicsymptom.total_score, object_flag = tools_calculatingScores.ManicSymptom_total_score(
        rPatientManicsymptom)
    tools_utils.object_judgment(object_flag)
    # 插入前的级联检验
    tools_insertCascadeCheck.insert_mainicsymptom_check(rPatientManicsymptom)
    # 插入数据库
    rPatientManicsymptom.save()
    # 修改r_patient_scales表中state状态
    update_rscales_state(rPatientManicsymptom.patient_session_id, rPatientManicsymptom.scale_id, state)


# 斯奈斯和汉密尔顿快乐量表
def add_happiness_database(rPatienthappiness, state):
    # 存进数据库
    rPatienthappiness.total_score, object_flag = tools_calculatingScores.happiness_total_score(rPatienthappiness)
    tools_utils.object_judgment(object_flag)
    # 插入前的级联检验
    tools_insertCascadeCheck.insert_hapiness_check(rPatienthappiness)
    # 插入数据库
    rPatienthappiness.save()
    # 修改r_patient_scales表中state状态
    update_rscales_state(rPatienthappiness.patient_session_id, rPatienthappiness.scale_id, state)


def add_chinesehandle_database(rPatientChineseHandy, state):
    rPatientChineseHandy.result, object_flag = tools_calculatingScores.Handy_total_score(rPatientChineseHandy)
    tools_utils.object_judgment(object_flag)
    # 插入前的级联检验
    tools_insertCascadeCheck.insert_handle_check(rPatientChineseHandy)
    # 插入数据库
    rPatientChineseHandy.save()
    # 修改r_patient_scales表中state状态
    update_rscales_state(rPatientChineseHandy.patient_session_id, rPatientChineseHandy.scale_id, state)
    # 做完利手量表后，也需要修改patient_detail表中的利手状态
    patient_detail = patients_dao.get_patient_detail_byPK(rPatientChineseHandy.patient_session_id)
    patient_detail.handy = rPatientChineseHandy.result
    patients_dao.add_patient_detail(patient_detail)


def add_information_study_database(rPatientBasicInformationStudy, state):
    # 插入前的级联检验
    tools_insertCascadeCheck.insert_information_study_check(rPatientBasicInformationStudy)
    # 插入数据库
    rPatientBasicInformationStudy.save()
    # 修改r_patient_scales表中state状态
    update_rscales_state(rPatientBasicInformationStudy.patient_session_id, rPatientBasicInformationStudy.scale_id,
                         state)


#############################################################################################
#############################################################################################syh


def add_patient_medical_history(rPatientMedicalHistory_object):
    # 插入前的级联检验
    tools_insertCascadeCheck.insert_patient_medical_history_check(rPatientMedicalHistory_object)
    # 插入数据库
    rPatientMedicalHistory_object.save()


def add_patient_drugs_information(rPatientDrugInformation_object):
    # 插入前的级联检验
    tools_insertCascadeCheck.insert_patient_drug_information_check(rPatientDrugInformation_object)
    # 插入数据库
    rPatientDrugInformation_object.save()


def add_cognitive_emotion_database(rPatientCognitiveEmotion, state):
    # 得分计算
    rPatientCognitiveEmotion.total_score, rPatientCognitiveEmotion.blame_self, rPatientCognitiveEmotion.blame_others, rPatientCognitiveEmotion.meditation, \
    rPatientCognitiveEmotion.catastrophization, rPatientCognitiveEmotion.accepted, rPatientCognitiveEmotion.positive_refocus, rPatientCognitiveEmotion.program_refocus, \
    rPatientCognitiveEmotion.positive_evaluation, rPatientCognitiveEmotion.rational_analysis, object_flag \
        = tools_calculatingScores.CognitiveEmotion_total_score(rPatientCognitiveEmotion)

    tools_utils.object_judgment(object_flag)
    # 插入前的级联检验
    tools_insertCascadeCheck.insert_cognitive_emotion_check(rPatientCognitiveEmotion)
    # 插入数据库
    rPatientCognitiveEmotion.save()
    # 修改r_patient_scales表中state状态
    update_rscales_state(rPatientCognitiveEmotion.patient_session_id, rPatientCognitiveEmotion.scale_id, state)


def add_pleasure_database(rPatientPleasure, state):
    rPatientPleasure.expectation_score, rPatientPleasure.consume_score, object_flag = tools_calculatingScores.pleasure_total_score(
        rPatientPleasure)
    if rPatientPleasure.expectation_score is not None and rPatientPleasure.consume_score is not None:
        rPatientPleasure.total_score = rPatientPleasure.expectation_score + rPatientPleasure.consume_score
        tools_utils.object_judgment(object_flag)
    else:
        tools_utils.object_judgment(True)
    # 插入前的级联检验
    tools_insertCascadeCheck.insert_pleasure_check(rPatientPleasure)
    # 插入数据库
    rPatientPleasure.save()
    # 修改r_patient_scales表中state状态
    update_rscales_state(rPatientPleasure.patient_session_id, rPatientPleasure.scale_id, state)


def add_bprs_database(rPatientbprs, state):
    rPatientbprs.total_score, object_flag = tools_calculatingScores.Bprs_total_score(rPatientbprs)
    tools_utils.object_judgment(object_flag)
    # 插入前的级联检验
    tools_insertCascadeCheck.insert_bprs_check(rPatientbprs)
    # 插入数据库
    rPatientbprs.save()
    # 修改r_patient_scales表中state状态
    update_rscales_state(rPatientbprs.patient_session_id, rPatientbprs.scale_id, state)


def add_rbans_database(rPatientrbans, state):
    # 插入前的级联检验
    tools_insertCascadeCheck.insert_rbans_check(rPatientrbans)
    # 插入数据库
    rPatientrbans.save()
    # 修改r_patient_scales表中state状态
    update_rscales_state(rPatientrbans.patient_session_id, rPatientrbans.scale_id, state)


def add_patient_basic_information_health_database(rPatientBasicInformationHealth, state):
    # 插入前的级联检验
    tools_insertCascadeCheck.insert_information_health_check(rPatientBasicInformationHealth)
    # 插入数据库
    rPatientBasicInformationHealth.save()
    # 修改r_patient_scales表中state状态
    update_rscales_state(rPatientBasicInformationHealth.patient_session_id, rPatientBasicInformationHealth.scale_id,
                         state)


#############################################################################################syh
############################################################
# zrq------------------------------------

def add_hama_database(rPatientHama, state):
    rPatientHama.total_score, object_flag = tools_calculatingScores.HAMA_total_score(rPatientHama)
    tools_utils.object_judgment(object_flag)
    # 插入前的级联检验
    tools_insertCascadeCheck.insert_hama_check(rPatientHama)
    # 插入数据库
    rPatientHama.save()
    # 修改r_patient_scales表中state状态
    update_rscales_state(rPatientHama.patient_session_id, rPatientHama.scale_id, state)


def add_abuse_database(rPatientBasicInformationAbuse, state):
    # 插入前的级联检验
    tools_insertCascadeCheck.insert_information_abuse_check(rPatientBasicInformationAbuse)
    # 插入数据库
    rPatientBasicInformationAbuse.save()
    # 修改r_patient_scales表中state状态
    update_rscales_state(rPatientBasicInformationAbuse.patient_session_id, rPatientBasicInformationAbuse.scale_id,
                         state)


def add_growth_database(rPatientGrowth, state):
    rPatientGrowth.emotion_abuse_score, rPatientGrowth.body_abuse_score, rPatientGrowth.sex_abuse_score, rPatientGrowth.emotion_ignore_score, \
    rPatientGrowth.body_ignore_score, object_flag = tools_calculatingScores.growth_total_score(rPatientGrowth)
    tools_utils.object_judgment(object_flag)
    # 插入前的级联检验
    tools_insertCascadeCheck.insert_growth_check(rPatientGrowth)
    # 插入数据库
    rPatientGrowth.save()
    # 修改r_patient_scales表中state状态
    update_rscales_state(rPatientGrowth.patient_session_id, rPatientGrowth.scale_id, state)


def add_adolescent_events_database(rPatientAdolescentEvents, state):
    rPatientAdolescentEvents.total_score, object_flag = tools_calculatingScores.AdolescentEvents_total_score(
        rPatientAdolescentEvents)
    tools_utils.object_judgment(object_flag)
    # 插入前的级联检验
    tools_insertCascadeCheck.insert_adolescnet_event_check(rPatientAdolescentEvents)
    # 插入数据库
    rPatientAdolescentEvents.save()
    # 修改r_patient_scales表中state状态
    update_rscales_state(rPatientAdolescentEvents.patient_session_id, rPatientAdolescentEvents.scale_id, state)


# 这里的total_score需要从前台获取，认知的所有表都需要手动填总分 面孔情绪感知
def add_fept_database(rPatientFept, state):
    # 存进数据库
    # 插入前的级联检验
    tools_insertCascadeCheck.insert_fept_check(rPatientFept)
    # 插入数据库
    rPatientFept.save()
    # 修改r_patient_scales表中state状态
    update_rscales_state(rPatientFept.patient_session_id, rPatientFept.scale_id, state)


# 这里的total_score需要从前台或许，认知的所有表都需要手动填总分 语音情绪感知
def add_vept_database(rPatientVept, state):
    # 存进数据库
    # 插入前的级联检验
    tools_insertCascadeCheck.insert_vept_check(rPatientVept)
    # 插入数据库
    rPatientVept.save()
    # 修改r_patient_scales表中state状态
    update_rscales_state(rPatientVept.patient_session_id, rPatientVept.scale_id, state)


###################################

def add_ymrs_database(rPatientYmrs, state):
    rPatientYmrs.total_score, object_flag = tools_calculatingScores.YMRS_total_score(rPatientYmrs)
    tools_utils.object_judgment(object_flag)
    # 插入前的级联检验
    tools_insertCascadeCheck.insert_ymrs_check(rPatientYmrs)
    # 插入数据库
    rPatientYmrs.save()
    # 修改r_patient_scales表中state状态
    update_rscales_state(rPatientYmrs.patient_session_id, rPatientYmrs.scale_id, state)


def add_sembu_database(rPatientSembu, state):
    rPatientSembu.refusal_mother, rPatientSembu.refusal_father, rPatientSembu.emotional_warmth_mother, \
    rPatientSembu.emotional_warmth_father, rPatientSembu.overprotection_mother, rPatientSembu.overprotection_father, \
    object_flag = tools_calculatingScores.SEmbu_total_score(rPatientSembu)

    tools_utils.object_judgment(object_flag)
    # 插入前的级联检验
    tools_insertCascadeCheck.insert_sembu_check(rPatientSembu)
    # 插入数据库
    rPatientSembu.save()
    # 修改r_patient_scales表中state状态
    update_rscales_state(rPatientSembu.patient_session_id, rPatientSembu.scale_id, state)


def dao_add_family_info(patient_basic_info_family, state):
    # 插入前的级联检验
    tools_insertCascadeCheck.insert_information_family_check(patient_basic_info_family)
    # 插入数据库
    patient_basic_info_family.save()
    # 修改r_patient_scales表中state状态
    update_rscales_state(patient_basic_info_family.patient_session_id, patient_basic_info_family.scale_id, state)


def dao_add_suicide(rpatientsuicidal, state):
    # 计算总分
    rpatientsuicidal.total_score_lastweek, rpatientsuicidal.total_score_mostdepressed, object_flag, rpatientsuicidal.suicide_ideation = tools_calculatingScores.Suicidal_total_score(
        rpatientsuicidal)
    tools_utils.object_judgment(object_flag)
    # 插入前的级联检验
    tools_insertCascadeCheck.insert_suicide_check(rpatientsuicidal)
    # 插入数据库
    rpatientsuicidal.save()
    # 修改r_patient_scales表中state状态
    update_rscales_state(rpatientsuicidal.patient_session_id, rpatientsuicidal.scale_id, state)


def dao_add_ybo(rpatientybobsessiontable, state):
    # 计算总分的函数写在这
    rpatientybobsessiontable.total_score, object_flag = tools_calculatingScores.YBO_total_score(
        rpatientybobsessiontable)
    tools_utils.object_judgment(object_flag)
    # 插入前的级联检验
    tools_insertCascadeCheck.insert_YBO_check(rpatientybobsessiontable)
    # 插入数据库
    rpatientybobsessiontable.save()
    # 修改r_patient_scales表中state状态
    update_rscales_state(rpatientybobsessiontable.patient_session_id, rpatientybobsessiontable.scale_id, state)


def add_atq_database(rPatientAtq, state):
    rPatientAtq.total_score, object_flag = tools_calculatingScores.ATQ_total_score(rPatientAtq)
    tools_utils.object_judgment(object_flag)
    # 插入前的级联检验
    tools_insertCascadeCheck.insert_ATQ_check(rPatientAtq)
    # 插入数据库
    rPatientAtq.save()
    # 修改r_patient_scales表中state状态
    update_rscales_state(rPatientAtq.patient_session_id, rPatientAtq.scale_id, state)


def add_pss_database(rPatientPss, state):
    rPatientPss.total_score = tools_calculatingScores.PSS_total_score(rPatientPss)
    # tools_utils.object_judgment(object_flag)
    # 插入前的级联检验
    tools_insertCascadeCheck.insert_Pss_check(rPatientPss)
    # 插入数据库
    rPatientPss.save()
    # 修改r_patient_scales表中state状态
    update_rscales_state(rPatientPss.patient_session_id, rPatientPss.scale_id, state)


def add_Insomnia_database(rPatientInsomnia, state):
    rPatientInsomnia.total_score = tools_calculatingScores.ISI_total_score(rPatientInsomnia)
    # tools_utils.object_judgment(object_flag)
    # 插入前的级联检验
    tools_insertCascadeCheck.insert_Insomnia_check(rPatientInsomnia)
    # 插入数据库
    rPatientInsomnia.save()
    # 修改r_patient_scales表中state状态
    update_rscales_state(rPatientInsomnia.patient_session_id, rPatientInsomnia.scale_id, state)


def add_Gad_database(rPatientGad, state):
    rPatientGad.total_score = tools_calculatingScores.GAD_total_score(rPatientGad)
    # tools_utils.object_judgment(object_flag)
    # 插入前的级联检验
    tools_insertCascadeCheck.insert_Gad_check(rPatientGad)
    # 插入数据库
    rPatientGad.save()
    # 修改r_patient_scales表中state状态
    update_rscales_state(rPatientGad.patient_session_id, rPatientGad.scale_id, state)


def add_Phq_database(rPatientPhq, state):
    rPatientPhq.total_score = tools_calculatingScores.PHQ_total_score(rPatientPhq)
    # tools_utils.object_judgment(object_flag)
    # 插入前的级联检验
    tools_insertCascadeCheck.insert_Phq_check(rPatientPhq)
    # 插入数据库
    rPatientPhq.save()
    # 修改r_patient_scales表中state状态
    update_rscales_state(rPatientPhq.patient_session_id, rPatientPhq.scale_id, state)


def add_wcst_database(rPatientWcst, state):
    # 插入前的级联检验
    tools_insertCascadeCheck.insert_wcst_check(rPatientWcst)
    # 插入数据库
    rPatientWcst.save()
    # 修改r_patient_scales表中state状态
    update_rscales_state(rPatientWcst.patient_session_id, rPatientWcst.scale_id, state)


def add_other_database(rPatientBasicInformationOther, state):
    # 插入前的级联检验
    tools_insertCascadeCheck.insert_information_other_check(rPatientBasicInformationOther)
    # 插入数据库
    rPatientBasicInformationOther.save()
    # 修改r_patient_scales表中state状态
    update_rscales_state(rPatientBasicInformationOther.patient_session_id, rPatientBasicInformationOther.scale_id,
                         state)


################### get方法部分 #####################
################### get方法部分 #####################
################### get方法部分 #####################
################### get方法部分 #####################

# r_patient_medical_history 表
def get_patient_medical_history_byPatientId(patient_detail_id):
    patient_medical_history = scales_models.RPatientMedicalHistory.objects.filter(patient_session=patient_detail_id)
    if patient_medical_history.count() == 0:
        return None
    else:
        return patient_medical_history[0]


# r_patient_drugs_information 表
def get_patient_drugs_information_byPatientId(patient_detail_id):
    historical_drugs_information_list = scales_models.RPatientDrugsInformation.objects.all().filter(
        patient_session=patient_detail_id, type='0')
    scanning_drugs_information_list = scales_models.RPatientDrugsInformation.objects.all().filter(
        patient_session=patient_detail_id, type='1')
    historical_drugs_information_num = scales_models.RPatientDrugsInformation.objects.all().filter(
        patient_session=patient_detail_id, type='0').count()
    scanning_drugs_information_num = scales_models.RPatientDrugsInformation.objects.all().filter(
        patient_session=patient_detail_id, type='1').count()
    return historical_drugs_information_list, scanning_drugs_information_list, historical_drugs_information_num, scanning_drugs_information_num


# patient base info 表
def get_patient_base_info_family_byPatientDetailId(patient_detail_id):
    patient_base_info_family = scales_models.RPatientBasicInformationFamily.objects.filter(
        patient_session=patient_detail_id)
    if patient_base_info_family.count() == 0:
        return None
    else:
        return patient_base_info_family[0]


def get_patient_base_info_study_byPatientDetailId(patient_detail_id):
    patient_base_info_study = scales_models.RPatientBasicInformationStudy.objects.filter(
        patient_session=patient_detail_id)
    if patient_base_info_study.count() == 0:
        return None
    else:
        return patient_base_info_study[0]


def get_patient_base_info_health_byPatientDetailId(patient_detail_id):
    patient_base_info_health = scales_models.RPatientBasicInformationHealth.objects.filter(
        patient_session=patient_detail_id)
    if patient_base_info_health.count() == 0:
        return None
    else:
        return patient_base_info_health[0]


def get_patient_base_info_abuse_byPatientDetailId(patient_detail_id):
    patient_base_info_abuse = scales_models.RPatientBasicInformationAbuse.objects.filter(
        patient_session=patient_detail_id)
    if patient_base_info_abuse.count() == 0:
        return None
    else:
        return patient_base_info_abuse[0]


def get_patient_base_info_other_byPatientDetailId(patient_detail_id):
    patient_base_info_other = scales_models.RPatientBasicInformationOther.objects.filter(
        patient_session=patient_detail_id)
    if patient_base_info_other.count() == 0:
        return None
    else:
        return patient_base_info_other[0]


# 中国人利手量表
def get_patient_handy_byPatientDetailId(patient_detail_id):
    patient_handy = scales_models.RPatientChineseHandy.objects.filter(patient_session=patient_detail_id)
    if patient_handy.count() == 0:
        return None
    else:
        return patient_handy[0]


# 汉密尔顿抑郁量表HAMD17
def get_patient_HAMD17_byPatientDetailId(patient_detail_id):
    patient_HAMD17 = scales_models.RPatientHamd17.objects.filter(patient_session=patient_detail_id)
    if patient_HAMD17.count() == 0:
        return None
    else:
        return patient_HAMD17[0]


# 汉密尔顿焦虑量表HAMA
def get_patient_HAMA_byPatientDetailId(patient_detail_id):
    patient_HAMA = scales_models.RPatientHama.objects.filter(patient_session=patient_detail_id)
    if patient_HAMA.count() == 0:
        return None
    else:
        return patient_HAMA[0]


# 杨氏躁狂量表YMRS
def get_patient_YMRS_byPatientDetailId(patient_detail_id):
    patient_YMRS = scales_models.RPatientYmrs.objects.filter(patient_session=patient_detail_id)
    if patient_YMRS.count() == 0:
        return None
    else:
        return patient_YMRS[0]


# BPRS简明精神量表
def get_patient_BPRS_byPatientDetailId(patient_detail_id):
    patient_BPRS = scales_models.RPatientBprs.objects.filter(patient_session=patient_detail_id)
    if patient_BPRS.count() == 0:
        return None
    else:
        return patient_BPRS[0]


# 耶鲁布朗
def get_patient_YBO_byPatientDetailId(patient_detail_id):
    patient_YBO = scales_models.RPatientYbobsessiontable.objects.filter(patient_session=patient_detail_id)
    if patient_YBO.count() == 0:
        return None
    else:
        return patient_YBO[0]


# 自杀意念及行为史
def get_patient_suicidal_byPatientDetailId(patient_detail_id):
    patient_suicidal = scales_models.RPatientSuicidal.objects.filter(patient_session=patient_detail_id)
    if patient_suicidal.count() == 0:
        return None
    else:
        return patient_suicidal[0]


# 33项轻躁狂
def get_patient_manicSymptom_byPatientDetailId(patient_detail_id):
    patient_manicSymptom = scales_models.RPatientManicsymptom.objects.filter(patient_session=patient_detail_id)
    if patient_manicSymptom.count() == 0:
        return None
    else:
        return patient_manicSymptom[0]


# 斯奈斯和汉密尔顿快乐
def get_patient_happiness_byPatientDetailId(patient_detail_id):
    patient_happiness = scales_models.RPatientHappiness.objects.filter(patient_session=patient_detail_id)
    if patient_happiness.count() == 0:
        return None
    else:
        return patient_happiness[0]


# 快感体验能力量表
def get_patient_pleasure_byPatientDetailId(patient_detail_id):
    patient_pleasure = scales_models.RPatientPleasure.objects.filter(patient_session=patient_detail_id)
    if patient_pleasure.count() == 0:
        return None
    else:
        return patient_pleasure[0]


# 儿童期（16岁前）成长经历
def get_patient_growth_byPatientDetailId(patient_detail_id):
    patient_growth = scales_models.RPatientGrowth.objects.filter(patient_session=patient_detail_id)
    if patient_growth.count() == 0:
        return None
    else:
        return patient_growth[0]


# 青少年生活事件量表
def get_patient_adolescent_byPatientDetailId(patient_detail_id):
    patient_adolescent = scales_models.RPatientAdolescentEvents.objects.filter(patient_session=patient_detail_id)
    if patient_adolescent.count() == 0:
        return None
    else:
        return patient_adolescent[0]


# 认知情绪调节量表
def get_patient_cognitive_byPatientDetailId(patient_detail_id):
    patient_cognitive = scales_models.RPatientCognitiveEmotion.objects.filter(patient_session=patient_detail_id)
    if patient_cognitive.count() == 0:
        return None
    else:
        return patient_cognitive[0]


# 简式父母养育方式问卷表
def get_patient_SEmbu_byPatientDetailId(patient_detail_id):
    patient_SEmbu = scales_models.RPatientSembu.objects.filter(patient_session=patient_detail_id)
    if patient_SEmbu.count() == 0:
        return None
    else:
        return patient_SEmbu[0]


# 自动思维问卷表
def get_patient_ATQ_byPatientDetailId(patient_detail_id):
    patient_ATQ = scales_models.RPatientAtq.objects.filter(patient_session=patient_detail_id)
    if patient_ATQ.count() == 0:
        return None
    else:
        return patient_ATQ[0]


# PHQ-9
def get_patient_PHQ_9_byPatientDetailId(patient_detail_id):
    patient_PHQ_9 = scales_models.RPatientPhq.objects.filter(patient_session=patient_detail_id)
    if patient_PHQ_9.count() == 0:
        return None
    else:
        return patient_PHQ_9[0]


# GAD_7
def get_patient_GAD_7_byPatientDetailId(patient_detail_id):
    patient_GAD_7 = scales_models.RPatientGad.objects.filter(patient_session=patient_detail_id)
    if patient_GAD_7.count() == 0:
        return None
    else:
        return patient_GAD_7[0]


# 失眠严重指数量表
def get_patient_Insomnia_byPatientDetailId(patient_detail_id):
    patient_insomnia = scales_models.RPatientInsomnia.objects.filter(patient_session=patient_detail_id)
    if patient_insomnia.count() == 0:
        return None
    else:
        return patient_insomnia[0]


# 压力知觉量表
def get_patient_Pss_byPatientDetailId(patient_detail_id):
    patient_Pss = scales_models.RPatientPss.objects.filter(patient_session=patient_detail_id)
    if patient_Pss.count() == 0:
        return None
    else:
        return patient_Pss[0]


# 威斯康星WCST
def get_patient_wcst_byPatientDetailId(patient_detail_id):
    patient_wcst = scales_models.RPatientWcst.objects.filter(patient_session=patient_detail_id)
    if patient_wcst.count() == 0:
        return None
    else:
        return patient_wcst[0]


# 重复成套性神经心理状态测验系统RBANS
def get_patient_rbans_byPatientDetailId(patient_detail_id):
    patient_rbans = scales_models.RPatientRbans.objects.filter(patient_session=patient_detail_id)
    if patient_rbans.count() == 0:
        return None
    else:
        return patient_rbans[0]


# 面孔情绪感知能力测试
def get_patient_fept_byPatientDetailId(patient_detail_id):
    patient_fept = scales_models.RPatientFept.objects.filter(patient_session=patient_detail_id)
    if patient_fept.count() == 0:
        return None
    else:
        return patient_fept[0]


# 语音情绪感知能力测试VEPT
def get_patient_vept_byPatientDetailId(patient_detail_id):
    patient_vept = scales_models.RPatientVept.objects.filter(patient_session=patient_detail_id)
    if patient_vept.count() == 0:
        return None
    else:
        return patient_vept[0]


def get_handy_byPatientDetailId(patient_detail_id):
    patient_handy = scales_models.RPatientChineseHandy.objects.filter(patient_session_id=patient_detail_id)
    if patient_handy.count() == 0:
        return None
    else:
        return patient_handy[0]


# 获取某个类别的量表未完成的最小值,都已经完成了，那么返回None
def get_min_unfinished_scale(do_scale_type, patient_session_id, cur_scale_id):
    res = scales_models.RPatientScales.objects.filter(scale__do_scale_type=do_scale_type,
                                                      patient_session_id=patient_session_id,
                                                      state=0).values("scale_id").order_by('scale_id').first()
    print("next scales")
    print(res)
    if res is None:
        return None
    return res["scale_id"]


def get_scalename_bytype(do_scale_type, patient_session_id):
    res = scales_models.RPatientScales.objects.all().select_related().filter(scale__do_scale_type=do_scale_type,
                                                                             patient_session_id=patient_session_id).values(
        'scale__scale_name', 'state')
    return res


# 获取未完成的scale量表
def get_uodo_scales(patient_session_id):
    scales_list = scales_models.RPatientScales.objects.all().select_related('scale'). \
        filter(patient_session_id=patient_session_id, state=0).values('scale__do_scale_type', 'scale__scale_name')
    information_list = []
    other_test_list = []
    self_test_list = []
    cognition_list = []
    no_type_list = []
    for scale in scales_list:
        if scale['scale__do_scale_type'] == 0:
            information_list.append(scale)
        elif scale['scale__do_scale_type'] == 1:
            other_test_list.append(scale)
        elif scale['scale__do_scale_type'] == 2:
            self_test_list.append(scale)
        elif scale['scale__do_scale_type'] == 3:
            cognition_list.append(scale)
        else:
            no_type_list.append(scale)
    return information_list, other_test_list, self_test_list, cognition_list


# 根据获取量表
def get_scale_by_id(scale_id):
    scale = scales_models.DScales.objects.filter(pk=scale_id)
    if scale.exists():
        return scale[0]
    else:
        return None


def get_scale_by_doscaletype(type):
    res = scales_models.DScales.objects.filter(do_scale_type=type)
    if res.exists():
        return res
    return None


################__________________###################3
# 获取hama填写结果
def get_hama_answer(patient_id):
    hama_list = scales_models.RPatientHama.objects.filter(patient_session_id=patient_id)[0]
    return hama_list


# 获取hamd填写结果
def get_hamd_answer(patient_id):
    hamd_list = scales_models.RPatientHamd17.objects.filter(patient_session_id=patient_id)[0]
    return hamd_list


# 获取ymrs填写结果
def get_ymrs_answer(patient_id):
    ymrs_list = scales_models.RPatientYmrs.objects.filter(patient_session_id=patient_id)[0]
    return ymrs_list


# 获取bprs填写结果
def get_bprs_answer(patient_id):
    bprs_list = scales_models.RPatientBprs.objects.filter(patient_session_id=patient_id)[0]
    return bprs_list


##############__________________________######################
def get_last_scales_detail(patient_session_id, scale_id):
    do_scale_type = scales_models.DScales.objects.filter(id=scale_id)[0].do_scale_type
    scale_queryset = scales_models.RPatientScales.objects.filter(patient_session_id=patient_session_id,
                                                                 scale_id__lt=scale_id).select_related('scale'). \
        filter(scale__do_scale_type=do_scale_type).order_by('-scale_id')
    if not scale_queryset.exists():
        return None
    return scale_queryset[0]


def get_next_scales_detail(patient_session_id, scale_id):
    # 按顺序查找patient_session_id=patient_session_id，大于scale_id
    do_scale_type = scales_models.DScales.objects.filter(id=scale_id)[0].do_scale_type
    scale_queryset = scales_models.RPatientScales.objects.filter(patient_session_id=patient_session_id,
                                                                 scale_id__gt=scale_id).select_related('scale'). \
        filter(scale__do_scale_type=do_scale_type).order_by('scale_id')
    if not scale_queryset.exists():
        return None
    return scale_queryset[0]


def get_order(patient_session_id, scale_id):
    do_scale_type = scales_models.DScales.objects.filter(id=scale_id)[0].do_scale_type
    scales_order = scales_models.RPatientScales.objects.filter(patient_session_id=patient_session_id).select_related(
        'scale'). \
        filter(scale__do_scale_type=do_scale_type).order_by('scale_id')
    invert_scales_order = scales_models.RPatientScales.objects.filter(
        patient_session_id=patient_session_id).select_related('scale'). \
        filter(scale__do_scale_type=do_scale_type).order_by('-scale_id')
    first = scales_order[0].scale_id
    last = invert_scales_order[0].scale_id
    return first, last


def get_scale_state(patient_session_id, scale_id):
    res = scales_models.RPatientScales.objects.filter(patient_session_id=patient_session_id, scale_id=scale_id)
    if not res.exists():
        return None
    return res[0].state


def del_hamd(patient_session_id, scale_id):
    res = scales_models.RPatientHamd17.objects.filter(patient_session_id=patient_session_id, scale_id=scale_id)
    if res.exists():
        res[0].delete()


def del_hama(patient_session_id, scale_id):
    res = scales_models.RPatientHama.objects.filter(patient_session_id=patient_session_id, scale_id=scale_id)
    if res.exists():
        res[0].delete()


def del_bprs(patient_session_id, scale_id):
    res = scales_models.RPatientBprs.objects.filter(patient_session_id=patient_session_id, scale_id=scale_id)
    if res.exists():
        res[0].delete()


def del_ymrs(patient_session_id, scale_id):
    res = scales_models.RPatientYmrs.objects.filter(patient_session_id=patient_session_id, scale_id=scale_id)
    if res.exists():
        res[0].delete()


# =================================================认知==============================


def del_wcst(patient_session_id, scale_id):
    res = scales_models.RPatientWcst.objects.filter(patient_session_id=patient_session_id, scale_id=scale_id)
    if res.exists():
        res[0].delete()


def del_rbans(patient_session_id, scale_id):
    res = scales_models.RPatientRbans.objects.filter(patient_session_id=patient_session_id, scale_id=scale_id)
    if res.exists():
        res[0].delete()


def del_fept(patient_session_id, scale_id):
    res = scales_models.RPatientFept.objects.filter(patient_session_id=patient_session_id, scale_id=scale_id)
    if res.exists():
        res[0].delete()


def del_vept(patient_session_id, scale_id):
    res = scales_models.RPatientVept.objects.filter(patient_session_id=patient_session_id, scale_id=scale_id)
    if res.exists():
        res[0].delete()


'''取量表对象 如果不存在就返回一个'''


def get_or_default_patient_YBO_byPatientDetailId(patient_detail_id, doctor_id):
    print('DAODAODAODAODAODAODAODAODAODAODAODAODAODAODAODAODAODAODAODAODAODAODAODAODAODAODAODAODAODAODAODAO')
    print(patient_detail_id)
    patient_YBO = scales_models.RPatientYbobsessiontable.objects.filter(patient_session=patient_detail_id).all()
    print(scales_models.RPatientYbobsessiontable.objects.filter(patient_session_id=patient_detail_id).first())
    if patient_YBO.count() == 0:
        print(100)
        return scales_models.RPatientYbobsessiontable(patient_session_id=patient_detail_id,
                                                      doctor_id=doctor_id,
                                                      scale_id=11)
    else:
        print(111)
        return patient_YBO[0]


# 自杀意念及行为史
def get_or_default_patient_suicidal_byPatientDetailId(patient_detail_id, doctor_id):
    patient_suicidal = scales_models.RPatientSuicidal.objects.filter(patient_session=patient_detail_id)
    print(patient_suicidal)
    if patient_suicidal.count() == 0:
        return scales_models.RPatientSuicidal(patient_session_id=patient_detail_id,
                                              doctor_id=doctor_id,
                                              scale_id=12)
    else:
        return patient_suicidal[0]


# 33项轻躁狂
def get_or_default_patient_manicSymptom_byPatientDetailId(patient_detail_id, doctor_id):
    patient_manicSymptom = scales_models.RPatientManicsymptom.objects.filter(patient_session=patient_detail_id)
    if patient_manicSymptom.count() == 0:
        return scales_models.RPatientManicsymptom(patient_session_id=patient_detail_id,
                                                  doctor_id=doctor_id,
                                                  scale_id=13)
    else:
        return patient_manicSymptom[0]


# 斯奈斯和汉密尔顿快乐
def get_or_default_patient_happiness_byPatientDetailId(patient_detail_id, doctor_id):
    patient_happiness = scales_models.RPatientHappiness.objects.filter(patient_session=patient_detail_id)
    if patient_happiness.count() == 0:
        return scales_models.RPatientHappiness(patient_session_id=patient_detail_id,
                                               doctor_id=doctor_id,
                                               scale_id=14)
    else:

        return patient_happiness[0]


# 快感体验能力量表
def get_or_default_patient_pleasure_byPatientDetailId(patient_detail_id, doctor_id):
    patient_pleasure = scales_models.RPatientPleasure.objects.filter(patient_session=patient_detail_id)
    if patient_pleasure.count() == 0:
        return scales_models.RPatientPleasure(patient_session_id=patient_detail_id,
                                              doctor_id=doctor_id,
                                              scale_id=15)
    else:
        return patient_pleasure[0]


# 儿童期（16岁前）成长经历
def get_or_default_patient_growth_byPatientDetailId(patient_detail_id, doctor_id):
    patient_growth = scales_models.RPatientGrowth.objects.filter(patient_session=patient_detail_id)
    if patient_growth.count() == 0:
        return scales_models.RPatientGrowth(patient_session_id=patient_detail_id,
                                            doctor_id=doctor_id,
                                            scale_id=16)
    else:
        return patient_growth[0]


# 青少年生活事件量表
def get_or_default_patient_adolescent_byPatientDetailId(patient_detail_id, doctor_id):
    patient_adolescent = scales_models.RPatientAdolescentEvents.objects.filter(patient_session=patient_detail_id)
    if patient_adolescent.count() == 0:
        return scales_models.RPatientAdolescentEvents(patient_session_id=patient_detail_id,
                                                      doctor_id=doctor_id,
                                                      scale_id=17)
    else:
        return patient_adolescent[0]


# 认知情绪调节量表
def get_or_default_patient_cognitive_byPatientDetailId(patient_detail_id, doctor_id):
    patient_cognitive = scales_models.RPatientCognitiveEmotion.objects.filter(patient_session=patient_detail_id)
    if patient_cognitive.count() == 0:
        return scales_models.RPatientCognitiveEmotion(patient_session_id=patient_detail_id,
                                                      doctor_id=doctor_id,
                                                      scale_id=18)
    else:
        return patient_cognitive[0]


# 简式父母养育方式问卷表
def get_or_default_patient_SEmbu_byPatientDetailId(patient_detail_id, doctor_id):
    patient_SEmbu = scales_models.RPatientSembu.objects.filter(patient_session=patient_detail_id)
    if patient_SEmbu.count() == 0:
        return scales_models.RPatientSembu(patient_session_id=patient_detail_id,
                                           doctor_id=doctor_id,
                                           scale_id=19)
    else:
        return patient_SEmbu[0]


# 自动思维问卷表
def get_or_default_patient_ATQ_byPatientDetailId(patient_detail_id, doctor_id):
    patient_ATQ = scales_models.RPatientAtq.objects.filter(patient_session=patient_detail_id)
    if patient_ATQ.count() == 0:
        return scales_models.RPatientAtq(patient_session_id=patient_detail_id,
                                         doctor_id=doctor_id,
                                         scale_id=20)
    else:
        return patient_ATQ[0]


def get_or_default_patient_PHQ_byPatientDetailId(patient_detail_id, doctor_id):
    patient_PHQ = scales_models.RPatientPhq.objects.filter(patient_session=patient_detail_id)
    if patient_PHQ.count() == 0:
        return scales_models.RPatientPhq(patient_session_id=patient_detail_id,
                                         doctor_id=doctor_id,
                                         scale_id=20)
    else:
        return patient_PHQ[0]


def get_or_default_patient_GAD_byPatientDetailId(patient_detail_id, doctor_id):
    patient_GAD = scales_models.RPatientGad.objects.filter(patient_session=patient_detail_id)
    if patient_GAD.count() == 0:
        return scales_models.RPatientGad(patient_session_id=patient_detail_id,
                                         doctor_id=doctor_id,
                                         scale_id=20)
    else:
        return patient_GAD[0]


def get_or_default_patient_PSS_byPatientDetailId(patient_detail_id, doctor_id):
    patient_PSS = scales_models.RPatientPss.objects.filter(patient_session=patient_detail_id)
    if patient_PSS.count() == 0:
        return scales_models.RPatientPss(patient_session_id=patient_detail_id,
                                         doctor_id=doctor_id,
                                         scale_id=20)
    else:
        return patient_PSS[0]


def get_or_default_patient_ISI_byPatientDetailId(patient_detail_id, doctor_id):
    patient_ISI = scales_models.RPatientInsomnia.objects.filter(patient_session=patient_detail_id)
    if patient_ISI.count() == 0:
        return scales_models.RPatientInsomnia(patient_session_id=patient_detail_id,
                                              doctor_id=doctor_id,
                                              scale_id=20)
    else:
        return patient_ISI[0]


def self_tests_total_score(scale_id, obj):
    if scale_id == 11:
        obj.total_score, object_flag = tools_calculatingScores.YBO_total_score(obj)
    elif scale_id == 12:
        obj.total_score_lastweek, obj.total_score_mostdepressed, object_flag, obj.suicide_ideation = tools_calculatingScores.Suicidal_total_score(
            obj)
    elif scale_id == 13:
        obj.total_score, object_flag = tools_calculatingScores.ManicSymptom_total_score(obj)
    elif scale_id == 14:
        obj.total_score, object_flag = tools_calculatingScores.happiness_total_score(obj)
    elif scale_id == 15:
        obj.expectation_score, obj.consume_score, object_flag = tools_calculatingScores.pleasure_total_score(obj)
    elif scale_id == 16:
        obj.emotion_abuse_score, obj.body_abuse_score, obj.sex_abuse_score, obj.emotion_ignore_score, \
        obj.body_ignore_score, object_flag = tools_calculatingScores.growth_total_score(obj)
    elif scale_id == 17:
        obj.total_score, obj.blame_self, obj.blame_others, obj.meditation, obj.catastrophization, obj.accepted, \
        obj.positive_refocus, obj.program_refocus, obj.positive_evaluation, obj.rational_analysis, object_flag \
            = tools_calculatingScores.CognitiveEmotion_total_score(obj)
    elif scale_id == 18:
        obj.total_score, object_flag = tools_calculatingScores.AdolescentEvents_total_score(obj)
    elif scale_id == 19:
        obj.refusal_mother, obj.refusal_father, obj.emotional_warmth_mother, obj.emotional_warmth_father, \
        obj.overprotection_mother, obj.overprotection_father, object_flag = tools_calculatingScores.SEmbu_total_score(
            obj)
    elif scale_id == 20:
        obj.total_score, object_flag = tools_calculatingScores.ATQ_total_score(obj)
    elif scale_id == 29:
        obj.total_score = tools_calculatingScores.PHQ_total_score(obj)
    elif scale_id == 30:
        obj.total_score = tools_calculatingScores.GAD_total_score(obj)
    elif scale_id == 31:
        obj.total_score = tools_calculatingScores.ISI_total_score(obj)
    elif scale_id == 32:
        obj.total_score = tools_calculatingScores.PSS_total_score(obj)


def get_or_default_self_tests_obj_by_scale_id(scale_id, patient_session_id, doctor_id):
    if scale_id == 11:
        return get_or_default_patient_YBO_byPatientDetailId(patient_session_id, doctor_id)
    elif scale_id == 12:
        return get_or_default_patient_suicidal_byPatientDetailId(patient_session_id, doctor_id)
    elif scale_id == 13:
        return get_or_default_patient_manicSymptom_byPatientDetailId(patient_session_id, doctor_id)
    elif scale_id == 14:
        return get_or_default_patient_happiness_byPatientDetailId(patient_session_id, doctor_id)
    elif scale_id == 15:
        return get_or_default_patient_pleasure_byPatientDetailId(patient_session_id, doctor_id)
    elif scale_id == 16:
        return get_or_default_patient_growth_byPatientDetailId(patient_session_id, doctor_id)
    elif scale_id == 17:
        return get_or_default_patient_cognitive_byPatientDetailId(patient_session_id, doctor_id)
    elif scale_id == 18:
        return get_or_default_patient_adolescent_byPatientDetailId(patient_session_id, doctor_id)
    elif scale_id == 19:
        return get_or_default_patient_SEmbu_byPatientDetailId(patient_session_id, doctor_id)
    elif scale_id == 20:
        return get_or_default_patient_ATQ_byPatientDetailId(patient_session_id, doctor_id)
    elif scale_id == 29:
        return get_or_default_patient_PHQ_byPatientDetailId(patient_session_id, doctor_id)
    elif scale_id == 30:
        return get_or_default_patient_GAD_byPatientDetailId(patient_session_id, doctor_id)
    elif scale_id == 31:
        return get_or_default_patient_ISI_byPatientDetailId(patient_session_id, doctor_id)
    elif scale_id == 32:
        return get_or_default_patient_PSS_byPatientDetailId(patient_session_id, doctor_id)


def del_duration_by_scale_id(patient_session_id, scale_id):
    scales_models.RSelfTestDuration.objects.filter(patient_session_id=patient_session_id, scale_id=scale_id).delete()


def add_suibe_database(rPatientSuicideBehavior, state):
    # 插入前的级联检验
    tools_insertCascadeCheck.insert_suibe_check(rPatientSuicideBehavior)
    # 插入数据库
    rPatientSuicideBehavior.save()
    # 修改r_patient_scales表中state状态
    update_rscales_state(rPatientSuicideBehavior.patient_session_id, rPatientSuicideBehavior.scale_id, state)


# 自杀行为表
def get_patient_suibe_byPatientDetailId(patient_detail_id):
    patient_suibe = scales_models.RPatientSuicideBehavior.objects.filter(patient_session=patient_detail_id)
    if patient_suibe.count() == 0:
        return None
    else:
        return patient_suibe[0]


# 获取suibe填写结果
def get_suibe_answer(patient_id):
    suibe_list = scales_models.RPatientSuicideBehavior.objects.filter(patient_session_id=patient_id)[0]
    return suibe_list


def get_suibe_isfirst(patient_id):
    scale_queryset = patient_models.DPatientDetail.objects.filter(id=patient_id)
    isfirst = scale_queryset[0].session_id
    return isfirst


def del_suibe(patient_session_id, scale_id):
    res = scales_models.RPatientSuicideBehavior.objects.filter(patient_session_id=patient_session_id, scale_id=scale_id)
    if res.exists():
        res[0].delete()


# 根据scale_definition_id取scale_content,默认取最新版本
def get_scale_content_by_id(scale_id):
    res = scales_models.TScalesContent.objects.filter(scale_definition_id=scale_id, delete=config.Del_No
                                                      ).order_by("-scale_version").first()
    return res


# 根据根据scale_definition_id取对应版本的scale_content
def get_scale_content_by_id_and_version(scale_id, scale_version):
    res = scales_models.TScalesContent.objects.filter(scale_definition_id=scale_id, scale_version=scale_version,
                                                      delete=config.Del_No).order_by("-scale_version").first()
    return res


# 根据scale_definition_id取scale_content的最新版本的版本号
def get_scale_content_version_by_id(scale_id):
    res = scales_models.TScalesContent.objects.filter(scale_definition_id=scale_id, delete=config.Del_No
                                                      ).order_by("-scale_version").values("scale_version").first()
    if res is None:
        return res
    return res["scale_version"]


# 插入一条scale_content
def insert_scale_content(scale_content_model):
    try:
        scale_content_model.save()
        return True
    except ValueError:
        return False


# 删除一条scale_content
def delete_scale_content(scale_id, scale_version):
    res = scales_models.TScalesContent.objects.filter(scale_id=scale_id,
                                                      scale_version=scale_version).update(delete=config.Del_Yse)
    return res


# 取某一个量表的答题记录
def get_scale_answers(scale_model, patient_session_id):
    res = scale_model.objects.filter(patient_session_id=patient_session_id, delete=config.Del_No).first()
    return res


# 删除某一个量表的答题记录
def delete_scale_answers(scale_model, patient_session_id):
    res = scale_model.objects.filter(patient_session_id=patient_session_id,
                                     delete=config.Del_No).update(delete=config.Del_Yse)
    return res


# 更新量表中某道题的答案
def update_scales(scale_model, patient_session_id, form_content, doctor_id, scale_id):
    print("update_scales entry: ", scale_model, patient_session_id, form_content, doctor_id, scale_id)
    # 先去查有没有记录
    res = scale_model.objects.filter(patient_session_id=patient_session_id, delete=config.Del_No).first()
    print(res)
    if res is None:
        # 没有记录说明是写入第一道题 所以先创建一个
        res = scale_model.objects.create(patient_session_id=patient_session_id,
                                         doctor_id=doctor_id,
                                         create_time=int(time.time()),
                                         version=get_scale_content_version_by_id(scale_id),
                                         update_time=int(time.time()),
                                         )
        # 创建完成之后再查出来
        res = scale_model.objects.filter(patient_session_id=patient_session_id, delete=config.Del_No).first()
    # 把对应题目的答案更新 同时更新更新时间和医生id
    for key in form_content.keys():
        setattr(res, key, str(form_content[key]))
    res.update_time = int(time.time())
    res.doctor_id = doctor_id
    res.save()


# 插入题目的响应时间
def insert_scale_duration(patient_session_id, scale_id, question_index, duration):
    scales_models.RSelfTestDuration.objects.create(patient_session_id=patient_session_id, scale_id=scale_id,
                                                   question_index=question_index, duration=duration)


# 取之前答题记录对应的量表版本号
def get_version_of_history_scale(scale_model, patient_session_id):
    res = scale_model.objects.filter(patient_session_id=patient_session_id, delete=config.Del_No). \
        values("version").first()
    if res is None:
        return None
    return res["version"]


# 根据题目index取答案 考虑到性能这里不返回整条记录，只反映对应字段的值
def get_answer_by_index(scale_model, patient_session_id, question_index):
    res = scale_model.objects.filter(patient_session_id=patient_session_id, delete=config.Del_No).values(
        question_index).first()[question_index]
    return res


# 根据 patient_session_id 返回对应的 patient id
def get_patient_id(patient_session_id):
    res = patient_models.DPatientDetail.objects.filter(pk=patient_session_id).values("patient").first()[
        "patient"]
    return res
