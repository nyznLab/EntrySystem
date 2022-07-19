from django.conf.urls import url
from . import views

urlpatterns = [
    # url(r'^subjectSelfTestbuild', views.subjectSelfTest_build),
    # rtms:
    url(r'^get_rtms_forms', views.get_rtms_forms),
    url(r'^add_rtms', views.add_rtms),

    url(r'^get_self_test_forms', views.get_self_test_forms),
    url(r'^get_other_test_forms', views.get_other_test_forms),
    # 被试详细信息录入
    url(r'^get_general_info_forms', views.get_general_info_forms),
    # 被试认知
    url(r'^get_cognition_forms', views.get_cognition_forms),
    url(r'^select_scales', views.get_select_scales),

    url(r'^get_family_form', views.get_family_form),
    url(r'^get_study_form', views.get_study_form),
    url(r'^get_health_form', views.get_health_form),
    url(r'^get_abuse_form', views.get_abuse_form),
    url(r'^get_other_form', views.get_other_form),
    url(r'^get_chi_form', views.get_chi_form),

    url(r'^get_hamd_17_form', views.get_hamd_17_form),
    url(r'^get_madrs_form', views.get_madrs_form),
    url(r'^get_cgi_form',views.get_cgi_form),
    url(r'^get_hama_form', views.get_hama_form),
    url(r'^get_ymrs_form', views.get_ymrs_form),
    url(r'^get_bprs_form', views.get_bprs_form),
    url(r'^get_wcst_form', views.get_wcst_form),
    url(r'^get_rbans_form', views.get_rbans_form),
    url(r'^get_fept_form', views.get_fept_form),
    url(r'^get_vept_form', views.get_vept_form),
    url(r'^get_patient_medical_history_form', views.get_patient_medical_history_form),
    ##################################################

    url(r'^patient_basic_information', views.patient_basic_information),
    url(r'^add_chinesehandle', views.add_chinesehandle),
    url(r'^add_information_study', views.add_information_study),
    url(r'^add_hamd', views.add_hamd),
    url(r'^add_family_info', views.add_family_info),
    url(r'^add_patient_medical_history', views.add_patient_medical_history),
    url(r'^add_bprs', views.add_bprs),
    url(r'^add_rbans', views.add_rbans),
    url(r'^add_patient_basic_information_health', views.add_patient_basic_information_health),
    url(r'^add_abuse', views.add_abuse),
    url(r'^add_hama', views.add_hama),
    url(r'^add_madrs', views.add_madrs),
    url(r'^add_cgi', views.add_cgi),
    url(r'^add_fept', views.add_fept),
    url(r'^add_vept', views.add_vept),

    ######################################################
    url(r'^add_ymrs', views.add_ymrs),
    url(r'^add_wcst', views.add_wcst),
    url(r'^add_other', views.add_other),
    url(r'^add_study', views.add_information_study),
    url(r'^add_health', views.add_patient_basic_information_health),
    url(r'^skip_scale', views.skip_scale),
    # -----------------------------------------------------------------#
    url(r'^get_check_hama_form', views.get_check_hama_form),
    url(r'^get_check_hamd_17_form', views.get_check_hamd_17_form),
    url(r'^get_check_madrs_form', views.get_check_madrs_form),
    url(r'^get_check_cgi_form', views.get_check_cgi_form),
    url(r'^get_check_ymrs_form', views.get_check_ymrs_form),
    url(r'^get_check_bprs_form', views.get_check_bprs_form),
    url(r'^get_last_url', views.get_last_url),
    url(r'^get_next_url', views.get_next_url),


    url(r'^get_last_baseinfo_url', views.get_last_baseinfo_url),
    url(r'^get_next_baseinfo_url', views.get_next_baseinfo_url),
    url(r'^get_check_wcst_form', views.get_check_wcst_form),
    url(r'^get_check_rbans_form', views.get_check_rbans_form),
    url(r'^get_check_fept_form', views.get_check_fept_form),
    url(r'^get_check_vept_form', views.get_check_vept_form),
    url(r'^get_self_next_url', views.get_self_next_url),
    url(r'^get_self_last_url', views.get_self_last_url),

    # -----------------------------------------------------------------#
    url(r'^get_next_self_scale_url', views.get_next_self_scale_url),
    url(r'^testtesttest', views.testNewAjax),
    url(r'^get_suibe_form', views.get_suibe_form),
    url(r'^add_suibe', views.add_suibe),
    url(r'^get_check_suibe_form', views.get_check_suibe_form),

    url('get_next_question', views.get_next_question),
    url('submit_scale', views.submit_scale),
    url('update_scales_content', views.update_scales_content),
    url('redo_scale', views.redo_scale),
    url('delete_scale_content', views.delete_scale_content),
    url('get_question_by_index', views.get_question_by_index),
    url('get_scale_metadata', views.get_scale_metadata),
    url('get_scale_content_question', views.get_scale_content_question),
    url("self_test_display", views.selfTestDisplay),
    url('self_test', views.selfTest),
    url('get_answer_by_index', views.get_answer_by_index),
    url('get_total_score', views.get_total_score)
]
