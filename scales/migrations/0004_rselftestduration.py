# Generated by Django 2.2.6 on 2021-01-22 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scales', '0003_auto_20201217_1847'),
    ]

    operations = [
        migrations.CreateModel(
            name='RSelfTestDuration',
            fields=[
                ('id', models.IntegerField(auto_created=True, primary_key=True, serialize=False)),
                ('question_index', models.IntegerField(blank=True, null=True)),
                ('duration', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'r_self_test_duration',
                'managed': False,
            },
        ),
    ]
