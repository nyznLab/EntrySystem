from django.contrib import admin
from django.urls import path, re_path
from . import views
from django.conf.urls import url
import scales.views as scales_views

urlpatterns = [
    # 返回测试
    # url(r'^test', views.test_view),
    # 创建基本信息
    url(r'^add_patient_baseinfo', views.add_patient_baseinfo),
    # 创建复扫基本信息
    url(r'^add_patient_followup', views.add_patient_followup),
    # 获取病人详细信息
    url(r'^get_patient_detail', views.get_patient_detail),
    # 获取被试统计
    # url(r'^patient_statistics', views.patient_statistics, name='patient_statistics'),
    # 自动生成id
    url(r'^get_generateId_and_nation', views.get_generateId),
    # 添加复扫
    url(r'^get_select_scales', scales_views.get_select_scales),
    # 删除病人记录
    url(r'^del_patient', views.del_patient),
    # 删除复扫记录
    url(r'^del_followup', views.del_followup),
    # 修改病人基本信息
    url(r'^update_base_info', views.update_base_info),
    # 更新patient_detail以及patient_base_info
    url(r'^update_patient_detail', views.update_patient_detail),
    # 修改病人基本信息
    url(r'^update_base_info', views.update_base_info),
    # 貌似未使用
    url(r'^subjectDetailInfo', views.subjectDetailInfo),
    url(r'^del_blood', views.del_blood),
    url(r'^add_blood', views.add_blood),

    url(r'^get_patient_by_search', views.get_patient_by_search),

    # 用来捕获未匹配成功的url
    url(r'', views.get_patient_by_search),


]
