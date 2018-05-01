# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-05-31 18:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PlatonicConcept',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('_id', models.CharField(max_length=36)),
                ('term', models.CharField(max_length=255)),
                ('comments', models.TextField()),
                ('creation_username', models.CharField(max_length=255)),
                ('creation_timestamp', models.DateField(auto_now_add=True)),
                ('modification_username', models.CharField(max_length=255)),
                ('modification_timestamp', models.DateField(auto_now=True)),
            ],
        ),
    ]