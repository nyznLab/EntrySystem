from . import views
from django.urls import path, include
urlpatterns = [
    path('', views.get_patient_data, name='big_table_main')
]