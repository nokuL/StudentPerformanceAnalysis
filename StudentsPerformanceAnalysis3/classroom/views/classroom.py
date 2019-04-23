from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from classroom.models import Student

class SignUpView(TemplateView):
    template_name = 'registration/signup.html'


def home(request):
    if request.user.is_authenticated:
        if request.user.is_teacher:
            return redirect('teachers:teacher_dashboard')
        else:
            return redirect('students:student_detail', pk=request.user.pk,)
    return render(request, 'classroom/home.html')