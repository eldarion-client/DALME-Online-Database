# Generated by Django 2.1.7 on 2019-05-09 22:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dalme_app', '0067_auto_20190509_1821'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attribute_type',
            name='data_type',
            field=models.CharField(choices=[('DATE', 'DATE (date)'), ('INT', 'INT (integer)'), ('STR', 'STR (string)'), ('TXT', 'TXT (text)')], max_length=15),
        ),
    ]