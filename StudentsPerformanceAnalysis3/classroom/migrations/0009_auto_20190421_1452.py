# Generated by Django 2.1.5 on 2019-04-21 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classroom', '0008_auto_20190421_1445'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='resources_used_for_study',
        ),
        migrations.AddField(
            model_name='student',
            name='internet_access',
            field=models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], default='', max_length=3),
        ),
    ]
