# Generated by Django 2.1.5 on 2019-02-22 09:11

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
                ('day_number', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='Personality',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier', models.IntegerField(default='')),
                ('personality_name', models.CharField(default='', max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='PersonalityAttribute',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attribute_name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='PersonalityRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('psy_energy1', models.CharField(choices=[('Introvert', 'stay glued to my phone'), ('Extrovert', 'chat to the person next to me')], default='', max_length=10)),
                ('psy_energy2', models.CharField(choices=[('Extrovert', 'when you are part of a group'), ('Introvert', 'when you can work by yourself')], default='', max_length=10)),
                ('psy_energy3', models.CharField(choices=[('Extrovert', 'enjoy having a circle of acquaintances'), ('Introvert', 'relatively reserved and quiet')], default='', max_length=10)),
                ('psy_energy4', models.CharField(choices=[('Extrovert', 'You become friends on the spot'), ('Introvert', 'It will take a few more conversations before you open up')], default='', max_length=10)),
                ('psy_energy5', models.CharField(choices=[('Introvert', 'You would much rather live by yourself'), ('Extrovert', 'It is great to have someone there when you get home')], default='', max_length=10)),
                ('info1', models.CharField(choices=[('Sensing', 'the most important thing for me is what is happening here and now. I assess real situations and pay attention to detail'), ('Intuition', 'facts are boring. I love to dream and play over upcoming events in my mind')], default='', max_length=10)),
                ('info2', models.CharField(choices=[('Sensing', 'No'), ('Intuition', 'Yes')], default='', max_length=10)),
                ('info3', models.CharField(choices=[('Sensing', 'pay more attention to the current situation'), ('Intuition', 'think of  possible sequence of events')], default='', max_length=10)),
                ('info4', models.CharField(choices=[('Sensing', 'No'), ('Intuition', 'Yes')], default='', max_length=10)),
                ('info5', models.CharField(choices=[('Intuition', 'Books and manuals'), ('Sensing', 'hands on experience')], default='', max_length=10)),
                ('decision1', models.CharField(choices=[('Thinking', 'argue your point completely as long as it is factual'), ('Feeling', 'give in if your counter part becomes sensitive')], default='', max_length=10)),
                ('decision2', models.CharField(choices=[('Thinking', 'assess the situation, outline the pros and cons, then decide'), ('Feeling', 'listen to your feelings , always follow your heart')], default='', max_length=10)),
                ('decision3', models.CharField(choices=[('Thinking', 'logical'), ('Feeling', 'emotional')], default='', max_length=10)),
                ('decision4', models.CharField(choices=[('Thinking', 'sticking to facts'), ('Feeling', 'understanding why something happened')], default='', max_length=10)),
                ('decision5', models.CharField(choices=[('Thinking', 'True'), ('Feeling', 'False')], default='', max_length=10)),
                ('lyf1', models.CharField(choices=[('Judging', 'Yes'), ('Perceiving', 'No')], default='', max_length=10)),
                ('lyf2', models.CharField(choices=[('Judging', 'stick to the methods taught by your teacher'), ('Perceiving', 'explore different methods for discovery')], default='', max_length=10)),
                ('lyf3', models.CharField(choices=[('Judging', 'Inquire thoroughly about the trip details for planning purposes. It is better to be fully armed'), ('Perceiving', 'Just get in the school bus and go , the best things happen spontaneously')], default='', max_length=10)),
                ('lyf4', models.CharField(choices=[('Judging', 'Yes'), ('Perceiving', 'No')], default='', max_length=10)),
                ('lyf5', models.CharField(choices=[('Judging', 'super organised'), ('Perceiving', 'a jumble of things you are working on')], default='', max_length=10)),
                ('personality_category', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject_title', models.CharField(max_length=30)),
                ('number_of_tests', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('test_title', models.CharField(default='', max_length=45)),
                ('total_score', models.IntegerField(default=100)),
                ('test_number', models.IntegerField(default=1)),
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
                ('free_time_after_school', models.IntegerField(default=1)),
                ('average_weekly_study_time', models.IntegerField(default=1)),
                ('family_size', models.IntegerField(default=1)),
                ('email', models.CharField(default='', max_length=100)),
                ('guardian_education_level', models.CharField(choices=[('Primary', 'Primary'), ('Secondary', 'Secondary'), ('Tertiary', 'Tertiary')], default='', max_length=10)),
                ('personality', models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.PROTECT, to='classroom.Personality')),
                ('subjects', models.ManyToManyField(to='classroom.Subject')),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('first_name', models.CharField(default='', max_length=45)),
                ('last_name', models.CharField(default='', max_length=45)),
                ('email', models.CharField(default='', max_length=100)),
                ('phone_number', models.CharField(default='', max_length=20)),
                ('class_name', models.CharField(default='', max_length=10)),
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
