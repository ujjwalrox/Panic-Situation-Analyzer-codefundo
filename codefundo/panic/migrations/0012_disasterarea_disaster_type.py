# Generated by Django 2.1.2 on 2018-10-26 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('panic', '0011_disasterarea'),
    ]

    operations = [
        migrations.AddField(
            model_name='disasterarea',
            name='disaster_type',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
