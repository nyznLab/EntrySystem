from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
import patients.models as patients_models
import followup.models as followup_models
import tools.insertCascadeCheck as tools_insertCascadeCheck
import patients.dao as patients_dao
def get_followup_by_patient_id(patient_id):
    followup_res = followup_models.RPatientFollowup.objects.select_related('patient','patient_session').filter(patient_id=patient_id)
    if followup_res.count() == 0:
        return None
    else:
        return followup_res.last()
def get_all_patient_id():
    patient_id_list=patients_models.BPatientBaseInfo.objects.all().values('id').order_by('id')
    return patient_id_list

def get_first_scan_date_by_patientid(patient_id):
    first_scan_detail=patients_models.DPatientDetail.objects.filter(patient_id=patient_id,session_id=1).first()
    first_scan_date=first_scan_detail.scan_date
    return first_scan_date

def del_followup_by_patient_detail_id(patient_detail_id):
    followup_res=followup_models.RPatientFollowup.objects.filter(patient_session=patient_detail_id)
    if followup_res:
        followup_res.delete()

def del_followup_by_patient_id(patient_id):
    patient_followup_list=followup_models.RPatientFollowup.objects.filter(patient_id=patient_id)
    if patient_followup_list.count()>0:
        patient_followup_list.delete()

def add_followup(patient_id,session_id,patient_detail_id,scan_date):
    if session_id!=1:
        scan_date=get_first_scan_date_by_patientid(patient_id)
    followup_res = followup_models.RPatientFollowup(patient_id=patient_id, session_id=session_id,patient_session_id=patient_detail_id,
                                                    first_scan_time=scan_date)
    followup_res.save()