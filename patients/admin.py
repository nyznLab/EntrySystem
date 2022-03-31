from django.contrib import admin
from .models import BPatientAdmission
# Register your models here.

@admin.register(BPatientAdmission)

class BPAdmissionAdmin(admin.ModelAdmin):
    list_display = ('patient_id', 'admission_id', 'is_medical_advice', 'is_progress_note')