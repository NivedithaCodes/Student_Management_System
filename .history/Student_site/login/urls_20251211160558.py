from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('login/', views.login_view, {'popup': 'login'}, name='login'),
    path('signup/', views.signup_view, {'popup': 'signup'}, name='signup'),

    path('student/', views.student_view, name='student'),
    path('teacher/', views.teacher_view, name='teacher'),
    path('principal/', views.principal_view, name='principal'),
    path('profile/', views.profile_view, name='profile'),
    path('edit-profile/', views.edit_profile_view, name='edit_profile'),

    path('logout/', views.logout_view, name='logout'),

    # Admin / User Management
    path('add-admin/', views.add_admin, name='add_admin'),
    path('add-teacher/', views.add_teacher, name='add_teacher'),
    path('add-student/', views.add_student, name='add_student'),
    path('edit-user/<int:id>/', views.edit_user, name='edit_user'),
    path('delete-user/<int:id>/', views.delete_user, name='delete_user'),

    # Class Management
    path('add-class/', views.add_class, name='add_class'),
    path('edit-class/<int:id>/', views.edit_class, name='edit_class'),
    path('delete-class/<int:id>/', views.delete_class, name='delete_class'),

    # Subject Management
    path("add-only-subject/", views.add_only_subject, name="add_only_subject"),
    path("edit-subject-base/<int:id>/", views.edit_subject_base,name="edit_subject_base"),
    path("delete-subject-base/<int:id>/", views.delete_subject_base,name="delete_subject_base"),

    # AssignSubject Management
    path('add-subject/', views.assign_subject, name='add_subject'),
    path('edit-subject/<int:id>/', views.edit_subject, name='edit_subject'),
    path('delete-subject/<int:id>/', views.delete_subject, name='delete_subject'),

    # Syllabus Management
    path('add-syllabus/', views.add_syllabus, name='add_syllabus'),
    path('edit-syllabus/<int:id>/', views.edit_syllabus, name='edit_syllabus'),
    path('delete-syllabus/<int:id>/', views.delete_syllabus, name='delete_syllabus'),

    # Timetable Management
    path('add-timetable/', views.add_timetable, name='add_timetable'),
    path('edit-timetable/<int:id>/', views.edit_timetable, name='edit_timetable'),
    path('delete-timetable/<int:id>/', views.delete_timetable, name='delete_timetable'),

    # # Attendance
    # path("teacher/mark-attendance/", views.mark_attendance, name="mark_attendance"),
    # path("teacher/submit-attendance/", views.submit_attendance, name="submit_attendance"),

    # # Marks
    # path("teacher/add-marks/", views.add_marks, name="add_marks"),
    # path("teacher/submit-marks/", views.submit_marks, name="submit_marks"),

    # # Notifications
    # path("teacher/send-notification/", views.send_notification, name="send_notification"),
    
    #Settings
    path('settings/', views.settings_view, name='settings'),
    path('change-password/', views.change_password, name='change_password'),

    #Teacher Dashboard
    path('teacher/student/<int:student_id>/', views.student_profile_view, name='student_profile'),
    path('teacher/submit-attendance/', views.submit_attendance, name='submit_attendance'),
    # path('teacher/view-attendance/', views.view_attendance, name='view_attendance'),
    path("teacher/view-students/", views.view_students, name="view_students"),
   
    # path('teacher/', views.teacher_view, name='teacher'),
    # path('submit-attendance/', views.submit_attendance, name='submit_attendance'),
    path('get-attendance/', views.get_attendance, name='get_attendance'),  # <-- AJAX endpoint


]
 