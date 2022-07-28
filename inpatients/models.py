# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

from django.db import models
from patients.models import BPatientBaseInfo
from tools.Utils import get_progress_note_direct,get_out_record_direct,get_medical_advice_direct
class BInpatientInfo(models.Model):
    id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(BPatientBaseInfo, models.DO_NOTHING)
    in_time = models.IntegerField(blank=True, null=True)
    department = models.CharField(max_length=40, blank=True, null=True)
    inpatient_area = models.CharField(max_length=20, blank=True, null=True)
    bed_number = models.CharField(max_length=20, blank=True, null=True)
    inpatient_number = models.CharField(max_length=20, blank=True, null=True)
    in_date = models.DateField(blank=True, null=True)
    out_date = models.DateField(blank=True, null=True)
    out_record = models.FileField(upload_to=get_out_record_direct)
    progress_note = models.FileField(upload_to=get_progress_note_direct)
    medical_advice_path = models.FileField(upload_to=get_medical_advice_direct)
    inpatient_state = models.IntegerField(blank=True, null=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'b_inpatient_info'

class BInpatientData(models.Model):
    DATA_TYPE = (
        (0, '长期医嘱单'),
        (1, '病程记录'),
        (2, '采血化验单')
    )
    id = models.AutoField(primary_key=True)
    inpatient_id = models.IntegerField(blank=True, null=True)
    data_type = models.CharField(max_length=20, blank=True, null=True)
    file = models.TextField(blank=True, null=True)
    data_date = models.DateField(blank=True, null=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    class Meta:
        managed = False
        db_table = 'b_inpatient_data'
        
        
class BInpatientMedicalAdvice(models.Model):
    inpatient = models.ForeignKey('BInpatientInfo', models.DO_NOTHING)
    start_time = models.DateTimeField(blank=True, null=True)
    medical_name = models.CharField(max_length=40, blank=True, null=True)
    dose_num = models.FloatField(blank=True, null=True)
    dose_unit = models.CharField(max_length=10, blank=True, null=True)
    group = models.CharField(max_length=10, blank=True, null=True)
    drug_type = models.CharField(max_length=20, blank=True, null=True)
    type = models.IntegerField(blank=True, null=True)
    usage_way = models.CharField(max_length=20, blank=True, null=True)
    start_doctor = models.CharField(max_length=20, blank=True, null=True)
    start_nurse = models.CharField(max_length=20, blank=True, null=True)
    end_doctor = models.CharField(max_length=20, blank=True, null=True)
    end_nurse = models.CharField(max_length=20, blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    class Meta:
        managed = False
        db_table = 'b_inpatient_medical_advice'

class DMedicalAdvice(models.Model):
    medical_name = models.CharField(max_length=40, blank=True, null=True)
    type = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'd_medical_advice'


class DBloodTest(models.Model):
    id = models.AutoField(primary_key=True)
    data_id = models.IntegerField(blank=True, null=True)
    case_num = models.CharField(max_length=40, blank=True, null=True)
    barcode_num = models.CharField(max_length=40, blank=True, null=True)
    item_name = models.CharField(max_length=40, blank=True, null=True)
    item_value = models.FloatField(blank=True, null=True)
    item_unit = models.CharField(max_length=10, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'd_blood_test'