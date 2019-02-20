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
Education_level = (('Primary', 'Primary'), ('Secondary', 'Secondary'), ('Tertiary', 'Tertiary'))
Argument = (('Thinking', 'argue your point completely as long as it is factual'),
            ('Feeling', 'give in if your counter part becomes sensitive'))
making_a_decision = (('Thinking', 'assess the situation, outline the pros and cons, then decide'),
                     ('Feeling', 'listen to your feelings , always follow your heart'))
word_description = (('Thinking', 'logical'),  ('Feeling', 'emotional'))
facts = (('Thinking', 'sticking to facts'), ('Feeling', 'understanding why something happened'))
relating = (('Thinking', 'True'), ('Feeling', 'False'))
queue = (('Introvert', 'stay glued to my phone'),
         ('Extrovert', 'chat to the person next to me'))
class_projects = (('Extrovert', 'when you are part of a group'),
                  ('Introvert', 'when you can work by yourself'))
description = (('Extrovert', 'enjoy having a circle of acquaintances'),
               ('Introvert', 'relatively reserved and quiet'))
friends = (('Extrovert', 'You become friends on the spot'),
           ('Introvert', 'It will take a few more conversations before you open up'))
roommates = (('Introvert', 'You would much rather live by yourself'),
             ('Extrovert', 'It is great to have someone there when you get home'))
mathematical = (('Judging', 'stick to the methods taught by your teacher'),
                ('Perceiving', 'explore different methods for discovery'))
yes_or_no = (('Judging', 'Yes'), ('Perceiving', 'No'))
trip = (('Judging', 'Inquire thoroughly about the trip details for planning purposes. It is better to be fully armed'),
        ('Perceiving', 'Just get in the school bus and go , the best things happen spontaneously'))
appointments = (('Judging', 'Yes'), ('Perceiving', 'No'))
order = (('Judging', 'super organised'),
         ('Sensing', 'a jumble of things you are working on'))
info_description = (('Sensing', 'the most important thing for me is what is happening here and now. '
                                'I assess real situations and pay attention to detail'),
                    ('Intuition', 'facts are boring. I love to dream and play over upcoming events in my mind'))
yes_no = (('Sensing', 'No'), ('Intuition', 'Yes'))
situation = (('Sensing', 'pay more attention to the current situation'),
             ('Intuition', 'think of  possible sequence of events'))
imagination = (('Sensing', 'No'), ('Intuition', 'Yes'))
knowledge = (('Intuition', 'Books and manuals'), ('Sensing', 'hands on experience'))




class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)


class Test(models.Model):
    test_title = models.CharField(max_length=45, default='')
    total_score = models.IntegerField(default=100)
    subject = models.ForeignKey('Subject', on_delete=models.PROTECT, blank=True, null=True)
    test_number = models.IntegerField(default=1)

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
        number_of_tests = models.IntegerField(default=1)

        def __str__(self):
            return self.subject_title


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    first_name = models.CharField(max_length=45, default='')
    last_name = models.CharField(max_length=45, default='')
    email = models.CharField(max_length=100, default='')
    phone_number = models.CharField(max_length=20, default='')
    class_name = models.CharField(max_length=10, default='')

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
    free_time_after_school = models.IntegerField(default=1)
    average_weekly_study_time = models.IntegerField(default=1)
    family_size = models.IntegerField(default=1)
    email = models.CharField(max_length=100, default='')
    subjects = models.ManyToManyField(Subject)
    guardian_education_level = models.CharField(max_length=10, choices=Education_level, default='')

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
    day_number = models.IntegerField(default=1)

    def __str__(self):
        return self.day_title


class Question(models.Model):
    text = models.CharField(max_length=200)
    question_number = models.IntegerField(default=1)

    def __str__(self):
        return self.text


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    text = models.CharField('Answer', max_length=255)
    personality_attribute = models.ForeignKey('PersonalityAttribute', on_delete=models.CASCADE,
                                              related_name='personality_attribute')

    def __str__(self):
        return self.text


class PersonalityAttribute(models.Model):
    attribute_name = models.CharField(max_length=20)

    def __str__(self):
        return self.attribute_name


class PersonalityRecord(models.Model):
    psy_energy1 = models.CharField(max_length=10, choices=queue, default='')
    psy_energy2 = models.CharField(max_length=10, choices=class_projects, default='')
    psy_energy3 = models.CharField(max_length=10, choices=description, default='')
    psy_energy4 = models.CharField(max_length=10, choices=friends, default='')
    psy_energy5 = models.CharField(max_length=10, choices=roommates, default='')
    info1 = models.CharField(max_length=10, choices=info_description, default='')
    info2 = models.CharField(max_length=10, choices=yes_no, default='')
    info3 = models.CharField(max_length=10, choices=situation , default='')
    info4 = models.CharField(max_length=10, choices=imagination, default='')
    info5 = models.CharField(max_length=10, choices=knowledge, default='')
    decision1 = models.CharField(max_length=10, choices=Argument, default='')
    decision2 = models.CharField(max_length=10, choices=making_a_decision, default='')
    decision3 = models.CharField(max_length=10, choices=word_description, default='')
    decision4 = models.CharField(max_length=10, choices=facts, default='')
    decision5 = models.CharField(max_length=10, choices=relating, default='')
    lyf1 = models.CharField(max_length=10, choices=yes_or_no, default='')
    lyf2 = models.CharField(max_length=10, choices=mathematical, default='')
    lyf3 = models.CharField(max_length=10, choices=trip, default='')
    lyf4 = models.CharField(max_length=10, choices=appointments, default='')
    lyf5 = models.CharField(max_length=10, choices=order, default='')
    personality_category = models.CharField(max_length=10)







