# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from tools.ConfigClass import HospitalizedState
from tools.Utils import get_patient_progress_note_direct, get_patient_medical_advice_direct
class BPatientBaseInfo(models.Model):
    SEX_TYPE = (
        (0, '男'),
        (1, '女'),
    )
    DIAGNOSIS_TYPE = (
        (0, '未诊断'),
        (1, '健康'),
        (2, '重症抑郁障碍'),
        (3, '焦虑障碍'),
        (4, '双相障碍'),
        (5, '精神分裂症'),
        (6, '强迫症'),
        (7, '高危遗传'),
        (8, '临床高危'),
        (9, '抑郁症状'),
        (99, '其他诊断')
    )
    HOSPITALIZED_TYPE = (
        (HospitalizedState.NOT_HOSPITALIZED,'未入院'),
        (HospitalizedState.INPATIENT,'在院'),
        (HospitalizedState.OUT_HOSPITAL,'出院'),
    )
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20)
    sex = models.IntegerField(blank=True, null=True, choices=SEX_TYPE)
    birth_date = models.DateField()
    nation = models.CharField(max_length=10)
    doctor = models.ForeignKey('users.SUser', models.DO_NOTHING)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    diagnosis = models.IntegerField(blank=True, null=True, choices=DIAGNOSIS_TYPE)
    other_diagnosis = models.CharField(max_length=45)
    inpatient_state = models.IntegerField(choices=HOSPITALIZED_TYPE,default=HospitalizedState.NOT_HOSPITALIZED)
    class Meta:
        managed = False
        db_table = 'b_patient_base_info'

class DPatientDetail(models.Model):

    SCAN_OPTIONS = [
        (1, '初扫'),
        (2, '只采血'),
        (3, '复扫'),
        (4, '出院前'),
        (5, '随访'),
        (6, '再次入院')
    ]



    patient = models.ForeignKey(BPatientBaseInfo, models.DO_NOTHING, blank=True, null=True)
    session_id = models.IntegerField(blank=True, null=True)
    standard_id = models.CharField(max_length=20, blank=True, null=True)
    cognitive = models.IntegerField(blank=True, null=True)
    sound = models.IntegerField(blank=True, null=True)
    blood = models.IntegerField(blank=True, null=True)
    hairs = models.IntegerField(blank=True, null=True)
    manure = models.IntegerField(blank=True, null=True)
    drugs_information = models.IntegerField(blank=True, null=True)
    mri_examination = models.IntegerField(blank=True, null=True)
    tms = models.IntegerField(blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    occupation = models.CharField(max_length=40, blank=True, null=True)
    education = models.CharField(max_length=20, blank=True, null=True)
    years = models.IntegerField(blank=True, null=True)
    emotional_state = models.IntegerField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    source = models.IntegerField(blank=True, null=True)
    height = models.FloatField(blank=True, null=True)
    weight = models.FloatField(blank=True, null=True)
    waist = models.FloatField(blank=True, null=True)
    hip = models.FloatField(blank=True, null=True)
    handy = models.IntegerField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    doctor = models.ForeignKey('users.SUser', models.DO_NOTHING)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    disease_state =  models.CharField(max_length=30, blank=True, null=True)
    first = models.IntegerField(blank=True, null=True)
    contact_way = models.IntegerField(blank=True, null=True)
    contact_info = models.CharField(max_length=45, blank=True, null=True)
    scan_date = models.DateField()
    head_motion_parameters = models.FloatField(blank=True, null=True)
    blood_sampling_date = models.DateField()
    ua = models.FloatField(blank=True, null=True)
    scan_note_option = models.IntegerField(blank=True, null=True, choices=SCAN_OPTIONS)
    scan_note_num = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'd_patient_detail'


# 民族字典表
class DEthnicity(models.Model):
    ethnicity_name = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'd_ethnicity'


class DPatientAppointment(models.Model):
    date = models.DateTimeField()
    name = models.CharField(max_length=20)
    sex = models.IntegerField()
    birth_date = models.DateField()
    phone = models.CharField(max_length=20)
    note = models.TextField(blank=True, null=True)
    pre_diagnosis = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'd_patient_appointment'


class RPatientGhr(models.Model):
    ghr_id = models.IntegerField()
    kin_patient_id = models.IntegerField(blank=True, null=True)
    diagnosis = models.IntegerField(blank=True, null=True)
    kinship = models.IntegerField(blank=True, null=True)
    doctor_id = models.IntegerField()
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'r_patient_ghr'


#rtms
class BPatientRtms(models.Model):
    id = models.IntegerField(primary_key=True)
    patient_session = models.OneToOneField('DPatientDetail', models.DO_NOTHING)
    treatment_num = models.IntegerField()
    treatment_date = models.DateField()
    therapeutic_target = models.TextField(blank=True, null=True)
    times_per_day = models.IntegerField(blank=True, null=True)
    total_num = models.IntegerField()
    resting_motor_threshold = models.IntegerField()
    intensity = models.IntegerField()
    frequency = models.IntegerField()
    pulses = models.IntegerField()
    stimulation_time = models.IntegerField()
    inter_train_intervals = models.IntegerField()
    pulse_trains = models.IntegerField()
    total_pulses = models.IntegerField()
    total_time_minute = models.IntegerField()
    total_time_second = models.IntegerField()
    note = models.TextField(blank=True, null=True)
    doctor = models.ForeignKey('users.Suser', models.DO_NOTHING)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'b_patient_rtms'

#blood
class RPatientBlood(models.Model):
    patient_session = models.ForeignKey(DPatientDetail, models.DO_NOTHING)
    blood_sample_id = models.CharField(max_length=45, blank=True, null=True)
    blood_sampling_date = models.DateField(blank=True, null=True)
    inspect_date = models.DateField(blank=True, null=True)
    total_blood_number = models.IntegerField(blank=True, null=True)
    plasma_number = models.IntegerField(blank=True, null=True)
    hemocyte_number = models.IntegerField(blank=True, null=True)
    extract_dna = models.FloatField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'r_patient_blood'

class DPatientIsMedicalAdvice(models.Model):
    patient_id = models.IntegerField(blank=True, null=True)
    is_medical_advice = models.IntegerField(blank=True, null=True)
    medical_advice_path = models.FileField(upload_to=get_patient_medical_advice_direct)
    ma_create_time = models.DateTimeField(blank=True, null=True)
    ma_update_time = models.DateTimeField(blank=True, null=True)
    is_progress_note = models.IntegerField(blank=True, null=True)
    progress_note_path = models.FileField(upload_to=get_patient_progress_note_direct)
    pn_create_time = models.DateTimeField(blank=True, null=True)
    pn_update_time = models.DateTimeField(blank=True, null=True)
    postscript = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'd_patient_is_medical_advice'


class BPatientMedicalAdviceDetail(models.Model):
    patient_id = models.IntegerField()
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
        db_table = 'b_patient_medical_advice_detail'