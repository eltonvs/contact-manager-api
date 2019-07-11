# Generated by Django 2.1.3 on 2018-11-05 19:38

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0011_auto_20181102_0359'),
    ]

    operations = [
        migrations.AlterField(
            model_name='phonenumber',
            name='phone',
            field=models.CharField(max_length=20, unique=True, validators=[django.core.validators.RegexValidator(regex='^[0-9 -+]+$')]),
        ),
    ]