# Generated by Django 2.1.5 on 2019-01-30 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classroom', '0024_auto_20190130_1253'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='gender',
            field=models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], default='', max_length=1),
        ),
    ]
