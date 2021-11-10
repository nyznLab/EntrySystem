# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class RPatientBlood(models.Model):
    patient_session = models.ForeignKey('DPatientDetail', models.DO_NOTHING)
    blood_sample_id = models.CharField(max_length=45, blank=True, null=True)
    fake_name = models.CharField(max_length=45, blank=True, null=True)
    blood_sampling_date = models.DateField(blank=True, null=True)
    centrifugal_date = models.DateField(blank=True, null=True)
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
