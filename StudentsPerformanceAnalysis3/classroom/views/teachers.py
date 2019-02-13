from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponse
from django.db.models import Avg, Count
from django.forms import inlineformset_factory
from django.shortcuts import get_object_or_404, redirect, render
from django.template import RequestContext
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView, TemplateView)

from ..decorators import teacher_required
from ..forms import TeacherSignUpForm
from ..models import  User, Student, Day, AttendanceRecord, Subject, Day


class TeacherSignUpView(CreateView):
    model = User
    form_class = TeacherSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'teacher'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('teachers:teacher_dashboard')


@method_decorator([login_required, teacher_required], name='dispatch')
class TeacherDashboard(TemplateView):
        template_name = 'classroom/teachers/teacher_dashboard.html'

        def get_context_data(self, **kwargs):
            students = Student.objects.all()
            total_students = students.count()
            subjects = Subject.objects.all()
            total_subjects = subjects.count()
            days = Day.objects.all()
            total_days = days.count()
            context = super(TeacherDashboard, self).get_context_data(**kwargs)
            context = {'students': students, 'total_students': total_students, 'total_subjects': total_subjects,
                       'total_days': total_days}
            return context


class Attendance(TemplateView):
    template_name = 'classroom/teachers/attendance_register.html'

    def get_context_data(self, **kwargs):
        day_pk = self.kwargs['pk']
        day = Day.objects.get(pk=day_pk)
        students = Student.objects.all()
        attendance_records_list = list()
        for student in students:
            attendance_record = AttendanceRecord.objects.create(student=student, day=day, attendance_status=False)
            attendance_record.save()
            attendance_records_list.append(attendance_record)
        super(Attendance, self).get_context_data(**kwargs)
        context = {'attendance_records_list': attendance_records_list, 'day':day}
        return context

    @csrf_exempt
    def set_attendance_status(self, pk):
        attendance_record_id = pk
        if attendance_record_id:
            attendance_record = AttendanceRecord.objects.get(pk=attendance_record_id)
            attendance_record.attendance_status = True
            attendance_record.save()
            print(str(attendance_record.attendance_status))
        return HttpResponse('')

    @csrf_exempt
    def set_absent(self, pk):
        attendance_record_id = pk
        if attendance_record_id:
            attendance_record = AttendanceRecord.objects.get(pk=attendance_record_id)
            attendance_record.attendance_status = False
            attendance_record.save()
            print(str(attendance_record.attendance_status))
        return HttpResponse('')

    @csrf_exempt
    def save_records(self, pk):
        day = Day.objects.get(pk=pk)
        day.checked = True
        print("MMMMMMMMMMMMMMMMMMMMMMMMMMMM" + str(day.day_title))
        day.save()
        return redirect('classroom:attendance_days')


class AttendanceDays(TemplateView):
    template_name = 'classroom/teachers/attendance_days.html'

    def get_context_data(self, **kwargs):
        days = Day.objects.all()
        super(AttendanceDays, self).get_context_data(**kwargs)
        context = {'days': days}
        return context






