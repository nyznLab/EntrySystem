from django.db import models
from patients.models import BPatientBaseInfo

# Create your models here.


# 待办


class TSchedule(models.Model):
    schedule_id = models.AutoField(primary_key=True)
    # patient_id = models.IntegerField()
    patient = models.ForeignKey(BPatientBaseInfo, models.DO_NOTHING, blank=True, null=True)
    patient_session_id = models.IntegerField()
    name = models.CharField(max_length=20, blank=True, null=True)
    standard_id = models.CharField(max_length=20, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=255)
    is_urgent = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    item_type = models.IntegerField()
    remark = models.CharField(max_length=255, blank=True, null=True)
    status = models.IntegerField()
    doctor_id = models.IntegerField()
    create_time = models.BigIntegerField()
    update_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_schedule'
