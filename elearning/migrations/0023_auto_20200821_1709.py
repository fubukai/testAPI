# Generated by Django 3.0.3 on 2020-08-21 10:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('elearning', '0022_auto_20200819_2306'),
    ]

    operations = [
        migrations.AlterField(
            model_name='closed_class',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]
