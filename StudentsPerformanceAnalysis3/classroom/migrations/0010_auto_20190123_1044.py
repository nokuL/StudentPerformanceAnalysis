# Generated by Django 2.1.5 on 2019-01-23 08:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('classroom', '0009_auto_20190123_1035'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subject',
            name='tests',
        ),
        migrations.DeleteModel(
            name='Test',
        ),
    ]