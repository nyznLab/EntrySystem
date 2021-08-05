from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
    path('index', views.index_schedule, name='index_schedule'),  # 待办列表视图
    path('list', views.list_schedule, name='list_schedule'),  # 待办列表数据
    path('list_patient_detail', views.list_patient_detail, name='list_patient_detail'),  # 根据病人编号查询扫描列表
    path('delete/<int:schedule_id>/', views.delete_schedule, name='delete_schedule'),  # 删除待办
    path('delete_batch', views.delete_batch_schedule, name='delete_batch_schedule'),  # 批量删除待办
    path('cancel/<int:schedule_id>/', views.cancel_schedule, name='cancel_schedule'),  # 取消待办
    path('init/<int:schedule_id>/', views.init_schedule, name='init_schedule'),  # 恢复待办
    path('done/<int:schedule_id>/', views.done_schedule, name='done_schedule'),  # 完成待办
    path('check/<int:schedule_id>/', views.check_schedule, name='check_schedule'),  # 检查是否存在待办
    path('edit/<int:schedule_id>/', views.edit_schedule, name='edit_schedule'),  # 编辑待办
    path('create', views.create_schedule, name='create_schedule'),  # 创建待办
    path('toggle', views.toggle_schedule, name='toggle_schedule'),  # 更新“字段”状态
    path('calendar', views.calendar_schedule, name='calendar_schedule'),  # 待办视图（日历）
    path('calendar_list_schedule', views.calendar_list_schedule, name='calendar_list_schedule'),  # 待办列表（日历）
]
