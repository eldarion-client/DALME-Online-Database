# Generated by Django 2.2.2 on 2019-08-06 12:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dalme_app', '0139_auto_20190802_1319'),
    ]

    operations = [
        migrations.AlterField(
            model_name='source_pages',
            name='transcription',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='source_pages', to='dalme_app.Transcription'),
        ),
    ]