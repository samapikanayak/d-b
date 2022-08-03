# Generated by Django 4.0.4 on 2022-07-15 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sellingrule', '0009_remove_itemsellingrule_lu_gp_tnd_rst_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemsellingrule',
            name='DC_ITM_SLS',
            field=models.DateTimeField(blank=True, null=True, verbose_name='SellingStatusCodeEffectiveDate'),
        ),
        migrations.AlterField(
            model_name='itemsellingrule',
            name='expired_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Expired Date'),
        ),
    ]
