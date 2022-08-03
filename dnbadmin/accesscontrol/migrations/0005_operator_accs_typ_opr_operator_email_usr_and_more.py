# Generated by Django 4.0.4 on 2022-07-25 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accesscontrol', '0004_alter_workstationgroup_id_wsgp_prnt'),
    ]

    operations = [
        migrations.AddField(
            model_name='operator',
            name='ACCS_TYP_OPR',
            field=models.CharField(choices=[('Backend', 'Backend'), ('POS Terminal', 'POS Terminal')], default='Backend', max_length=255, verbose_name='Access Type'),
        ),
        migrations.AddField(
            model_name='operator',
            name='EMAIL_USR',
            field=models.EmailField(max_length=254, null=True, unique=True, verbose_name='Email'),
        ),
        migrations.AddField(
            model_name='operator',
            name='RS_TYP_OPR',
            field=models.CharField(choices=[('NA', 'No Access'), ('GA', 'Group Access'), ('RA', 'Resource Access')], default='NA', max_length=2, verbose_name='Resource Type'),
        ),
        migrations.AlterField(
            model_name='accesspassword',
            name='TS_EP',
            field=models.DateTimeField(blank=True, null=True, verbose_name='ExpirationDateTime'),
        ),
        migrations.AlterField(
            model_name='groupresourceaccess',
            name='FL_ACS_GP_RD',
            field=models.BooleanField(default=False, verbose_name='GroupReadAccessLevelFlag'),
        ),
        migrations.AlterField(
            model_name='groupresourceaccess',
            name='FL_ACS_GP_WR',
            field=models.BooleanField(default=False, verbose_name='GroupWriteAccessLevelFlag'),
        ),
        migrations.AlterField(
            model_name='operatorbusinessunitassignment',
            name='NU_OPR',
            field=models.IntegerField(blank=True, null=True, verbose_name='OperatorNumber'),
        ),
        migrations.AlterField(
            model_name='operatorbusinessunitassignment',
            name='TS_EF',
            field=models.DateTimeField(blank=True, null=True, verbose_name='EffectiveDateTime'),
        ),
        migrations.AlterField(
            model_name='operatorbusinessunitassignment',
            name='TS_EP',
            field=models.DateTimeField(blank=True, null=True, verbose_name='ExpirationDateTime'),
        ),
        migrations.AlterField(
            model_name='operatorresourceaccess',
            name='PR_ACS_WR',
            field=models.BooleanField(default=False, verbose_name='WriteAccessLevelCode'),
        ),
        migrations.AlterField(
            model_name='operatorresourceaccess',
            name='PS_ACS_RD',
            field=models.BooleanField(default=False, verbose_name='ReadAccessLevelCode'),
        ),
        migrations.AlterField(
            model_name='workstationresourceaccess',
            name='PS_ACS_RD',
            field=models.CharField(choices=[('NA', 'No Access'), ('GA', 'Group Access'), ('RA', 'Resource Access')], default='NA', max_length=2, verbose_name='ReadAccessLevelCode'),
        ),
        migrations.AlterField(
            model_name='workstationresourceaccess',
            name='PS_ACS_WR',
            field=models.CharField(choices=[('NA', 'No Access'), ('GA', 'Group Access'), ('RA', 'Resource Access')], default='NA', max_length=2, verbose_name='WriteAccessLevelCode'),
        ),
    ]