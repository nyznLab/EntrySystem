import requests
import json
import patients.models as patients_models
import patients.dao as patients_dao
import scales.models as scales_models
import scales.dao as scales_dao
from tools import idAssignments
# 公众号数据转移处理脚本

# 公众号数据查询接口
def get_patient_data(patient_id, start_date=None, end_date=None):
    if start_date is None or end_date is None:
        url = "http://www.braintechnet.cn/port.php?r=scale&patient_id="+str(patient_id)
    else:
        url = "http://www.braintechnet.cn/port.php?r=scale&patient_id="+str(patient_id)+"&start_date="+str(start_date)+"&end_date="+str(end_date)
    ret = requests.get(url)
    if ret.status_code == 200:
        patient_data = json.loads(ret.text)
        return patient_data
    else:
        patient_data = False
        return patient_data


### main
def trans_interface(patient_id_official_account,patient_id,session_id,start_date=None,end_date=None):
    # 参数：patient_id_official_account, patient_id, start_date, end_date, session_id
    # patient_id_official_account = 411
    # patient_id = 553
    # start_date = "2021-01-31"
    # end_date = "2021-01-31"
    # session_id = 3
    patient_data = get_patient_data(patient_id_official_account,start_date,end_date)
    if patient_data is False:
        print("参数错误")

    # scale_id：公众号中的量表流水id
    scale_id = patient_data['data']['scale_id']
    print("scale_id: "+str(scale_id))


    # base_info：对应d_patient_detail和d_patient_base_info中的数据
    base_info = patient_data['data']['base_info']
    print("base_info: "+str(base_info))
    # 先判断是否存在这个人，如果存在则证明其之前的诊断已在库中，不需要填充base_info，若不存在，则此条记录为初扫,需要新建base_info插入
    base_info_pre = patients_models.BPatientBaseInfo.objects.filter(id=patient_id).first()
    if base_info_pre is None:
        # 需要特别注意birth，这里需要填写：如果birth为空，查找这一id是否有以前的记录，将birth填充进来；
        # 如果以前没有的记录，这一条记录是初扫，那么通过今天的日期减去age估算出一个birth填充进去
        BPatientBaseInfo_object = patients_models.BPatientBaseInfo(id=patient_id,name=base_info['name'],sex=base_info['sex'],birth_date=base_info['birth_date'],
                                                            nation=base_info['nation'],doctor_id=2,create_time=end_date,update_time=end_date,
                                                            diagnosis=0)
        BPatientBaseInfo_object.save()
        #patients_dao.add_base_info(BPatientBaseInfo_object)
    # 插入d_patient_detail表,若不存在则插入新记录，若存在则更新相关数据
    patient_detail_pre = patients_dao.get_patient_detail_byPatientIdAndSessionId(patient_id, session_id)
    if patient_detail_pre is None:
        standard_id = idAssignments.generate_standard_id(patient_id, session_id)
        DPatientDetail_object = patients_models.DPatientDetail(patient_id=patient_id,session_id=session_id,age=base_info['age'],occupation=base_info['occupation'],
                                                               education=base_info['education'],years=base_info['years'],emotional_state=base_info['emotional_state'],
                                                               phone=base_info['phone'],height=base_info['height'],weight=base_info['weight'],waist=base_info['waist'],
                                                               hip=base_info['hip'],doctor_id=2,create_time=end_date,update_time=end_date,contact_way=2,
                                                               contact_info=base_info['contact_info'],scan_date=end_date,standard_id=standard_id)
        DPatientDetail_object.save()
        #patients_dao.add_patient_detail(DPatientDetail_object)
    else:
        patient_detail_pre.age=base_info['age']
        patient_detail_pre.occupation=base_info['occupation']
        patient_detail_pre.education=base_info['education']
        patient_detail_pre.years=base_info['years']
        patient_detail_pre.emotional_state=base_info['emotional_state']
        patient_detail_pre.phone=base_info['phone']
        patient_detail_pre.height=base_info['height']
        patient_detail_pre.weight=base_info['weight']
        patient_detail_pre.waist=base_info['waist']
        patient_detail_pre.hip=base_info['hip']
        patient_detail_pre.update_time=end_date
        patient_detail_pre.contact_way=2
        patient_detail_pre.contact_info=base_info['contact_info']
        patient_detail_pre.save()

    # 新的全局变量：patient_detail_id 的流水id
    patient_detail_id =patients_dao.get_patient_detail_byPatientIdAndSessionId(patient_id, session_id).id

    # basic_information_family：对应r_patient_basic_information_family表数据
    basic_information_family = patient_data['data']['basic_information_family']
    print("basic_information_family: "+str(basic_information_family))
    if basic_information_family['linkman']:
        patient_phone = basic_information_family['linkman'].split("\"")[3]
    else:
        patient_phone = None
    RPatientBasicInformationFamily_pre = scales_models.RPatientBasicInformationFamily.objects.filter(patient_session_id=patient_detail_id).first()
    if RPatientBasicInformationFamily_pre is None:
        patient_scale_family = scales_models.RPatientScales.objects.filter(patient_session_id=patient_detail_id,scale_id=1)
        if not patient_scale_family:
        # 级联分配r_patient_scales表
            scale = scales_models.DScales.objects.filter(id=1)
            patients_dao.add_rscales(scale, patient_detail_id)
        # 修改对应的表
        RPatientBasicInformationFamily_object = scales_models.RPatientBasicInformationFamily(patient_session_id=patient_detail_id, scale_id=1,patient_urban_rural=basic_information_family['patient_urban_rural'],
                                                                                             patient_address=basic_information_family['patient_address'],patient_live_type=basic_information_family['patient_live_type'],
                                                                                             patient_live_type_other=basic_information_family['patient_live_type_other'],patient_only_child=basic_information_family['patient_only_child'],
                                                                                             patient_older_brother_num=basic_information_family['patient_older_brother_num'],patient_older_sister_num=basic_information_family['patient_older_sister_num'],
                                                                                             patient_younger_brother_num=basic_information_family['patient_youger_brother_num'],pathent_younger_sister_num=basic_information_family['patient_youger_sister_num'],
                                                                                             parents_favour=basic_information_family['parents_favour'],father_occupation=basic_information_family['father_occupation'],mother_occupation=basic_information_family['mother_occupation'],
                                                                                             father_tele=patient_phone,mother_tele=patient_phone,father_education=basic_information_family['father_education'],
                                                                                             mother_education=basic_information_family['mother_education'],parent_marry=basic_information_family['parent_marry'],patient_parent_death=basic_information_family['patient_parent_death'],
                                                                                             patient_parent_death_age=basic_information_family['patient_parent_death_age'],parent_argument=basic_information_family['parent_argument'],patient_adopt=basic_information_family['patient_adopt'],
                                                                                             patient_adopt_age=basic_information_family['patient_adopt_age'],father_relationship=basic_information_family['father_relationship'],mother_relationship=basic_information_family['mother_relationship'],
                                                                                             doctor_id=2,create_time=end_date,update_time=end_date)
        #scales_dao.dao_add_family_info(RPatientBasicInformationFamily_object,1)
        RPatientBasicInformationFamily_object.save()
        scales_dao.update_rscales_state(RPatientBasicInformationFamily_object.patient_session_id, RPatientBasicInformationFamily_object.scale_id, 1)
    else:
        # 更新字段
        RPatientBasicInformationFamily_pre.patient_urban_rural = basic_information_family['patient_urban_rural']
        RPatientBasicInformationFamily_pre.patient_address = basic_information_family['patient_address']
        RPatientBasicInformationFamily_pre.patient_live_type = basic_information_family['patient_live_type']
        RPatientBasicInformationFamily_pre.patient_live_type_other = basic_information_family['patient_live_type_other']
        RPatientBasicInformationFamily_pre.patient_only_child = basic_information_family['patient_only_child']
        RPatientBasicInformationFamily_pre.patient_older_brother_num = basic_information_family['patient_older_brother_num']
        RPatientBasicInformationFamily_pre.patient_older_sister_num = basic_information_family['patient_older_sister_num']
        RPatientBasicInformationFamily_pre.patient_younger_brother_num = basic_information_family['patient_youger_brother_num']
        RPatientBasicInformationFamily_pre.pathent_younger_sister_num = basic_information_family['patient_youger_sister_num']
        RPatientBasicInformationFamily_pre.parents_favour = basic_information_family['parents_favour']
        RPatientBasicInformationFamily_pre.father_occupation = basic_information_family['father_occupation']
        RPatientBasicInformationFamily_pre.mother_occupation = basic_information_family['mother_occupation']
        RPatientBasicInformationFamily_pre.father_tele = patient_phone
        RPatientBasicInformationFamily_pre.mother_tele = patient_phone
        RPatientBasicInformationFamily_pre.father_education = basic_information_family['father_education']
        RPatientBasicInformationFamily_pre.mother_education = basic_information_family['mother_education']
        RPatientBasicInformationFamily_pre.parent_marry = basic_information_family['parent_marry']
        RPatientBasicInformationFamily_pre.patient_parent_death = basic_information_family['patient_parent_death']
        RPatientBasicInformationFamily_pre.patient_parent_death_age = basic_information_family['patient_parent_death_age']
        RPatientBasicInformationFamily_pre.parent_argument = basic_information_family['parent_argument']
        RPatientBasicInformationFamily_pre.patient_adopt = basic_information_family['patient_adopt']
        RPatientBasicInformationFamily_pre.patient_adopt_age = basic_information_family['patient_adopt_age']
        RPatientBasicInformationFamily_pre.father_relationship = basic_information_family['father_relationship']
        RPatientBasicInformationFamily_pre.mother_relationship = basic_information_family['mother_relationship']
        RPatientBasicInformationFamily_pre.create_time = end_date
        RPatientBasicInformationFamily_pre.update_time = end_date
        RPatientBasicInformationFamily_pre.save()
        # 更新r_patient_scales state
        scales_dao.update_rscales_state(RPatientBasicInformationFamily_pre.patient_session_id, RPatientBasicInformationFamily_pre.scale_id, 1)



    # basic_information_study：对应r_patient_basic_information_study表数据
    basic_information_study = patient_data['data']['basic_information_study']
    print("basic_information_study: "+str(basic_information_study))
    RPatientBasicInformationStudy_pre = scales_models.RPatientBasicInformationStudy.objects.filter(patient_session_id=patient_detail_id).first()
    if RPatientBasicInformationStudy_pre is None:
        patient_scale_study = scales_models.RPatientScales.objects.filter(patient_session_id=patient_detail_id,
                                                                           scale_id=2)
        if not patient_scale_study:
        # 级联分配r_patient_scales表
            scale = scales_models.DScales.objects.filter(id=2)
            patients_dao.add_rscales(scale, patient_detail_id)
        # 修改对应的表
        RPatientBasicInformationStudy_object = scales_models.RPatientBasicInformationStudy(patient_session_id=patient_detail_id,scale_id=2,patient_current_achievement=basic_information_study['patient_current_achievement'],
                                                                                           patient_last_semester_achievement_difference=basic_information_study['patient_last_semester_achievement_difference'],
                                                                                           patient_mood_symptom_achievement_difference=basic_information_study['patient_mood_symptom_achievement_difference'],
                                                                                           patient_leader=basic_information_study['patient_leader'],patient_leader_occupation=basic_information_study['patient_leader_occupation'],
                                                                                           patient_live_school=basic_information_study['patient_live_school'],doctor_id=2,create_time=end_date,update_time=end_date)
        #scales_dao.add_information_study_database(RPatientBasicInformationStudy_object,1)
        RPatientBasicInformationStudy_object.save()
        scales_dao.update_rscales_state(RPatientBasicInformationStudy_object.patient_session_id, RPatientBasicInformationStudy_object.scale_id, 1)
    else:
        RPatientBasicInformationStudy_pre.patient_current_achievement = basic_information_study['patient_current_achievement']
        RPatientBasicInformationStudy_pre.patient_last_semester_achievement_difference = basic_information_study['patient_last_semester_achievement_difference']
        RPatientBasicInformationStudy_pre.patient_mood_symptom_achievement_difference = basic_information_study['patient_mood_symptom_achievement_difference']
        RPatientBasicInformationStudy_pre.patient_leader = basic_information_study['patient_leader']
        RPatientBasicInformationStudy_pre.patient_leader_occupation = basic_information_study['patient_leader_occupation']
        RPatientBasicInformationStudy_pre.patient_live_school = basic_information_study['patient_live_school']
        RPatientBasicInformationStudy_pre.create_time = end_date
        RPatientBasicInformationStudy_pre.update_time = end_date
        RPatientBasicInformationStudy_pre.save()
        scales_dao.update_rscales_state(RPatientBasicInformationStudy_pre.patient_session_id, RPatientBasicInformationStudy_pre.scale_id, 1)


    # basic_information_health：对应r_patient_basic_information_health表数据
    basic_information_health = patient_data['data']['basic_information_health']
    print("basic_information_health: "+str(basic_information_health))
    RPatientBasicInformationHealth_pre = scales_models.RPatientBasicInformationHealth.objects.filter(patient_session_id=patient_detail_id).first()
    if RPatientBasicInformationHealth_pre is None:
        patient_scale_health = scales_models.RPatientScales.objects.filter(patient_session_id=patient_detail_id,
                                                                           scale_id=3)
        if not patient_scale_health:
            # 级联分配r_patient_scales表
            scale = scales_models.DScales.objects.filter(id=3)
            patients_dao.add_rscales(scale, patient_detail_id)
        # 修改对应的表
        RPatientBasicInformationHealth_object = scales_models.RPatientBasicInformationHealth(patient_session_id=patient_detail_id,scale_id=3,doctor_id=2,create_time=end_date,update_time=end_date,
                                                                                             patient_somatic_diseases=basic_information_health['patient_somatic_diseases'],patient_somatic_diseases_name=basic_information_health['patient_somatic_diseases_name'],
                                                                                             patient_somatic_diseases_year=basic_information_health['patient_somatic_diseases_year'],patient_mental_diseases=basic_information_health['patient_mental_diseases'],
                                                                                             patient_mental_diseases_name=basic_information_health['patient_mental_diseases_name'],patient_mental_diseases_year=basic_information_health['patient_mental_diseases_year'],
                                                                                             patient_family_diseases_history=basic_information_health['patient_family_diseases_history'],patient_family_diseases_name=basic_information_health['patient_family_diseases_name'],
                                                                                             patient_medicine_information=basic_information_health['patient_medicine_information'],patient_treatment_information=basic_information_health['patient_treatment_information'])
        #scales_dao.add_patient_basic_information_health_database(RPatientBasicInformationHealth_object,1)
        RPatientBasicInformationHealth_object.save()
        scales_dao.update_rscales_state(RPatientBasicInformationHealth_object.patient_session_id, RPatientBasicInformationHealth_object.scale_id, 1)
    else:
        RPatientBasicInformationHealth_pre.create_time = end_date
        RPatientBasicInformationHealth_pre.update_time = end_date
        RPatientBasicInformationHealth_pre.patient_somatic_diseases = basic_information_health['patient_somatic_diseases']
        RPatientBasicInformationHealth_pre.patient_somatic_diseases_name = basic_information_health['patient_somatic_diseases_name']
        RPatientBasicInformationHealth_pre.patient_somatic_diseases_year = basic_information_health['patient_somatic_diseases_year']
        RPatientBasicInformationHealth_pre.patient_mental_diseases = basic_information_health['patient_mental_diseases']
        RPatientBasicInformationHealth_pre.patient_mental_diseases_name = basic_information_health['patient_mental_diseases_name']
        RPatientBasicInformationHealth_pre.patient_mental_diseases_year = basic_information_health['patient_mental_diseases_year']
        RPatientBasicInformationHealth_pre.patient_family_diseases_history = basic_information_health['patient_family_diseases_history']
        RPatientBasicInformationHealth_pre.patient_family_diseases_name = basic_information_health['patient_family_diseases_name']
        patient_medicine_information = basic_information_health['patient_medicine_information']
        RPatientBasicInformationHealth_pre.patient_treatment_information = basic_information_health['patient_treatment_information']
        RPatientBasicInformationHealth_pre.save()
        scales_dao.update_rscales_state(RPatientBasicInformationHealth_pre.patient_session_id, RPatientBasicInformationHealth_pre.scale_id, 1)

    # basic_information_abuse：对应r_patient_basic_information_abuse表数据
    basic_information_abuse = patient_data['data']['basic_information_abuse']
    print("basic_information_abuse: "+str(basic_information_abuse))
    RPatientBasicInformationAbuse_pre = scales_models.RPatientBasicInformationAbuse.objects.filter(patient_session_id=patient_detail_id).first()
    if RPatientBasicInformationAbuse_pre is None:
        patient_scale_abuse = scales_models.RPatientScales.objects.filter(patient_session_id=patient_detail_id,
                                                                           scale_id=4)
        if not patient_scale_abuse:
            # 级联分配r_patient_scales表
            scale = scales_models.DScales.objects.filter(id=4)
            patients_dao.add_rscales(scale, patient_detail_id)
        # 修改对应的表
        RPatientBasicInformationAbuse_object = scales_models.RPatientBasicInformationAbuse(patient_session_id=patient_detail_id,scale_id=4,doctor_id=2,create_time=end_date,update_time=end_date,
                                                                                           patient_smoke=basic_information_abuse['patient_smoke'],patient_smoke_age=basic_information_abuse['patient_smoke_age'],
                                                                                           patient_stop_smoke_age=basic_information_abuse['patient_stop_smoke_age'],patient_alcohol=basic_information_abuse['patient_alcohol'],
                                                                                           patient_alcohol_age=basic_information_abuse['patient_alcohol_age'],patient_other_abuse=basic_information_abuse['patient_other_abuse'],
                                                                                           patient_other_abuse_age=basic_information_abuse['patient_other_abuse_age'])
        #scales_dao.add_abuse_database(RPatientBasicInformationAbuse_object,1)
        RPatientBasicInformationAbuse_object.save()
        scales_dao.update_rscales_state(RPatientBasicInformationAbuse_object.patient_session_id, RPatientBasicInformationAbuse_object.scale_id, 1)
    else:
        RPatientBasicInformationAbuse_pre.create_time = end_date
        RPatientBasicInformationAbuse_pre.update_time = end_date
        RPatientBasicInformationAbuse_pre.patient_smoke = basic_information_abuse['patient_smoke']
        RPatientBasicInformationAbuse_pre.patient_smoke_age = basic_information_abuse['patient_smoke_age']
        RPatientBasicInformationAbuse_pre.patient_stop_smoke_age = basic_information_abuse['patient_stop_smoke_age']
        RPatientBasicInformationAbuse_pre.patient_alcohol = basic_information_abuse['patient_alcohol']
        RPatientBasicInformationAbuse_pre.patient_alcohol_age = basic_information_abuse['patient_alcohol_age']
        RPatientBasicInformationAbuse_pre.patient_other_abuse = basic_information_abuse['patient_other_abuse']
        RPatientBasicInformationAbuse_pre.patient_other_abuse_age = basic_information_abuse['patient_other_abuse_age']
        RPatientBasicInformationAbuse_pre.save()
        scales_dao.update_rscales_state(RPatientBasicInformationAbuse_pre.patient_session_id, RPatientBasicInformationAbuse_pre.scale_id, 1)


    # basic_information_other：对应r_patient_basic_information_other表数据
    basic_information_other = patient_data['data']['basic_information_other']
    print("basic_information_other: "+str(basic_information_other))
    RPatientBasicInformationOther_pre = scales_models.RPatientBasicInformationOther.objects.filter(patient_session_id=patient_detail_id).first()
    if RPatientBasicInformationOther_pre is None:
        patient_scale_other = scales_models.RPatientScales.objects.filter(patient_session_id=patient_detail_id,
                                                                          scale_id=5)
        if not patient_scale_other:
            # 级联分配r_patient_scales表
            scale = scales_models.DScales.objects.filter(id=5)
            patients_dao.add_rscales(scale, patient_detail_id)
        # 修改对应的表
        RPatientBasicInformationOther_object = scales_models.RPatientBasicInformationOther(patient_session_id=patient_detail_id,scale_id=5,doctor_id=2,create_time=end_date,update_time=end_date,
                                                                                           patient_friend_num=basic_information_other['patient_friend_num'],patient_big_event=basic_information_other['patient_big_event'],
                                                                                           patient_big_event_describtion=basic_information_other['patient_big_event_describtion'])
        #scales_dao.add_other_database(RPatientBasicInformationOther_object,1)
        RPatientBasicInformationOther_object.save()
        scales_dao.update_rscales_state(RPatientBasicInformationOther_object.patient_session_id, RPatientBasicInformationOther_object.scale_id, 1)

    else:
        RPatientBasicInformationOther_pre.create_time = end_date
        RPatientBasicInformationOther_pre.update_time = end_date
        RPatientBasicInformationOther_pre.patient_friend_num = basic_information_other['patient_friend_num']
        RPatientBasicInformationOther_pre.patient_big_event = basic_information_other['patient_big_event']
        RPatientBasicInformationOther_pre.patient_big_event_describtion = basic_information_other['patient_big_event_describtion']
        RPatientBasicInformationOther_pre.save()
        scales_dao.update_rscales_state(RPatientBasicInformationOther_pre.patient_session_id, RPatientBasicInformationOther_pre.scale_id, 1)


    # scale_handy：利手量表
    scale_handy = patient_data['data']['scale_handy']
    print("scale_handy: "+str(scale_handy))
    RPatientChineseHandy_pre = scales_models.RPatientChineseHandy.objects.filter(patient_session_id=patient_detail_id).first()
    # 删除原有量表
    if RPatientChineseHandy_pre is not None and scale_handy:
        RPatientChineseHandy_pre.delete()
    if scale_handy:
        # scale_handy表示判断非空，python中空字典为False，非空字典为True
        patient_scale_handy = scales_models.RPatientScales.objects.filter(patient_session_id=patient_detail_id,
                                                                          scale_id=6)
        if not patient_scale_handy:
            # 级联分配r_patient_scales表
            scale = scales_models.DScales.objects.filter(id=6)
            patients_dao.add_rscales(scale, patient_detail_id)
        # 修改对应的表
        RPatientChineseHandy_object = scales_models.RPatientChineseHandy(patient_session_id=patient_detail_id,scale_id=6, doctor_id=2,create_time=end_date,update_time=end_date,
                                                                         hold_pen=scale_handy['hold_pen'],hold_chopsticks=scale_handy['hold_chopsticks'],throw_things=scale_handy['throw_things'],
                                                                         brush_tooth=scale_handy['brush_tooth'],use_scissors=scale_handy['use_scissors'],use_match=scale_handy['use_match'],
                                                                         use_needle=scale_handy['use_needle'],hold_hammer=scale_handy['hold_hammer'],hold_racket=scale_handy['hold_hammer'],
                                                                         wash_face=scale_handy['wash_face'],result=scale_handy['result'])
        #scales_dao.add_chinesehandle_database(RPatientChineseHandy_object,1)
        RPatientChineseHandy_object.save()
        scales_dao.update_rscales_state(RPatientChineseHandy_object.patient_session_id, RPatientChineseHandy_object.scale_id, 1)
        # 这个量表在填充过以后，需要更新下detail表中的handy
        detail = patients_models.DPatientDetail.objects.filter(id=patient_detail_id).first()
        detail.handy = scale_handy['result']
        detail.save()


    # scale_handy_duration：利手量表答题时间（array格式）
    scale_handy_duration = patient_data['data']['scale_handy_duration']
    print("scale_handy_duration: "+str(scale_handy_duration))

    # scale_ocd：耶鲁布朗强迫症严重程度标准量表
    scale_ocd = patient_data['data']['scale_ocd']
    print("scale_ocd: "+str(scale_ocd))
    RPatientYbobsessiontable_pre = scales_models.RPatientYbobsessiontable.objects.filter(patient_session_id=patient_detail_id).first()
    # 删除原有量表
    if RPatientYbobsessiontable_pre is not None and scale_ocd:
        RPatientYbobsessiontable_pre.delete()
    if scale_ocd:
        # scale_handy表示判断非空，python中空字典为False，非空字典为True
        patient_scale_ybo = scales_models.RPatientScales.objects.filter(patient_session_id=patient_detail_id,
                                                                          scale_id=11)
        if not patient_scale_ybo:
            # 级联分配r_patient_scales表
            scale = scales_models.DScales.objects.filter(id=11)
            patients_dao.add_rscales(scale, patient_detail_id)
        # 修改对应的表
        RPatientYbobsessiontable_object = scales_models.RPatientYbobsessiontable(patient_session_id=patient_detail_id,scale_id=11, doctor_id=2,create_time=end_date,update_time=end_date,
                                                                                 forced_frequency=scale_ocd['forced_frequency'],impediment_degree1=scale_ocd['impediment_degree1'],
                                                                                 impediment_degree2=scale_ocd['impediment_degree2'],distress=scale_ocd['distress'],fightforced_degree=scale_ocd['fightforced_degree'],
                                                                                 control_ability1=scale_ocd['control_ability1'],control_ability2=scale_ocd['control_ability2'],
                                                                                 compulsion_frequency=scale_ocd['compulsion_frequency'],stopcompulsion_anxiety=scale_ocd['stopcompulsion_anxiety'],
                                                                                 stopforced_frequency=scale_ocd['stopforced_frequency'],total_score=scale_ocd['total_score'])
        # scales_dao.dao_add_ybo(RPatientYbobsessiontable_object,1)
        RPatientYbobsessiontable_object.save()
        scales_dao.update_rscales_state(RPatientYbobsessiontable_object.patient_session_id,RPatientYbobsessiontable_object.scale_id, 1)

    # scale_ocd_duration：答题时间
    scale_ocd_duration = patient_data['data']['scale_ocd_duration']
    print("scale_ocd_duration: "+str(scale_ocd_duration))

    # scale_suicidal：自杀量表
    scale_suicidal = patient_data['data']['scale_suicidal']
    print("scale_suicidal: "+str(scale_suicidal))
    RPatientSuicidal_pre = scales_models.RPatientSuicidal.objects.filter(patient_session_id=patient_detail_id).first()
    # 删除原有量表
    if RPatientSuicidal_pre is not None and scale_suicidal:
        RPatientSuicidal_pre.delete()
    if scale_suicidal:
        # scale_handy表示判断非空，python中空字典为False，非空字典为True
        patient_scale_suicidal = scales_models.RPatientScales.objects.filter(patient_session_id=patient_detail_id,scale_id=12)
        if not patient_scale_suicidal:
            # 级联分配r_patient_scales表
            scale = scales_models.DScales.objects.filter(id=12)
            patients_dao.add_rscales(scale, patient_detail_id)
        # 修改对应的表
        RPatientSuicidal_object = scales_models.RPatientSuicidal(patient_session_id=patient_detail_id,scale_id=12, doctor_id=2,create_time=end_date,update_time=end_date,
                                                                 question1_lastweek=scale_suicidal['question1_lastweek'],question1_mostdepressed=scale_suicidal['question1_mostdepressed'],
                                                                 question2_lastweek=scale_suicidal['question2_lastweek'],question2_mostdepressed=scale_suicidal['question2_mostdepressed'],
                                                                 question3_lastweek=scale_suicidal['question3_lastweek'],question3_mostdepressed=scale_suicidal['question3_mostdepressed'],
                                                                 question4_lastweek=scale_suicidal['question4_lastweek'],question4_mostdepressed=scale_suicidal['question4_mostdepressed'],
                                                                 question5_lastweek=scale_suicidal['question5_lastweek'],question5_mostdepressed=scale_suicidal['question5_mostdepressed'],
                                                                 question6_lastweek=scale_suicidal['question6_lastweek'],question6_mostdepressed=scale_suicidal['question6_mostdepressed'],
                                                                 question7_lastweek=scale_suicidal['question7_lastweek'],question7_mostdepressed=scale_suicidal['question7_mostdepressed'],
                                                                 question8_lastweek=scale_suicidal['question8_lastweek'],question8_mostdepressed=scale_suicidal['question8_mostdepressed'],
                                                                 question9_lastweek=scale_suicidal['question9_lastweek'],question9_mostdepressed=scale_suicidal['question9_mostdepressed'],
                                                                 question10_lastweek=scale_suicidal['question10_lastweek'],question10_mostdepressed=scale_suicidal['question10_mostdepressed'],
                                                                 question11_lastweek=scale_suicidal['question11_lastweek'],question11_mostdepressed=scale_suicidal['question11_mostdepressed'],
                                                                 question12_lastweek=scale_suicidal['question12_lastweek'],question12_mostdepressed=scale_suicidal['question12_mostdepressed'],
                                                                 question13_lastweek=scale_suicidal['question13_lastweek'],question13_mostdepressed=scale_suicidal['question13_mostdepressed'],
                                                                 question14_lastweek=scale_suicidal['question14_lastweek'],question14_mostdepressed=scale_suicidal['question14_mostdepressed'],
                                                                 question15_lastweek=scale_suicidal['question15_lastweek'],question15_mostdepressed=scale_suicidal['question15_mostdepressed'],
                                                                 question16_lastweek=scale_suicidal['question16_lastweek'],question16_mostdepressed=scale_suicidal['question16_mostdepressed'],
                                                                 question17_lastweek=scale_suicidal['question17_lastweek'],question17_mostdepressed=scale_suicidal['question17_mostdepressed'],
                                                                 question18_lastweek=scale_suicidal['question18_lastweek'],question18_mostdepressed=scale_suicidal['question18_mostdepressed'],
                                                                 question19_lastweek=scale_suicidal['question19_lastweek'],question19_mostdepressed=scale_suicidal['question19_mostdepressed'],
                                                                 total_score_lastweek=scale_suicidal['total_score_lastweek'],total_score_mostdepressed=scale_suicidal['total_score_mostdepressed'])
        # scales_dao.dao_add_suicide(RPatientSuicidal_object,1)
        RPatientSuicidal_object.save()
        scales_dao.update_rscales_state(RPatientSuicidal_object.patient_session_id, RPatientSuicidal_object.scale_id, 1)

    # scale_suicidal_duration：答题时间
    scale_suicidal_duration = patient_data['data']['scale_suicidal_duration']
    print("scale_suicidal_duration: "+str(scale_suicidal_duration))

    # scale_manic： 躁狂症
    scale_manic = patient_data['data']['scale_manic']
    print("scale_manic: "+str(scale_manic))
    RPatientManicsymptom_pre = scales_models.RPatientManicsymptom.objects.filter(patient_session_id=patient_detail_id).first()
    # 删除原有量表
    if RPatientManicsymptom_pre is not None and scale_manic:
        RPatientManicsymptom_pre.delete()
    if scale_manic:
        # scale_handy表示判断非空，python中空字典为False，非空字典为True
        patient_scale_manic = scales_models.RPatientScales.objects.filter(patient_session_id=patient_detail_id,
                                                                             scale_id=13)
        if not patient_scale_manic:
            # 级联分配r_patient_scales表
            scale = scales_models.DScales.objects.filter(id=13)
            patients_dao.add_rscales(scale, patient_detail_id)
        # 修改对应的表
        RPatientManicsymptom_object = scales_models.RPatientManicsymptom(patient_session_id=patient_detail_id,scale_id=13, doctor_id=2,create_time=end_date,update_time=end_date,
                                                                         question1=scale_manic['question1'],question2=scale_manic['question2'],question3_1=scale_manic['question3_1'],
                                                                         question3_2=scale_manic['question3_2'],question3_3=scale_manic['question3_3'],question3_4=scale_manic['question3_4'],
                                                                         question3_5=scale_manic['question3_5'],question3_6=scale_manic['question3_6'],question3_7=scale_manic['question3_7'],
                                                                         question3_8=scale_manic['question3_8'],question3_9=scale_manic['question3_9'],question3_10=scale_manic['question3_10'],
                                                                         question3_11=scale_manic['question3_11'],question3_12=scale_manic['question3_12'],question3_13=scale_manic['question3_13'],
                                                                         question3_14=scale_manic['question3_14'],question3_15=scale_manic['question3_15'],question3_16=scale_manic['question3_16'],
                                                                         question3_17=scale_manic['question3_17'],question3_18=scale_manic['question3_18'],question3_19=scale_manic['question3_19'],
                                                                         question3_20=scale_manic['question3_20'],question3_21=scale_manic['question3_21'],question3_22=scale_manic['question3_22'],
                                                                         question3_23=scale_manic['question3_23'],question3_24=scale_manic['question3_24'],question3_25=scale_manic['question3_25'],
                                                                         question3_26=scale_manic['question3_26'],question3_27=scale_manic['question3_27'],question3_28=scale_manic['question3_28'],
                                                                         question3_29=scale_manic['question3_29'],question3_30=scale_manic['question3_30'],question3_31=scale_manic['question3_31'],
                                                                         question3_32=scale_manic['question3_32'],question3_33=scale_manic['question3_33'],question4_1=scale_manic['question4_1'],
                                                                         question4_2=scale_manic['question4_2'],question4_3=scale_manic['question4_3'],question4_4=scale_manic['question4_4'],
                                                                         question5=scale_manic['question5'],question6_1=scale_manic['question6'],question6_2=scale_manic['question6'],
                                                                         question7=scale_manic['question7'],question8=scale_manic['question8'],question9=scale_manic['question9'],
                                                                         question10=scale_manic['question10'],total_score=scale_manic['total_score'])
        # scales_dao.add_manicsymptom_database(RPatientManicsymptom_object,1)
        RPatientManicsymptom_object.save()
        scales_dao.update_rscales_state(RPatientManicsymptom_object.patient_session_id, RPatientManicsymptom_object.scale_id, 1)

    # scale_manic_duration：答题时间
    scale_manic_duration = patient_data['data']['scale_manic_duration']
    print("scale_manic_duration: "+str(scale_manic_duration))

    # scale_happiness：斯奈斯和汉密尔顿快乐量表
    scale_happiness = patient_data['data']['scale_happiness']
    print("scale_happiness: "+str(scale_happiness))
    RPatientHappiness_pre = scales_models.RPatientHappiness.objects.filter(patient_session_id=patient_detail_id).first()
    # 删除原有量表
    if RPatientHappiness_pre is not None and scale_happiness:
        RPatientHappiness_pre.delete()
    if scale_happiness:
        # scale_handy表示判断非空，python中空字典为False，非空字典为True
        patient_scale_happiness = scales_models.RPatientScales.objects.filter(patient_session_id=patient_detail_id,
                                                                          scale_id=14)
        if not patient_scale_happiness:
            # 级联分配r_patient_scales表
            scale = scales_models.DScales.objects.filter(id=14)
            patients_dao.add_rscales(scale, patient_detail_id)
        # 修改对应的表
        RPatientHappiness_object = scales_models.RPatientHappiness(patient_session_id=patient_detail_id,scale_id=14, doctor_id=2,create_time=end_date,update_time=end_date,
                                                                   question1_answer=scale_happiness['question1_answer'],question2_answer=scale_happiness['question2_answer'],question3_answer=scale_happiness['question3_answer'],
                                                                   question4_answer=scale_happiness['question4_answer'],question5_answer=scale_happiness['question5_answer'],question6_answer=scale_happiness['question6_answer'],
                                                                   question7_answer=scale_happiness['question7_answer'],question8_answer=scale_happiness['question8_answer'],question9_answer=scale_happiness['question9_answer'],
                                                                   question10_answer=scale_happiness['question10_answer'],question11_answer=scale_happiness['question11_answer'],question12_answer=scale_happiness['question12_answer'],
                                                                   question13_answer=scale_happiness['question13_answer'],question14_answer=scale_happiness['question14_answer'],total_score=scale_happiness['total_score'])
        #scales_dao.add_happiness_database(RPatientHappiness_object,1)
        RPatientHappiness_object.save()
        scales_dao.update_rscales_state(RPatientHappiness_object.patient_session_id, RPatientHappiness_object.scale_id, 1)


    # scale_happiness_duration：答题时间
    scale_happiness_duration = patient_data['data']['scale_happiness_duration']
    print("scale_happiness_duration: "+str(scale_happiness_duration))

    # scale_pleasure：快感体验能力量表表
    scale_pleasure = patient_data['data']['scale_pleasure']
    print("scale_pleasure: "+str(scale_pleasure))
    RPatientPleasure_pre = scales_models.RPatientPleasure.objects.filter(patient_session_id=patient_detail_id).first()
    # 删除原有量表
    if RPatientPleasure_pre is not None and scale_pleasure:
        RPatientPleasure_pre.delete()
    if scale_pleasure:
        # scale_handy表示判断非空，python中空字典为False，非空字典为True
        patient_scale_pleasure = scales_models.RPatientScales.objects.filter(patient_session_id=patient_detail_id,
                                                                              scale_id=15)
        if not patient_scale_pleasure:
            # 级联分配r_patient_scales表
            scale = scales_models.DScales.objects.filter(id=15)
            patients_dao.add_rscales(scale, patient_detail_id)
        # 修改对应的表
        RPatientPleasure_object = scales_models.RPatientPleasure(patient_session_id=patient_detail_id,scale_id=15, doctor_id=2,create_time=end_date,update_time=end_date,
                                                                 question1_answer=scale_pleasure['question1_answer'],question2_answer=scale_pleasure['question2_answer'],question3_answer=scale_pleasure['question3_answer'],
                                                                 question4_answer=scale_pleasure['question4_answer'],question5_answer=scale_pleasure['question5_answer'],question6_answer=scale_pleasure['question6_answer'],
                                                                 question7_answer=scale_pleasure['question7_answer'],question8_answer=scale_pleasure['question8_answer'],question9_answer=scale_pleasure['question9_answer'],
                                                                 question10_answer=scale_pleasure['question10_answer'],question11_answer=scale_pleasure['question11_answer'],question12_answer=scale_pleasure['question12_answer'],
                                                                 question13_answer=scale_pleasure['question13_answer'],question14_answer=scale_pleasure['question14_answer'],question15_answer=scale_pleasure['question15_answer'],
                                                                 question16_answer=scale_pleasure['question16_answer'],question17_answer=scale_pleasure['question17_answer'],question18_answer=scale_pleasure['question18_answer'],
                                                                 total_score=scale_pleasure['total_score'],expectation_score=scale_pleasure['expectation_score'],consume_score=scale_pleasure['consume_score'])
        #scales_dao.add_pleasure_database(RPatientPleasure_object,1)
        RPatientPleasure_object.save()
        scales_dao.update_rscales_state(RPatientPleasure_object.patient_session_id, RPatientPleasure_object.scale_id, 1)

    # scale_pleasure_duration：答题时间
    scale_pleasure_duration = patient_data['data']['scale_pleasure_duration']
    print("scale_pleasure_duration: "+str(scale_pleasure_duration))

    # scale_growth：儿童成长经历
    scale_growth = patient_data['data']['scale_growth']
    print("scale_growth: "+str(scale_growth))
    RPatientGrowth_pre = scales_models.RPatientGrowth.objects.filter(patient_session_id=patient_detail_id).first()
    # 删除原有量表
    if RPatientGrowth_pre is not None and scale_growth:
        RPatientGrowth_pre.delete()
    if scale_growth:
        # scale_handy表示判断非空，python中空字典为False，非空字典为True
        patient_scale_growth = scales_models.RPatientScales.objects.filter(patient_session_id=patient_detail_id,
                                                                             scale_id=16)
        if not patient_scale_growth:
            # 级联分配r_patient_scales表
            scale = scales_models.DScales.objects.filter(id=16)
            patients_dao.add_rscales(scale, patient_detail_id)
        # 修改对应的表
        RPatientGrowth_object = scales_models.RPatientGrowth(patient_session_id=patient_detail_id,scale_id=16, doctor_id=2,create_time=end_date,update_time=end_date,
                                                             question1_answer=scale_growth['question1_answer'],question2_answer=scale_growth['question2_answer'],question3_answer=scale_growth['question3_answer'],
                                                             question4_answer=scale_growth['question4_answer'],question5_answer=scale_growth['question5_answer'],question6_answer=scale_growth['question6_answer'],
                                                             question7_answer=scale_growth['question7_answer'],question8_answer=scale_growth['question8_answer'],question9_answer=scale_growth['question9_answer'],
                                                             question10_answer=scale_growth['question10_answer'],question11_answer=scale_growth['question11_answer'],question12_answer=scale_growth['question12_answer'],
                                                             question13_answer=scale_growth['question13_answer'],question14_answer=scale_growth['question14_answer'],question15_answer=scale_growth['question15_answer'],
                                                             question16_answer=scale_growth['question16_answer'],question17_answer=scale_growth['question17_answer'],question18_answer=scale_growth['question18_answer'],
                                                             question19_answer=scale_growth['question19_answer'],question20_answer=scale_growth['question20_answer'],question21_answer=scale_growth['question21_answer'],
                                                             question22_answer=scale_growth['question22_answer'],question23_answer=scale_growth['question23_answer'],question24_answer=scale_growth['question24_answer'],
                                                             question25_answer=scale_growth['question25_answer'],question26_answer=scale_growth['question26_answer'],question27_answer=scale_growth['question27_answer'],
                                                             question28_answer=scale_growth['question28_answer'],first_sex_age=scale_growth['first_sex_age'],emotion_abuse_score=scale_growth['emotion_abuse_score'],
                                                             body_abuse_score=scale_growth['body_abuse_score'],sex_abuse_score=scale_growth['sex_abuse_score'],emotion_ignore_score=scale_growth['emotion_ignore_score'],
                                                             body_ignore_score=scale_growth['body_ignore_score'])
        #scales_dao.add_growth_database(RPatientGrowth_object,1)
        RPatientGrowth_object.save()
        scales_dao.update_rscales_state(RPatientGrowth_object.patient_session_id, RPatientGrowth_object.scale_id, 1)

    # scale_growth_duration：答题时间
    scale_growth_duration = patient_data['data']['scale_growth_duration']
    print("scale_growth_duration: "+str(scale_growth_duration))

    # scale_cerq：认知情绪调节
    scale_cerq = patient_data['data']['scale_cerq']
    print("scale_cerq: "+str(scale_cerq))
    RPatientCognitiveEmotion_pre = scales_models.RPatientCognitiveEmotion.objects.filter(patient_session_id=patient_detail_id).first()
    # 删除原有量表
    if RPatientCognitiveEmotion_pre is not None and scale_cerq:
        RPatientCognitiveEmotion_pre.delete()
    if scale_cerq:
        # scale_handy表示判断非空，python中空字典为False，非空字典为True
        patient_scale_cerq = scales_models.RPatientScales.objects.filter(patient_session_id=patient_detail_id,
                                                                           scale_id=17)
        if not patient_scale_cerq:
            # 级联分配r_patient_scales表
            scale = scales_models.DScales.objects.filter(id=17)
            patients_dao.add_rscales(scale, patient_detail_id)
        # 修改对应的表
        RPatientCognitiveEmotion_object = scales_models.RPatientCognitiveEmotion(patient_session_id=patient_detail_id,scale_id=17, doctor_id=2,create_time=end_date,update_time=end_date,
                                                                                 question1_answer=scale_cerq['question1_answer'],question2_answer=scale_cerq['question2_answer'],question3_answer=scale_cerq['question3_answer'],
                                                                                 question4_answer=scale_cerq['question4_answer'],question5_answer=scale_cerq['question5_answer'],question6_answer=scale_cerq['question6_answer'],
                                                                                 question7_answer=scale_cerq['question7_answer'],question8_answer=scale_cerq['question8_answer'],question9_answer=scale_cerq['question9_answer'],
                                                                                 question10_answer=scale_cerq['question10_answer'],question11_answer=scale_cerq['question11_answer'],question12_answer=scale_cerq['question12_answer'],
                                                                                 question13_answer=scale_cerq['question13_answer'],question14_answer=scale_cerq['question14_answer'],question15_answer=scale_cerq['question15_answer'],
                                                                                 question16_answer=scale_cerq['question16_answer'],question17_answer=scale_cerq['question17_answer'],question18_answer=scale_cerq['question18_answer'],
                                                                                 question19_answer=scale_cerq['question19_answer'],question20_answer=scale_cerq['question20_answer'],question21_answer=scale_cerq['question21_answer'],
                                                                                 question22_answer=scale_cerq['question22_answer'],question23_answer=scale_cerq['question23_answer'],question24_answer=scale_cerq['question24_answer'],
                                                                                 question25_answer=scale_cerq['question25_answer'],question26_answer=scale_cerq['question26_answer'],question27_answer=scale_cerq['question27_answer'],
                                                                                 question28_answer=scale_cerq['question28_answer'],question29_answer=scale_cerq['question29_answer'],question30_answer=scale_cerq['question30_answer'],
                                                                                 question31_answer=scale_cerq['question31_answer'],question32_answer=scale_cerq['question32_answer'],question33_answer=scale_cerq['question33_answer'],
                                                                                 question34_answer=scale_cerq['question34_answer'],question35_answer=scale_cerq['question35_answer'],question36_answer=scale_cerq['question36_answer'],
                                                                                 total_score=scale_cerq['total_score'],blame_self=scale_cerq['blame_self'],blame_others=scale_cerq['blame_others'],meditation=scale_cerq['meditation'],
                                                                                 catastrophization=scale_cerq['catastrophization'],accepted=scale_cerq['accepted'],positive_refocus=scale_cerq['positive_refocus'],
                                                                                 program_refocus=scale_cerq['program_refocus'],positive_evaluation=scale_cerq['positive_evaluation'],rational_analysis=scale_cerq['rational_analysis'])
        # scales_dao.add_cognitive_emotion_database(RPatientCognitiveEmotion_object,1)
        RPatientCognitiveEmotion_object.save()
        scales_dao.update_rscales_state(RPatientCognitiveEmotion_object.patient_session_id, RPatientCognitiveEmotion_object.scale_id, 1)

    # scale_cerq_duration：答题时间
    scale_cerq_duration = patient_data['data']['scale_cerq_duration']
    print("scale_cerq_duration: "+str(scale_cerq_duration))

    # scale_asles：青少年生活事件
    scale_asles = patient_data['data']['scale_asles']
    print("scale_asles: "+str(scale_asles))
    RPatientAdolescentEvents_pre = scales_models.RPatientAdolescentEvents.objects.filter(patient_session_id=patient_detail_id).first()
    # 删除原有量表
    if RPatientAdolescentEvents_pre is not None and scale_asles:
        RPatientAdolescentEvents_pre.delete()
    if scale_asles:
        # scale_handy表示判断非空，python中空字典为False，非空字典为True
        patient_scale_asles = scales_models.RPatientScales.objects.filter(patient_session_id=patient_detail_id,
                                                                         scale_id=18)
        if not patient_scale_asles:
            # 级联分配r_patient_scales表
            scale = scales_models.DScales.objects.filter(id=18)
            patients_dao.add_rscales(scale, patient_detail_id)
        # 修改对应的表
        RPatientAdolescentEvents_object = scales_models.RPatientAdolescentEvents(patient_session_id=patient_detail_id,scale_id=18, doctor_id=2,create_time=end_date,update_time=end_date,
                                                                                 question1_answer=scale_asles['question1_answer'],question2_answer=scale_asles['question2_answer'],question3_answer=scale_asles['question3_answer'],
                                                                                 question4_answer=scale_asles['question4_answer'],question5_answer=scale_asles['question5_answer'],question6_answer=scale_asles['question6_answer'],
                                                                                 question7_answer=scale_asles['question7_answer'],question8_answer=scale_asles['question8_answer'],question9_answer=scale_asles['question9_answer'],
                                                                                 question10_answer=scale_asles['question10_answer'],question11_answer=scale_asles['question11_answer'],question12_answer=scale_asles['question12_answer'],
                                                                                 question13_answer=scale_asles['question13_answer'],question14_answer=scale_asles['question14_answer'],question15_answer=scale_asles['question15_answer'],
                                                                                 question16_answer=scale_asles['question16_answer'],question17_answer=scale_asles['question17_answer'],question18_answer=scale_asles['question18_answer'],
                                                                                 question19_answer=scale_asles['question19_answer'],question20_answer=scale_asles['question20_answer'],question21_answer=scale_asles['question21_answer'],
                                                                                 question22_answer=scale_asles['question22_answer'],question23_answer=scale_asles['question23_answer'],question24_answer=scale_asles['question24_answer'],
                                                                                 question25_answer=scale_asles['question25_answer'],question26_answer=scale_asles['question26_answer'],question27_answer=scale_asles['question27_answer'],
                                                                                 total_score=scale_asles['total_score'])
        # scales_dao.add_adolescent_events_database(RPatientAdolescentEvents_object,1)
        RPatientAdolescentEvents_object.save()
        scales_dao.update_rscales_state(RPatientAdolescentEvents_object.patient_session_id, RPatientAdolescentEvents_object.scale_id, 1)

    # scale_asles_duration：答题时间
    scale_asles_duration = patient_data['data']['scale_asles_duration']
    print("scale_asles_duration: "+str(scale_asles_duration))

    # scale_embu：简式父母
    scale_embu = patient_data['data']['scale_embu']
    print("scale_embu: "+str(scale_embu))
    RPatientSembu_pre = scales_models.RPatientSembu.objects.filter(patient_session_id=patient_detail_id).first()
    # 删除原有量表
    if RPatientSembu_pre is not None and scale_embu:
        RPatientSembu_pre.delete()
    if scale_embu:
        # scale_handy表示判断非空，python中空字典为False，非空字典为True
        patient_scale_embu = scales_models.RPatientScales.objects.filter(patient_session_id=patient_detail_id,
                                                                          scale_id=19)
        if not patient_scale_embu:
            # 级联分配r_patient_scales表
            scale = scales_models.DScales.objects.filter(id=19)
            patients_dao.add_rscales(scale, patient_detail_id)
        # 修改对应的表
        RPatientSembu_object = scales_models.RPatientSembu(patient_session_id=patient_detail_id,scale_id=19, doctor_id=2,create_time=end_date,update_time=end_date,
                                                           year_of_school=scale_embu['year_of_school'],grade=scale_embu['grade'],region=scale_embu['region'],
                                                           mark_level=scale_embu['mark_level'],parents_status=scale_embu['parents_status'],question1_father=scale_embu['question1_father'],
                                                           question1_mother=scale_embu['question1_mother'],question2_father=scale_embu['question2_father'],question2_mother=scale_embu['question2_mother'],
                                                           question3_father=scale_embu['question3_father'],question3_mother=scale_embu['question3_mother'],question4_father=scale_embu['question4_father'],
                                                           question4_mother=scale_embu['question4_mother'],question5_father=scale_embu['question5_father'],question5_mother=scale_embu['question5_mother'],
                                                           question6_father=scale_embu['question6_father'],question6_mother=scale_embu['question6_mother'],question7_father=scale_embu['question7_father'],
                                                           question7_mother=scale_embu['question7_mother'],question8_father=scale_embu['question8_father'],question8_mother=scale_embu['question8_mother'],
                                                           question9_father=scale_embu['question9_father'],question9_mother=scale_embu['question9_mother'],question10_father=scale_embu['question10_father'],
                                                           question10_mother=scale_embu['question10_mother'],question11_father=scale_embu['question11_father'],question11_mother=scale_embu['question11_mother'],
                                                           question12_father=scale_embu['question12_father'],question12_mother=scale_embu['question12_mother'],question13_father=scale_embu['question13_father'],
                                                           question13_mother=scale_embu['question13_mother'],question14_father=scale_embu['question14_father'],question14_mother=scale_embu['question14_mother'],
                                                           question15_father=scale_embu['question15_father'],question15_mother=scale_embu['question15_mother'],question16_father=scale_embu['question16_father'],
                                                           question16_mother=scale_embu['question16_mother'],question17_father=scale_embu['question17_father'],question17_mother=scale_embu['question17_mother'],
                                                           question18_father=scale_embu['question18_father'],question18_mother=scale_embu['question18_mother'],question19_father=scale_embu['question19_father'],
                                                           question19_mother=scale_embu['question19_mother'],question20_father=scale_embu['question20_father'],question20_mother=scale_embu['question20_mother'],
                                                           question21_father=scale_embu['question21_father'],question21_mother=scale_embu['question21_mother'],refusal_mother=scale_embu['refusal_mother'],
                                                           refusal_father=scale_embu['refusal_father'],emotional_warmth_mother=scale_embu['emotional_warmth_mother'],emotional_warmth_father=scale_embu['emotional_warmth_father'],
                                                           overprotection_mother=scale_embu['overprotection_mother'],overprotection_father=scale_embu['overprotection_father'])
        # scales_dao.add_sembu_database(RPatientSembu_object,1)
        RPatientSembu_object.save()
        scales_dao.update_rscales_state(RPatientSembu_object.patient_session_id, RPatientSembu_object.scale_id, 1)

    # scale_embu_duration：答题时间
    scale_embu_duration = patient_data['data']['scale_embu_duration']
    print("scale_embu_duration: "+str(scale_embu_duration))

    # scale_atq：自动思维
    scale_atq = patient_data['data']['scale_atq']
    print("scale_atq: "+str(scale_atq))
    RPatientAtq_pre = scales_models.RPatientAtq.objects.filter(patient_session_id=patient_detail_id).first()
    # 删除原有量表
    if RPatientAtq_pre is not None and scale_atq:
        RPatientAtq_pre.delete()
    if scale_atq:
        # scale_handy表示判断非空，python中空字典为False，非空字典为True
        patient_scale_atq = scales_models.RPatientScales.objects.filter(patient_session_id=patient_detail_id,
                                                                         scale_id=20)
        if not patient_scale_atq:
            # 级联分配r_patient_scales表
            scale = scales_models.DScales.objects.filter(id=20)
            patients_dao.add_rscales(scale, patient_detail_id)
        # 修改对应的表
        RPatientAtq_object = scales_models.RPatientAtq(patient_session_id=patient_detail_id,scale_id=20, doctor_id=2,create_time=end_date,update_time=end_date,
                                                       question1_answer=scale_atq['question1_answer'],question2_answer=scale_atq['question2_answer'],question3_answer=scale_atq['question3_answer'],
                                                       question4_answer=scale_atq['question4_answer'],question5_answer=scale_atq['question5_answer'],question6_answer=scale_atq['question6_answer'],
                                                       question7_answer=scale_atq['question7_answer'],question8_answer=scale_atq['question8_answer'],question9_answer=scale_atq['question9_answer'],
                                                       question10_answer=scale_atq['question10_answer'],question11_answer=scale_atq['question11_answer'],question12_answer=scale_atq['question12_answer'],
                                                       question13_answer=scale_atq['question13_answer'],question14_answer=scale_atq['question14_answer'],question15_answer=scale_atq['question15_answer'],
                                                       question16_answer=scale_atq['question16_answer'],question17_answer=scale_atq['question17_answer'],question18_answer=scale_atq['question18_answer'],
                                                       question19_answer=scale_atq['question19_answer'],question20_answer=scale_atq['question20_answer'],question21_answer=scale_atq['question21_answer'],
                                                       question22_answer=scale_atq['question22_answer'],question23_answer=scale_atq['question23_answer'],question24_answer=scale_atq['question24_answer'],
                                                       question25_answer=scale_atq['question25_answer'],question26_answer=scale_atq['question26_answer'],question27_answer=scale_atq['question27_answer'],
                                                       question28_answer=scale_atq['question28_answer'],question29_answer=scale_atq['question29_answer'],question30_answer=scale_atq['question30_answer'],
                                                       total_score=scale_atq['total_score'])
        # scales_dao.add_atq_database(RPatientAtq_object,1)
        RPatientAtq_object.save()
        scales_dao.update_rscales_state(RPatientAtq_object.patient_session_id, RPatientAtq_object.scale_id, 1)


    # scale_atq_duration：答题时间
    scale_atq_duration = patient_data['data']['scale_atq_duration']
    print("scale_atq_duration: "+str(scale_atq_duration))

    # scale_phq：抑郁症
    scale_phq = patient_data['data']['scale_phq']
    print("scale_phq: " + str(scale_phq))
    phq_pre = scales_models.RPatientPhq.objects.filter(patient_session_id=patient_detail_id).first()
    # 删除原有量表
    if phq_pre is not None and scale_phq:
        phq_pre.delete()
    if scale_phq:
        # scale_handy表示判断非空，python中空字典为False，非空字典为True
        patient_scale_phq = scales_models.RPatientScales.objects.filter(patient_session_id=patient_detail_id,
                                                                        scale_id=29)
        if not patient_scale_phq:
            # 级联分配r_patient_scales表
            scale = scales_models.DScales.objects.filter(id=29)
            patients_dao.add_rscales(scale, patient_detail_id)
        RPatientPhq_object = scales_models.RPatientPhq(patient_session_id=patient_detail_id, scale_id=29,
                                                       question1_answer=scale_phq['question1_answer'],
                                                       question2_answer=scale_phq['question2_answer'],
                                                       question3_answer=scale_phq['question3_answer'],
                                                       question4_answer=scale_phq['question4_answer'],
                                                       question5_answer=scale_phq['question5_answer'],
                                                       question6_answer=scale_phq['question6_answer'],
                                                       question7_answer=scale_phq['question7_answer'],
                                                       question8_answer=scale_phq['question8_answer'],
                                                       question9_answer=scale_phq['question9_answer'],
                                                       total_score=scale_phq['total_score'], doctor_id=2,
                                                       create_time=end_date, update_time=end_date)
        # scales_dao.add_Phq_database(RPatientPhq_object, 1)
        RPatientPhq_object.save()
        scales_dao.update_rscales_state(RPatientPhq_object.patient_session_id, RPatientPhq_object.scale_id, 1)

    # scale_phq_duration：答题时间
    scale_phq_duration = patient_data['data']['scale_phq_duration']
    print("scale_phq_duration: "+str(scale_phq_duration))

    # scale_gad：gad-7
    scale_gad = patient_data['data']['scale_gad']
    print("scale_gad: " + str(scale_gad))
    gad_pre = scales_models.RPatientGad.objects.filter(patient_session_id=patient_detail_id).first()
    # 删除原有量表
    if gad_pre is not None and scale_gad:
        gad_pre.delete()
    if scale_gad:
        # scale_handy表示判断非空，python中空字典为False，非空字典为True
        patient_scale_gad = scales_models.RPatientScales.objects.filter(patient_session_id=patient_detail_id,
                                                                        scale_id=30)
        if not patient_scale_gad:
            # 级联分配r_patient_scales表
            scale = scales_models.DScales.objects.filter(id=30)
            patients_dao.add_rscales(scale, patient_detail_id)
        RPatientGad_object = scales_models.RPatientGad(patient_session_id=patient_detail_id, scale_id=30,
                                                       question1_answer=scale_gad['question1_answer'],
                                                       question2_answer=scale_gad['question2_answer'],
                                                       question3_answer=scale_gad['question3_answer'],
                                                       question4_answer=scale_gad['question4_answer'],
                                                       question5_answer=scale_gad['question5_answer'],
                                                       question6_answer=scale_gad['question6_answer'],
                                                       question7_answer=scale_gad['question7_answer'],
                                                       total_score=scale_gad['total_score'], doctor_id=2,
                                                       create_time=end_date, update_time=end_date)
        # scales_dao.add_Gad_database(RPatientGad_object, 1)
        RPatientGad_object.save()
        scales_dao.update_rscales_state(RPatientGad_object.patient_session_id, RPatientGad_object.scale_id, 1)

    # scale_gad_duration：答题时间
    scale_gad_duration = patient_data['data']['scale_gad_duration']
    print("scale_gad_duration: "+str(scale_gad_duration))

    # scale_insomnia：失眠
    scale_insomnia = patient_data['data']['scale_insomnia']
    print("scale_insomnia: " + str(scale_insomnia))
    insomnia_pre = scales_models.RPatientInsomnia.objects.filter(patient_session_id=patient_detail_id).first()
    # 删除原有量表
    if insomnia_pre is not None and scale_insomnia:
        insomnia_pre.delete()
    if scale_insomnia:
        # scale_handy表示判断非空，python中空字典为False，非空字典为True
        patient_scale_insomnia = scales_models.RPatientScales.objects.filter(patient_session_id=patient_detail_id,
                                                                        scale_id=31)
        if not patient_scale_insomnia:
            # 级联分配r_patient_scales表
            scale = scales_models.DScales.objects.filter(id=31)
            patients_dao.add_rscales(scale, patient_detail_id)
        RPatientInsomnia_object = scales_models.RPatientInsomnia(patient_session_id=patient_detail_id, scale_id=31,
                                                                 question1_answer=scale_insomnia['question1_answer'],
                                                                 question2_answer=scale_insomnia['question2_answer'],
                                                                 question3_answer=scale_insomnia['question3_answer'],
                                                                 question4_answer=scale_insomnia['question4_answer'],
                                                                 question5_answer=scale_insomnia['question5_answer'],
                                                                 question6_answer=scale_insomnia['question6_answer'],
                                                                 question7_answer=scale_insomnia['question7_answer'],
                                                                 total_score=scale_insomnia['total_score'], doctor_id=2,
                                                                 create_time=end_date, update_time=end_date)
        # scales_dao.add_Insomnia_database(RPatientInsomnia_object, 1)
        RPatientInsomnia_object.save()
        scales_dao.update_rscales_state(RPatientInsomnia_object.patient_session_id, RPatientInsomnia_object.scale_id, 1)

    # scale_insomnia_duration：答题时间
    scale_insomnia_duration = patient_data['data']['scale_insomnia_duration']
    print("scale_insomnia_duration: "+str(scale_insomnia_duration))

    # scale_pss：压力量表
    scale_pss = patient_data['data']['scale_pss']
    print("scale_pss: " + str(scale_pss))
    pss_pre = scales_models.RPatientPss.objects.filter(patient_session_id=patient_detail_id).first()
    # 删除原有量表
    if pss_pre is not None and scale_pss:
        pss_pre.delete()
    if scale_pss:
        # scale_handy表示判断非空，python中空字典为False，非空字典为True
        patient_scale_pss = scales_models.RPatientScales.objects.filter(patient_session_id=patient_detail_id,
                                                                             scale_id=32)
        if not patient_scale_pss:
            # 级联分配r_patient_scales表
            scale = scales_models.DScales.objects.filter(id=32)
            patients_dao.add_rscales(scale, patient_detail_id)
        RPatientPss_object = scales_models.RPatientPss(patient_session_id=patient_detail_id, scale_id=32,
                                                       question1_answer=scale_pss['question1_answer'],
                                                       question2_answer=scale_pss['question2_answer'],
                                                       question3_answer=scale_pss['question3_answer'],
                                                       question4_answer=scale_pss['question4_answer'],
                                                       question5_answer=scale_pss['question5_answer'],
                                                       question6_answer=scale_pss['question6_answer'],
                                                       question7_answer=scale_pss['question7_answer'],
                                                       question8_answer=scale_pss['question8_answer'],
                                                       question9_answer=scale_pss['question9_answer'],
                                                       question10_answer=scale_pss['question10_answer'],
                                                       question11_answer=scale_pss['question11_answer'],
                                                       question12_answer=scale_pss['question12_answer'],
                                                       question13_answer=scale_pss['question13_answer'],
                                                       question14_answer=scale_pss['question14_answer'],
                                                       total_score=scale_pss['total_score'], doctor_id=2,
                                                       create_time=end_date, update_time=end_date)
        # scales_dao.add_pss_database(RPatientPss_object,1)
        RPatientPss_object.save()
        scales_dao.update_rscales_state(RPatientPss_object.patient_session_id, RPatientPss_object.scale_id, 1)

    # scale_pss_duration：答题时间
    scale_pss_duration = patient_data['data']['scale_pss_duration']
    print("scale_pss_duration: "+str(scale_pss_duration))

    print("patient: "+str(patient_id)+" session: "+str(session_id)+" insert over ! ")

# 分配他评、认知等非自评量表
def insert_patient_scale_interface(patient_id,session_id):
    patient_session_id = patients_dao.get_patient_detail_byPatientIdAndSessionId(patient_id, session_id).id
    #中国利手量表
    patient_scale_handy = scales_models.RPatientScales.objects.filter(patient_session_id=patient_session_id, scale_id=6)
    if not patient_scale_handy:
        # 级联分配r_patient_scales表
        scale = scales_models.DScales.objects.filter(id=6)
        patients_dao.add_rscales(scale, patient_session_id)
        print(str(patient_id) + ',' + str(session_id) + 'handy insert success')
    else:
        print(str(patient_id) + ',' + str(session_id) + 'handy exists')

    #汉密尔顿抑郁量表（HAMD-17）
    patient_scale_hamd = scales_models.RPatientScales.objects.filter(patient_session_id=patient_session_id,scale_id=7)
    if not patient_scale_hamd:
        # 级联分配r_patient_scales表
        scale = scales_models.DScales.objects.filter(id=7)
        patients_dao.add_rscales(scale, patient_session_id)
        print(str(patient_id)+','+str(session_id)+'hamd insert success')
    else:
        print(str(patient_id)+','+str(session_id)+'hamd exists')
    #汉密尔顿焦虑量表（HAMA）
    patient_scale_hama = scales_models.RPatientScales.objects.filter(patient_session_id=patient_session_id, scale_id=8)
    if not patient_scale_hama:
        # 级联分配r_patient_scales表
        scale = scales_models.DScales.objects.filter(id=8)
        patients_dao.add_rscales(scale, patient_session_id)
        print(str(patient_id) + ',' + str(session_id) + 'hama insert success')
    else:
        print(str(patient_id) + ',' + str(session_id) + 'hama exists')

    #杨氏躁狂量表（YMRS）
    patient_scale_ymrs = scales_models.RPatientScales.objects.filter(patient_session_id=patient_session_id, scale_id=9)
    if not patient_scale_ymrs:
        # 级联分配r_patient_scales表
        scale = scales_models.DScales.objects.filter(id=9)
        patients_dao.add_rscales(scale, patient_session_id)
        print(str(patient_id) + ',' + str(session_id) + 'ymrs insert success')
    else:
        print(str(patient_id) + ',' + str(session_id) + 'ymrs exists')

    #简明精神病量表(BPRS)
    patient_scale_bprs = scales_models.RPatientScales.objects.filter(patient_session_id=patient_session_id, scale_id=10)
    if not patient_scale_bprs:
        # 级联分配r_patient_scales表
        scale = scales_models.DScales.objects.filter(id=10)
        patients_dao.add_rscales(scale, patient_session_id)
        print(str(patient_id) + ',' + str(session_id) + 'bprs insert success')
    else:
        print(str(patient_id) + ',' + str(session_id) + 'bprs exists')

    # 威斯康星卡片分类测验（WCST）
    patient_scale_wcst = scales_models.RPatientScales.objects.filter(patient_session_id=patient_session_id, scale_id=21)
    if not patient_scale_wcst:
        # 级联分配r_patient_scales表
        scale = scales_models.DScales.objects.filter(id=21)
        patients_dao.add_rscales(scale, patient_session_id)
        print(str(patient_id) + ',' + str(session_id) + 'wcst insert success')
    else:
        print(str(patient_id) + ',' + str(session_id) + 'wcst exists')

    # 22
    # 重复成套性神经心理状态测验系统(RBANS)
    patient_scale_rbans = scales_models.RPatientScales.objects.filter(patient_session_id=patient_session_id, scale_id=22)
    if not patient_scale_rbans:
        # 级联分配r_patient_scales表
        scale = scales_models.DScales.objects.filter(id=22)
        patients_dao.add_rscales(scale, patient_session_id)
        print(str(patient_id) + ',' + str(session_id) + 'RBANS insert success')
    else:
        print(str(patient_id) + ',' + str(session_id) + 'RBANS exists')

    # 23
    # 面孔情绪感知能力测试(FEPT)
    patient_scale_fept = scales_models.RPatientScales.objects.filter(patient_session_id=patient_session_id,
                                                                     scale_id=23)
    if not patient_scale_fept:
        # 级联分配r_patient_scales表
        scale = scales_models.DScales.objects.filter(id=23)
        patients_dao.add_rscales(scale, patient_session_id)
        print(str(patient_id) + ',' + str(session_id) + 'fept insert success')
    else:
        print(str(patient_id) + ',' + str(session_id) + 'fept exists')

    # 24
    # 语音情绪感知能力测试(VEPT)
    patient_scale_vept = scales_models.RPatientScales.objects.filter(patient_session_id=patient_session_id,
                                                                                scale_id=24)
    if not patient_scale_vept:
        # 级联分配r_patient_scales表
        scale = scales_models.DScales.objects.filter(id=24)
        patients_dao.add_rscales(scale, patient_session_id)
        print(str(patient_id) + ',' + str(session_id) + 'vept insert success')
    else:
        print(str(patient_id) + ',' + str(session_id) + 'vept exists')

    # 简要病史
    patient_scale_medical_history = scales_models.RPatientScales.objects.filter(patient_session_id=patient_session_id,
                                                                     scale_id=25)
    if not patient_scale_medical_history:
        # 级联分配r_patient_scales表
        scale = scales_models.DScales.objects.filter(id=25)
        patients_dao.add_rscales(scale, patient_session_id)
        print(str(patient_id) + ',' + str(session_id) + 'medical history insert success')
    else:
        print(str(patient_id) + ',' + str(session_id) + 'medical history exists')


    # 磁共振检查情况
    patient_scale_fmri = scales_models.RPatientScales.objects.filter(patient_session_id=patient_session_id,
                                                                     scale_id=26)
    if not patient_scale_fmri:
        # 级联分配r_patient_scales表
        scale = scales_models.DScales.objects.filter(id=26)
        patients_dao.add_rscales(scale, patient_session_id)
        print(str(patient_id) + ',' + str(session_id) + 'fmri insert success')
    else:
        print(str(patient_id) + ',' + str(session_id) + 'fmri exists')

    # r - TMS治疗反馈
    patient_scale_rtms = scales_models.RPatientScales.objects.filter(patient_session_id=patient_session_id,
                                                                               scale_id=27)
    if not patient_scale_rtms:
        # 级联分配r_patient_scales表
        scale = scales_models.DScales.objects.filter(id=27)
        patients_dao.add_rscales(scale, patient_session_id)
        print(str(patient_id) + ',' + str(session_id) + 'rtms insert success')
    else:
        print(str(patient_id) + ',' + str(session_id) + 'rtms exists')

    # 诊断类型
    patient_scale_diagnosis_type = scales_models.RPatientScales.objects.filter(patient_session_id=patient_session_id, scale_id=28)
    if not patient_scale_diagnosis_type:
        # 级联分配r_patient_scales表
        scale = scales_models.DScales.objects.filter(id=28)
        patients_dao.add_rscales(scale, patient_session_id)
        print(str(patient_id) + ',' + str(session_id) + 'diagnosis_type insert success')
    else:
        print(str(patient_id) + ',' + str(session_id) + 'diagnosis_type exists')


