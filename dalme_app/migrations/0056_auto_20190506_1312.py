# Generated by Django 2.1.7 on 2019-05-06 17:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dalme_app', '0055_dt_fields_filter_lookup'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dt_fields',
            name='dt_name',
            field=models.CharField(blank=True, max_length=55, null=True),
        ),
        migrations.AlterField(
            model_name='dt_fields',
            name='dte_name',
            field=models.CharField(blank=True, max_length=55, null=True),
        ),
        migrations.AlterField(
            model_name='dt_fields',
            name='dte_options',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='dt_fields',
            name='dte_opts',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='dt_fields',
            name='dte_type',
            field=models.CharField(blank=True, max_length=55, null=True),
        ),
        migrations.AlterField(
            model_name='dt_fields',
            name='filter_lookup',
            field=models.CharField(blank=True, max_length=55, null=True),
        ),
        migrations.AlterField(
            model_name='dt_fields',
            name='filter_mode',
            field=models.CharField(blank=True, max_length=55, null=True),
        ),
        migrations.AlterField(
            model_name='dt_fields',
            name='filter_options',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='dt_fields',
            name='filter_type',
            field=models.CharField(blank=True, max_length=55, null=True),
        ),
        migrations.AlterField(
            model_name='dt_fields',
            name='list',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fields', to='dalme_app.DT_list'),
        ),
        migrations.AlterField(
            model_name='dt_fields',
            name='render_exp',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='dt_list',
            name='api_url',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='dt_list',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='dt_list',
            name='form_helper',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='dt_list',
            name='preview_helper',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
