from django.contrib import admin
from .models import Student, Subject, User, Test, TestResult, AttendanceRecord, Day, Teacher, PersonalityAttribute,\
    Personality, SubjectAverage, CareerField, CareerPersonalityCategory, Fruit
# Register your models here.
admin.site.register(Student)
admin.site.register(Subject)
admin.site.register(User)
admin.site.register(Test)
admin.site.register(TestResult)
admin.site.register(AttendanceRecord)
admin.site.register(Day)
admin.site.register(Teacher)
admin.site.register(PersonalityAttribute)
admin.site.register(Personality)
admin.site.register(SubjectAverage)
admin.site.register(CareerField)
admin.site.register(CareerPersonalityCategory)
admin.site.register(Fruit)
