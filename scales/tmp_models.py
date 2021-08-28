# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class BInpatientInfo(models.Model):
    patient = models.ForeignKey('BPatientBaseInfo', models.DO_NOTHING)
    in_time = models.IntegerField(blank=True, null=True)
    department = models.CharField(max_length=40, blank=True, null=True)
    inpatient_area = models.CharField(max_length=20, blank=True, null=True)
    bed_number = models.CharField(max_length=20, blank=True, null=True)
    inpatient_number = models.CharField(max_length=20, blank=True, null=True)
    in_date = models.DateField(blank=True, null=True)
    out_date = models.DateField(blank=True, null=True)
    create_time = models.DateTimeField()
    update_time = models.DateTimeField()
    out_record = models.CharField(max_length=50, blank=True, null=True)
    progress_note = models.CharField(max_length=50, blank=True, null=True)
    medical_advice_path = models.CharField(max_length=50, blank=True, null=True)
    inpatient_state = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'b_inpatient_info'


class BInpatientMedicalAdvice(models.Model):
    inpatient = models.ForeignKey(BInpatientInfo, models.DO_NOTHING)
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
    create_time = models.DateTimeField()
    update_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'b_inpatient_medical_advice'


class BPatientBaseInfo(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20)
    sex = models.IntegerField()
    birth_date = models.DateField()
    nation = models.CharField(max_length=20)
    doctor = models.ForeignKey('SUser', models.DO_NOTHING)
    create_time = models.DateTimeField()
    update_time = models.DateTimeField()
    diagnosis = models.IntegerField(blank=True, null=True)
    other_diagnosis = models.CharField(max_length=45, blank=True, null=True)
    inpatient_state = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'b_patient_base_info'


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
    create_time = models.DateTimeField()
    update_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'b_patient_medical_advice_detail'


class BPatientRtms(models.Model):
    patient_session_id = models.IntegerField(blank=True, null=True)
    treatment_num = models.IntegerField(blank=True, null=True)
    treatment_date = models.DateField(blank=True, null=True)
    therapeutic_target = models.TextField(blank=True, null=True)
    times_per_day = models.IntegerField(blank=True, null=True)
    total_num = models.IntegerField(blank=True, null=True)
    resting_motor_threshold = models.IntegerField(blank=True, null=True)
    intensity = models.IntegerField(blank=True, null=True)
    frequency = models.IntegerField(blank=True, null=True)
    pulses = models.IntegerField(blank=True, null=True)
    stimulation_time = models.IntegerField(blank=True, null=True)
    inter_train_intervals = models.IntegerField(blank=True, null=True)
    pulse_trains = models.IntegerField(blank=True, null=True)
    total_pulses = models.IntegerField(blank=True, null=True)
    total_time_minute = models.IntegerField(blank=True, null=True)
    total_time_second = models.IntegerField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    doctor = models.ForeignKey('SUser', models.DO_NOTHING, blank=True, null=True)
    create_time = models.DateTimeField()
    update_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'b_patient_rtms'


class DEthnicity(models.Model):
    ethnicity_name = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'd_ethnicity'


class DMedicalAdvice(models.Model):
    medical_name = models.CharField(max_length=40, blank=True, null=True)
    type = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'd_medical_advice'


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


class DPatientDetail(models.Model):
    patient = models.ForeignKey(BPatientBaseInfo, models.DO_NOTHING)
    session_id = models.IntegerField()
    standard_id = models.CharField(max_length=20)
    height = models.FloatField(blank=True, null=True)
    cognitive = models.IntegerField(blank=True, null=True)
    sound = models.IntegerField(blank=True, null=True)
    blood = models.IntegerField(blank=True, null=True)
    hairs = models.IntegerField(blank=True, null=True)
    manure = models.IntegerField(blank=True, null=True)
    drugs_information = models.IntegerField(blank=True, null=True)
    mri_examination = models.IntegerField(blank=True, null=True)
    first = models.IntegerField(blank=True, null=True)
    tms = models.IntegerField(blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    occupation = models.CharField(max_length=40, blank=True, null=True)
    education = models.CharField(max_length=20, blank=True, null=True)
    years = models.IntegerField(blank=True, null=True)
    emotional_state = models.IntegerField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    source = models.IntegerField(blank=True, null=True)
    weight = models.FloatField(blank=True, null=True)
    waist = models.FloatField(blank=True, null=True)
    hip = models.FloatField(blank=True, null=True)
    handy = models.IntegerField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    doctor_id = models.IntegerField()
    create_time = models.DateTimeField()
    update_time = models.DateTimeField()
    disease_state = models.CharField(max_length=40, blank=True, null=True)
    contact_way = models.IntegerField(blank=True, null=True)
    contact_info = models.CharField(max_length=45, blank=True, null=True)
    scan_date = models.DateField(blank=True, null=True)
    d_patient_detailcol = models.CharField(max_length=45, blank=True, null=True)
    head_motion_parameters = models.FloatField(blank=True, null=True)
    blood_sampling_date = models.DateField(blank=True, null=True)
    ua = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'd_patient_detail'


class DPatientIsMedicalAdvice(models.Model):
    patient_id = models.IntegerField(blank=True, null=True)
    is_medical_advice = models.IntegerField(blank=True, null=True)
    medical_advice_path = models.CharField(max_length=50, blank=True, null=True)
    ma_create_time = models.DateTimeField(blank=True, null=True)
    ma_update_time = models.DateTimeField(blank=True, null=True)
    is_progress_note = models.IntegerField(blank=True, null=True)
    progress_note_path = models.CharField(max_length=50, blank=True, null=True)
    pn_create_time = models.DateTimeField(blank=True, null=True)
    pn_update_time = models.DateTimeField(blank=True, null=True)
    postscript = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'd_patient_is_medical_advice'


class DScales(models.Model):
    scale_name = models.CharField(max_length=40)
    scale_type = models.IntegerField()
    do_scale_type = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'd_scales'


class DTreatments(models.Model):
    name = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'd_treatments'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class RPatientAdolescentEvents(models.Model):
    patient_session = models.ForeignKey(DPatientDetail, models.DO_NOTHING, unique=True)
    scale = models.ForeignKey(DScales, models.DO_NOTHING)
    question1_answer = models.IntegerField(blank=True, null=True)
    question2_answer = models.IntegerField(blank=True, null=True)
    question3_answer = models.IntegerField(blank=True, null=True)
    question4_answer = models.IntegerField(blank=True, null=True)
    question5_answer = models.IntegerField(blank=True, null=True)
    question6_answer = models.IntegerField(blank=True, null=True)
    question7_answer = models.IntegerField(blank=True, null=True)
    question8_answer = models.IntegerField(blank=True, null=True)
    question9_answer = models.IntegerField(blank=True, null=True)
    question10_answer = models.IntegerField(blank=True, null=True)
    question11_answer = models.IntegerField(blank=True, null=True)
    question12_answer = models.IntegerField(blank=True, null=True)
    question13_answer = models.IntegerField(blank=True, null=True)
    question14_answer = models.IntegerField(blank=True, null=True)
    question15_answer = models.IntegerField(blank=True, null=True)
    question16_answer = models.IntegerField(blank=True, null=True)
    question17_answer = models.IntegerField(blank=True, null=True)
    question18_answer = models.IntegerField(blank=True, null=True)
    question19_answer = models.IntegerField(blank=True, null=True)
    question20_answer = models.IntegerField(blank=True, null=True)
    question21_answer = models.IntegerField(blank=True, null=True)
    question22_answer = models.IntegerField(blank=True, null=True)
    question23_answer = models.IntegerField(blank=True, null=True)
    question24_answer = models.IntegerField(blank=True, null=True)
    question25_answer = models.IntegerField(blank=True, null=True)
    question26_answer = models.IntegerField(blank=True, null=True)
    question27_answer = models.IntegerField(blank=True, null=True)
    total_score = models.IntegerField(blank=True, null=True)
    doctor_id = models.IntegerField()
    create_time = models.DateTimeField()
    update_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'r_patient_adolescent_events'


class RPatientAtq(models.Model):
    patient_session = models.ForeignKey(DPatientDetail, models.DO_NOTHING, unique=True)
    scale = models.ForeignKey(DScales, models.DO_NOTHING)
    question1_answer = models.IntegerField(blank=True, null=True)
    question2_answer = models.IntegerField(blank=True, null=True)
    question3_answer = models.IntegerField(blank=True, null=True)
    question4_answer = models.IntegerField(blank=True, null=True)
    question5_answer = models.IntegerField(blank=True, null=True)
    question6_answer = models.IntegerField(blank=True, null=True)
    question7_answer = models.IntegerField(blank=True, null=True)
    question8_answer = models.IntegerField(blank=True, null=True)
    question9_answer = models.IntegerField(blank=True, null=True)
    question10_answer = models.IntegerField(blank=True, null=True)
    question11_answer = models.IntegerField(blank=True, null=True)
    question12_answer = models.IntegerField(blank=True, null=True)
    question13_answer = models.IntegerField(blank=True, null=True)
    question14_answer = models.IntegerField(blank=True, null=True)
    question15_answer = models.IntegerField(blank=True, null=True)
    question16_answer = models.IntegerField(blank=True, null=True)
    question17_answer = models.IntegerField(blank=True, null=True)
    question18_answer = models.IntegerField(blank=True, null=True)
    question19_answer = models.IntegerField(blank=True, null=True)
    question20_answer = models.IntegerField(blank=True, null=True)
    question21_answer = models.IntegerField(blank=True, null=True)
    question22_answer = models.IntegerField(blank=True, null=True)
    question23_answer = models.IntegerField(blank=True, null=True)
    question24_answer = models.IntegerField(blank=True, null=True)
    question25_answer = models.IntegerField(blank=True, null=True)
    question26_answer = models.IntegerField(blank=True, null=True)
    question27_answer = models.IntegerField(blank=True, null=True)
    question28_answer = models.IntegerField(blank=True, null=True)
    question29_answer = models.IntegerField(blank=True, null=True)
    question30_answer = models.IntegerField(blank=True, null=True)
    total_score = models.IntegerField(blank=True, null=True)
    doctor = models.ForeignKey('SUser', models.DO_NOTHING)
    create_time = models.DateTimeField()
    update_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'r_patient_atq'


class RPatientBasicInformationAbuse(models.Model):
    patient_session = models.ForeignKey(DPatientDetail, models.DO_NOTHING, unique=True)
    scale = models.ForeignKey(DScales, models.DO_NOTHING)
    patient_smoke = models.IntegerField(blank=True, null=True)
    patient_smoke_age = models.IntegerField(blank=True, null=True)
    patient_daily_smoke_num = models.IntegerField(blank=True, null=True)
    patient_stop_smoke_age = models.IntegerField(blank=True, null=True)
    patient_alcohol = models.IntegerField(blank=True, null=True)
    patient_alcohol_age = models.IntegerField(blank=True, null=True)
    patient_other_abuse = models.IntegerField(blank=True, null=True)
    patient_other_abuse_age = models.IntegerField(blank=True, null=True)
    doctor = models.ForeignKey('SUser', models.DO_NOTHING)
    create_time = models.DateTimeField()
    update_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'r_patient_basic_information_abuse'


class RPatientBasicInformationFamily(models.Model):
    patient_session = models.ForeignKey(DPatientDetail, models.DO_NOTHING, unique=True)
    scale = models.ForeignKey(DScales, models.DO_NOTHING)
    patient_urban_rural = models.IntegerField(blank=True, null=True)
    patient_address = models.CharField(max_length=300, blank=True, null=True)
    patient_live_type = models.IntegerField(blank=True, null=True)
    patient_live_type_other = models.CharField(max_length=50, blank=True, null=True)
    patient_only_child = models.IntegerField(blank=True, null=True)
    patient_older_brother_num = models.IntegerField(blank=True, null=True)
    patient_older_sister_num = models.IntegerField(blank=True, null=True)
    patient_younger_brother_num = models.IntegerField(blank=True, null=True)
    pathent_younger_sister_num = models.IntegerField(blank=True, null=True)
    parents_favour = models.IntegerField(blank=True, null=True)
    father_occupation = models.CharField(max_length=30, blank=True, null=True)
    mother_occupation = models.CharField(max_length=30, blank=True, null=True)
    father_tele = models.CharField(max_length=20, blank=True, null=True)
    mother_tele = models.CharField(max_length=20, blank=True, null=True)
    father_education = models.IntegerField(blank=True, null=True)
    mother_education = models.IntegerField(blank=True, null=True)
    parent_marry = models.IntegerField(blank=True, null=True)
    step_parent = models.IntegerField(blank=True, null=True)
    patient_parent_death = models.IntegerField(blank=True, null=True)
    patient_parent_death_age = models.IntegerField(blank=True, null=True)
    parent_argument = models.IntegerField(blank=True, null=True)
    patient_adopt = models.IntegerField(blank=True, null=True)
    patient_adopt_age = models.IntegerField(blank=True, null=True)
    father_relationship = models.IntegerField(blank=True, null=True)
    mother_relationship = models.IntegerField(blank=True, null=True)
    doctor = models.ForeignKey('SUser', models.DO_NOTHING)
    create_time = models.DateTimeField()
    update_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'r_patient_basic_information_family'


class RPatientBasicInformationHealth(models.Model):
    patient_session = models.ForeignKey(DPatientDetail, models.DO_NOTHING, unique=True)
    scale = models.ForeignKey(DScales, models.DO_NOTHING)
    patient_somatic_diseases = models.IntegerField(blank=True, null=True)
    patient_somatic_diseases_name = models.CharField(max_length=100, blank=True, null=True)
    patient_somatic_diseases_year = models.CharField(max_length=20, blank=True, null=True)
    patient_mental_diseases = models.IntegerField(blank=True, null=True)
    patient_mental_diseases_name = models.CharField(max_length=100, blank=True, null=True)
    patient_mental_diseases_year = models.CharField(max_length=20, blank=True, null=True)
    patient_family_diseases_history = models.IntegerField(blank=True, null=True)
    patient_family_diseases_name = models.CharField(max_length=100, blank=True, null=True)
    patient_medicine_information = models.TextField(blank=True, null=True)
    patient_treatment_information = models.TextField(blank=True, null=True)
    doctor = models.ForeignKey('SUser', models.DO_NOTHING)
    create_time = models.DateTimeField()
    update_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'r_patient_basic_information_health'


class RPatientBasicInformationOther(models.Model):
    patient_session = models.ForeignKey(DPatientDetail, models.DO_NOTHING, unique=True)
    scale = models.ForeignKey(DScales, models.DO_NOTHING)
    patient_friend_num = models.IntegerField(blank=True, null=True)
    patient_big_event = models.IntegerField(blank=True, null=True)
    patient_big_event_describtion = models.TextField(blank=True, null=True)
    doctor = models.ForeignKey('SUser', models.DO_NOTHING)
    create_time = models.DateTimeField()
    update_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'r_patient_basic_information_other'


class RPatientBasicInformationStudy(models.Model):
    patient_session = models.ForeignKey(DPatientDetail, models.DO_NOTHING, unique=True)
    scale = models.ForeignKey(DScales, models.DO_NOTHING)
    patient_current_achievement = models.IntegerField(blank=True, null=True)
    patient_last_semester_achievement_difference = models.IntegerField(blank=True, null=True)
    patient_mood_symptom_achievement_difference = models.IntegerField(blank=True, null=True)
    patient_leader = models.IntegerField(blank=True, null=True)
    patient_leader_occupation = models.CharField(max_length=30, blank=True, null=True)
    patient_live_school = models.IntegerField(blank=True, null=True)
    patient_home_frequency = models.IntegerField(blank=True, null=True)
    doctor = models.ForeignKey('SUser', models.DO_NOTHING)
    create_time = models.DateTimeField()
    update_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'r_patient_basic_information_study'


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
    create_time = models.DateTimeField()
    update_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'r_patient_blood'


class RPatientBprs(models.Model):
    patient_session = models.ForeignKey(DPatientDetail, models.DO_NOTHING, unique=True)
    scale = models.ForeignKey(DScales, models.DO_NOTHING, blank=True, null=True)
    health_care = models.IntegerField(blank=True, null=True)
    anxious = models.IntegerField(blank=True, null=True)
    emocommunicat_barrier = models.IntegerField(blank=True, null=True)
    conceptual_disorder = models.IntegerField(blank=True, null=True)
    guilt_concept = models.IntegerField(blank=True, null=True)
    nervous = models.IntegerField(blank=True, null=True)
    look_act = models.IntegerField(blank=True, null=True)
    exaggerate = models.IntegerField(blank=True, null=True)
    mood_depression = models.IntegerField(blank=True, null=True)
    hostility = models.IntegerField(blank=True, null=True)
    suspicion = models.IntegerField(blank=True, null=True)
    hallucination = models.IntegerField(blank=True, null=True)
    slow_movement = models.IntegerField(blank=True, null=True)
    no_cooperation = models.IntegerField(blank=True, null=True)
    unusual_thinking = models.IntegerField(blank=True, null=True)
    feeling_flat = models.IntegerField(blank=True, null=True)
    excitement = models.IntegerField(blank=True, null=True)
    directional_disorder = models.IntegerField(blank=True, null=True)
    total_score = models.IntegerField(blank=True, null=True)
    doctor = models.ForeignKey('SUser', models.DO_NOTHING, blank=True, null=True)
    create_time = models.DateTimeField(blank=True, null=True)
    update_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'r_patient_bprs'


class RPatientChineseHandy(models.Model):
    patient_session = models.ForeignKey(DPatientDetail, models.DO_NOTHING, unique=True)
    scale = models.ForeignKey(DScales, models.DO_NOTHING)
    hold_pen = models.IntegerField(blank=True, null=True)
    hold_chopsticks = models.IntegerField(blank=True, null=True)
    throw_things = models.IntegerField(blank=True, null=True)
    brush_tooth = models.IntegerField(blank=True, null=True)
    use_scissors = models.IntegerField(blank=True, null=True)
    use_match = models.IntegerField(blank=True, null=True)
    use_needle = models.IntegerField(blank=True, null=True)
    hold_hammer = models.IntegerField(blank=True, null=True)
    hold_racket = models.IntegerField(blank=True, null=True)
    wash_face = models.IntegerField(blank=True, null=True)
    result = models.IntegerField(blank=True, null=True)
    doctor = models.ForeignKey('SUser', models.DO_NOTHING)
    create_time = models.DateTimeField()
    update_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'r_patient_chinese_handy'


class RPatientCognitiveEmotion(models.Model):
    patient_session = models.ForeignKey(DPatientDetail, models.DO_NOTHING, unique=True)
    scale = models.ForeignKey(DScales, models.DO_NOTHING)
    question1_answer = models.IntegerField(blank=True, null=True)
    question2_answer = models.IntegerField(blank=True, null=True)
    question3_answer = models.IntegerField(blank=True, null=True)
    question4_answer = models.IntegerField(blank=True, null=True)
    question5_answer = models.IntegerField(blank=True, null=True)
    question6_answer = models.IntegerField(blank=True, null=True)
    question7_answer = models.IntegerField(blank=True, null=True)
    question8_answer = models.IntegerField(blank=True, null=True)
    question9_answer = models.IntegerField(blank=True, null=True)
    question10_answer = models.IntegerField(blank=True, null=True)
    question11_answer = models.IntegerField(blank=True, null=True)
    question12_answer = models.IntegerField(blank=True, null=True)
    question13_answer = models.IntegerField(blank=True, null=True)
    question14_answer = models.IntegerField(blank=True, null=True)
    question15_answer = models.IntegerField(blank=True, null=True)
    question16_answer = models.IntegerField(blank=True, null=True)
    question17_answer = models.IntegerField(blank=True, null=True)
    question18_answer = models.IntegerField(blank=True, null=True)
    question19_answer = models.IntegerField(blank=True, null=True)
    question20_answer = models.IntegerField(blank=True, null=True)
    question21_answer = models.IntegerField(blank=True, null=True)
    question22_answer = models.IntegerField(blank=True, null=True)
    question23_answer = models.IntegerField(blank=True, null=True)
    question24_answer = models.IntegerField(blank=True, null=True)
    question25_answer = models.IntegerField(blank=True, null=True)
    question26_answer = models.IntegerField(blank=True, null=True)
    question27_answer = models.IntegerField(blank=True, null=True)
    question28_answer = models.IntegerField(blank=True, null=True)
    question29_answer = models.IntegerField(blank=True, null=True)
    question30_answer = models.IntegerField(blank=True, null=True)
    question31_answer = models.IntegerField(blank=True, null=True)
    question32_answer = models.IntegerField(blank=True, null=True)
    question33_answer = models.IntegerField(blank=True, null=True)
    question34_answer = models.IntegerField(blank=True, null=True)
    question35_answer = models.IntegerField(blank=True, null=True)
    question36_answer = models.IntegerField(blank=True, null=True)
    total_score = models.IntegerField(blank=True, null=True)
    doctor = models.ForeignKey('SUser', models.DO_NOTHING)
    create_time = models.DateTimeField()
    update_time = models.DateTimeField()
    blame_self = models.IntegerField(blank=True, null=True)
    blame_others = models.IntegerField(blank=True, null=True)
    meditation = models.IntegerField(blank=True, null=True)
    catastrophization = models.IntegerField(blank=True, null=True)
    accepted = models.IntegerField(blank=True, null=True)
    positive_refocus = models.IntegerField(blank=True, null=True)
    program_refocus = models.IntegerField(blank=True, null=True)
    positive_evaluation = models.IntegerField(blank=True, null=True)
    rational_analysis = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'r_patient_cognitive_emotion'


class RPatientDiagnosticType(models.Model):
    patient_session_id = models.IntegerField(unique=True)
    scale_id = models.IntegerField(blank=True, null=True)
    diagnostic_type = models.IntegerField(blank=True, null=True)
    diagnostic_type_other = models.CharField(max_length=20, blank=True, null=True)
    diagnostic_doctor1_signature = models.TextField(blank=True, null=True)
    diagnostic_doctor1_date = models.DateField(blank=True, null=True)
    diagnostic_doctor2_signature = models.TextField(blank=True, null=True)
    diagnostic_doctor2_date = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'r_patient_diagnostic_type'


class RPatientDrugsInformation(models.Model):
    patient_session = models.ForeignKey(DPatientDetail, models.DO_NOTHING)
    scale = models.ForeignKey(DScales, models.DO_NOTHING)
    type = models.IntegerField(blank=True, null=True)
    drug_name = models.CharField(max_length=40, blank=True, null=True)
    drug_general_name = models.CharField(max_length=40, blank=True, null=True)
    drug_type = models.CharField(max_length=40, blank=True, null=True)
    dosage = models.CharField(max_length=50, blank=True, null=True)
    begin_time = models.DateField(blank=True, null=True)
    end_time = models.DateField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    doctor = models.ForeignKey('SUser', models.DO_NOTHING)
    create_time = models.DateTimeField()
    update_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'r_patient_drugs_information'


class RPatientFept(models.Model):
    patient_session = models.ForeignKey(DPatientDetail, models.DO_NOTHING, unique=True)
    scale = models.ForeignKey(DScales, models.DO_NOTHING)
    calm = models.IntegerField(blank=True, null=True)
    angry = models.IntegerField(blank=True, null=True)
    disgusting = models.IntegerField(blank=True, null=True)
    fear = models.IntegerField(blank=True, null=True)
    happy = models.IntegerField(blank=True, null=True)
    sad = models.IntegerField(blank=True, null=True)
    wonder = models.IntegerField(blank=True, null=True)
    quality_control = models.FloatField(blank=True, null=True)
    total_score = models.IntegerField(blank=True, null=True)
    doctor = models.ForeignKey('SUser', models.DO_NOTHING)
    create_time = models.DateTimeField()
    update_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'r_patient_fept'


class RPatientFollowup(models.Model):
    patient = models.ForeignKey(BPatientBaseInfo, models.DO_NOTHING)
    session_id = models.IntegerField()
    patient_session = models.ForeignKey(DPatientDetail, models.DO_NOTHING, unique=True)
    first_scan_time = models.DateTimeField(blank=True, null=True)
    followup_intention = models.IntegerField(blank=True, null=True)
    intention_note = models.TextField(blank=True, null=True)
    create_tiime = models.DateTimeField()
    update_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'r_patient_followup'


class RPatientGad(models.Model):
    patient_session = models.ForeignKey(DPatientDetail, models.DO_NOTHING, unique=True)
    scale = models.ForeignKey(DScales, models.DO_NOTHING)
    question1_answer = models.IntegerField(blank=True, null=True)
    question2_answer = models.IntegerField(blank=True, null=True)
    question3_answer = models.IntegerField(blank=True, null=True)
    question4_answer = models.IntegerField(blank=True, null=True)
    question5_answer = models.IntegerField(blank=True, null=True)
    question6_answer = models.IntegerField(blank=True, null=True)
    question7_answer = models.IntegerField(blank=True, null=True)
    total_score = models.IntegerField(blank=True, null=True)
    doctor = models.ForeignKey('SUser', models.DO_NOTHING)
    create_time = models.DateTimeField()
    update_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'r_patient_gad'


class RPatientGhr(models.Model):
    ghr_id = models.IntegerField()
    kin_patient_id = models.IntegerField(blank=True, null=True)
    diagnosis = models.IntegerField(blank=True, null=True)
    kinship = models.IntegerField(blank=True, null=True)
    doctor_id = models.IntegerField()
    create_time = models.DateTimeField()
    update_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'r_patient_ghr'


class RPatientGrowth(models.Model):
    patient_session = models.ForeignKey(DPatientDetail, models.DO_NOTHING, unique=True)
    scale = models.ForeignKey(DScales, models.DO_NOTHING)
    question1_answer = models.IntegerField(blank=True, null=True)
    question2_answer = models.IntegerField(blank=True, null=True)
    question3_answer = models.IntegerField(blank=True, null=True)
    question4_answer = models.IntegerField(blank=True, null=True)
    question5_answer = models.IntegerField(blank=True, null=True)
    question6_answer = models.IntegerField(blank=True, null=True)
    question7_answer = models.IntegerField(blank=True, null=True)
    question8_answer = models.IntegerField(blank=True, null=True)
    question9_answer = models.IntegerField(blank=True, null=True)
    question10_answer = models.IntegerField(blank=True, null=True)
    question11_answer = models.IntegerField(blank=True, null=True)
    question12_answer = models.IntegerField(blank=True, null=True)
    question13_answer = models.IntegerField(blank=True, null=True)
    question14_answer = models.IntegerField(blank=True, null=True)
    question15_answer = models.IntegerField(blank=True, null=True)
    question16_answer = models.IntegerField(blank=True, null=True)
    question17_answer = models.IntegerField(blank=True, null=True)
    question18_answer = models.IntegerField(blank=True, null=True)
    question19_answer = models.IntegerField(blank=True, null=True)
    question20_answer = models.IntegerField(blank=True, null=True)
    question21_answer = models.IntegerField(blank=True, null=True)
    question22_answer = models.IntegerField(blank=True, null=True)
    question23_answer = models.IntegerField(blank=True, null=True)
    question24_answer = models.IntegerField(blank=True, null=True)
    question25_answer = models.IntegerField(blank=True, null=True)
    question26_answer = models.IntegerField(blank=True, null=True)
    question27_answer = models.IntegerField(blank=True, null=True)
    question28_answer = models.IntegerField(blank=True, null=True)
    first_sex_age = models.CharField(max_length=50, blank=True, null=True)
    doctor = models.ForeignKey('SUser', models.DO_NOTHING)
    create_time = models.DateTimeField()
    update_time = models.DateTimeField()
    emotion_abuse_score = models.IntegerField(blank=True, null=True)
    body_abuse_score = models.IntegerField(blank=True, null=True)
    sex_abuse_score = models.IntegerField(blank=True, null=True)
    emotion_ignore_score = models.IntegerField(blank=True, null=True)
    body_ignore_score = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'r_patient_growth'


class RPatientHama(models.Model):
    patient_session = models.ForeignKey(DPatientDetail, models.DO_NOTHING, unique=True)
    scale = models.ForeignKey(DScales, models.DO_NOTHING)
    anxiety = models.IntegerField(blank=True, null=True)
    nervous = models.IntegerField(blank=True, null=True)
    fear = models.IntegerField(blank=True, null=True)
    insomnia = models.IntegerField(blank=True, null=True)
    cognitive_function = models.IntegerField(blank=True, null=True)
    depression = models.IntegerField(blank=True, null=True)
    somaticanxiety_muscle = models.IntegerField(blank=True, null=True)
    somaticanxiety_sensory = models.IntegerField(blank=True, null=True)
    cardiovascular_symptoms = models.IntegerField(blank=True, null=True)
    respiratory_symptoms = models.IntegerField(blank=True, null=True)
    gastrointestinal_symptoms = models.IntegerField(blank=True, null=True)
    genitourinary_symptoms = models.IntegerField(blank=True, null=True)
    plantnervous_symptoms = models.IntegerField(blank=True, null=True)
    interview_behavior = models.IntegerField(blank=True, null=True)
    total_score = models.IntegerField(blank=True, null=True)
    doctor = models.ForeignKey('SUser', models.DO_NOTHING)
    create_time = models.DateTimeField()
    update_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'r_patient_hama'


class RPatientHamd17(models.Model):
    patient_session = models.ForeignKey(DPatientDetail, models.DO_NOTHING, unique=True)
    scale = models.ForeignKey(DScales, models.DO_NOTHING)
    depression = models.IntegerField(blank=True, null=True)
    guilt = models.IntegerField(blank=True, null=True)
    suicide = models.IntegerField(blank=True, null=True)
    difficulty_sleeping = models.IntegerField(blank=True, null=True)
    sleep_deep = models.IntegerField(blank=True, null=True)
    wake_early = models.IntegerField(blank=True, null=True)
    work_interest = models.IntegerField(blank=True, null=True)
    slow = models.IntegerField(blank=True, null=True)
    intense = models.IntegerField(blank=True, null=True)
    psycho_anxiety = models.IntegerField(blank=True, null=True)
    somatic_anxiety = models.IntegerField(blank=True, null=True)
    gastrointestinal_symptoms = models.IntegerField(blank=True, null=True)
    systemic_symptoms = models.IntegerField(blank=True, null=True)
    sexual_symptoms = models.IntegerField(blank=True, null=True)
    hypochondria = models.IntegerField(blank=True, null=True)
    lose_weight = models.IntegerField(blank=True, null=True)
    self_awareness = models.IntegerField(blank=True, null=True)
    total_score = models.IntegerField(blank=True, null=True)
    doctor = models.ForeignKey('SUser', models.DO_NOTHING)
    create_time = models.DateTimeField()
    update_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'r_patient_hamd17'


class RPatientHappiness(models.Model):
    patient_session = models.ForeignKey(DPatientDetail, models.DO_NOTHING, unique=True)
    scale = models.ForeignKey(DScales, models.DO_NOTHING)
    question1_answer = models.IntegerField(blank=True, null=True)
    question2_answer = models.IntegerField(blank=True, null=True)
    question3_answer = models.IntegerField(blank=True, null=True)
    question4_answer = models.IntegerField(blank=True, null=True)
    question5_answer = models.IntegerField(blank=True, null=True)
    question6_answer = models.IntegerField(blank=True, null=True)
    question7_answer = models.IntegerField(blank=True, null=True)
    question8_answer = models.IntegerField(blank=True, null=True)
    question9_answer = models.IntegerField(blank=True, null=True)
    question10_answer = models.IntegerField(blank=True, null=True)
    question11_answer = models.IntegerField(blank=True, null=True)
    question12_answer = models.IntegerField(blank=True, null=True)
    question13_answer = models.IntegerField(blank=True, null=True)
    question14_answer = models.IntegerField(blank=True, null=True)
    total_score = models.IntegerField(blank=True, null=True)
    doctor = models.ForeignKey('SUser', models.DO_NOTHING)
    create_time = models.DateTimeField()
    update_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'r_patient_happiness'


class RPatientInclusionExclusionCriteria(models.Model):
    patient_session = models.ForeignKey(DPatientDetail, models.DO_NOTHING, unique=True)
    scale = models.ForeignKey(DScales, models.DO_NOTHING)
    informaed_consent_signature = models.IntegerField(blank=True, null=True)
    informaed_consent_date = models.DateField(blank=True, null=True)
    answer_1 = models.IntegerField(blank=True, null=True)
    answer_2 = models.IntegerField(blank=True, null=True)
    answer_3 = models.IntegerField(blank=True, null=True)
    answer_4 = models.IntegerField(blank=True, null=True)
    answer_5 = models.IntegerField(blank=True, null=True)
    answer_6 = models.IntegerField(blank=True, null=True)
    answer_7 = models.IntegerField(blank=True, null=True)
    answer_8 = models.IntegerField(blank=True, null=True)
    answer_9 = models.IntegerField(blank=True, null=True)
    answer_10 = models.IntegerField(blank=True, null=True)
    answer_11 = models.IntegerField(blank=True, null=True)
    answer_12 = models.IntegerField(blank=True, null=True)
    answer_13 = models.IntegerField(blank=True, null=True)
    answer_14 = models.IntegerField(blank=True, null=True)
    answer_15 = models.IntegerField(blank=True, null=True)
    answer_16 = models.IntegerField(blank=True, null=True)
    answer_17 = models.IntegerField(blank=True, null=True)
    qualified = models.IntegerField(blank=True, null=True)
    blood_sample = models.IntegerField(blank=True, null=True)
    hair_sample = models.IntegerField(blank=True, null=True)
    saliva_sample = models.IntegerField(blank=True, null=True)
    faeces_sample = models.IntegerField(blank=True, null=True)
    doctor = models.ForeignKey('SUser', models.DO_NOTHING)
    create_time = models.DateTimeField()
    update_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'r_patient_inclusion_exclusion_criteria'


class RPatientInformedConsentSignaturePage(models.Model):
    patient_session = models.ForeignKey(DPatientDetail, models.DO_NOTHING, unique=True)
    scale = models.ForeignKey(DScales, models.DO_NOTHING)
    subject_name = models.CharField(max_length=20, blank=True, null=True)
    guardian_name = models.TextField(blank=True, null=True)
    researcher_name = models.TextField(blank=True, null=True)
    chief_researcher_name = models.TextField(blank=True, null=True)
    subject_signature_date = models.DateField(blank=True, null=True)
    guardian_signature_date = models.DateField(blank=True, null=True)
    researcher_signature_date = models.DateField(blank=True, null=True)
    chief_researcher_signature_date = models.DateField(blank=True, null=True)
    doctor = models.ForeignKey('SUser', models.DO_NOTHING)
    create_time = models.DateTimeField()
    update_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'r_patient_informed_consent_signature_page'


class RPatientInsomnia(models.Model):
    patient_session = models.ForeignKey(DPatientDetail, models.DO_NOTHING, unique=True)
    scale = models.ForeignKey(DScales, models.DO_NOTHING)
    question1_answer = models.IntegerField(blank=True, null=True)
    question2_answer = models.IntegerField(blank=True, null=True)
    question3_answer = models.IntegerField(blank=True, null=True)
    question4_answer = models.IntegerField(blank=True, null=True)
    question5_answer = models.IntegerField(blank=True, null=True)
    question6_answer = models.IntegerField(blank=True, null=True)
    question7_answer = models.IntegerField(blank=True, null=True)
    total_score = models.IntegerField(blank=True, null=True)
    doctor = models.ForeignKey('SUser', models.DO_NOTHING)
    create_time = models.DateTimeField()
    update_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'r_patient_insomnia'


class RPatientManicsymptom(models.Model):
    patient_session = models.ForeignKey(DPatientDetail, models.DO_NOTHING, unique=True)
    scale = models.ForeignKey(DScales, models.DO_NOTHING)
    question1 = models.IntegerField(blank=True, null=True)
    question2 = models.IntegerField(blank=True, null=True)
    question3_1 = models.IntegerField(blank=True, null=True)
    question3_2 = models.IntegerField(blank=True, null=True)
    question3_3 = models.IntegerField(blank=True, null=True)
    question3_4 = models.IntegerField(blank=True, null=True)
    question3_5 = models.IntegerField(blank=True, null=True)
    question3_6 = models.IntegerField(blank=True, null=True)
    question3_7 = models.IntegerField(blank=True, null=True)
    question3_8 = models.IntegerField(blank=True, null=True)
    question3_9 = models.IntegerField(blank=True, null=True)
    question3_10 = models.IntegerField(blank=True, null=True)
    question3_11 = models.IntegerField(blank=True, null=True)
    question3_12 = models.IntegerField(blank=True, null=True)
    question3_13 = models.IntegerField(blank=True, null=True)
    question3_14 = models.IntegerField(blank=True, null=True)
    question3_15 = models.IntegerField(blank=True, null=True)
    question3_16 = models.IntegerField(blank=True, null=True)
    question3_17 = models.IntegerField(blank=True, null=True)
    question3_18 = models.IntegerField(blank=True, null=True)
    question3_19 = models.IntegerField(blank=True, null=True)
    question3_20 = models.IntegerField(blank=True, null=True)
    question3_21 = models.IntegerField(blank=True, null=True)
    question3_22 = models.IntegerField(blank=True, null=True)
    question3_23 = models.IntegerField(blank=True, null=True)
    question3_24 = models.IntegerField(blank=True, null=True)
    question3_25 = models.IntegerField(blank=True, null=True)
    question3_26 = models.IntegerField(blank=True, null=True)
    question3_27 = models.IntegerField(blank=True, null=True)
    question3_28 = models.IntegerField(blank=True, null=True)
    question3_29 = models.IntegerField(blank=True, null=True)
    question3_30 = models.IntegerField(blank=True, null=True)
    question3_31 = models.IntegerField(blank=True, null=True)
    question3_32 = models.IntegerField(blank=True, null=True)
    question3_33 = models.IntegerField(blank=True, null=True)
    question4_1 = models.IntegerField(blank=True, null=True)
    question4_2 = models.IntegerField(blank=True, null=True)
    question4_3 = models.IntegerField(blank=True, null=True)
    question4_4 = models.IntegerField(blank=True, null=True)
    question5 = models.IntegerField(blank=True, null=True)
    question6_1 = models.IntegerField(blank=True, null=True)
    question6_2 = models.IntegerField(blank=True, null=True)
    question7 = models.IntegerField(blank=True, null=True)
    question8 = models.CharField(max_length=20, blank=True, null=True)
    question9 = models.IntegerField(blank=True, null=True)
    question10 = models.IntegerField(blank=True, null=True)
    total_score = models.IntegerField(blank=True, null=True)
    doctor = models.ForeignKey('SUser', models.DO_NOTHING)
    create_time = models.DateTimeField()
    update_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'r_patient_manicsymptom'


class RPatientMedicalHistory(models.Model):
    patient_session = models.ForeignKey(DPatientDetail, models.DO_NOTHING, unique=True)
    scale = models.ForeignKey(DScales, models.DO_NOTHING)
    disease_history = models.TextField(blank=True, null=True)
    prophase_begin = models.DateField(blank=True, null=True)
    prophase_end = models.DateField(blank=True, null=True)
    first_time_begin = models.DateField(blank=True, null=True)
    first_time_end = models.DateField(blank=True, null=True)
    first_episode_diagnosis = models.CharField(max_length=20, blank=True, null=True)
    number_of_episode = models.IntegerField(blank=True, null=True)
    current_episode_date = models.DateField(blank=True, null=True)
    current_episode_diagnosis = models.CharField(max_length=20, blank=True, null=True)
    historical_drugs = models.IntegerField(blank=True, null=True)
    historical_drugs_month = models.IntegerField(blank=True, null=True)
    scanning_state = models.IntegerField(blank=True, null=True)
    scanning_using_drugs = models.IntegerField(blank=True, null=True)
    scanning_drugs_month = models.IntegerField(blank=True, null=True)
    doctor = models.ForeignKey('SUser', models.DO_NOTHING)
    create_time = models.DateTimeField()
    update_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'r_patient_medical_history'


class RPatientMriExamination(models.Model):
    patient_session = models.ForeignKey(DPatientDetail, models.DO_NOTHING, unique=True)
    scale = models.ForeignKey(DScales, models.DO_NOTHING)
    finishing_3d = models.IntegerField(db_column='finishing_3D', blank=True, null=True)  # Field name made lowercase.
    finishing_dti = models.IntegerField(db_column='finishing_DTI', blank=True, null=True)  # Field name made lowercase.
    finishing_fmri = models.IntegerField(db_column='finishing_fMRI', blank=True, null=True)  # Field name made lowercase.
    finishing_time = models.DateField(blank=True, null=True)
    having_special_events = models.IntegerField(blank=True, null=True)
    special_events_note = models.TextField(blank=True, null=True)
    having_abnormal_region = models.IntegerField(blank=True, null=True)
    abnormal_region_note = models.TextField(blank=True, null=True)
    researcher_sign = models.TextField(blank=True, null=True)
    sign_date = models.DateField(blank=True, null=True)
    doctor = models.ForeignKey('SUser', models.DO_NOTHING)
    create_time = models.DateTimeField()
    update_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'r_patient_mri_examination'


class RPatientMriSafetyQuestionnaire(models.Model):
    patient_session = models.ForeignKey(DPatientDetail, models.DO_NOTHING, unique=True)
    scale = models.ForeignKey(DScales, models.DO_NOTHING)
    birth_date = models.DateField(blank=True, null=True)
    inspection_date = models.DateField(blank=True, null=True)
    patient_weight = models.FloatField(blank=True, null=True)
    patient_height = models.FloatField(blank=True, null=True)
    answer_1 = models.IntegerField(blank=True, null=True)
    answer_2 = models.IntegerField(blank=True, null=True)
    answer_3 = models.IntegerField(blank=True, null=True)
    answer_4 = models.IntegerField(blank=True, null=True)
    answer_5 = models.IntegerField(blank=True, null=True)
    answer_6 = models.IntegerField(blank=True, null=True)
    answer_7 = models.IntegerField(blank=True, null=True)
    answer_8 = models.IntegerField(blank=True, null=True)
    answer_9 = models.IntegerField(blank=True, null=True)
    answer_10 = models.IntegerField(blank=True, null=True)
    answer_11 = models.IntegerField(blank=True, null=True)
    answer_11_1 = models.IntegerField(blank=True, null=True)
    answer_12 = models.IntegerField(blank=True, null=True)
    answer_13 = models.IntegerField(blank=True, null=True)
    answer_14 = models.IntegerField(blank=True, null=True)
    answer_15 = models.IntegerField(blank=True, null=True)
    answer_16 = models.IntegerField(blank=True, null=True)
    answer_17 = models.IntegerField(blank=True, null=True)
    answer_18 = models.IntegerField(blank=True, null=True)
    answer_19 = models.IntegerField(blank=True, null=True)
    answer_20 = models.IntegerField(blank=True, null=True)
    answer_21 = models.IntegerField(blank=True, null=True)
    answer_22 = models.IntegerField(blank=True, null=True)
    answer_23 = models.IntegerField(blank=True, null=True)
    answer_24 = models.IntegerField(blank=True, null=True)
    answer_25 = models.IntegerField(blank=True, null=True)
    answer_26 = models.IntegerField(blank=True, null=True)
    answer_27 = models.IntegerField(blank=True, null=True)
    answer_28 = models.IntegerField(blank=True, null=True)
    answer_29 = models.IntegerField(blank=True, null=True)
    answer_29_1 = models.IntegerField(blank=True, null=True)
    answer_30 = models.IntegerField(blank=True, null=True)
    answer_30_1 = models.IntegerField(blank=True, null=True)
    answer_30_2 = models.IntegerField(blank=True, null=True)
    answer_31 = models.IntegerField(blank=True, null=True)
    answer_31_1 = models.IntegerField(blank=True, null=True)
    answer_32 = models.IntegerField(blank=True, null=True)
    answer_33 = models.IntegerField(blank=True, null=True)
    answer_33_1 = models.IntegerField(blank=True, null=True)
    answer_34 = models.IntegerField(blank=True, null=True)
    doctor = models.ForeignKey('SUser', models.DO_NOTHING)
    create_time = models.DateTimeField()
    update_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'r_patient_mri_safety_questionnaire'


class RPatientPhq(models.Model):
    patient_session = models.ForeignKey(DPatientDetail, models.DO_NOTHING, unique=True)
    scale = models.ForeignKey(DScales, models.DO_NOTHING)
    question1_answer = models.IntegerField(blank=True, null=True)
    question2_answer = models.IntegerField(blank=True, null=True)
    question3_answer = models.IntegerField(blank=True, null=True)
    question4_answer = models.IntegerField(blank=True, null=True)
    question5_answer = models.IntegerField(blank=True, null=True)
    question6_answer = models.IntegerField(blank=True, null=True)
    question7_answer = models.IntegerField(blank=True, null=True)
    question8_answer = models.IntegerField(blank=True, null=True)
    question9_answer = models.IntegerField(blank=True, null=True)
    total_score = models.IntegerField(blank=True, null=True)
    doctor = models.ForeignKey('SUser', models.DO_NOTHING)
    create_time = models.DateTimeField()
    update_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'r_patient_phq'


class RPatientPleasure(models.Model):
    patient_session = models.ForeignKey(DPatientDetail, models.DO_NOTHING, unique=True)
    scale = models.ForeignKey(DScales, models.DO_NOTHING)
    question1_answer = models.IntegerField(blank=True, null=True)
    question2_answer = models.IntegerField(blank=True, null=True)
    question3_answer = models.IntegerField(blank=True, null=True)
    question4_answer = models.IntegerField(blank=True, null=True)
    question5_answer = models.IntegerField(blank=True, null=True)
    question6_answer = models.IntegerField(blank=True, null=True)
    question7_answer = models.IntegerField(blank=True, null=True)
    question8_answer = models.IntegerField(blank=True, null=True)
    question9_answer = models.IntegerField(blank=True, null=True)
    question10_answer = models.IntegerField(blank=True, null=True)
    question11_answer = models.IntegerField(blank=True, null=True)
    question12_answer = models.IntegerField(blank=True, null=True)
    question13_answer = models.IntegerField(blank=True, null=True)
    question14_answer = models.IntegerField(blank=True, null=True)
    question15_answer = models.IntegerField(blank=True, null=True)
    question16_answer = models.IntegerField(blank=True, null=True)
    question17_answer = models.IntegerField(blank=True, null=True)
    question18_answer = models.IntegerField(blank=True, null=True)
    total_score = models.IntegerField(blank=True, null=True)
    expectation_score = models.IntegerField(blank=True, null=True)
    consume_score = models.IntegerField(blank=True, null=True)
    doctor = models.ForeignKey('SUser', models.DO_NOTHING)
    create_time = models.DateTimeField()
    update_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'r_patient_pleasure'


class RPatientPss(models.Model):
    patient_session = models.ForeignKey(DPatientDetail, models.DO_NOTHING, unique=True)
    scale = models.ForeignKey(DScales, models.DO_NOTHING)
    question1_answer = models.IntegerField(blank=True, null=True)
    question2_answer = models.IntegerField(blank=True, null=True)
    question3_answer = models.IntegerField(blank=True, null=True)
    question4_answer = models.IntegerField(blank=True, null=True)
    question5_answer = models.IntegerField(blank=True, null=True)
    question6_answer = models.IntegerField(blank=True, null=True)
    question7_answer = models.IntegerField(blank=True, null=True)
    question8_answer = models.IntegerField(blank=True, null=True)
    question9_answer = models.IntegerField(blank=True, null=True)
    question10_answer = models.IntegerField(blank=True, null=True)
    question11_answer = models.IntegerField(blank=True, null=True)
    question12_answer = models.IntegerField(blank=True, null=True)
    question13_answer = models.IntegerField(blank=True, null=True)
    question14_answer = models.IntegerField(blank=True, null=True)
    total_score = models.IntegerField(blank=True, null=True)
    doctor = models.ForeignKey('SUser', models.DO_NOTHING)
    create_time = models.DateTimeField()
    update_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'r_patient_pss'


class RPatientRbans(models.Model):
    patient_session = models.ForeignKey(DPatientDetail, models.DO_NOTHING, unique=True)
    scale = models.ForeignKey(DScales, models.DO_NOTHING)
    instant_memory_word = models.IntegerField(blank=True, null=True)
    instant_memory_story = models.IntegerField(blank=True, null=True)
    vision_graph = models.IntegerField(blank=True, null=True)
    vision_line = models.IntegerField(blank=True, null=True)
    speech_graph = models.IntegerField(blank=True, null=True)
    speech_fluency = models.IntegerField(blank=True, null=True)
    attention_number = models.IntegerField(blank=True, null=True)
    attention_code = models.IntegerField(blank=True, null=True)
    delayed_retention_word = models.IntegerField(blank=True, null=True)
    delayed_retention_word2 = models.IntegerField(blank=True, null=True)
    delayed_retention_story = models.IntegerField(blank=True, null=True)
    delayed_retention_graph = models.IntegerField(blank=True, null=True)
    instant_memory_total = models.IntegerField(blank=True, null=True)
    vision_total = models.IntegerField(blank=True, null=True)
    speech_total = models.IntegerField(blank=True, null=True)
    attention_total = models.IntegerField(blank=True, null=True)
    delayed_retention_total = models.IntegerField(blank=True, null=True)
    total_score = models.IntegerField(blank=True, null=True)
    doctor = models.ForeignKey('SUser', models.DO_NOTHING)
    create_time = models.DateTimeField()
    update_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'r_patient_rbans'


class RPatientScales(models.Model):
    patient_session = models.ForeignKey(DPatientDetail, models.DO_NOTHING)
    scale = models.ForeignKey(DScales, models.DO_NOTHING)
    state = models.IntegerField(blank=True, null=True)
    end_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'r_patient_scales'


class RPatientSembu(models.Model):
    patient_session = models.ForeignKey(DPatientDetail, models.DO_NOTHING, unique=True)
    scale = models.ForeignKey(DScales, models.DO_NOTHING)
    year_of_school = models.CharField(max_length=20, blank=True, null=True)
    grade = models.CharField(max_length=20, blank=True, null=True)
    region = models.IntegerField(blank=True, null=True)
    mark_level = models.IntegerField(blank=True, null=True)
    parents_status = models.IntegerField(blank=True, null=True)
    question1_father = models.IntegerField(blank=True, null=True)
    question1_mother = models.IntegerField(blank=True, null=True)
    question2_father = models.IntegerField(blank=True, null=True)
    question2_mother = models.IntegerField(blank=True, null=True)
    question3_father = models.IntegerField(blank=True, null=True)
    question3_mother = models.IntegerField(blank=True, null=True)
    question4_father = models.IntegerField(blank=True, null=True)
    question4_mother = models.IntegerField(blank=True, null=True)
    question5_father = models.IntegerField(blank=True, null=True)
    question5_mother = models.IntegerField(blank=True, null=True)
    question6_father = models.IntegerField(blank=True, null=True)
    question6_mother = models.IntegerField(blank=True, null=True)
    question7_father = models.IntegerField(blank=True, null=True)
    question7_mother = models.IntegerField(blank=True, null=True)
    question8_father = models.IntegerField(blank=True, null=True)
    question8_mother = models.IntegerField(blank=True, null=True)
    question9_father = models.IntegerField(blank=True, null=True)
    question9_mother = models.IntegerField(blank=True, null=True)
    question10_father = models.IntegerField(blank=True, null=True)
    question10_mother = models.IntegerField(blank=True, null=True)
    question11_father = models.IntegerField(blank=True, null=True)
    question11_mother = models.IntegerField(blank=True, null=True)
    question12_father = models.IntegerField(blank=True, null=True)
    question12_mother = models.IntegerField(blank=True, null=True)
    question13_father = models.IntegerField(blank=True, null=True)
    question13_mother = models.IntegerField(blank=True, null=True)
    question14_father = models.IntegerField(blank=True, null=True)
    question14_mother = models.IntegerField(blank=True, null=True)
    question15_father = models.IntegerField(blank=True, null=True)
    question15_mother = models.IntegerField(blank=True, null=True)
    question16_father = models.IntegerField(blank=True, null=True)
    question16_mother = models.IntegerField(blank=True, null=True)
    question17_father = models.IntegerField(blank=True, null=True)
    question17_mother = models.IntegerField(blank=True, null=True)
    question18_father = models.IntegerField(blank=True, null=True)
    question18_mother = models.IntegerField(blank=True, null=True)
    question19_father = models.IntegerField(blank=True, null=True)
    question19_mother = models.IntegerField(blank=True, null=True)
    question20_father = models.IntegerField(blank=True, null=True)
    question20_mother = models.IntegerField(blank=True, null=True)
    question21_father = models.IntegerField(blank=True, null=True)
    question21_mother = models.IntegerField(blank=True, null=True)
    refusal_mother = models.FloatField(blank=True, null=True)
    refusal_father = models.FloatField(blank=True, null=True)
    emotional_warmth_mother = models.FloatField(blank=True, null=True)
    emotional_warmth_father = models.FloatField(blank=True, null=True)
    overprotection_mother = models.FloatField(blank=True, null=True)
    overprotection_father = models.FloatField(blank=True, null=True)
    doctor = models.ForeignKey('SUser', models.DO_NOTHING)
    create_time = models.DateTimeField()
    update_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'r_patient_sembu'


class RPatientSuicidal(models.Model):
    patient_session = models.ForeignKey(DPatientDetail, models.DO_NOTHING, unique=True)
    scale = models.ForeignKey(DScales, models.DO_NOTHING)
    suicide_history = models.IntegerField(blank=True, null=True)
    suicide_times = models.CharField(max_length=50, blank=True, null=True)
    question1_lastweek = models.IntegerField(blank=True, null=True)
    question1_mostdepressed = models.IntegerField(blank=True, null=True)
    question2_lastweek = models.IntegerField(blank=True, null=True)
    question2_mostdepressed = models.IntegerField(blank=True, null=True)
    question3_lastweek = models.IntegerField(blank=True, null=True)
    question3_mostdepressed = models.IntegerField(blank=True, null=True)
    question4_lastweek = models.IntegerField(blank=True, null=True)
    question4_mostdepressed = models.IntegerField(blank=True, null=True)
    question5_lastweek = models.IntegerField(blank=True, null=True)
    question5_mostdepressed = models.IntegerField(blank=True, null=True)
    question6_lastweek = models.IntegerField(blank=True, null=True)
    question6_mostdepressed = models.IntegerField(blank=True, null=True)
    question7_lastweek = models.IntegerField(blank=True, null=True)
    question7_mostdepressed = models.IntegerField(blank=True, null=True)
    question8_lastweek = models.IntegerField(blank=True, null=True)
    question8_mostdepressed = models.IntegerField(blank=True, null=True)
    question9_lastweek = models.IntegerField(blank=True, null=True)
    question9_mostdepressed = models.IntegerField(blank=True, null=True)
    question10_lastweek = models.IntegerField(blank=True, null=True)
    question10_mostdepressed = models.IntegerField(blank=True, null=True)
    question11_lastweek = models.IntegerField(blank=True, null=True)
    question11_mostdepressed = models.IntegerField(blank=True, null=True)
    question12_lastweek = models.IntegerField(blank=True, null=True)
    question12_mostdepressed = models.IntegerField(blank=True, null=True)
    question13_lastweek = models.IntegerField(blank=True, null=True)
    question13_mostdepressed = models.IntegerField(blank=True, null=True)
    question14_lastweek = models.IntegerField(blank=True, null=True)
    question14_mostdepressed = models.IntegerField(blank=True, null=True)
    question15_lastweek = models.IntegerField(blank=True, null=True)
    question15_mostdepressed = models.IntegerField(blank=True, null=True)
    question16_lastweek = models.IntegerField(blank=True, null=True)
    question16_mostdepressed = models.IntegerField(blank=True, null=True)
    question17_lastweek = models.IntegerField(blank=True, null=True)
    question17_mostdepressed = models.IntegerField(blank=True, null=True)
    question18_lastweek = models.IntegerField(blank=True, null=True)
    question18_mostdepressed = models.IntegerField(blank=True, null=True)
    question19_lastweek = models.IntegerField(blank=True, null=True)
    question19_mostdepressed = models.IntegerField(blank=True, null=True)
    total_score_lastweek = models.FloatField(blank=True, null=True)
    total_score_mostdepressed = models.FloatField(blank=True, null=True)
    doctor = models.ForeignKey('SUser', models.DO_NOTHING)
    create_time = models.DateTimeField()
    update_time = models.DateTimeField()
    self_mutilation_remark = models.CharField(max_length=50, blank=True, null=True)
    suicide_ideation = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'r_patient_suicidal'


class RPatientTms(models.Model):
    patient_session = models.ForeignKey(DPatientDetail, models.DO_NOTHING, unique=True)
    treatment = models.ForeignKey('DTreatment', models.DO_NOTHING)
    treatment_type = models.CharField(max_length=2, blank=True, null=True)
    treatment_site = models.CharField(max_length=40, blank=True, null=True)
    motion_threshold = models.IntegerField(blank=True, null=True)
    energy_intensity = models.FloatField(blank=True, null=True)
    frequency = models.IntegerField(blank=True, null=True)
    pulses_number = models.IntegerField(blank=True, null=True)
    duration = models.IntegerField(blank=True, null=True)
    interval_time = models.IntegerField(blank=True, null=True)
    researcher_sign = models.IntegerField(blank=True, null=True)
    stimulate_num = models.IntegerField(blank=True, null=True)
    treatment_duration = models.IntegerField(blank=True, null=True)
    treatment_number = models.IntegerField(blank=True, null=True)
    feelings = models.TextField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    begin_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    doctor = models.ForeignKey('SUser', models.DO_NOTHING)
    create_time = models.DateTimeField()
    update_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'r_patient_tms'


class RPatientVept(models.Model):
    patient_session = models.ForeignKey(DPatientDetail, models.DO_NOTHING, unique=True)
    scale = models.ForeignKey(DScales, models.DO_NOTHING)
    calm = models.IntegerField(blank=True, null=True)
    angry = models.IntegerField(blank=True, null=True)
    disgusting = models.IntegerField(blank=True, null=True)
    fear = models.IntegerField(blank=True, null=True)
    satire = models.IntegerField(blank=True, null=True)
    sad = models.IntegerField(blank=True, null=True)
    wonder = models.IntegerField(blank=True, null=True)
    quality_control = models.FloatField(blank=True, null=True)
    total_score = models.IntegerField(blank=True, null=True)
    doctor = models.ForeignKey('SUser', models.DO_NOTHING)
    create_time = models.DateTimeField()
    update_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'r_patient_vept'


class RPatientWcst(models.Model):
    patient_session = models.ForeignKey(DPatientDetail, models.DO_NOTHING, unique=True)
    scale = models.ForeignKey(DScales, models.DO_NOTHING)
    ra = models.IntegerField(blank=True, null=True)
    cc = models.IntegerField(blank=True, null=True)
    rc = models.IntegerField(blank=True, null=True)
    rcp = models.FloatField(blank=True, null=True)
    re = models.IntegerField(blank=True, null=True)
    rf = models.IntegerField(blank=True, null=True)
    rfp = models.FloatField(blank=True, null=True)
    rp = models.IntegerField(blank=True, null=True)
    rpe = models.IntegerField(blank=True, null=True)
    rpep = models.FloatField(blank=True, null=True)
    nrpe = models.IntegerField(blank=True, null=True)
    fm = models.IntegerField(blank=True, null=True)
    l_l = models.FloatField(blank=True, null=True)
    doctor = models.ForeignKey('SUser', models.DO_NOTHING)
    create_time = models.DateTimeField()
    update_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'r_patient_wcst'


class RPatientYbobsessiontable(models.Model):
    patient_session = models.ForeignKey(DPatientDetail, models.DO_NOTHING, unique=True)
    scale = models.ForeignKey(DScales, models.DO_NOTHING)
    forced_frequency = models.IntegerField(blank=True, null=True)
    impediment_degree1 = models.IntegerField(blank=True, null=True)
    impediment_degree2 = models.IntegerField(blank=True, null=True)
    distress = models.IntegerField(blank=True, null=True)
    fightforced_degree = models.IntegerField(blank=True, null=True)
    control_ability1 = models.IntegerField(blank=True, null=True)
    control_ability2 = models.IntegerField(blank=True, null=True)
    compulsion_frequency = models.IntegerField(blank=True, null=True)
    stopcompulsion_anxiety = models.IntegerField(blank=True, null=True)
    stopforced_frequency = models.IntegerField(blank=True, null=True)
    total_score = models.IntegerField(blank=True, null=True)
    doctor = models.ForeignKey('SUser', models.DO_NOTHING)
    create_time = models.DateTimeField()
    update_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'r_patient_ybobsessiontable'


class RPatientYmrs(models.Model):
    patient_session = models.ForeignKey(DPatientDetail, models.DO_NOTHING, unique=True)
    scale = models.ForeignKey(DScales, models.DO_NOTHING)
    emotional_upsurge = models.IntegerField(blank=True, null=True)
    vigorous_energy = models.IntegerField(blank=True, null=True)
    sexual_desire = models.IntegerField(blank=True, null=True)
    sleep = models.IntegerField(blank=True, null=True)
    irritability = models.IntegerField(blank=True, null=True)
    speech = models.IntegerField(blank=True, null=True)
    language = models.IntegerField(blank=True, null=True)
    thinking_content = models.IntegerField(blank=True, null=True)
    aggressive_behavior = models.IntegerField(blank=True, null=True)
    appearance = models.IntegerField(blank=True, null=True)
    self_awareness = models.IntegerField(blank=True, null=True)
    total_score = models.IntegerField(blank=True, null=True)
    doctor = models.ForeignKey('SUser', models.DO_NOTHING)
    create_time = models.DateTimeField()
    update_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'r_patient_ymrs'


class RSelfTestDuration(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    patient_session_id = models.IntegerField()
    scale_id = models.IntegerField()
    question_index = models.IntegerField()
    duration = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'r_self_test_duration'


class RUserRecord(models.Model):
    user_id = models.IntegerField(blank=True, null=True)
    login_time = models.DateTimeField(blank=True, null=True)
    operate_type = models.IntegerField(blank=True, null=True)
    patient_id = models.IntegerField(blank=True, null=True)
    operation_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'r_user_record'


class SUser(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    active = models.IntegerField()
    name = models.CharField(max_length=45, blank=True, null=True)
    type = models.IntegerField()

    class Meta:
        managed = False
        db_table = 's_user'
