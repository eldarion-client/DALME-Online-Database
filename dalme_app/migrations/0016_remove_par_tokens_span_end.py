# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2017-08-05 13:18
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dalme_app', '0015_par_tokens_span_end'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='par_tokens',
            name='span_end',
        ),
    ]