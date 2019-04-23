from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, UpdateView, TemplateView, DetailView, DeleteView
from ..models import User, Student, Subject, Test, TestResult, AttendanceRecord, Day, Teacher,  PersonalityRecord,\
    Personality, SubjectAverage, CategoryAverage, CareerField, CareerPersonalityCategory
from ..forms import StudentSignUpForm, StudentUpdateForm, EditSubjectsForm, RecordTestResult, EditTestResult, \
    GuardianUpdateForm, OtherDetailsUpdateForm, PersonalityTestForm, PersonalityTestForm2, PersonalityTestForm3, \
    PersonalityTestForm4
from ..decorators import student_required, teacher_required
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
import pandas as pd
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
import time
from  django.http import  HttpResponse
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import io
import matplotlib.pyplot as pyplot
pyplot.rcdefaults()
from pygal.style import CleanStyle

from .charts import FruitPieChart
import pygal


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

    def pass_fail_risk(self, student):
        print("STUUUUUUUDEEEENT STUDENT STUDENT" + str(student.average_weekly_study_time))
        return 0

    def best_subject_category(self, student, subjects):
        commercials_list = list()
        arts_list = list()
        sciences_list = list()
        comm_average_list = list()
        arts_average_list = list()
        science_average_list = list()
        category_averages = list()
        sorted_categories = ["0", "1", "2"]
        # categorising subjects
        for subject in subjects:
            if subject.category == "Commercials":
                commercials_list.append(subject)
            elif subject.category == "Arts":
                arts_list.append(subject)
            elif subject.category == "Sciences":
                sciences_list.append(subject)
            else:
                print("NO SUBJECT")

       #calculating commercials average
        for comm_subject in commercials_list:
            comm_test_results = list()
            subject_sum = 0
            subject_average_mark = 0
            tests = Test.objects.filter(subject=comm_subject)
            number_of_tests = len(tests)
            for test in tests:
                try:
                    test_result = TestResult.objects.get(student=student, test=test)
                except TestResult.DoesNotExist:
                    test_result = None
                if test_result is not None:
                    comm_test_results.append(test_result)
            for result in comm_test_results:
                subject_sum = subject_sum + result.test_score
                if number_of_tests > 0:
                    subject_average_mark = (subject_sum/number_of_tests)
            subject_average = SubjectAverage()
            subject_average.subject = comm_subject
            subject_average.student = student
            subject_average.subject_average_mark = subject_average_mark
            comm_average_list.append(subject_average)
        comm_average = self.category_average(comm_average_list)
        comm_sub_average = CategoryAverage()
        comm_sub_average.student = student
        comm_sub_average.category_name = "Commercials"
        comm_sub_average.category_average_mark = comm_average
        category_averages.append(comm_sub_average)

            #calculating arts average
        for art_sub in arts_list:
            arts_test_results = list()
            subject_sum = 0
            subject_average_mark = 0
            tests = Test.objects.filter(subject=art_sub)
            number_of_tests = len(tests)
            for test in tests:
                try:
                    test_result = TestResult.objects.get(student=student, test=test)
                except TestResult.DoesNotExist:
                    test_result = None
                if test_result is not None:
                    arts_test_results.append(test_result)
            for result in arts_test_results:
                subject_sum = subject_sum + result.test_score
                if number_of_tests > 0:
                    subject_average_mark = (subject_sum/number_of_tests)
            subject_average = SubjectAverage()
            subject_average.subject = art_sub
            subject_average.student = student
            subject_average.subject_average_mark = subject_average_mark
            arts_average_list.append(subject_average)
        arts_average = self.category_average(arts_average_list)
        arts_sub_average = CategoryAverage()
        arts_sub_average.student = student
        arts_sub_average.category_name = "Arts"
        arts_sub_average.category_average_mark = arts_average
        category_averages.append(arts_sub_average)

        #calculating sciences average
        for science_sub in sciences_list:
            science_test_results = list()
            subject_sum = 0
            subject_average_mark = 0
            tests = Test.objects.filter(subject=science_sub)
            number_of_tests = len(tests)
            for test in tests:
                try:
                    test_result = TestResult.objects.get(student=student, test=test)
                except TestResult.DoesNotExist:
                    test_result = None
                if test_result is not None:
                    science_test_results.append(test_result)
            for result in science_test_results:
                subject_sum = subject_sum + result.test_score
                if number_of_tests > 0:
                    subject_average_mark = (subject_sum / number_of_tests)
            subject_average = SubjectAverage()
            subject_average.subject = science_sub
            subject_average.student = student
            subject_average.subject_average_mark = subject_average_mark
            science_average_list.append(subject_average)
        sciences_average = self.category_average(science_average_list)
        sciences_sub_average = CategoryAverage()
        sciences_sub_average.student = student
        sciences_sub_average.category_name = "Sciences"
        sciences_sub_average.category_average_mark = sciences_average
        category_averages.append(sciences_sub_average)
        print(category_averages)
        sorted_average_marks = self.highest_mark_category(category_averages)
        print("SORTED AVERAGE MARKS" + str(sorted_average_marks))
        for category_average in category_averages:
            if category_average.category_average_mark == sorted_average_marks[0]:
                first_category = category_average.category_name
                sorted_categories[0] = first_category
            if category_average.category_average_mark == sorted_average_marks[1]:
                second_category = category_average.category_name
                sorted_categories[1] = second_category
            if category_average.category_average_mark == sorted_average_marks[2]:
                third_category = category_average.category_name
                sorted_categories[2] = third_category
        print(sorted_categories)
        return sorted_categories

    def category_average(self, categorylist):
        category_sum = 0
        for category in categorylist:
            if len(categorylist) > 0:
                category_sum = category_sum + category.subject_average_mark
        if len(categorylist) > 0:
            no_of_subjects = len(categorylist)
            category_average = (category_sum / no_of_subjects)
            return category_average
        else:
            return 0

    def highest_mark_category(self, category_average_list):
        category_averages = list()
        for category in category_average_list:
            category_averages.append(category.category_average_mark)
        category_averages.sort(reverse=True)
        return category_averages

    def best_subjects(self, student, subjects):
        subject_average_list = list()
        best_subjects = subjects
        for subject in subjects:
            tests_result_array = list()
            subject_sum = 0
            subject_average_mark = 0
            tests = Test.objects.filter(subject=subject)
            number_of_tests = len(tests)
            for test in tests:
                try:
                    test_result = TestResult.objects.get(student=student, test=test)
                except TestResult.DoesNotExist:
                    test_result = None
                if test_result is not None:
                    tests_result_array.append(test_result)
            for result in tests_result_array:
                subject_sum = subject_sum + result.test_score
                if number_of_tests > 0:
                    subject_average_mark = (subject_sum/number_of_tests)
            subject_average = SubjectAverage()
            subject_average.subject = subject
            subject_average.student = student
            subject_average.subject_average_mark = subject_average_mark
            subject_average_list.append(subject_average)
        subject_marks = self.max_subject_average(subject_average_list)
        print("SUBJECT MARKS" + str(subject_marks))
        for subject_average in subject_average_list:
            if len(subject_average_list) >= 3:
                if subject_average.subject_average_mark == subject_marks[0]:
                    first_best_subject = subject_average.subject
                    best_subjects[0] = first_best_subject
                if subject_average.subject_average_mark == subject_marks[1]:
                    second_best_subject = subject_average.subject
                    best_subjects[1] = second_best_subject
                if subject_average.subject_average_mark == subject_marks[2]:
                    third_best_subject = subject_average.subject
                    best_subjects[2] = third_best_subject
            elif len(subject_average_list) == 2:
                if subject_average.subject_average_mark == subject_marks[0]:
                    first_best_subject = subject_average.subject
                    best_subjects[0] = first_best_subject
                if subject_average.subject_average_mark == subject_marks[1]:
                    second_best_subject = subject_average.subject
                    best_subjects[1] = second_best_subject
            else:
                if subject_average.subject_average_mark == subject_marks[0]:
                    first_best_subject = subject_average.subject
                    best_subjects[0] = first_best_subject

        return best_subjects

    def max_subject_average(self, subject_average_list):
        subject_marks = list()
        for subject_average in subject_average_list:
            subject_mark = subject_average.subject_average_mark
            subject_marks.append(subject_mark)
        subject_marks.sort(reverse=True)
        return subject_marks

    def best_subjects_in_career(self, student, careers):
        related_subjects = list()
        for career in careers:
            subjects = list(career.dominant_subjects.all())
            for subject in subjects:
                related_subjects.append(subject)
        best_subject_in_career = self.best_subjects(student, related_subjects)
        return best_subject_in_career

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
            self.pass_fail_risk(student)
            test_results = TestResult.objects.filter(student=student)
            for test_result in test_results:
                self.pass_status(test_result)
            subjects = student.subjects.all()
            user = self.request.user
            attendance_records = AttendanceRecord.objects.filter(student=student)
            attendance_percentage = self.attendance_percentage(student)
            best_categories = self.best_subject_category(student, subjects)
            first_best = best_categories[0]
            second_best = best_categories[1]
            third_best = best_categories[2]
            if student.has_taken_test:
                career_category_ids = self.process_career(first_best, second_best, student)
                first_career_category_id = career_category_ids[0]
                second_career_category_id = career_category_ids[1]
                first_career_category = CareerPersonalityCategory.objects.get(
                    career_personality_identifier=first_career_category_id)
                second_career_category = CareerPersonalityCategory.objects.get(
                    career_personality_identifier=second_career_category_id)
                first_careers = CareerField.objects.filter(career_personality_category=first_career_category)
                print("FIRST CAREERS" + str(first_careers))
                first_best_subjects_in_career = self.best_subjects_in_career(student, first_careers)
                print("FIRST BEST SUBJECTS IN CAREER" + str(first_best_subjects_in_career))
                second_careers = CareerField.objects.filter(career_personality_category=second_career_category)
                print("SECOND CAREERS " + str(second_careers))
                second_best_subjects_in_career = self.best_subjects_in_career(student, second_careers)
                official_first_careers = CareerField.objects.filter(career_personality_category=first_career_category,
                                                                    dominant_subjects=first_best_subjects_in_career[0])
                official_second_careers = CareerField.objects.filter(career_personality_category=second_career_category,
                                                                     dominant_subjects=second_best_subjects_in_career[0])
                print("SECOND BEST SUBJECTS IN CAREER" + str(second_best_subjects_in_career))
                print("********************************" + str(official_first_careers))
                context = super(StudentsDetailView, self).get_context_data(**kwargs)
                cht_fruits = FruitPieChart(

                    height=600,
                    width=800,
                    explicit_size=True,
                    style=CleanStyle,
                    student=student,

                )

                # Call the `.generate()` method on our chart object
                # and pass it to template context.
                cht_fruits = cht_fruits.generate()
                context = {'test_results': test_results, 'student': student,
                           'subjects': subjects, 'user': user, 'attendance_records': attendance_records,
                           'attendance_percentage': attendance_percentage,
                           'first_best': first_best, 'second_best': second_best, 'third_best': third_best,
                           'first_careers': official_first_careers, 'second_careers': official_second_careers,
                           'cht_fruits': cht_fruits}
                return context
            else:
                context = super(StudentsDetailView, self).get_context_data(**kwargs)
                context = {'test_results': test_results, 'student': student,
                           'subjects': subjects, 'user': user, 'attendance_records': attendance_records,
                           'attendance_percentage': attendance_percentage,
                           'first_best': first_best, 'second_best': second_best, 'third_best': third_best,
                           }
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
            best_categories = self.best_subject_category(student, subjects)
            first_best = best_categories[0]
            second_best = best_categories[1]
            third_best = best_categories[2]
            print("KKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKK" + first_best)
            print("KKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKK" + second_best)
            print("KKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKK" + third_best)

            if student.has_taken_test:
                career_category_ids = self.process_career(first_best, second_best, student)
                first_career_category_id = career_category_ids[0]
                second_career_category_id = career_category_ids[1]
                first_career_category = CareerPersonalityCategory.objects.get(
                    career_personality_identifier=first_career_category_id)
                second_career_category = CareerPersonalityCategory.objects.get(
                    career_personality_identifier=second_career_category_id)
                first_careers = CareerField.objects.filter(career_personality_category=first_career_category)
                print("FIRST CAREERS" + str(first_careers))
                first_best_subjects_in_career = self.best_subjects_in_career(student, first_careers)
                print("FIRST BEST SUBJECTS IN CAREER" + str(first_best_subjects_in_career))
                second_careers = CareerField.objects.filter(career_personality_category=second_career_category)
                print("SECOND CAREERS " + str(second_careers))
                second_best_subjects_in_career = self.best_subjects_in_career(student, second_careers)
                official_first_careers = CareerField.objects.filter(career_personality_category=first_career_category,
                                                                    dominant_subjects=first_best_subjects_in_career[0])
                official_second_careers = CareerField.objects.filter(career_personality_category=second_career_category,
                                                                     dominant_subjects=second_best_subjects_in_career[
                                                                         0])
                print("SECOND BEST SUBJECTS IN CAREER" + str(second_best_subjects_in_career))
                print("********************************" + str(official_first_careers))
                context = super(StudentsDetailView, self).get_context_data(**kwargs)
                cht_fruits = FruitPieChart(
                    height=600,
                    width=800,
                    explicit_size=True,
                    style=CleanStyle,
                    student=student
                )

                # Call the `.generate()` method on our chart object
                # and pass it to template context.
                cht_fruits = cht_fruits.generate()
                context = {'test_results': test_results, 'student': student,
                           'subjects': subjects, 'user': user, 'attendance_records': attendance_records,
                           'attendance_percentage': attendance_percentage,
                           'first_best': first_best, 'second_best': second_best, 'third_best': third_best,
                           'first_careers': official_first_careers, 'second_careers': official_second_careers,
                           'cht_fruits': cht_fruits}
                return context
            else:
                context = super(StudentsDetailView, self).get_context_data(**kwargs)
                context = {'test_results': test_results, 'student': student,
                           'subjects': subjects, 'user': user, 'attendance_records': attendance_records,
                           'attendance_percentage': attendance_percentage,
                           'first_best': first_best, 'second_best': second_best, 'third_best': third_best,
                           }
                return context

    def process_career(self, first_best, second_best, student):
            personality_identifier = student.personality.identifier
            if first_best == 'Sciences':
                first_subject_category = 1
            elif first_best == 'Commercials':
                first_subject_category = 2
            else:
                first_subject_category = 3

            if second_best == 'Sciences':
                second_subject_category = 1
            elif second_best == 'Commercials':
                second_subject_category = 2
            else:
                second_subject_category = 3

            data = pd.read_csv('classroom/uploads/career.csv', delimiter=',')

            gnb = GaussianNB()
            data = data[[
                "personality",
                "subject_category",
                "career_category"
            ]].dropna(axis=0, how='any')
            used_features = [
                "personality",
                "subject_category",
            ]
            print('jjjjjjjjjjjjjjjjjjjjjjjjjjj' + str(personality_identifier) + '' + str(first_subject_category))
            X_train, X_test = train_test_split(data, test_size=0.56, random_state=int(time.time()))
            gnb.fit(
                X_train[used_features].astype(float),
                X_train["career_category"].astype(float)
            )
            print(data.head())
            print("Dataset Lenght:: ", len(data))
            print("Dataset Shape:: ", data.shape)
            predict_first = gnb.predict(
            [[personality_identifier, first_subject_category]])
            predict_second = gnb.predict(
                [[personality_identifier, second_subject_category]])
            first_career_category_id = int(predict_first)
            second_career_category_id = int(predict_second)
            career_category_ids = [0, 1]
            career_category_ids[0] = first_career_category_id
            career_category_ids[1] = second_career_category_id
            return career_category_ids


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


class PersonalityTest4(UpdateView):
    model = PersonalityRecord
    form_class = PersonalityTestForm4
    template_name = 'classroom/students/personality_test2.html'

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
        print('jjjjjjjjjjjjjjjjjjjjjjjjjjj' + str(energy) + '' + str(information) + '' + str(decision) + '' + str(life))
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


class PersonalityTest3(UpdateView):
    model = PersonalityRecord
    form_class = PersonalityTestForm3
    template_name = 'classroom/students/personality_test2.html'

    def form_valid(self, form):
        personality_record = form.save()
        personality_record_pk = personality_record.pk

        return redirect('students:update_personality4', pk=personality_record_pk)


class PersonalityTest2(UpdateView):
    model = PersonalityRecord
    form_class = PersonalityTestForm2
    template_name = 'classroom/students/personality_test2.html'

    def form_valid(self, form):

        personality_record = form.save()
        personality_record_pk = personality_record.pk

        return redirect('students:update_personality3', pk=personality_record_pk)


class PersonalityTest(CreateView):
    model = PersonalityRecord
    template_name = 'classroom/students/personality_test.html'
    form_class = PersonalityTestForm

    def form_valid(self, form):

        personality_record = form.save()
        personality_record_pk = personality_record.pk

        return redirect('students:update_personality', pk=personality_record_pk)


class CareerListView(TemplateView):
    template_name = 'classroom/students/career_list.html'

    def get_context_data(self, **kwargs):

        return 0


class BarGraph(TemplateView):
    template_name = 'classroom/students/subject_bar_graphs.html'

    def get_context_data(self, **kwargs):
        test_results = list()
        test_1 = 0
        test_2 = 0
        test_3 = 0
        test_4 = 0

        student_pk = self.kwargs['student_pk']
        subject_pk = self.kwargs['sub_pk']
        student = Student.objects.get(pk=student_pk)
        subject = Subject.objects.get(pk=subject_pk)
        print("HHHHHHHHHHHHHHHHHHHHHHH" + student.first_name)
        print("HHHHHHHHHHHHHHHHHHHHHHH" + subject.subject_title)
        tests = Test.objects.filter(subject=subject)
        for test in tests:
            try:
                test_result = TestResult.objects.get(student=student, test=test)
            except TestResult.DoesNotExist:
                test_result = None
            if test_result is not None:
                test_results.append(test_result)
        for test_result in test_results:
            if test_result.test.test_number == 1:
                test_1 = test_result.test_score
            if test_result.test.test_number == 2:
                test_2 = test_result.test_score
            if test_result.test.test_number == 3:
                test_3 = test_result.test_score
            if test_result.test.test_number == 4:
                test_4 = test_result.test_score
        data = {'test_1': test_1, 'test_2': test_2, 'test_3': test_3, 'test_4': test_4}
        graph = self.graphs(data)
        context = super(BarGraph, self).get_context_data(**kwargs)
        context ={'subject': subject, 'graph': graph}
        return context

    def graphs(self, data):
        b_chart = pygal.Bar()
        b_chart.title = "Performance graph"
        b_chart_data = data
        for key, value in b_chart_data.items():
            b_chart.add(key, value)
        return b_chart.render(is_unicode=True)
