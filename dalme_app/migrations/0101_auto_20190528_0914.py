# Generated by Django 2.2.1 on 2019-05-28 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dalme_app', '0100_auto_20190527_1006'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dt_fields',
            name='dt_name',
            field=models.CharField(blank=True, default=None, max_length=55, null=True),
        ),
    ]
