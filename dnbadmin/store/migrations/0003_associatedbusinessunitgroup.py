# Generated by Django 4.0.4 on 2022-06-13 10:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_businessunitgroupfunction_businessunitgrouplevel'),
    ]

    operations = [
        migrations.CreateModel(
            name='AssociatedBusinessUnitGroup',
            fields=[
                ('ID_A_BSNGP', models.BigAutoField(primary_key=True, serialize=False, verbose_name='AssociatedBusinessUnitGroupID')),
                ('DC_EF', models.DateTimeField(auto_now_add=True, db_column='Effective date', null=True)),
                ('DC_EP', models.DateTimeField(auto_now_add=True, db_column='Expiry date', null=True)),
                ('ID_BSNGP_CHLD', models.ForeignKey(db_column='ID_BSNGP_CHLD', on_delete=django.db.models.deletion.CASCADE, related_name='BSNGP_CHLD', to='store.businessunitgroup', verbose_name='ChildBusinessUnitGroupID')),
                ('ID_BSNGP_FNCA', models.ForeignKey(db_column='ID_BSNGP_FNCA', on_delete=django.db.models.deletion.CASCADE, related_name='BSNGP_FNCA', to='store.businessunitgrouplevel', verbose_name='BusinessUnitGroupFunctionID')),
                ('ID_BSNGP_LVL', models.ForeignKey(db_column='ID_BSNGP_LVL', on_delete=django.db.models.deletion.CASCADE, related_name='BSNGP_LVL', to='store.businessunitgrouplevel', verbose_name='ParentBusinessUnitGroupLevelID')),
                ('ID_BSNGP_PRNT', models.ForeignKey(db_column='ID_BSNGP_PRNT', on_delete=django.db.models.deletion.CASCADE, related_name='BSNGP_PRNT', to='store.businessunitgroup', verbose_name='ParentBusinessUnitGroupID')),
            ],
            options={
                'db_table': 'ST_ASCTN_BSNGP',
            },
        ),
    ]
