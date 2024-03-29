# Generated by Django 5.0.1 on 2024-02-03 04:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='invitationhistory',
            options={'verbose_name': 'Invitation History', 'verbose_name_plural': 'Invitation History'},
        ),
        migrations.AlterField(
            model_name='country',
            name='alpha2',
            field=models.CharField(max_length=100, verbose_name='alpha 2'),
        ),
        migrations.AlterField(
            model_name='country',
            name='alpha3',
            field=models.CharField(max_length=100, verbose_name='apha 3'),
        ),
        migrations.AlterField(
            model_name='country',
            name='currency_code',
            field=models.CharField(max_length=100, verbose_name='currency code'),
        ),
        migrations.AlterField(
            model_name='country',
            name='currency_symbol',
            field=models.CharField(max_length=100, verbose_name='currency symbol'),
        ),
        migrations.AlterField(
            model_name='country',
            name='isd_code',
            field=models.CharField(max_length=50, verbose_name='isd code'),
        ),
        migrations.AlterField(
            model_name='country',
            name='name',
            field=models.CharField(max_length=255, verbose_name='country name'),
        ),
        migrations.AlterField(
            model_name='state',
            name='name',
            field=models.CharField(max_length=255, verbose_name='state'),
        ),
    ]
