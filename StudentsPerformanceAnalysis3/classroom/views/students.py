from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, UpdateView, TemplateView, DetailView, DeleteView
from ..models import User, Student, Subject, Test, TestResult, AttendanceRecord, Day, Teacher,  PersonalityRecord, Personality
from ..forms import StudentSignUpForm, StudentUpdateForm, EditSubjectsForm, RecordTestResult, EditTestResult, \
    GuardianUpdateForm, OtherDetailsUpdateForm, PersonalityTestForm
from ..decorators import student_required, teacher_required
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
import pandas as pd
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
import time


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
            context = super(StudentsDetailView, self).get_context_data(**kwargs)
            context = {'test_results': test_results, 'student': student,
                       'subjects': subjects, 'user': user, 'attendance_records': attendance_records,
                       'attendance_percentage': attendance_percentage}
            return context


class StudentUpdateView(UpdateView):
    model = Student
    form_class = StudentUpdateForm
    template_name = 'classroom/students/student_update_form.html'


class GuardianUpdateView(UpdateView):
    model = Student
    form_class = GuardianUpdateForm
    template_name = 'classroom/students/guardian_update_form.html'


class OtherDetailsUpdateView(UpdateView):
    model = Student
    form_class = OtherDetailsUpdateForm
    template_name = 'classroom/students/other_student_details_update_form.html'


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
        return redirect('students:student_detail', pk=student.pk )


class TestResultDelete(DeleteView):
    model = TestResult
    success_url = reverse_lazy('students:view_subjects')
    template_name = 'classroom/students/testresult_confirm_delete.html'


class PersonalityTest(CreateView):
    model = PersonalityRecord
    template_name = 'classroom/students/personality_test.html'
    form_class = PersonalityTestForm

    def form_valid(self, form):
        user = self.request.user
        student = Student.objects.get(user=user)
        student_pk = student.pk
        personality_record = form.save()
        personality_id = self.process(personality_record)
        personality = Personality.objects.get(identifier=personality_id)
        student.personality = personality
        student.has_taken_test = True
        student.save()
        print('#################################'+ student.first_name + '###################'
              + student.personality.personality_name)
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>' + str(personality_record.psy_energy1))
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>' + str(personality_record.psy_energy2))
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>' + str(personality_record.psy_energy3))
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'+  str(personality_record.psy_energy4))
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>' + str(personality_record.psy_energy5))
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>' + str(personality_record.decision1))
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>' + str(personality_record.decision2))
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>' + str(personality_record.decision3))
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>' + str(personality_record.decision4))
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>' + str(personality_record.decision5))
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>' + str(personality_record.info1))
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>' + str(personality_record.info2))
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>' + str(personality_record.info3))
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>' + str(personality_record.info4))
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>' + str(personality_record.info5))
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>' + str(personality_record.lyf1))
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>' + str(personality_record.lyf2))
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>' + str(personality_record.lyf3))
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>' + str(personality_record.lyf4))
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>' + str(personality_record.lyf5))

        return redirect('students:student_detail', pk=student_pk)

    def process(self, personality_record):
        introvertcount = 0
        extrovertcount = 0
        intuitioncount = 0
        thinkingcount = 0
        feelingcount = 0
        judgingcount = 0
        sensingcount = 0
        percievingcount = 0
        # processing for psy_energy, counting the instances
        psy_list = list()
        psy_energy1 = personality_record.psy_energy1
        psy_list.append(psy_energy1)
        psy_energy2 = personality_record.psy_energy2
        psy_list.append(psy_energy2)
        psy_energy3 = personality_record.psy_energy3
        psy_list.append(psy_energy3)
        psy_energy4 = personality_record.psy_energy4
        psy_list.append(psy_energy4)
        psy_energy5 = personality_record.psy_energy5
        psy_list.append(psy_energy5)
        for psy_energy in psy_list:
            if psy_energy == 'Introvert':
                introvertcount = introvertcount + 1
            else:
                extrovertcount = extrovertcount + 1
        if introvertcount > extrovertcount:
            energy = 2
        else:
            energy = 1

        # processing for information
        info_list = list()
        info1 = personality_record.info1
        info_list.append(info1)
        info2 = personality_record.info2
        info_list.append(info2)
        info3 = personality_record.info3
        info_list.append(info3)
        info4 = personality_record.info4
        info_list.append(info4)
        info5 = personality_record.info5
        info_list.append(info5)
        for info in info_list:
            if info == 'Sensing':
                sensingcount = sensingcount + 1
            else:
                intuitioncount = intuitioncount + 1
        if intuitioncount > sensingcount:
            information = 2
        else:
            information = 1
        # processing decision making
        decision_list = list()
        decision1 = personality_record.decision1
        decision_list.append(decision1)
        decision2 = personality_record.decision2
        decision_list.append(decision2)
        decision3 = personality_record.decision3
        decision_list.append(decision3)
        decision4 = personality_record.decision4
        decision_list.append(decision4)
        decision5 = personality_record.decision5
        decision_list.append(decision5)
        for decision_attribute in decision_list:
            if decision_attribute == 'Thinking':
                thinkingcount = thinkingcount + 1
            else:
                feelingcount = feelingcount + 1
        if thinkingcount > feelingcount:
            decision = 1
        else:
            decision = 2
        # processing for life decisions
        lyf_list = list()
        lyf1 = personality_record.lyf1
        lyf_list.append(lyf1)
        lyf2 = personality_record.lyf2
        lyf_list.append(lyf2)
        lyf3 = personality_record.lyf3
        lyf_list.append(lyf3)
        lyf4 = personality_record.lyf4
        lyf_list.append(lyf4)
        lyf5 = personality_record.lyf5
        lyf_list.append(lyf5)
        for lyf in lyf_list:
            if lyf == 'Judging':
                judgingcount = judgingcount + 1
            else:
                percievingcount = percievingcount + 1
        if judgingcount > percievingcount:
            life = 1
        else:
            life = 2
        # GaussianNB
        data = pd.read_csv('classroom/uploads/personalities.csv', delimiter=',')

        gnb = GaussianNB()
        data = data[[
            "energy",
            "information",
            "decision",
            "life",
            "type"
        ]].dropna(axis=0, how='any')
        used_features = [
            "energy",
            "information",
            "decision",
            "life"
        ]
        print('jjjjjjjjjjjjjjjjjjjjjjjjjjj' + str(energy)+''+str(information)+''+str(decision)+''+str(life))
        X_train, X_test = train_test_split(data, test_size=0.56, random_state=int(time.time()))
        gnb.fit(
            X_train[used_features].astype(float),
            X_train["type"].astype(float)
        )
        print(data.head())
        print("Dataset Lenght:: ", len(data))
        print("Dataset Shape:: ", data.shape)
        predict = gnb.predict(
            [[energy, information, decision, life]])
        print("Predict Value !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!", str(predict))

        personality_id = int(predict)

        return personality_id








