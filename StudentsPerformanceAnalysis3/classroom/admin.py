from django.contrib import admin
from .models import Student, Subject, User, Test, TestResult, AttendanceRecord, Day, Teacher, Question, PersonalityAttribute, Answer
# Register your models here.
admin.site.register(Student)
admin.site.register(Subject)
admin.site.register(User)
admin.site.register(Test)
admin.site.register(TestResult)
admin.site.register(AttendanceRecord)
admin.site.register(Day)
admin.site.register(Teacher)
admin.site.register(Question)
admin.site.register(PersonalityAttribute)
admin.site.register(Answer)