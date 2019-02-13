from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.html import escape, mark_safe
from datetime import date
from django.urls import reverse

# Create your models here.

Gender_Choices = (('Male', 'Male'), ('Female', 'Female'))
Guardian = (('Father', 'Father'),
                ('Mother', 'Mother'),
                ('Other', 'Other'))
YES_OR_NO = (('Yes', 'Yes'), ('No', 'No'))


class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)


class Test(models.Model):
    test_title = models.CharField(max_length=45, default='')
    total_score = models.IntegerField(default=100)
    subject = models.ForeignKey('Subject', on_delete=models.PROTECT, blank=True, null=True)

    def __str__(self):
        return self.test_title


class TestResult(models.Model):
    test_score = models.IntegerField(default=0)
    test = models.ForeignKey(Test, on_delete=models.PROTECT, blank=True, null=True)
    student = models.ForeignKey('Student', on_delete=models.PROTECT, blank=True, null=True)
    pass_status = models.CharField(max_length=10, default='')
    percentage = models.FloatField(max_length=10, default=0.0)

    def __str__(self):
        return self.test.test_title


class Subject(models.Model):
        subject_title = models.CharField(max_length=30)

        def __str__(self):
            return self.subject_title


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    first_name = models.CharField(max_length=45, default='')
    second_name = models.CharField(max_length=45, default='')
    last_name = models.CharField(max_length=45, default='')
    gender = models.CharField(max_length=10, choices=Gender_Choices, default='')
    email = models.CharField(max_length=100, default='')

    def __str__(self):
        return self.last_name


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    first_name = models.CharField(max_length=45, default='')
    second_name = models.CharField(max_length=45, default='')
    last_name = models.CharField(max_length=45, default='')
    age = models.IntegerField(default=1)
    gender = models.CharField(max_length=10, choices=Gender_Choices, default='')
    date_of_birth = models.DateField("Date", default=date.today)
    guardian = models.CharField(max_length=10, choices=Guardian, default='')
    guardian_first_name = models.CharField(max_length=20, default='')
    guardian_last_name = models.CharField(max_length=20, default='')
    guardian_phone_number = models.CharField(max_length=20, default='')
    guardian_email = models.EmailField(max_length=100, default='')
    extra_paid_classes = models.CharField(max_length=3, choices=YES_OR_NO, default='')
    internet_access = models.CharField(max_length=3, choices=YES_OR_NO, default='')
    intend_to_pursue = models.CharField(max_length=3, choices=YES_OR_NO, default='')
    out_going = models.CharField(max_length=3, choices=YES_OR_NO, default='')
    email = models.CharField(max_length=100, default='')
    subjects = models.ManyToManyField(Subject)

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        print(self.pk)
        return reverse('students:student_detail', kwargs={'pk': self.pk})


class AttendanceRecord(models.Model):
    student = models.ForeignKey(Student, on_delete=models.PROTECT, blank=True, null=True)
    attendance_status = models.BooleanField(default=False)
    day = models.ForeignKey('Day', on_delete=models.PROTECT, blank=True, null=True)

    def __str__(self):
        return self.student.first_name + " " + self.day.day_title


class Day(models.Model):
    day_title = models.CharField(max_length=20)
    checked = models.BooleanField(default=False)

    def __str__(self):
        return self.day_title





