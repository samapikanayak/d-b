# Generated by Django 4.0.4 on 2022-06-23 11:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accesscontrol', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workgroup',
            name='ID_GP_WRK_PRNT',
            field=models.ForeignKey(blank=True, db_column='ID_GP_WRK_PRNT', null=True, on_delete=django.db.models.deletion.CASCADE, to='accesscontrol.workgroup', verbose_name='ParentWorkGroupID'),
        ),
    ]