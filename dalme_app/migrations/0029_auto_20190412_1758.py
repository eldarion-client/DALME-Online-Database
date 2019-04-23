# Generated by Django 2.1.7 on 2019-04-12 21:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dalme_app', '0028_auto_20190412_1741'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='dam_usergroup',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='dam_userid',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='wiki_groups',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='wiki_userid',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='wiki_username',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='wp_avatar_url',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='wp_role',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='wp_userid',
        ),
        migrations.AddField(
            model_name='profile',
            name='dam_user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='dalme_app.rs_user'),
        ),
        migrations.AddField(
            model_name='profile',
            name='wiki_user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='dalme_app.wiki_user'),
        ),
        migrations.AddField(
            model_name='profile',
            name='wp_user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='dalme_app.wp_users'),
        ),
    ]