# Generated by Django 2.1.5 on 2019-02-12 20:58

import datetime
from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('is_student', models.BooleanField(default=False)),
                ('is_teacher', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='AttendanceRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attendance_status', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Day',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day_title', models.CharField(max_length=20)),
                ('checked', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject_title', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('test_title', models.CharField(default='', max_length=45)),
                ('total_score', models.IntegerField(default=100)),
                ('subject', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='classroom.Subject')),
            ],
        ),
        migrations.CreateModel(
            name='TestResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('test_score', models.IntegerField(default=0)),
                ('pass_status', models.CharField(default='', max_length=10)),
                ('percentage', models.FloatField(default=0.0, max_length=10)),
                ('test', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='classroom.Test')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('first_name', models.CharField(default='', max_length=45)),
                ('second_name', models.CharField(default='', max_length=45)),
                ('last_name', models.CharField(default='', max_length=45)),
                ('age', models.IntegerField(default=1)),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], default='', max_length=10)),
                ('date_of_birth', models.DateField(default=datetime.date.today, verbose_name='Date')),
                ('guardian', models.CharField(choices=[('Father', 'Father'), ('Mother', 'Mother'), ('Other', 'Other')], default='', max_length=10)),
                ('guardian_first_name', models.CharField(default='', max_length=20)),
                ('guardian_last_name', models.CharField(default='', max_length=20)),
                ('guardian_phone_number', models.CharField(default='', max_length=20)),
                ('guardian_email', models.EmailField(default='', max_length=100)),
                ('extra_paid_classes', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], default='', max_length=3)),
                ('internet_access', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], default='', max_length=3)),
                ('intend_to_pursue', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], default='', max_length=3)),
                ('out_going', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], default='', max_length=3)),
                ('email', models.CharField(default='', max_length=100)),
                ('subjects', models.ManyToManyField(to='classroom.Subject')),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('first_name', models.CharField(default='', max_length=45)),
                ('second_name', models.CharField(default='', max_length=45)),
                ('last_name', models.CharField(default='', max_length=45)),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], default='', max_length=10)),
                ('email', models.CharField(default='', max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='attendancerecord',
            name='day',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='classroom.Day'),
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
        migrations.AddField(
            model_name='testresult',
            name='student',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='classroom.Student'),
        ),
        migrations.AddField(
            model_name='attendancerecord',
            name='student',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='classroom.Student'),
        ),
    ]
