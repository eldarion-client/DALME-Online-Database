# Generated by Django 2.1.7 on 2019-02-18 19:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dalme_app', '0007_content_type_default_headers'),
    ]

    operations = [
        migrations.CreateModel(
            name='Content_list',
            fields=[
                ('id', models.AutoField(db_index=True, primary_key=True, serialize=False, unique=True)),
                ('creation_username', models.CharField(blank=True, max_length=255, null=True)),
                ('creation_timestamp', models.DateTimeField(auto_now_add=True, null=True)),
                ('modification_username', models.CharField(blank=True, max_length=255, null=True)),
                ('modification_timestamp', models.DateTimeField(auto_now=True, null=True)),
                ('name', models.CharField(max_length=255)),
                ('short_name', models.CharField(max_length=55)),
                ('description', models.TextField()),
                ('default_headers', models.CharField(max_length=255, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Content_list_x_content_type',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_username', models.CharField(blank=True, max_length=255, null=True)),
                ('creation_timestamp', models.DateTimeField(auto_now_add=True, null=True)),
                ('modification_username', models.CharField(blank=True, max_length=255, null=True)),
                ('modification_timestamp', models.DateTimeField(auto_now=True, null=True)),
                ('content_list', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dalme_app.Content_list')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='content_type',
            name='default_headers',
        ),
        migrations.AddField(
            model_name='content_list_x_content_type',
            name='content_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='dalme_app.Content_type'),
        ),
    ]