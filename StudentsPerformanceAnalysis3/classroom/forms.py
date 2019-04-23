from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.forms.utils import ValidationError
from classroom.models import Student, User, Subject, Test, TestResult, Teacher, PersonalityRecord, relating
# importing answers from models
from classroom.models import YES_OR_NO, Guardian, Gender_Choices, Education_level, Argument,\
    making_a_decision, word_description, description, class_projects, queue, mathematical, yes_or_no, trip, info_description,\
    yes_no, situation, imagination, knowledge, friends, roommates, facts, appointments, order, relating


class TeacherSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_teacher = True
        if commit:
            user.save()
        return user


class StudentSignUpForm(UserCreationForm):
        subjects = forms.ModelMultipleChoiceField(
          queryset=Subject.objects.all(),
          widget=forms.CheckboxSelectMultiple,
          required=True
         )

        class Meta(UserCreationForm.Meta):
            model = User

        @transaction.atomic
        def save(self):
            user = super().save(commit=False)
            user.is_student = True
            user.save()
            student = Student.objects.create(user=user)
            student.subjects.add(*self.cleaned_data.get('subjects'))
            return user


class StudentUpdateForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))
    second_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
    }))

    date_of_birth = forms.CharField(widget=forms.DateInput(attrs={
        'class': 'form-control',
    }))
    age = forms.CharField(widget=forms.NumberInput(attrs={
        'class': 'form-control',
    }))
    gender = forms.ChoiceField(choices=Gender_Choices, widget=forms.Select(attrs={
        'class': 'form-control'
    }))

    class Meta:
        model = Student
        fields = ('first_name', 'second_name', 'last_name', 'email', 'age', 'date_of_birth',
                  'gender',)


class GuardianUpdateForm(forms.ModelForm):
    guardian = forms.ChoiceField(choices=Guardian, widget=forms.Select(attrs={
        'class': 'form-control'
    }))
    guardian_first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))

    guardian_last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))
    guardian_phone_number = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))
    guardian_email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
    }))
    guardian_education_level = forms.ChoiceField(choices=Education_level, widget=forms.Select(attrs={
        'class': 'form-control'
    }))

    class Meta:
        model = Student
        fields = ('guardian', 'guardian_first_name', 'guardian_last_name', 'guardian_phone_number',
                  'guardian_email', 'guardian_education_level')


class OtherDetailsUpdateForm(forms.ModelForm):
    extra_paid_classes = forms.ChoiceField(choices=YES_OR_NO, widget=forms.Select(attrs={
        'class': 'form-control'
    }))
    internet_access = forms.ChoiceField(label='Do you often use the internet for further research?', choices=YES_OR_NO,
                                  widget=forms.Select(attrs={
                                      'class': 'form-control'
                                  }))

    intend_to_pursue = forms.ChoiceField(label='Do you intend to pursue with further education?', choices=YES_OR_NO,
                                         widget=forms.Select(attrs={'class': 'form-control'
                                                                    }))

    free_time_after_school = forms.IntegerField(label='How much free time do you have after school?',
                                                widget=forms.NumberInput(attrs={'class': 'form-control'
                                                                                }))
    average_weekly_study_time = forms.IntegerField(label='What is your average weekly study time?',
                                                   widget=forms.NumberInput(attrs={
                                                       'class': 'form-control'
                                                   }))

    class Meta:
        model = Student
        fields = ('extra_paid_classes', 'internet_access', 'intend_to_pursue',  'free_time_after_school',
                  'average_weekly_study_time')


class TeacherUpdateForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ('first_name', 'last_name', 'email', 'phone_number', 'class_name')


class EditSubjectsForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('subjects',)
        widgets = {
            'subjects': forms.CheckboxSelectMultiple(attrs={
                'class': 'form-control'
            })
        }


class RecordTestResult(forms.ModelForm):
    test_score = forms.IntegerField(widget=forms.NumberInput(attrs={
        'class': 'form-control'
    }))
    test = forms.ModelChoiceField(
        widget=forms.Select(attrs={
            'class': 'form-control',
        }),
        queryset=Test.objects.all()
       )
    student = forms.ModelChoiceField(
        widget=forms.Select(attrs={
          'class': 'form-control',
        }),
        queryset=Student.objects.all())

    class Meta:
        model = TestResult
        fields = ('test_score', 'test')


class EditTestResult(forms.ModelForm):
    test_score = forms.IntegerField(widget=forms.NumberInput(attrs={
        'class': 'form-control'
    }))
    test = forms.ModelChoiceField(
        widget=forms.Select(attrs={
            'class': 'form-control',
        }),
        queryset=Test.objects.all())
    student = forms.ModelChoiceField(
        widget=forms.Select(attrs={
            'class': 'form-control',
        }),
        queryset=Student.objects.all())

    class Meta:
        model = TestResult
        fields = ('test_score', 'test', 'student')


class PersonalityTestForm(forms.ModelForm):
    psy_energy1 = forms.CharField(label='You find yourself in a long queue, what would you rather do ?',  max_length=10,
                                  widget=forms.RadioSelect(choices=queue))
    psy_energy2 = forms.CharField(label='Class projects are far better  : ', max_length=10,
                                  widget=forms.RadioSelect(choices=class_projects))
    psy_energy3 = forms.CharField(label='How would you describe yourself :', max_length=10,
                                  widget=forms.RadioSelect(choices=description))
    psy_energy4 = forms.CharField(label='You have been introduced to a friend of a friend :', max_length=10,
                                  widget=forms.RadioSelect(choices=friends))
    psy_energy5 = forms.CharField(label='Roommates:', max_length=10, widget=forms.RadioSelect(choices=roommates))


    class Meta:
        model = PersonalityRecord
        fields = ('psy_energy1', 'psy_energy2', 'psy_energy3', 'psy_energy4', 'psy_energy5')


class PersonalityTestForm2(forms.ModelForm):
    decision1 = forms.CharField(label='In an argument, you would rather :', max_length=10,
                                widget=forms.RadioSelect(choices=Argument))
    decision2 = forms.CharField(label='When making a decision you often : ', max_length=10,
                                widget=forms.RadioSelect(choices=making_a_decision))
    decision3 = forms.CharField(label='Choose the word that best describes you :', max_length=10,
                                widget=forms.RadioSelect(choices=word_description))
    decision4 = forms.CharField(label='What do you often think is important in any case ?', max_length=10,
                                widget=forms.RadioSelect(choices=facts))
    decision5 = forms.CharField(label='It is often difficult for you to relate to the way other people feel',
                                max_length=10, widget=forms.RadioSelect(choices=relating))

    class Meta:
        model = PersonalityRecord
        fields = ( 'decision1', 'decision2', 'decision3', 'decision4', 'decision5')


class PersonalityTestForm3(forms.ModelForm):
    info1 = forms.CharField(label='Which of these descriptions suits you more ?', max_length=10,
                            widget=forms.RadioSelect(choices=info_description))
    info2 = forms.CharField(label='Do you often get carried away by fantasies and ideas ?', max_length=10,
                            widget=forms.RadioSelect(choices=yes_no))
    info3 = forms.CharField(label='When considering a situation what do you often do ?', max_length=10,
                            widget=forms.RadioSelect(choices=situation))
    info4 = forms.CharField(label='Would you classify yourself as someone with strong imagination skills?',
                            max_length=10, widget=forms.RadioSelect(choices=imagination))
    info5 = forms.CharField(label='Which way do you find easier for you to gain knowledge', max_length=10,
                            widget=forms.RadioSelect(choices=knowledge))

    class Meta:
        model = PersonalityRecord
        fields = ('info1', 'info2', 'info3', 'info4', 'info5')


class PersonalityTestForm4(forms.ModelForm):
    lyf1 = forms.CharField(label='Do you often find yourself completing tasks within the stipulated time lines?',
                           max_length=10, widget=forms.RadioSelect(choices=yes_or_no))
    lyf2 = forms.CharField(label='When given mathematical problems for an assignment, do you often :', max_length=10,
                           widget=forms.RadioSelect(choices=mathematical))
    lyf3 = forms.CharField(label='There is an upcoming trip arranged for your class, would you rather', max_length=10,
                           widget=forms.RadioSelect(choices=trip))
    lyf4 = forms.CharField(label='You are almost always early for an appointment', max_length=10,
                           widget=forms.RadioSelect(choices=appointments))
    lyf5 = forms.CharField(label='Your study desk is usually', max_length=10,
                           widget=forms.RadioSelect(choices=order))

    class Meta:
        model = PersonalityRecord
        fields = ('lyf1', 'lyf2', 'lyf3', 'lyf4', 'lyf5')
