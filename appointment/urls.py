from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
    path('index', views.index_appointment, name='index_appointment'), # 预约列表视图
    path('list', views.list_appointment, name='list_appointment'), # 预约列表数据
    path('delete/<int:appointment_id>/', views.delete_appointment, name='delete_appointment'), # 删除预约
    path('delete_batch', views.delete_batch_appointment, name='delete_batch_appointment'), # 批量删除预约
    path('cancel/<int:appointment_id>/', views.cancel_appointment, name='cancel_appointment'), # 取消预约
    path('init/<int:appointment_id>/', views.init_appointment, name='init_appointment'),  # 恢复预约
    path('check_patient/<int:appointment_id>/', views.check_patient, name='check_patient'), # 检查是否是已存在患者
    path('check_in', views.check_in_appointment, name='check_in_appointment'), # 预约报到
    path('check/<int:appointment_id>/', views.check_appointment, name='check_appointment'), # 检查是否存在预约
    path('edit/<int:appointment_id>/', views.edit_appointment, name='edit_appointment'), # 编辑预约
    path('create', views.create_appointment, name='create_appointment'), # 创建预约
    path('calendar', views.calendar_appointment, name='calendar_appointment'),  # 预约视图（日历）
    path('calendar_list_appointment', views.calendar_list_appointment, name='calendar_list_appointment'),  # 预约列表（日历）
]
