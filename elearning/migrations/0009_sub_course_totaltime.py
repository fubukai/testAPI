# Generated by Django 3.0.3 on 2020-07-16 03:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('elearning', '0008_staff_vdolog_link_course'),
    ]

    operations = [
        migrations.AddField(
            model_name='sub_course',
            name='TotalTime',
            field=models.IntegerField(default=0, null=True),
        ),
    ]
