# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class RPatientSuicideBehavior(models.Model):
    patient_session = models.ForeignKey('DPatientDetail', models.DO_NOTHING, unique=True)
    scale = models.ForeignKey('DScales', models.DO_NOTHING)
    suicide_action = models.IntegerField(blank=True, null=True)
    suicide_times = models.CharField(max_length=45, blank=True, null=True)
    self_harming = models.IntegerField(blank=True, null=True)
    self_harming_times = models.CharField(max_length=45, blank=True, null=True)
    suicide_idea = models.IntegerField(blank=True, null=True)
    doctor = models.ForeignKey('SUser', models.DO_NOTHING)
    create_time = models.DateTimeField()
    update_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'r_patient_suicide_behavior'
