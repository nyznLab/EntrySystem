from . import views
from django.urls import path, include
urlpatterns = [
    path('', views.show_page, name='statistics'),
    path('get_patients/', views.get_patient_data, name='get_data'),
    path('names/', views.get_names, name='getNames'),
    path('sessions/', views.get_sessions, name='getSessions'),
    path('self_test/', views.get_restructured_self_rating, name='getRestructuredSelfTest'),
    path('api/v1/getPatients/', views.getPatients)
]