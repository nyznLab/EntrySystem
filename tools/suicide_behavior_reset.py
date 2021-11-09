from patients.models import DPatientDetail
import patients.dao as patients_dao
from scales.models import RPatientSuicideBehavior
import scales.dao as scales_dao

def fff():
    # patient_session_id_list = RPatientSuicideBehavior.objects.values('patient_session_id')
    # print(patient_session_id_list)
    record_list=RPatientSuicideBehavior.objects.all()
    for record in record_list:
        print(record.patient_session_id)
        # record=RPatientSuicideBehavior.objects.values(patient_session_id)
        scale_queryset = DPatientDetail.objects.filter(id=record.patient_session_id)
        isfirst = scale_queryset[0].session_id
        if(isfirst==1):
            record.first_suicide_action=record.suicide_action
            record.first_suicide_times = record.suicide_times
            record.first_self_harming=record.self_harming
            record.first_self_harming_times = record.self_harming_times
            record.first_suicide_idea=record.suicide_idea
            record.suicide_action=record.suicide_times=record.self_harming=record.self_harming_times=record.suicide_idea=0
            record.save()
            print("AAA")
        else:
            record.first_suicide_action=record.first_suicide_times=record.first_self_harming=record.first_self_harming_times=record.first_suicide_idea=-1
            record.save()
            print("BBB")
fff()