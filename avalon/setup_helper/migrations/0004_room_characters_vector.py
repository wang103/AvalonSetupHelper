# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-19 00:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('setup_helper', '0003_remove_room_updated_at_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='characters_vector',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]