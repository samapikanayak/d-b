# Generated by Django 4.0.4 on 2022-07-20 10:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('store', '0007_alter_businessunit_cd_cny_iso_4217_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('department_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(help_text='Department name', max_length=100)),
                ('description', models.TextField(blank=True, help_text='Department description', null=True)),
                ('status', models.CharField(blank=True, choices=[('Active', 'Active'), ('Inactive', 'Inactive')], help_text='Department status (Active/Inactive)', max_length=100, null=True)),
                ('isdeleted', models.BooleanField(blank=True, default=False, help_text='Is Deleted?', null=True)),
                ('createdby', models.IntegerField(help_text='Created By', null=True)),
                ('createddate', models.DateTimeField(auto_now_add=True, help_text='Date Created', null=True)),
                ('updatedby', models.IntegerField(help_text='Updated By ', null=True)),
                ('updateddate', models.DateTimeField(auto_now=True, help_text='Last Updated Date', null=True)),
                ('business_unit_group_code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='business_unit_group', to='store.businessunitgroup')),
                ('parent_department_id', models.ForeignKey(db_column='parent_department_id', null=True, on_delete=django.db.models.deletion.CASCADE, to='department.department', verbose_name='ParentDepartmentID')),
            ],
        ),
    ]
