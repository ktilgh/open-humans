# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-27 06:38
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('runkeeper', '0008_auto_20160209_0559'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userdata',
            name='user',
        ),
        migrations.DeleteModel(
            name='UserData',
        ),
    ]
