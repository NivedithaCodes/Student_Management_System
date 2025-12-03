from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('login/', views.login_view, {'popup': 'login'}, name='login'),
    path('signup/', views.signup_view, {'popup': 'signup'}, name='signup'),

    path('student/', views.student_view, name='student'),
    path('teacher/', views.teacher_view, name='teacher'),

    # principal dashboard url name is 'principal' — used by redirects in views
    path('principal/', views.principal_view, name='principal'),

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
    path('add-subject/', views.add_subject, name='add_subject'),
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


]
