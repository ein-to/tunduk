# Generated by Django 3.0.6 on 2021-08-18 05:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tunduk_app', '0003_auto_20210812_1641'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='userid',
            field=models.CharField(max_length=120, null=True),
        ),
    ]
