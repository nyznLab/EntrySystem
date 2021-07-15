#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：entry_system 
@File ：insert_suicide_behavior.py
@IDE  ：PyCharm 
@Author ：skj
@Date ：7/12/21 11:14 AM 
'''

from patients.models import DPatientDetail
import patients.dao as patients_dao
from scales.models import RPatientScales
from scales.models import RPatientSuicideBehavior
from scales.models import RPatientSuicidal
import scales.dao as scales_dao


def ttt():
    # patient_scales_list=RPatientScales.filter() patient_session_id['id']
    patient_session_id_list=DPatientDetail.objects.values('id')
    print(patient_session_id_list)
    for patient_session_id in patient_session_id_list:
        is_record=RPatientScales.objects.all().filter(patient_session=patient_session_id['id'], scale=33).exists()
        print(is_record, patient_session_id['id'])
        if(not(is_record)):
            create_record=RPatientScales.objects.create(patient_session_id=patient_session_id['id'],scale_id=33,state=0)
            is_suicidal_done=RPatientSuicidal.objects.all().filter(patient_session_id=patient_session_id['id']).exists()
            is_suibe_done = RPatientSuicideBehavior.objects.all().filter(patient_session_id=patient_session_id['id']).exists()
            if(is_suicidal_done and not(is_suibe_done)):
                create_record.state=1
                create_record.save()
                old_suicide=RPatientSuicidal.objects.filter(patient_session_id=patient_session_id['id'])[0]
                suicide_action=old_suicide.suicide_history
                suicide_times=old_suicide.suicide_times
                self_harming_times=old_suicide.self_mutilation_remark
                print(self_harming_times,type(self_harming_times))
                if(old_suicide.self_mutilation_remark !='NULL'and old_suicide.self_mutilation_remark!='0'):
                    self_harming=1
                else:
                    self_harming=0
                suicide_idea=old_suicide.suicide_ideation
                doctor_id=old_suicide.doctor_id
                create_time=old_suicide.create_time
                update_time=old_suicide.update_time
                RPatientSuicideBehavior.objects.create(patient_session_id=patient_session_id['id'],scale_id=33,suicide_action=suicide_action,
                                                       suicide_times=suicide_times,self_harming=self_harming,self_harming_times=self_harming_times,
                                                       suicide_idea=suicide_idea,doctor_id=doctor_id,create_time=create_time,update_time=update_time)
                print(is_record, patient_session_id['id'],suicide_action,suicide_times,self_harming,self_harming_times,suicide_idea,doctor_id,create_time,update_time)


ttt()
