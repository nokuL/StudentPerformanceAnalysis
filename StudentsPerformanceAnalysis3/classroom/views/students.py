from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, UpdateView, TemplateView, DetailView, DeleteView
from ..models import User, Student, Subject, Test, TestResult
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
        student = Student.objects.get(user=self.request.user)
        test_results = TestResult.objects.filter(student=student)
        context = super(SubjectsView, self).get_context_data(**kwargs)
        context = {'test_results': test_results}
        return context


class RecordTestResult(CreateView):
    model = TestResult
    form_class = RecordTestResult
    template_name = 'classroom/students/add_test_result.html'

    def form_valid(self, form):
        form.save()
        return redirect('students:view_subjects')


class TestResultEditView(UpdateView):
    model = TestResult
    form_class = EditTestResult
    template_name = 'classroom/students/add_test_result.html'

    def form_valid(self, form):
        form.save()
        return redirect('students:view_subjects')


class TestResultDelete(DeleteView):
    model = TestResult
    success_url = reverse_lazy('students:view_subjects')
    template_name = 'classroom/students/testresult_confirm_delete.html'








