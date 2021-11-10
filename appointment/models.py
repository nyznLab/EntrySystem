from django.db import models

# Create your models here.

# 预约
class TAppointment(models.Model):
    appointment_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    sex = models.IntegerField()
    birth_date = models.DateField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    doctor_id = models.IntegerField()
    items = models.CharField(max_length=255, blank=True, null=True)
    remark = models.CharField(max_length=255, blank=True, null=True)
    appointment_date = models.DateField()
    appointment_time = models.IntegerField()
    status = models.IntegerField()
    create_time = models.BigIntegerField()
    update_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_appointment'
