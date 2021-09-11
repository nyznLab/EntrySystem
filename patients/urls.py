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

    # 查看、上传长期医嘱以及病程记录
    url(r'^add_patient_ma_or_pn', views.add_medical_advice_or_progress_note),
    # 查看长期医嘱表信息
    url(r'^read_medical_advice', views.read_medical_advice),
    # 查看病程记录信息
    url(r'^read_progress_note', views.read_progress_note),
    # 上传长期医嘱表
    url(r'^upload_medical_advice', views.upload_medical_advice),
    # 上传病程记录
    url(r'^upload_progress_note', views.upload_progress_note),
    # 无需长期医嘱或病程记录，设置数据库相关字段
    url(r'^dont_need_ma', views.dont_need_ma_or_pn),
    # 添加长期医嘱表、病程记录备注
    url(r'^add_ps', views.add_ma_ps),

    # 貌似未使用
    url(r'^subjectDetailInfo', views.subjectDetailInfo),
    url(r'^add_blood', views.add_blood),

    url(r'^get_patient_by_search', views.get_patient_by_search),
    # 使用说明及日志
    url(r'^get_program_log', views.get_program_log),

    # 用来捕获未匹配成功的url
    url(r'', views.get_patient_by_search),



]
