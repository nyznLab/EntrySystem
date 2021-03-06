# Generated by Django 2.2.6 on 2021-01-27 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0004_rpatientghr'),
    ]

    operations = [
        migrations.CreateModel(
            name='BPatientRtms',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('treatment_num', models.IntegerField()),
                ('treatment_date', models.DateField()),
                ('therapeutic_target', models.IntegerField(blank=True, null=True)),
                ('times_per_day', models.IntegerField(blank=True, null=True)),
                ('total_num', models.IntegerField()),
                ('resting_motor_threshold', models.IntegerField()),
                ('intensity', models.IntegerField()),
                ('frequency', models.IntegerField()),
                ('pulses', models.IntegerField()),
                ('stimulation_time', models.IntegerField()),
                ('inter_train_intervals', models.IntegerField()),
                ('pulse_trains', models.IntegerField()),
                ('total_pulses', models.IntegerField()),
                ('total_time_minute', models.IntegerField()),
                ('total_time_second', models.IntegerField()),
                ('note', models.TextField(blank=True, null=True)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'b_patient_rtms',
                'managed': False,
            },
        ),
    ]
