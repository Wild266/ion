# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-27 02:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [('eighth', '0042_auto_20160829_1242')]

    operations = [
        migrations.AddField(
            model_name='eighthactivity',
            name='admin_comments',
            field=models.CharField(blank=True, max_length=1000),),
        migrations.AddField(
            model_name='historicaleighthactivity',
            name='admin_comments',
            field=models.CharField(blank=True, max_length=1000),),
    ]