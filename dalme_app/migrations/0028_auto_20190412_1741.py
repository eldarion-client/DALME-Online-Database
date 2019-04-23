# Generated by Django 2.1.7 on 2019-04-12 21:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dalme_app', '0027_auto_20190328_1149'),
    ]

    operations = [
        migrations.CreateModel(
            name='rs_collection',
            fields=[
                ('ref', models.IntegerField(max_length=11, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100, null=True)),
                ('user', models.IntegerField(max_length=11, null=True)),
                ('created', models.DateTimeField(blank=True, null=True)),
                ('public', models.IntegerField(default='0', max_length=11)),
                ('theme', models.CharField(max_length=100, null=True)),
                ('theme2', models.CharField(max_length=100, null=True)),
                ('theme3', models.CharField(max_length=100, null=True)),
                ('allow_changes', models.IntegerField(default='0', max_length=11)),
                ('cant_delete', models.IntegerField(default='0', max_length=11)),
                ('keywords', models.TextField()),
                ('savedsearch', models.IntegerField(max_length=11, null=True)),
                ('home_page_publish', models.IntegerField(max_length=11, null=True)),
                ('home_page_text', models.TextField()),
                ('home_page_image', models.IntegerField(max_length=11, null=True)),
                ('session_id', models.IntegerField(max_length=11, null=True)),
                ('theme4', models.CharField(max_length=100, null=True)),
                ('theme5', models.CharField(max_length=100, null=True)),
                ('theme6', models.CharField(max_length=100, null=True)),
                ('theme7', models.CharField(max_length=100, null=True)),
                ('theme8', models.CharField(max_length=100, null=True)),
                ('theme9', models.CharField(max_length=100, null=True)),
                ('theme10', models.CharField(max_length=100, null=True)),
                ('theme11', models.CharField(max_length=100, null=True)),
                ('theme12', models.CharField(max_length=100, null=True)),
                ('theme13', models.CharField(max_length=100, null=True)),
                ('theme14', models.CharField(max_length=100, null=True)),
                ('theme15', models.CharField(max_length=100, null=True)),
                ('theme16', models.CharField(max_length=100, null=True)),
                ('theme17', models.CharField(max_length=100, null=True)),
                ('theme18', models.CharField(max_length=100, null=True)),
                ('theme19', models.CharField(max_length=100, null=True)),
                ('theme20', models.CharField(max_length=100, null=True)),
            ],
            options={
                'db_table': 'collection',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='rs_collection_resource',
            fields=[
                ('collection', models.IntegerField(max_length=11, null=True)),
                ('resource', models.IntegerField(max_length=11, null=True)),
                ('date_added', models.DateTimeField(auto_now_add=True, primary_key=True, serialize=False)),
                ('comment', models.TextField()),
                ('rating', models.IntegerField(max_length=11, null=True)),
                ('use_as_theme_thumbnail', models.IntegerField(max_length=11, null=True)),
                ('purchase_size', models.CharField(max_length=10, null=True)),
                ('purchase_complete', models.IntegerField(default='0', max_length=11)),
                ('purchase_price', models.FloatField(default='0.00', max_length=10)),
                ('sortorder', models.IntegerField(max_length=11, null=True)),
            ],
            options={
                'db_table': 'collection_resource',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='rs_resource',
            fields=[
                ('ref', models.IntegerField(max_length=11, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=200, null=True)),
                ('resource_type', models.IntegerField(max_length=11, null=True)),
                ('has_image', models.IntegerField(default='0', max_length=11)),
                ('is_transcoding', models.IntegerField(default='0', max_length=11)),
                ('hit_count', models.IntegerField(default='0', max_length=11)),
                ('new_hit_count', models.IntegerField(default='0', max_length=11)),
                ('creation_date', models.DateTimeField(blank=True, null=True)),
                ('rating', models.IntegerField(max_length=11, null=True)),
                ('user_rating', models.IntegerField(max_length=11, null=True)),
                ('user_rating_count', models.IntegerField(max_length=11, null=True)),
                ('user_rating_total', models.IntegerField(max_length=11, null=True)),
                ('country', models.CharField(max_length=200, null=True)),
                ('file_extension', models.CharField(max_length=10, null=True)),
                ('preview_extension', models.CharField(max_length=10, null=True)),
                ('image_red', models.IntegerField(max_length=11, null=True)),
                ('image_green', models.IntegerField(max_length=11, null=True)),
                ('image_blue', models.IntegerField(max_length=11, null=True)),
                ('thumb_width', models.IntegerField(max_length=11, null=True)),
                ('thumb_height', models.IntegerField(max_length=11, null=True)),
                ('archive', models.IntegerField(default='0', max_length=11)),
                ('access', models.IntegerField(default='0', max_length=11)),
                ('colour_key', models.CharField(max_length=5, null=True)),
                ('created_by', models.IntegerField(max_length=11, null=True)),
                ('file_path', models.CharField(max_length=500, null=True)),
                ('file_modified', models.DateTimeField(blank=True, null=True)),
                ('file_checksum', models.CharField(max_length=32, null=True)),
                ('request_count', models.IntegerField(default='0', max_length=11)),
                ('expiry_notification_sent', models.IntegerField(default='0', max_length=11)),
                ('preview_tweaks', models.CharField(max_length=50, null=True)),
                ('geo_lat', models.FloatField(null=True)),
                ('geo_long', models.FloatField(null=True)),
                ('mapzoom', models.IntegerField(max_length=11, null=True)),
                ('disk_usage', models.IntegerField(max_length=20, null=True)),
                ('disk_usage_last_updated', models.DateTimeField(blank=True, null=True)),
                ('file_size', models.IntegerField(max_length=20, null=True)),
                ('preview_attempts', models.IntegerField(max_length=11, null=True)),
                ('field12', models.CharField(max_length=200, null=True)),
                ('field8', models.CharField(max_length=200, null=True)),
                ('field3', models.CharField(max_length=200, null=True)),
                ('annotation_count', models.IntegerField(max_length=11, null=True)),
                ('field51', models.CharField(max_length=200, null=True)),
                ('field79', models.CharField(max_length=200, null=True)),
                ('modified', models.DateTimeField(auto_now_add=True, null=True)),
            ],
            options={
                'db_table': 'resource',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='rs_resource_data',
            fields=[
                ('resource', models.IntegerField(max_length=11, primary_key=True, serialize=False)),
                ('resource_type_field', models.IntegerField(max_length=11, null=True)),
                ('value', models.TextField()),
            ],
            options={
                'db_table': 'resource_data',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='rs_resource_type_field',
            fields=[
                ('ref', models.IntegerField(max_length=11, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50, null=True)),
                ('title', models.CharField(max_length=400, null=True)),
                ('type', models.IntegerField(max_length=11, null=True)),
                ('order_by', models.IntegerField(default='0', max_length=11)),
                ('keywords_index', models.IntegerField(default='0', max_length=11)),
                ('partial_index', models.IntegerField(default='0', max_length=11)),
                ('resource_type', models.IntegerField(default='0', max_length=11)),
                ('resource_column', models.CharField(max_length=50, null=True)),
                ('display_field', models.IntegerField(default='1', max_length=11)),
                ('use_for_similar', models.IntegerField(default='1', max_length=11)),
                ('iptc_equiv', models.CharField(max_length=20, null=True)),
                ('display_template', models.TextField()),
                ('tab_name', models.CharField(max_length=50, null=True)),
                ('required', models.IntegerField(default='0', max_length=11)),
                ('smart_theme_name', models.CharField(max_length=200, null=True)),
                ('exiftool_field', models.CharField(max_length=200, null=True)),
                ('advanced_search', models.IntegerField(default='1', max_length=11)),
                ('simple_search', models.IntegerField(default='0', max_length=11)),
                ('help_text', models.TextField()),
                ('display_as_dropdown', models.IntegerField(default='0', max_length=11)),
                ('external_user_access', models.IntegerField(default='1', max_length=11)),
                ('autocomplete_macro', models.TextField()),
                ('hide_when_uploading', models.IntegerField(default='0', max_length=11)),
                ('hide_when_restricted', models.IntegerField(default='0', max_length=11)),
                ('value_filter', models.TextField()),
                ('exiftool_filter', models.TextField()),
                ('omit_when_copying', models.IntegerField(default='0', max_length=11)),
                ('tooltip_text', models.TextField()),
                ('regexp_filter', models.CharField(max_length=400, null=True)),
                ('sync_field', models.IntegerField(max_length=11, null=True)),
                ('display_condition', models.CharField(max_length=400, null=True)),
                ('onchange_macro', models.TextField()),
                ('field_constraint', models.IntegerField(max_length=11, null=True)),
                ('linked_data_field', models.TextField()),
                ('automatic_nodes_ordering', models.IntegerField(default='0', max_length=1)),
                ('fits_field', models.CharField(max_length=255, null=True)),
                ('personal_data', models.IntegerField(default='0', max_length=1)),
            ],
            options={
                'db_table': 'resource_type_field',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='rs_user',
            fields=[
                ('ref', models.IntegerField(max_length=11, primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=50, null=True)),
                ('password', models.CharField(max_length=64, null=True)),
                ('fullname', models.CharField(max_length=100, null=True)),
                ('email', models.CharField(max_length=100, null=True)),
                ('usergroup', models.IntegerField(max_length=11, null=True)),
                ('last_active', models.DateTimeField(blank=True, null=True)),
                ('logged_in', models.IntegerField(max_length=11, null=True)),
                ('last_browser', models.TextField()),
                ('last_ip', models.CharField(max_length=100, null=True)),
                ('current_collection', models.IntegerField(max_length=11, null=True)),
                ('accepted_terms', models.IntegerField(default='0', max_length=11)),
                ('account_expires', models.DateTimeField(blank=True, null=True)),
                ('comments', models.TextField()),
                ('session', models.CharField(max_length=50, null=True)),
                ('ip_restrict', models.TextField()),
                ('search_filter_override', models.TextField()),
                ('password_last_change', models.DateTimeField(null=True)),
                ('login_tries', models.IntegerField(default='0', max_length=11)),
                ('login_last_try', models.DateTimeField(blank=True, null=True)),
                ('approved', models.IntegerField(default='1', max_length=11)),
                ('lang', models.CharField(max_length=11, null=True)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('hidden_collections', models.TextField()),
                ('password_reset_hash', models.CharField(max_length=100, null=True)),
                ('origin', models.CharField(max_length=50, null=True)),
                ('unique_hash', models.CharField(max_length=50, null=True)),
                ('wp_authrequest', models.CharField(max_length=50, null=True)),
                ('csrf_token', models.CharField(max_length=255, null=True)),
            ],
            options={
                'db_table': 'user',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='wiki_page',
            fields=[
                ('page_id', models.IntegerField(max_length=10, primary_key=True, serialize=False)),
                ('page_namespace', models.IntegerField(max_length=11)),
                ('page_title', models.BinaryField(max_length=255)),
                ('page_restrictions', models.BinaryField()),
                ('page_is_redirect', models.IntegerField(default='0', max_length=3)),
                ('page_is_new', models.IntegerField(default='0', max_length=3)),
                ('page_random', models.FloatField()),
                ('page_touched', models.BinaryField(max_length=14)),
                ('page_links_updated', models.BinaryField(max_length=14, null=True)),
                ('page_latest', models.IntegerField(max_length=10)),
                ('page_len', models.IntegerField(max_length=10)),
                ('page_content_model', models.BinaryField(max_length=32, null=True)),
                ('page_lang', models.BinaryField(max_length=35, null=True)),
            ],
            options={
                'db_table': 'page',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='wiki_user',
            fields=[
                ('user_id', models.IntegerField(max_length=10, primary_key=True, serialize=False)),
                ('user_name', models.BinaryField(max_length=255, unique=True)),
                ('user_real_name', models.BinaryField(max_length=255)),
                ('user_password', models.BinaryField()),
                ('user_newpassword', models.BinaryField()),
                ('user_newpass_time', models.BinaryField(max_length=14, null=True)),
                ('user_email', models.BinaryField()),
                ('user_touched', models.BinaryField(max_length=14)),
                ('user_token', models.BinaryField(max_length=32)),
                ('user_email_authenticated', models.BinaryField(max_length=14, null=True)),
                ('user_email_token', models.BinaryField(max_length=32, null=True)),
                ('user_email_token_expires', models.BinaryField(max_length=14, null=True)),
                ('user_registration', models.BinaryField(max_length=14, null=True)),
                ('user_editcount', models.IntegerField(max_length=11, null=True)),
                ('user_password_expires', models.BinaryField(max_length=14, null=True)),
            ],
            options={
                'db_table': 'user',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='wiki_user_groups',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ug_user', models.IntegerField(default='0', max_length=10)),
                ('ug_group', models.BinaryField(max_length=255)),
                ('ug_expiry', models.BinaryField(max_length=14, null=True)),
            ],
            options={
                'db_table': 'user_groups',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='wp_usermeta',
            fields=[
                ('umeta_id', models.IntegerField(max_length=20, primary_key=True, serialize=False)),
                ('user_id', models.IntegerField(default='0', max_length=20)),
                ('meta_key', models.CharField(max_length=255, null=True)),
                ('meta_value', models.TextField()),
            ],
            options={
                'db_table': 'wp_usermeta',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='wp_users',
            fields=[
                ('ID', models.IntegerField(max_length=20, primary_key=True, serialize=False)),
                ('user_login', models.CharField(max_length=60)),
                ('user_pass', models.CharField(max_length=255)),
                ('user_nicename', models.CharField(max_length=50)),
                ('user_email', models.CharField(max_length=100)),
                ('user_url', models.CharField(max_length=100)),
                ('user_registered', models.DateTimeField(default='0000-00-00 00:00:00')),
                ('user_activation_key', models.CharField(max_length=255)),
                ('user_status', models.IntegerField(default='0', max_length=11)),
                ('display_name', models.CharField(max_length=250)),
            ],
            options={
                'db_table': 'wp_users',
                'managed': False,
            },
        ),
    ]