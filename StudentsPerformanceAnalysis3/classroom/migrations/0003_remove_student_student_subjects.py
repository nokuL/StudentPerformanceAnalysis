# Generated by Django 2.1.5 on 2019-01-21 10:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('classroom', '0002_auto_20190121_1216'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='student_subjects',
        ),
    ]