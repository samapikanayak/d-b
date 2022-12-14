# Generated by Django 4.0.4 on 2022-07-11 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('party', '0003_alter_iso3166_1country_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='legalorganizationtype',
            name='createdby',
            field=models.IntegerField(help_text='Created By', null=True),
        ),
        migrations.AddField(
            model_name='legalorganizationtype',
            name='createddate',
            field=models.DateTimeField(auto_now_add=True, help_text='Date Created', null=True),
        ),
        migrations.AddField(
            model_name='legalorganizationtype',
            name='status',
            field=models.CharField(blank=True, choices=[('A', 'Active'), ('I', 'Inactive')], help_text='Legal Organization type status (Active/Inactive)', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='legalorganizationtype',
            name='updatedby',
            field=models.IntegerField(help_text='Updated By ', null=True),
        ),
        migrations.AddField(
            model_name='legalorganizationtype',
            name='updateddate',
            field=models.DateTimeField(auto_now=True, help_text='Last Updated Date', null=True),
        ),
    ]
