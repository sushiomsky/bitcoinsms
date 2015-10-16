# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Sms',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('status', models.PositiveSmallIntegerField(editable=False, default=0, choices=[(0, 'WAITING_FOR_PAYMENT'), (1, 'PREPARING_TO_SEND'), (2, 'SENT_SUCCESSFULLY'), (3, 'ERROR_ON_SEND')], db_index=True)),
                ('payment_address', models.CharField(editable=False, unique=True, max_length=35, db_index=True)),
                ('time_created', models.DateTimeField(auto_now_add=True)),
                ('time_payment_recieved', models.DateTimeField(editable=False, blank=True, null=True)),
                ('time_sent', models.DateTimeField(editable=False, blank=True, null=True)),
                ('cost_in_satoshis', models.PositiveIntegerField(editable=False)),
                ('ip_address', models.GenericIPAddressField(editable=False)),
                ('to', models.CharField(validators=[django.core.validators.RegexValidator(message="Number invalid, suggested format: '333-555-6666'", regex='^\\+?1?\\d{11}$')], max_length=12)),
                ('text', models.CharField(max_length=160)),
                ('status_message', models.CharField(editable=False, max_length=255)),
            ],
            options={
                'db_table': 'sms',
            },
        ),
    ]
