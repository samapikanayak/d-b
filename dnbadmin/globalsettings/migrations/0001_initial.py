# Generated by Django 4.0.4 on 2022-06-28 10:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('party', '0003_alter_iso3166_1country_options_and_more'),
        ('store', '0006_alter_businessunitgrouplevel_id_bsngp_lv_prnt'),
        ('basics', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GlobalSetting',
            fields=[
                ('ID_GB_STNG', models.BigAutoField(primary_key=True, serialize=False, verbose_name='GlobalSettingID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Setting name')),
                ('status', models.CharField(choices=[('A', 'Active'), ('I', 'Inactive')], default='A', max_length=2, verbose_name='Status Code')),
                ('is_default', models.BooleanField(blank=True, default=False, null=True, verbose_name='Is Default Settings?')),
                ('page_title', models.CharField(blank=True, help_text='Page title', max_length=100, null=True, verbose_name='Page title')),
                ('page_description', models.TextField(blank=True, help_text='Page description', null=True, verbose_name='Page description')),
                ('page_keyword', models.CharField(blank=True, help_text='Page keyword', max_length=100, null=True, verbose_name='Page keyword')),
                ('meta_locale', models.CharField(blank=True, help_text='Meta location', max_length=255, null=True, verbose_name='Meta locale')),
                ('meta_robots', models.CharField(blank=True, help_text='Meta robots', max_length=255, null=True, verbose_name='Meta robots')),
                ('meta_referral', models.CharField(blank=True, help_text='Meta referral', max_length=255, null=True, verbose_name='Meta referral')),
                ('meta_rights', models.CharField(blank=True, help_text='Meta rights', max_length=255, null=True, verbose_name='Meta rights')),
                ('og_type', models.CharField(blank=True, help_text='OG type', max_length=100, null=True, verbose_name='OG type')),
                ('og_url', models.CharField(blank=True, help_text='OG url', max_length=255, null=True, verbose_name='OG url')),
                ('og_title', models.CharField(blank=True, help_text='OG title', max_length=100, null=True, verbose_name='OG title')),
                ('og_description', models.TextField(blank=True, help_text='OG description', null=True, verbose_name='OG description')),
                ('og_image', models.CharField(blank=True, help_text='OG image', max_length=255, null=True, verbose_name='OG image')),
                ('og_locale', models.CharField(blank=True, help_text='OG locale', max_length=255, null=True, verbose_name='OG locale')),
                ('twitter_card', models.CharField(blank=True, help_text='Twitter card', max_length=255, null=True, verbose_name='Twitter card')),
                ('view_point', models.CharField(blank=True, help_text='View point', max_length=255, null=True, verbose_name='View point')),
                ('script', models.TextField(blank=True, help_text='Script', null=True, verbose_name='Script')),
                ('createdby', models.IntegerField(null=True, verbose_name='Created By')),
                ('createddate', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Date Created')),
                ('updatedby', models.IntegerField(null=True, verbose_name='Updated By')),
                ('updateddate', models.DateTimeField(auto_now=True, null=True, verbose_name='Last Updated Date')),
                ('ID_BA_DFMT', models.ForeignKey(blank=True, db_column='ID_BA_DFMT', null=True, on_delete=django.db.models.deletion.SET_NULL, to='basics.dateformat', verbose_name='DateFormatID')),
                ('ID_BA_TZN', models.ForeignKey(blank=True, db_column='ID_BA_TZN', null=True, on_delete=django.db.models.deletion.SET_NULL, to='basics.timezone', verbose_name='TimezoneID')),
                ('ID_LGE', models.ForeignKey(blank=True, db_column='ID_LGE', null=True, on_delete=django.db.models.deletion.SET_NULL, to='party.language', verbose_name='LanguageID')),
            ],
            options={
                'db_table': 'CO_GB_STNG',
            },
        ),
        migrations.CreateModel(
            name='BusinessUnitSetting',
            fields=[
                ('ID_BSN_UN_STNG', models.BigAutoField(primary_key=True, serialize=False, verbose_name='BusinessUnitSettingID')),
                ('ID_BSN_UN', models.ForeignKey(db_column='ID_BSN_UN', on_delete=django.db.models.deletion.CASCADE, to='store.businessunit', verbose_name='BusinessUnitID')),
                ('ID_GB_STNG', models.ForeignKey(db_column='ID_GB_STNG', on_delete=django.db.models.deletion.CASCADE, to='globalsettings.globalsetting', verbose_name='GlobalSettingID')),
            ],
            options={
                'db_table': 'CO_BSN_UN_STNG',
            },
        ),
    ]
