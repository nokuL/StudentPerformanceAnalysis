from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.forms.utils import ValidationError
from classroom.models import Student, User, Subject, Test, TestResult
from classroom.models import YES_OR_NO, Guardian, Gender_Choices


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
    guardian = forms.ChoiceField(choices=Guardian, widget=forms.Select(attrs={
        'class': 'form-control'
    }))
    extra_paid_classes = forms.ChoiceField(choices=YES_OR_NO, widget=forms.Select(attrs={
        'class': 'form-control'
    }))
    internet_access = forms.ChoiceField(choices=YES_OR_NO, widget=forms.Select(attrs={
        'class': 'form-control'
    }))
    intend_to_pursue = forms.ChoiceField(choices=YES_OR_NO, widget=forms.Select(attrs={
        'class': 'form-control'
    }))
    out_going = forms.ChoiceField(choices=YES_OR_NO, widget=forms.Select(attrs={
        'class': 'form-control'
    }))

    class Meta:
        model = Student
        fields = ('first_name', 'second_name', 'last_name', 'email', 'age', 'date_of_birth',
                  'gender', 'guardian', 'extra_paid_classes', 'internet_access', 'intend_to_pursue', 'out_going')


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
        fields = ('test_score', 'test', 'student')


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

