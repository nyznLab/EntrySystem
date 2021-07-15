

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scales', '0006_merge_20210305_1224'),
    ]

    operations = [
        migrations.CreateModel(
            name='RPatientGad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question1_answer', models.IntegerField(blank=True, null=True)),
                ('question2_answer', models.IntegerField(blank=True, null=True)),
                ('question3_answer', models.IntegerField(blank=True, null=True)),
                ('question4_answer', models.IntegerField(blank=True, null=True)),
                ('question5_answer', models.IntegerField(blank=True, null=True)),
                ('question6_answer', models.IntegerField(blank=True, null=True)),
                ('question7_answer', models.IntegerField(blank=True, null=True)),
                ('total_score', models.IntegerField(blank=True, null=True)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'r_patient_gad',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='RPatientInsomnia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question1_answer', models.IntegerField(blank=True, null=True)),
                ('question2_answer', models.IntegerField(blank=True, null=True)),
                ('question3_answer', models.IntegerField(blank=True, null=True)),
                ('question4_answer', models.IntegerField(blank=True, null=True)),
                ('question5_answer', models.IntegerField(blank=True, null=True)),
                ('question6_answer', models.IntegerField(blank=True, null=True)),
                ('question7_answer', models.IntegerField(blank=True, null=True)),
                ('total_score', models.IntegerField(blank=True, null=True)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'r_patient_insomnia',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='RPatientPhq',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question1_answer', models.IntegerField(blank=True, null=True)),
                ('question2_answer', models.IntegerField(blank=True, null=True)),
                ('question3_answer', models.IntegerField(blank=True, null=True)),
                ('question4_answer', models.IntegerField(blank=True, null=True)),
                ('question5_answer', models.IntegerField(blank=True, null=True)),
                ('question6_answer', models.IntegerField(blank=True, null=True)),
                ('question7_answer', models.IntegerField(blank=True, null=True)),
                ('question8_answer', models.IntegerField(blank=True, null=True)),
                ('question9_answer', models.IntegerField(blank=True, null=True)),
                ('total_score', models.IntegerField(blank=True, null=True)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'r_patient_phq',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='RPatientPss',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question1_answer', models.IntegerField(blank=True, null=True)),
                ('question2_answer', models.IntegerField(blank=True, null=True)),
                ('question3_answer', models.IntegerField(blank=True, null=True)),
                ('question4_answer', models.IntegerField(blank=True, null=True)),
                ('question5_answer', models.IntegerField(blank=True, null=True)),
                ('question6_answer', models.IntegerField(blank=True, null=True)),
                ('question7_answer', models.IntegerField(blank=True, null=True)),
                ('question8_answer', models.IntegerField(blank=True, null=True)),
                ('question9_answer', models.IntegerField(blank=True, null=True)),
                ('question10_answer', models.IntegerField(blank=True, null=True)),
                ('question11_answer', models.IntegerField(blank=True, null=True)),
                ('question12_answer', models.IntegerField(blank=True, null=True)),
                ('question13_answer', models.IntegerField(blank=True, null=True)),
                ('total_score', models.IntegerField(blank=True, null=True)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'r_patient_pss',
                'managed': False,
            },
        ),
    ]
