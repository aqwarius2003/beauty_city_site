# Generated by Django 4.2 on 2024-12-20 07:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('beautyservice', '0006_alter_schedule_options_note'),
    ]

    operations = [
        migrations.AddField(
            model_name='note',
            name='date',
            field=models.DateField(blank=True, null=True, verbose_name='Дата записи'),
        ),
        migrations.AddField(
            model_name='note',
            name='time',
            field=models.TimeField(blank=True, null=True, verbose_name='Время записи'),
        ),
    ]
