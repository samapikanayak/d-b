# Generated by Django 4.0.4 on 2022-07-21 08:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basics', '0002_businessunittype'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImageInformation',
            fields=[
                ('imageinformation_id', models.AutoField(help_text='Image information Identity', primary_key=True, serialize=False)),
                ('alt', models.CharField(blank=True, help_text='Alternative text for image', max_length=255, null=True)),
                ('title', models.CharField(blank=True, help_text='Title of the image', max_length=255, null=True)),
                ('image_info', models.CharField(blank=True, help_text='Image information', max_length=255, null=True)),
                ('image_license', models.CharField(blank=True, help_text='Image License', max_length=255, null=True)),
                ('acquire_license_page', models.CharField(blank=True, help_text='Acquire license page', max_length=255, null=True)),
                ('og_image_tag', models.CharField(blank=True, help_text='OG image tag', max_length=255, null=True)),
                ('image_slug', models.CharField(blank=True, help_text='Image slug', max_length=255, null=True)),
                ('modulename', models.CharField(blank=True, help_text='Module name', max_length=255, null=True)),
                ('imagename', models.CharField(blank=True, help_text='Image name', max_length=255, null=True)),
                ('imageurl', models.TextField(blank=True, help_text='Image url', null=True)),
                ('image_type', models.CharField(blank=True, help_text='Image Type', max_length=10, null=True)),
                ('imagesize', models.CharField(help_text='Image size', max_length=255)),
                ('status', models.CharField(blank=True, choices=[('A', 'Active'), ('I', 'Inactive')], default='Active', help_text=' Image info status (Active/Inactive)', max_length=100, null=True)),
                ('isdeleted', models.BooleanField(blank=True, default=False, help_text='Is Deleted?', null=True)),
                ('createdby', models.IntegerField(blank=True, default=0, help_text='Created By', null=True)),
                ('createddate', models.DateTimeField(auto_now_add=True, help_text='Date Created', null=True)),
                ('updatedby', models.IntegerField(blank=True, default=0, help_text='Updated By', null=True)),
                ('updateddate', models.DateTimeField(auto_now=True, help_text='Last Updated Date', null=True)),
            ],
            options={
                'db_table': 'image_info',
            },
        ),
    ]
