# Generated by Django 2.2.13 on 2021-05-15 22:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Recognize', '0003_auto_20210515_1828'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imageuploader',
            name='filter',
            field=models.CharField(choices=[('miss', 'MISSINGS'), ('crime', 'CRIMINALS'), ('mart', 'MARTYR')], max_length=7),
        ),
    ]