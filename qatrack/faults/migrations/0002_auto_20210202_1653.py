# Generated by Django 2.2.17 on 2021-02-02 21:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('faults', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='faulttype',
            name='code',
            field=models.CharField(help_text='Enter the fault code or number', max_length=255, verbose_name='code'),
        ),
    ]
