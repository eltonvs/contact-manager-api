# Generated by Django 2.1.2 on 2018-10-23 19:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0008_auto_20181023_0445'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='phonenumber',
            name='primary',
        ),
    ]