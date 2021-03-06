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
         ('Perceiving', 'a jumble of things you are working on'))
info_description = (('Sensing', 'the most important thing for me is what is happening here and now. '
                                'I assess real situations and pay attention to detail'),
                    ('Intuition', 'facts are boring. I love to dream and play over upcoming events in my mind'))
yes_no = (('Sensing', 'No'), ('Intuition', 'Yes'))
situation = (('Sensing', 'pay more attention to the current situation'),
             ('Intuition', 'think of  possible sequence of events'))
imagination = (('Sensing', 'No'), ('Intuition', 'Yes'))
knowledge = (('Intuition', 'Books and manuals'), ('Sensing', 'hands on experience'))
subject_category = (('Commercials', 'Commercials'), ('Arts', 'Arts'), ('Sciences', 'Sciences'))


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


class SubjectAverage(models.Model):
    subject_average_mark = models.IntegerField(default=0)
    subject = models.ForeignKey('Subject', on_delete=models.PROTECT)
    student = models.ForeignKey('Student', on_delete=models.PROTECT)

    def __str__(self):
        return self.student.first_name + " " + self.subject.subject_title


class CategoryAverage(models.Model):
    category_average_mark = models.IntegerField(default=0)
    category_name = models.CharField(choices=subject_category, max_length=20, default='')
    student = models.ForeignKey('Student', on_delete=models.PROTECT)

    def __str__(self):
        return self.student.first_name + "Category Average"


class TestResult(models.Model):
    test_score = models.IntegerField(default=0)
    test = models.ForeignKey(Test, on_delete=models.PROTECT, blank=True, null=True)
    student = models.ForeignKey('Student', on_delete=models.PROTECT, blank=True, null=True)
    pass_status = models.CharField(max_length=10, default='')
    percentage = models.FloatField(max_length=10, default=0.0)

    def __str__(self):
        return self.test.test_title


class Personality(models.Model):
    identifier = models.IntegerField(default='')
    personality_name = models.CharField(max_length=10, default='')
    image = models.ImageField(upload_to='personality_image', blank=True)
    energy_title = models.CharField(max_length=15, default='')
    energy_description1 = models.CharField(max_length=50, default='')
    energy_description2 = models.CharField(max_length=50, default='')
    energy_description3 = models.CharField(max_length=50, default='')
    energy_description4 = models.CharField(max_length=50, default='')
    energy_description5 = models.CharField(max_length=50, default='')
    information_title = models.CharField(max_length=15, default='')
    information_description1 = models.CharField(max_length=50, default='')
    information_description2 = models.CharField(max_length=50, default='')
    information_description3 = models.CharField(max_length=50, default='')
    information_description4 = models.CharField(max_length=50, default='')
    information_description5 = models.CharField(max_length=50, default='')
    decision_title = models.CharField(max_length=15, default='')
    decision_description1 = models.CharField(max_length=50, default='')
    decision_description2 = models.CharField(max_length=50, default='')
    decision_description3 = models.CharField(max_length=50, default='')
    decision_description4 = models.CharField(max_length=50, default='')
    decision_description5 = models.CharField(max_length=50, default='')
    life_title = models.CharField(max_length=15, default='')
    life_description1 = models.CharField(max_length=50, default='')
    life_description2 = models.CharField(max_length=50, default='')
    life_description3 = models.CharField(max_length=50, default='')
    life_description4 = models.CharField(max_length=50, default='')
    life_description5 = models.CharField(max_length=50, default='')
    energy_explanation = models.CharField(max_length=500, default='')
    information_explanation = models.CharField(max_length=500, default='')
    decision_explanation = models.CharField(max_length=500, default='')
    life_explanation = models.CharField(max_length=500, default='', blank=True)
    teaching_method1 = models.CharField(max_length=1000, default='', blank=True)
    teaching_method2 = models.CharField(max_length=1000, default='', blank=True)
    teaching_method3 = models.CharField(max_length=1000, default='', blank=True)
    teaching_method4 = models.CharField(max_length=1000, default='', blank=True)
    teaching_method5 = models.CharField(max_length=1000, default='', blank=True)
    teaching_method6 = models.CharField(max_length=1000, default='', blank=True)

    def __str__(self):
        return self.personality_name


class Subject(models.Model):
        subject_title = models.CharField(max_length=30)
        number_of_tests = models.IntegerField(default=1)
        category = models.CharField(max_length=15, choices=subject_category, blank=True, default='')

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
    last_name = models.CharField(max_length=45, default='', blank=True)
    age = models.IntegerField(default=1, blank=True)
    gender = models.CharField(max_length=10, choices=Gender_Choices, default='', blank=True)
    date_of_birth = models.DateField("Date", default=date.today, blank=True)
    guardian = models.CharField(max_length=10, choices=Guardian, default='', blank=True)
    guardian_first_name = models.CharField(max_length=20, default='', blank=True)
    guardian_last_name = models.CharField(max_length=20, default='', blank=True)
    guardian_phone_number = models.CharField(max_length=20, default='')
    guardian_email = models.EmailField(max_length=100, default='', blank=True)
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
    personality = models.ForeignKey(Personality, on_delete=models.PROTECT, default='', blank=True, null=True)
    has_taken_test = models.BooleanField(default=False)

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


class PersonalityAttribute(models.Model):
    attribute_name = models.CharField(max_length=20)

    def __str__(self):
        return self.attribute_name


class PersonalityRecord(models.Model):
    psy_energy1 = models.CharField(max_length=10, choices=queue, default='', blank=False)
    psy_energy2 = models.CharField(max_length=10, choices=class_projects, default='', blank=False)
    psy_energy3 = models.CharField(max_length=10, choices=description, default='', blank=False)
    psy_energy4 = models.CharField(max_length=10, choices=friends, default='', blank=False)
    psy_energy5 = models.CharField(max_length=10, choices=roommates, default='', blank=False)
    info1 = models.CharField(max_length=10, choices=info_description, default='', blank=False)
    info2 = models.CharField(max_length=10, choices=yes_no, default='', blank=False)
    info3 = models.CharField(max_length=10, choices=situation , default='', blank=False)
    info4 = models.CharField(max_length=10, choices=imagination, default='', blank=False)
    info5 = models.CharField(max_length=10, choices=knowledge, default='', blank=False)
    decision1 = models.CharField(max_length=10, choices=Argument, default='', blank=False)
    decision2 = models.CharField(max_length=10, choices=making_a_decision, default='', blank=False)
    decision3 = models.CharField(max_length=10, choices=word_description, default='', blank=False)
    decision4 = models.CharField(max_length=10, choices=facts, default='', blank=False)
    decision5 = models.CharField(max_length=10, choices=relating, default='', blank=False)
    lyf1 = models.CharField(max_length=10, choices=yes_or_no, default='', blank=False)
    lyf2 = models.CharField(max_length=10, choices=mathematical, default='', blank=False)
    lyf3 = models.CharField(max_length=10, choices=trip, default='', blank=False)
    lyf4 = models.CharField(max_length=10, choices=appointments, default='', blank=False)
    lyf5 = models.CharField(max_length=10, choices=order, default='', blank=False)
    personality_category = models.CharField(max_length=10)


class CareerField(models.Model):
    career_title = models.CharField(max_length=50, blank=False, default='')
    career_description = models.CharField(max_length=1000, blank=False, default='')
    career_subject_category = models.CharField(max_length=20, choices=subject_category, default='')
    career_image = models.ImageField(upload_to='career_image', blank=False, default='')
    dominant_subjects = models.ManyToManyField(Subject, blank=False, default='')
    career_personality_category = models.ManyToManyField('CareerPersonalityCategory')

    def __str__(self):
        return self.career_title


class Nokuthaba(models.Model):
    kjklllk = models.CharField(max_length=12)


class Fruit(models.Model):
    name = models.CharField(max_length=255)
    amt = models.IntegerField()

    def __str__(self):
        return self.name


class CareerPersonalityCategory(models.Model):
    career_personality_category_name = models.CharField(max_length=30)
    career_personality_identifier = models.IntegerField(default=0)
    career_personality = models.IntegerField

    def __str__(self):
        return self.career_personality_category_name







