# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2017-08-06 18:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dalme_app', '0024_error_messages'),
    ]

    operations = [
        migrations.AlterField(
            model_name='error_messages',
            name='_text',
            field=models.TextField(),
        ),
    ]