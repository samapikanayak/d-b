# Generated by Django 4.0.4 on 2022-07-15 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sellingrule', '0010_alter_itemsellingrule_dc_itm_sls_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemsellingrule',
            name='expired_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='ExpiredDate'),
        ),
    ]
