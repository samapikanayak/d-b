# Generated by Django 4.0.4 on 2022-07-26 06:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accesscontrol', '0006_operator_createdby_operator_createddate_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='resource',
            name='display_order',
            field=models.IntegerField(blank=True, help_text='Display order', null=True),
        ),
        migrations.AddField(
            model_name='resource',
            name='is_visible_menu',
            field=models.BooleanField(blank=True, default=True, help_text='Is Visible in Menu?', null=True),
        ),
        migrations.AddField(
            model_name='resource',
            name='menu_url',
            field=models.CharField(blank=True, help_text='Menu Url', max_length=255, null=True),
        ),
    ]
