# Generated by Django 3.0.4 on 2020-03-16 07:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_subscription'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='expired_at',
            field=models.DateTimeField(verbose_name='Expired at'),
        ),
    ]
