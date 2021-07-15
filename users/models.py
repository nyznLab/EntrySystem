# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


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


class RUserRecord(models.Model):
    user_id = models.IntegerField(blank=True, null=True)
    login_time = models.DateTimeField(blank=True, null=True)
    operate_type = models.IntegerField(blank=True, null=True)
    patient_id = models.IntegerField(blank=True, null=True)
    operation_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'r_user_record'