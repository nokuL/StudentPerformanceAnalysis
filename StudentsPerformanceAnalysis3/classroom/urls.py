from django.urls import include, path

from .views import classroom, students, teachers
urlpatterns = [
    path('', classroom.home, name='home'),

    path('students/', include(([
        path('studentdetail/<int:pk>', students.StudentsDetailView.as_view(), name='student_detail'),
        path('student/<int:pk>', students.StudentUpdateView.as_view(), name='student_update')
    ], 'classroom'), namespace='students')),

    path('teachers/', include(([
        path('', teachers.TeacherDashboard.as_view(), name='teacher_dashboard'),
    ], 'classroom'), namespace='teachers')),
]