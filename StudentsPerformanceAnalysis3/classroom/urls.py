from django.urls import include, path

from .views import classroom, students, teachers
urlpatterns = [
    path('', classroom.home, name='home'),

    path('students/', include(([
        path('studentdetail/<int:pk>', students.StudentsDetailView.as_view(), name='student_detail'),
        path('student/<int:pk>', students.StudentUpdateView.as_view(), name='student_update'),
        path('editsubjects/<int:pk>', students.EditSubjectsView.as_view(), name='edit_subjects'),
        path('viewSubjects', students.SubjectsView.as_view(), name='view_subjects'),
        path('recordResult', students.RecordTestResult.as_view(), name='record_test_result'),
        path('editTestResult/<int:pk>', students.TestResultEditView.as_view(), name='edit_test_result'),
        path('delete/<int:pk>', students.TestResultDelete.as_view(), name='delete')
    ], 'classroom'), namespace='students')),

    path('teachers/', include(([
        path('', teachers.TeacherDashboard.as_view(), name='teacher_dashboard'),
    ], 'classroom'), namespace='teachers')),
]