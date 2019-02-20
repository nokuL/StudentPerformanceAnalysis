# Generated by Django 2.1.5 on 2019-02-13 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classroom', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teacher',
            name='gender',
        ),
        migrations.RemoveField(
            model_name='teacher',
            name='second_name',
        ),
        migrations.AddField(
            model_name='teacher',
            name='class_name',
            field=models.CharField(default='', max_length=10),
        ),
        migrations.AddField(
            model_name='teacher',
            name='phone_number',
            field=models.CharField(default='', max_length=20),
        ),
    ]
