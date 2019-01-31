# Generated by Django 2.1.5 on 2019-01-23 08:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('classroom', '0010_auto_20190123_1044'),
    ]

    operations = [
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField(default=0)),
                ('test_title', models.CharField(default='', max_length=45)),
            ],
        ),
        migrations.AddField(
            model_name='subject',
            name='tests',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='classroom.Test'),
        ),
    ]