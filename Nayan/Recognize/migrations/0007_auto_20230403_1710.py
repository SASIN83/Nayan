# Generated by Django 3.1.7 on 2023-04-03 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Recognize', '0006_auto_20230403_1709'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imageuploader',
            name='category',
            field=models.CharField(choices=[('miss', 'MISSINGS'), ('crime', 'CRIMINALS'), ('mart', 'MARTYR')], default='miss', max_length=7),
        ),
    ]
