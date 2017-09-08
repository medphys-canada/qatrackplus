# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-02-21 21:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('units', '0002_029_to_030_first'),
        ('service_log', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PartCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Part',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('part_number', models.CharField(help_text='Part number', max_length=32, unique=True)),
                ('alt_part_number', models.CharField(blank=True, help_text='Alternate part number', max_length=32, null=True)),
                ('description', models.TextField(help_text='Brief description of this part')),
                ('quantity_min', models.PositiveIntegerField(default=0, help_text='Notify when the number parts falls below this number in storage')),
                ('quantity_current', models.PositiveIntegerField(default=0, editable=False, help_text='The number of parts in storage currently')),
                ('cost', models.DecimalField(decimal_places=2, default=0, help_text='Cost of this part', max_digits=10, blank=True, null=True)),
                ('notes', models.TextField(blank=True, help_text='Additional comments about this part', max_length=255, null=True)),
                ('is_obsolete', models.BooleanField(default=False, help_text='Is this part now obsolete', verbose_name='Obsolete')),
            ],
            options={'permissions': (('view_part', 'Can View Part'))},
        ),
        migrations.CreateModel(
            name='PartStorageCollection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('part', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='parts.Part')),
            ],
        ),
        migrations.CreateModel(
            name='PartSupplierCollection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('part_number', models.CharField(blank=True, help_text='Does this supplier have a different part number for this part', max_length=32, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PartUsed',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('part', models.ForeignKey(help_text='Select the part used', on_delete=django.db.models.deletion.CASCADE, to='parts.Part')),
                ('service_event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='service_log.ServiceEvent')),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Name of room or room number', max_length=32)),
                ('site', models.ForeignKey(blank=True, help_text='Site this storage room is located', null=True, on_delete=django.db.models.deletion.CASCADE, to='units.Site')),
            ],
            options={'ordering': ['site', 'name']},
        ),
        migrations.CreateModel(
            name='Storage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(blank=True, max_length=32, null=True)),
                ('description', models.TextField(blank=True, max_length=255, null=True)),
                ('room', models.ForeignKey(blank=True, help_text='Room for part storage', null=True, on_delete=django.db.models.deletion.CASCADE, to='parts.Room')),
            ],
            options={'verbose_name_plural': 'Storage'},
        ),
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, unique=True)),
                ('notes', models.TextField(blank=True, help_text='Additional comments about this supplier', max_length=255, null=True)),
            ],
            options={'ordering': ('name',)},
        ),
        migrations.AddField(
            model_name='partstoragecollection',
            name='storage',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='parts.Storage'),
        ),
        migrations.AddField(
            model_name='partsuppliercollection',
            name='part',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='parts.Part'),
        ),
        migrations.AddField(
            model_name='partsuppliercollection',
            name='supplier',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='parts.Supplier'),
        ),
        migrations.AddField(
            model_name='part',
            name='storage',
            field=models.ManyToManyField(related_name='parts', through='parts.PartStorageCollection', to='parts.Storage', help_text='Storage locations for this part'),
        ),
        migrations.AddField(
            model_name='part',
            name='suppliers',
            field=models.ManyToManyField(blank=True, help_text='Suppliers of this part', null=True, related_name='parts', through='parts.PartSupplierCollection', to='parts.Supplier')
        ),
        migrations.AlterUniqueTogether(
            name='room',
            unique_together=set([('site', 'name')]),
        ),
        migrations.AddField(
            model_name='part',
            name='part_category',
            field=models.ForeignKey(blank=True, help_text='Category for this part', null=True, on_delete=django.db.models.deletion.CASCADE, to='parts.PartCategory'),
        ),
        migrations.AddField(
            model_name='partused',
            name='from_storage',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='parts.Storage'),
        ),
        migrations.AlterUniqueTogether(
            name='storage',
            unique_together=set([('room', 'location')]),
        ),
        migrations.AlterUniqueTogether(
            name='partstoragecollection',
            unique_together=set([('part', 'storage')]),
        ),
        migrations.AlterUniqueTogether(
            name='partsuppliercollection',
            unique_together=set([('part', 'supplier')]),
        ),
    ]
