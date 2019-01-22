from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.html import escape, mark_safe
from datetime import date
from django.urls import reverse

# Create your models here.


class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)


class Subject(models.Model):
        subject_title = models.CharField(max_length=30)

        def __str__(self):
            return self.subject_title


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    first_name = models.CharField(max_length=45, default='')
    second_name = models.CharField(max_length=45, default='')
    email = models.CharField(max_length=100, default='')
    last_name = models.CharField(max_length=45, default='')
    age = models.IntegerField(default=1)
    date_of_birth = models.DateField("Date", default=date.today)
    student_subjects = models.ManyToManyField(Subject)

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        print(self.pk)
        return reverse('students:student_detail', kwargs={'pk': self.pk})




