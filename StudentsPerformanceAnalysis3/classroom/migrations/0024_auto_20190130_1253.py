# Generated by Django 2.1.5 on 2019-01-30 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classroom', '0023_auto_20190127_1329'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='extra_paid_classes',
            field=models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], default='', max_length=3),
        ),
        migrations.AddField(
            model_name='student',
            name='gender',
            field=models.CharField(choices=[('M', 'Male'), ('F', 'Female')], default='', max_length=1),
        ),
        migrations.AddField(
            model_name='student',
            name='guardian',
            field=models.CharField(choices=[('Father', 'Father'), ('Mother', 'Mother'), ('Other', 'Other')], default='', max_length=10),
        ),
        migrations.AddField(
            model_name='student',
            name='intend_to_pursue',
            field=models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], default='', max_length=3),
        ),
        migrations.AddField(
            model_name='student',
            name='internet_access',
            field=models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], default='', max_length=3),
        ),
        migrations.AddField(
            model_name='student',
            name='out_going',
            field=models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], default='', max_length=3),
        ),
    ]
