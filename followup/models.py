# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from patients.models import BPatientBaseInfo,DPatientDetail

class RPatientFollowup(models.Model):
    id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(BPatientBaseInfo, models.DO_NOTHING)
    session_id = models.IntegerField()
    patient_session = models.ForeignKey(DPatientDetail, models.DO_NOTHING, unique=True)
    first_scan_time = models.DateTimeField(blank=True, null=True)
    followup_intention = models.IntegerField(blank=True, null=True)
    intention_note = models.TextField(blank=True, null=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'r_patient_followup'
