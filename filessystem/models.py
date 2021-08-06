# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from patients.models import DPatientDetail


class RPatientFiles(models.Model):
    patient_session = models.ForeignKey(DPatientDetail, models.DO_NOTHING)
    create_time = models.DateTimeField(blank=True, null=True)
    update_time = models.DateTimeField(blank=True, null=True)
    dicom_save = models.IntegerField()
    dicom_quality = models.IntegerField(blank=True, null=True)
    reho_arwdcf_save = models.IntegerField(blank=True, null=True)
    fc_arwsdcf_save = models.IntegerField(blank=True, null=True)
    falff_arwsd_save = models.IntegerField(blank=True, null=True)
    alff_arwsd_save = models.IntegerField(blank=True, null=True)
    voxel_wose_fc = models.IntegerField(blank=True, null=True)
    image_description = models.TextField(blank=True, null=True)
    audio_save = models.IntegerField(blank=True, null=True)
    video_save = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'r_patient_files'
