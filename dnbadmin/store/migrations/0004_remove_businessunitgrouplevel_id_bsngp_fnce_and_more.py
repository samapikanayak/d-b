# Generated by Django 4.0.4 on 2022-06-15 11:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_associatedbusinessunitgroup'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='businessunitgrouplevel',
            name='ID_BSNGP_FNCE',
        ),
        migrations.AlterField(
            model_name='businessunitgrouplevel',
            name='ID_BSNGP_FNC',
            field=models.ForeignKey(db_column='ID_BSNGP_FNC', on_delete=django.db.models.deletion.CASCADE, to='store.businessunitgroupfunction', verbose_name='BusinessUnitGroupFunctionID'),
        ),
        migrations.DeleteModel(
            name='AssociatedBusinessUnitGroup',
        ),
    ]
