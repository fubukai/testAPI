# Generated by Django 3.0.3 on 2020-09-29 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('elearning', '0029_auto_20200920_2325'),
    ]

    operations = [
        migrations.AddField(
            model_name='hub_test',
            name='feedback',
            field=models.TextField(blank=True, null=True),
        ),
    ]