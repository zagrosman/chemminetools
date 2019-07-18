# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2019-07-17 11:11
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Compound',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cid', models.CharField(db_index=True, max_length=256)),
                ('name', models.CharField(max_length=256)),
                ('formula', models.CharField(max_length=1024)),
                ('weight', models.DecimalField(decimal_places=2, max_digits=10)),
                ('inchi', models.TextField()),
                ('smiles', models.TextField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='SDFFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sdffile', models.TextField()),
                ('compound', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='compounddb.Compound')),
            ],
        ),
    ]
