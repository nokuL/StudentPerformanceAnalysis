from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, UpdateView, TemplateView, DetailView, DeleteView
from ..models import User, Student, Subject, Test, TestResult, AttendanceRecord, Day
from ..forms import StudentSignUpForm, StudentUpdateForm, EditSubjectsForm, RecordTestResult, EditTestResult


class StudentSignUpView(CreateView):
    model = User
    form_class = StudentSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'student'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        student = Student.objects.get(user=user)
        return redirect('students:student_detail', pk=student.pk)


class StudentsDetailView(DetailView):
    model = Student
    template_name = 'classroom/students/student_detail.html'

    def pass_status(self, test_result):
        test = Test.objects.get(testresult=test_result)
        test_total = test.total_score
        percentage = (test_result.test_score / test_total) * 100
        if percentage >= 50.0:
            test_result.pass_status = 'PASS'
        else:
            test_result.pass_status = 'FAIL'
        test_result.percentage = percentage
        print(percentage)
        return percentage

    def attendance_percentage(self, student):
        days_present = AttendanceRecord.objects.filter(student=student, attendance_status=True)
        present_days = days_present.count()
        checked_days = Day.objects.filter(checked=True)
        number_of_checked_days = checked_days.count()
        if number_of_checked_days == 0:
            return 0
        else:
            attendance_percentage = (present_days / number_of_checked_days) * 100
            int_percentage = int(attendance_percentage)
            print(int_percentage)
            return int_percentage

    def get_context_data(self, **kwargs):
        if self.request.user.is_student:
            student = Student.objects.get(user=self.request.user)
            test_results = TestResult.objects.filter(student=student)
            for test_result in test_results:
                self.pass_status(test_result)
            subjects = student.subjects.all()
            user = self.request.user
            attendance_records = AttendanceRecord.objects.filter(student=student)
            attendance_percentage = self.attendance_percentage(student)
            print(attendance_percentage)
            context = super(StudentsDetailView, self).get_context_data(**kwargs)
            context = {'test_results': test_results, 'student': student, 'subjects': subjects, 'user': user,
                       'attendance_records': attendance_records, 'attendance_percentage': attendance_percentage}
            return context
        if self.request.user.is_teacher:
            student_pk = self.kwargs['pk']
            user = User.objects.get(pk=student_pk)
            student = Student.objects.get(user=user)
            test_results = TestResult.objects.filter(student=student)
            for test_result in test_results:
                self.pass_status(test_result)
            subjects = student.subjects.all()
            user = self.request.user
            attendance_records = AttendanceRecord.objects.filter(student=student)
            attendance_percentage = self.attendance_percentage(student)
            print(attendance_percentage)
            context = super(StudentsDetailView, self).get_context_data(**kwargs)
            context = {'test_results': test_results, 'student': student,
                       'subjects': subjects, 'user': user, 'attendance_records': attendance_records, 'attendance_percentage': attendance_percentage}
            return context


class StudentUpdateView(UpdateView):
    model = Student
    form_class = StudentUpdateForm
    template_name = 'classroom/students/student_update_form.html'


class EditSubjectsView(UpdateView):
    model = Student
    form_class = EditSubjectsForm
    template_name = 'classroom/students/edit_subject_form.html'


class SubjectsView(TemplateView):
    model = Subject
    template_name = 'classroom/students/subjects_view.html'

    def get_context_data(self, **kwargs):
        try:
            student = Student.objects.filter(user=self.request.user)
        except Student.DoesNotExist:
            student = None
        test_results = TestResult.objects.filter(student=student)
        context = super(SubjectsView, self).get_context_data(**kwargs)
        context = {'test_results': test_results}
        return context


class RecordTestResult(CreateView):
    model = TestResult
    form_class = RecordTestResult
    template_name = 'classroom/students/record_test_result.html'

    def form_valid(self, form):
        test_result = form.save()
        student = test_result.student
        return redirect('students:student_detail', pk=student.pk)


class TestResultEditView(UpdateView):
    model = TestResult
    form_class = EditTestResult
    template_name = 'classroom/students/add_test_result.html'

    def form_valid(self, form):
        student = self.object.student
        student_pk = student.pk
        form.save()
        return redirect('students:student_detail', pk=student.pk)


class TestResultDelete(DeleteView):
    model = TestResult
    success_url = reverse_lazy('students:view_subjects')
    template_name = 'classroom/students/testresult_confirm_delete.html'








