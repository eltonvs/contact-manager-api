# Generated by Django 2.1.2 on 2018-11-02 03:59

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0010_auto_20181024_0354'),
    ]

    operations = [
        migrations.AlterField(
            model_name='phonenumber',
            name='phone',
            field=models.CharField(max_length=20, unique=True, validators=[django.core.validators.RegexValidator(regex='^\\+(?:[0-9] ?){6,14}[0-9]$')]),
        ),
    ]
