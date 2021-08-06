from django.db import models  #用于模型对象和数据库交互
import patients.models as patients_models
import FilesSystem.models as filessystem_models


from FilesSystem.check_files import check_file_save

#新建一条记录
def add_patientfiles_object(patient_session_id):
    filessystem_models.RPatientFiles.objects

#更新字段方法
def update_all_field_info(standard_id,city_type):

    #获取patient_id和session_id
    id_list=standard_id.split('_')
    patient_id=int(id_list[1])
    session_id=int(id_list[2][1:])
    #判断病人编号是否在数据库中存在
    #patient_session_id
    dPatientDetail = patients_models.DPatientDetail.objects.filter(patient_id=patient_id, session_id=session_id)
    if dPatientDetail.count() == 0:
        return None  #数据库中无该病人编号存在，返回为None；
    else:
        patient_session_id=dPatientDetail[0]
        res=check_file_save(standard_id,city_type)
        filessystem_models.RPatientFiles.objects.filter(patient_session_id=patient_session_id).update(create_time=models.DateTimeField(auto_now_add=True),
                                                                                                      update_time=models.DateTimeField(auto_now=True),
                                                                                                      dicom_save=res[0],dicom_quality=res[1],reho_arwdcf_save=res[2],fc_arwsdcf_save=res[3],falff_arwsd_save=res[4],alff_arwsd_save=res[5],voxel_wose_fc=0,audio_save=0,video_save=0)

update_all_field_info('NN_00000001_S001','nanjing')

































