from django.db import models


class rPatientRtms(models.Model):
    id = models.IntegerField(primary_key=True)
    patient_id = models.IntegerField()
    session_id = models.IntegerField()
    treatment_id = models.IntegerField()
    resting_motor_threshold = models.IntegerField(blank=True, null=True)
    intensity = models.IntegerField(blank=True, null=True)
    treatment_date = models.DateField(blank=True, null=True)
    treatment_num = models.IntegerField(blank=True, null=True)
    times_per_day = models.IntegerField(blank=True, null=True)
    note = models.CharField(max_length=40, blank=True, null=True)
    doctor_id = models.IntegerField(null=False, blank=False)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    delete = models.IntegerField()

    def update_times_per_day(self, num):
        self.times_per_day = num

    class Meta:
        managed = False
        db_table = 'r_patient_rtms'


class tTreatmentRtms(models.Model):
    id = models.IntegerField(primary_key=True)
    treatment_id = models.IntegerField()
    treatment_name = models.CharField(max_length=40)
    therapeutic_target = models.CharField(max_length=40, blank=True, null=True)
    frequency = models.IntegerField(blank=True, null=True)
    pulses = models.IntegerField(blank=True, null=True)
    stimulation_time = models.IntegerField(blank=True, null=True)
    inter_train_intervals = models.IntegerField(blank=True, null=True)
    pulse_trains = models.IntegerField(blank=True, null=True)
    total_pulses = models.IntegerField(blank=True, null=True)
    total_time_minute = models.IntegerField(blank=True, null=True)
    total_time_second = models.IntegerField(blank=True, null=True)
    note = models.CharField(max_length=40, blank=True, null=True)
    doctor_id = models.IntegerField(null=False, blank=False)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    delete = models.IntegerField()

    class Meta:
        managed = False
        db_table = 't_treatment_rtms'
