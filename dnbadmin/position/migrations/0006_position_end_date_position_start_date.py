# Generated by Django 4.0.4 on 2022-07-25 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('position', '0005_position_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='position',
            name='end_date',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='position',
            name='start_date',
            field=models.DateField(null=True),
        ),
    ]
