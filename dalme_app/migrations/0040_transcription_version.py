# Generated by Django 2.1.7 on 2019-04-21 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dalme_app', '0039_dt_fields_filter_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='transcription',
            name='version',
            field=models.IntegerField(null=True),
        ),
    ]
