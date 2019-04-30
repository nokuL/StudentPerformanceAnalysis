from django.urls import include, path

from .views import classroom, students, teachers, charts
urlpatterns = [
    path('', classroom.home, name='home'),

    path('students/', include(([
        path('studentdetail/<int:pk>', students.StudentsDetailView.as_view(), name='student_detail'),
        path('student/<int:pk>', students.StudentUpdateView.as_view(), name='student_update'),
        path('editsubjects/<int:pk>', students.EditSubjectsView.as_view(), name='edit_subjects'),
        path('viewSubjects', students.SubjectsView.as_view(), name='view_subjects'),
        path('recordResult/<int:pk>', students.RecordTestResult.as_view(), name='record_test_result'),
        path('editTestResult/<int:pk>', students.TestResultEditView.as_view(), name='edit_test_result'),
        path('delete/<int:pk>', students.TestResultDelete.as_view(), name='delete'),
        path('guardianUpdate/<int:pk>', students.GuardianUpdateView.as_view(), name='guardian_update'),
        path('otherDetails/<int:pk>', students.OtherDetailsUpdateView.as_view(), name='other_details_update'),
        path('personalityTest', students.PersonalityTest.as_view(), name='personality_test'),
        path('updatePersonality/<int:pk>', students.PersonalityTest2.as_view(),  name='update_personality'),
        path('updatePersonality3/<int:pk>', students.PersonalityTest3.as_view(),  name='update_personality3'),
        path('updatePersonality4/<int:pk>', students.PersonalityTest4.as_view(),  name='update_personality4'),
        path('careers', students.CareerListView.as_view(), name='career_list_view'),
        path('bar_graph/<int:sub_pk>/<int:student_pk>', students.BarGraph.as_view(), name='bar_graphs'),
        path('second_careers', students.SecondCareers.as_view(), name='second_careers')
    ], 'classroom'), namespace='students')),

    path('teachers/', include(([
        path('', teachers.TeacherDashboard.as_view(), name='teacher_dashboard'),
        path('attendanceRegister/<int:pk>', teachers.Attendance.as_view(), name='attendance'),
        path('setAttendanceStatus/<int:pk>', teachers.Attendance.set_attendance_status, name='set_attendance_status'),
        path('setAbsent/<int:pk>', teachers.Attendance.set_absent, name='set_absent'),
        path('saveAttendanceRecord/<int:pk>', teachers.Attendance.save_records, name='save_records'),
        path('attendanceDay', teachers.AttendanceDays.as_view(), name='attendance_days'),
        path('subjects', teachers.Subjects.as_view(), name='teacher_subjects'),
        path('subject_test/<int:pk>', teachers.SubjectsTestsView.as_view(), name='subject_tests')

    ], 'classroom'), namespace='teachers')),
]