from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.forms.utils import ValidationError
from classroom.models import Student, User, Subject


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

        class Meta(UserCreationForm.Meta):
            model = User

        @transaction.atomic
        def save(self):
            user = super().save(commit=False)
            user.is_student = True
            user.save()
            student = Student.objects.create(user=user)
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
    email = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))

    date_of_birth = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))
    age = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))
    subjects = forms.ModelMultipleChoiceField(
        queryset=Subject.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    class Meta:
        model = Student
        fields = ('first_name', 'second_name', 'last_name', 'email', 'age', 'date_of_birth', 'subjects')

