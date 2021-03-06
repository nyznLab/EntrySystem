# Generated by Django 2.2 on 2022-05-11 21:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TAppointment',
            fields=[
                ('appointment_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20)),
                ('sex', models.IntegerField()),
                ('birth_date', models.DateField()),
                ('phone', models.CharField(blank=True, max_length=20, null=True)),
                ('doctor_id', models.IntegerField()),
                ('items', models.CharField(blank=True, max_length=255, null=True)),
                ('remark', models.CharField(blank=True, max_length=255, null=True)),
                ('appointment_date', models.DateField()),
                ('appointment_time', models.IntegerField()),
                ('status', models.IntegerField()),
                ('create_time', models.BigIntegerField()),
                ('update_time', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 't_appointment',
                'managed': False,
            },
        ),
    ]
