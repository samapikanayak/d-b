# Generated by Django 4.0.4 on 2022-06-11 08:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BusinessUnitGroupFunction',
            fields=[
                ('ID_BSNGP_FNC', models.BigAutoField(primary_key=True, serialize=False, verbose_name='BusinessUnitGroupFunctionID')),
                ('NM_BSNGP_FNC', models.CharField(max_length=40, verbose_name='BusinessUnitGroupFunctionName')),
            ],
            options={
                'db_table': 'CO_BSNGP_FNC',
            },
        ),
        migrations.CreateModel(
            name='BusinessUnitGroupLevel',
            fields=[
                ('ID_BSNGP_LV', models.BigAutoField(primary_key=True, serialize=False, verbose_name='BusinessUnitGroupLevelID')),
                ('NM_BSNGP_LV', models.CharField(max_length=40, verbose_name='BusinessUnitGroupLevelName')),
                ('ID_BSNGP_FNC', models.ForeignKey(db_column='ID_BSNGP_FNC', on_delete=django.db.models.deletion.CASCADE, related_name='BSNGP_FNC', to='store.businessunitgrouplevel', verbose_name='BusinessUnitGroupFunctionID')),
                ('ID_BSNGP_FNCE', models.ForeignKey(db_column='ID_BSNGP_FNCE', on_delete=django.db.models.deletion.CASCADE, to='store.businessunitgroupfunction', verbose_name='BusinessUnitGroupFunctionID')),
                ('ID_BSNGP_LV_PRNT', models.ForeignKey(db_column='ID_BSNGP_LV_PRNT', on_delete=django.db.models.deletion.CASCADE, related_name='BSNGP_LV', to='store.businessunitgrouplevel', verbose_name='BusinessUnitCenterGroupLevelID ')),
            ],
            options={
                'db_table': 'CO_BSNGP_LV',
            },
        ),
    ]
