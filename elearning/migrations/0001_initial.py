# Generated by Django 3.0.3 on 2020-07-13 03:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Check',
            fields=[
                ('StaffID', models.CharField(max_length=10, primary_key=True, serialize=False, unique=True)),
                ('Error_Detail', models.CharField(max_length=200, null=True)),
                ('Date_check', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('StaffID', models.CharField(max_length=10, primary_key=True, serialize=False, unique=True)),
                ('StaffName', models.CharField(max_length=150)),
                ('StaffPosition', models.CharField(max_length=10, null=True)),
                ('StaffLevelcode', models.CharField(max_length=5, null=True)),
                ('StaffDepshort', models.CharField(max_length=200)),
                ('DeptCode', models.CharField(max_length=50)),
                ('Organization', models.CharField(max_length=100)),
                ('Date_Start', models.DateTimeField(null=True)),
                ('Date_PreTest', models.DateTimeField(null=True)),
                ('Score_PreTest', models.IntegerField(default=0, null=True)),
                ('Vdo_pass', models.CharField(default='no', max_length=2, null=True)),
                ('Date_Vdo', models.DateTimeField(null=True)),
                ('Date_PostTest', models.DateTimeField(null=True)),
                ('Score_PostTest', models.IntegerField(default=0, null=True)),
            ],
        ),
    ]
