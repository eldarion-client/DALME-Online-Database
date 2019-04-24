# Generated by Django 2.1.7 on 2019-04-24 13:12

import dalme_app.models
import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0009_alter_user_last_name_max_length'),
        ('dalme_app', '0042_auto_20190424_0858'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(default=datetime.datetime.now)),
                ('file', models.FileField(max_length=255)),
                ('added_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=datetime.datetime.now)),
                ('email_from', models.CharField(blank=True, max_length=320, null=True)),
                ('email_message_id', models.CharField(blank=True, max_length=255, null=True)),
                ('body', models.TextField(blank=True)),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=140)),
                ('created_date', models.DateField(blank=True, default=django.utils.timezone.now, null=True)),
                ('due_date', models.DateField(blank=True, null=True)),
                ('completed', models.BooleanField(default=False)),
                ('completed_date', models.DateField(blank=True, null=True)),
                ('note', models.TextField(blank=True, null=True)),
                ('priority', models.PositiveIntegerField(blank=True, null=True)),
                ('assigned_to', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='todo_assigned_to', to=settings.AUTH_USER_MODEL)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='todo_created_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['priority', 'created_date'],
            },
        ),
        migrations.CreateModel(
            name='TaskList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60)),
                ('slug', models.SlugField(default='')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.Group')),
            ],
            options={
                'verbose_name_plural': 'Task Lists',
                'ordering': ['name'],
            },
        ),
        migrations.AddField(
            model_name='task',
            name='task_list',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='dalme_app.TaskList'),
        ),
        migrations.AddField(
            model_name='comment',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dalme_app.Task'),
        ),
        migrations.AddField(
            model_name='attachment',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dalme_app.Task'),
        ),
        migrations.AlterUniqueTogether(
            name='tasklist',
            unique_together={('group', 'slug')},
        ),
        migrations.AlterUniqueTogether(
            name='comment',
            unique_together={('task', 'email_message_id')},
        ),
    ]
