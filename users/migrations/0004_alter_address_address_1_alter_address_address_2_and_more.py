# Generated by Django 5.0.1 on 2024-02-03 05:59

import users.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_invitationhistory_options_alter_country_alpha2_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='address_1',
            field=models.CharField(max_length=100, verbose_name='address 1'),
        ),
        migrations.AlterField(
            model_name='address',
            name='address_2',
            field=models.CharField(max_length=100, verbose_name='address 2'),
        ),
        migrations.AlterField(
            model_name='address',
            name='internal_id',
            field=users.models.ULIDField(editable=False, max_length=26, verbose_name='address id'),
        ),
        migrations.AlterField(
            model_name='address',
            name='zip_code',
            field=models.CharField(max_length=50, verbose_name='zip code'),
        ),
        migrations.AlterField(
            model_name='company',
            name='branch',
            field=models.CharField(max_length=100, verbose_name='company branch'),
        ),
        migrations.AlterField(
            model_name='company',
            name='internal_id',
            field=users.models.ULIDField(editable=False, max_length=26, verbose_name='company id'),
        ),
        migrations.AlterField(
            model_name='company',
            name='name',
            field=models.CharField(max_length=100, verbose_name='company name'),
        ),
        migrations.AlterField(
            model_name='country',
            name='internal_id',
            field=users.models.ULIDField(editable=False, max_length=26, verbose_name='country ulid'),
        ),
        migrations.AlterField(
            model_name='invitation',
            name='internal_id',
            field=users.models.ULIDField(editable=False, max_length=26, verbose_name='invitation id'),
        ),
        migrations.AlterField(
            model_name='invitationhistory',
            name='expiry_date',
            field=models.DateTimeField(verbose_name='expires at'),
        ),
        migrations.AlterField(
            model_name='invitationhistory',
            name='internal_id',
            field=users.models.ULIDField(editable=False, max_length=26, verbose_name='invitation id'),
        ),
        migrations.AlterField(
            model_name='phonenumber',
            name='internal_id',
            field=users.models.ULIDField(editable=False, max_length=26, verbose_name='phone ulid'),
        ),
        migrations.AlterField(
            model_name='phonenumber',
            name='isd_code',
            field=models.CharField(blank=True, help_text='isd_code', verbose_name='isd code'),
        ),
        migrations.AlterField(
            model_name='phonenumber',
            name='phone',
            field=models.CharField(blank=True, help_text='phone number', verbose_name='phone number'),
        ),
        migrations.AlterField(
            model_name='role',
            name='internal_id',
            field=users.models.ULIDField(editable=False, max_length=26, verbose_name='role id'),
        ),
        migrations.AlterField(
            model_name='role',
            name='name',
            field=models.CharField(max_length=100, verbose_name='role name'),
        ),
        migrations.AlterField(
            model_name='useraccount',
            name='employee_code',
            field=models.CharField(max_length=50, verbose_name='employee code'),
        ),
        migrations.AlterField(
            model_name='useraccount',
            name='internal_id',
            field=users.models.ULIDField(editable=False, max_length=26, verbose_name='user id'),
        ),
        migrations.AlterField(
            model_name='useraccount',
            name='is_staff',
            field=models.BooleanField(default=False, verbose_name='is staff'),
        ),
    ]
