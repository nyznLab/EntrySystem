from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.db.models import Avg, Max, Min
from django.views.decorators.csrf import csrf_exempt
import patients.models as patients_models
import followup.models as followup_models
import patients.dao as patients_dao
import followup.dao as followup_dao
import tools.config as tools_config
import json
import time

#根据筛选条件获取
def get_followup_by_search(request):
    start_time = request.POST.get('start_time')
    end_time = request.POST.get('end_time')
    diagnosis_list = request.POST.getlist('diagnosis_list')
    # followup_list = followup_models.RPatientFollowup.objects.select_related('patient', 'patient_session'). \
    #     values('patient_id'). \
    #     annotate(Max('patient_session__session_id')).order_by('patient_id')
    # if start_time is not None or end_time is not None or diagnosis_list != []:
    #     followup_list = followup_list.filter(patient__diagnosis__in=diagnosis_list,patient_session__scan_date__range=(start_time,end_time))
    # return render(request, 'manage_followup.html', {"followup_list": followup_list})

    patient_id_list=followup_dao.get_all_patient_id()
    last_followup_list=[]
    for patient in patient_id_list:
        patient_id=patient["id"]
        last_followup=followup_dao.get_followup_by_patient_id(patient_id)
        last_followup_list.append(last_followup)
    if start_time is not None or end_time is not None or diagnosis_list != []:
        last_followup_list = last_followup_list.filter(patient__diagnosis__in=diagnosis_list,patient_session__scan_date__range=(start_time,end_time))
    return render(request, 'manage_followup.html', {"followup_list": last_followup_list})

#前台应该使用ajax局部刷新(只是写了，未测试)
def update_followup_intention(request):
    patient_id=request.GET.get('patient_id')
    followup_res=followup_dao.get_followup_by_patient_id(patient_id)
    fields_data = followup_models.RPatientFollowup._meta.fields
    data_dict = followup_res.__dict__
    for ele in fields_data:
        if request.POST.get(ele.name) is not None and request.POST.get(ele.name) is not '':
            data_dict[ele.name] = request.POST.get(ele.name)
    followup_res.save()




#用来第一次向followup表中插数据
# def test():
#     followup_list=followup_models.RPatientFollowup.objects.all()
#     for followup in followup_list:
#         if followup.session_id!=1:
#             patient_id=followup.patient_id
#             first_scan_date=followup_models.RPatientFollowup.objects.all().filter(patient_id=patient_id,session_id=1)[0].first_scan_time
#             followup.first_scan_time=first_scan_date
#         followup.save()
# test()
