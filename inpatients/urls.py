from . import views
from django.conf.urls import url

urlpatterns = [
    # 上传医嘱信息
    url(r'^upload_medical_advice', views.upload_medical_advice),
    # 添加住院
    url(r'^add_inpatient_info', views.add_inpatient_info),
    # 获取所有住院病人信息
    #url(r'^get_all_inpatient_info', views.get_all_inpatient_info),
    # 获取住院患者详细信息
    url(r'^get_inpatient_detail', views.get_inpatient_detail),

    # 患者设置为出院
    url(r'^out_inpatient', views.out_inpatient),
    # 删除住院患者信息
    url(r'^del_inpatient', views.del_inpatient),
    # 上传病程记录
    url(r'^upload_progress_note', views.upload_progress_note),
    # 读取医嘱记录信息
    url(r'^read_medical_advice', views.read_medical_advice),
    url(r'^update_inpatient_info', views.update_inpatient_info),
    url(r'^get_inpatient_by_search', views.get_inpatient_by_search),
    url(r'^del_inpatient', views.del_inpatient),
    # =============deprecated==================
    url(r'^insert_medical_dict', views.insert_medical_dict),

]