from . import views
from django.urls import path, include
urlpatterns = [
    path('', views.get_patient_data, name='statistics'),
    path('names/', views.get_names, name='getNames'),
    path('sessions/', views.get_sessions, name='getSessions'),
    path('self_test/', views.get_restructured_self_rating, name='getRestructuredSelfTest')
]