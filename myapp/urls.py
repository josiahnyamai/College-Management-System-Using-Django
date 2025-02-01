from django.urls import path
from .views import user_login, user_signup, user_logout, dashboard, student_list, student_add, student_update, student_delete, course_management, add_course, enroll_student, course_detail, course_list, grade_management

urlpatterns = [
    path('login/', user_login, name='login'),
    path('signup/', user_signup, name='user_signup'),
    path('logout/', user_logout, name='logout'),
    path('', dashboard, name='dashboard'),  # Dashboard homepage
    path('students/', student_list, name='student_list'),  # Student list view
    path('students/add/', student_add, name='student_add'),  # Add student view
    path('students/edit/<int:pk>/', student_update, name='student_update'),  # Edit student view
    path('students/delete/<int:pk>/', student_delete, name='student_delete'),  # Delete student view
    path('courses/', course_management, name='course_management'),
    path('courses/add/<int:school_id>/', add_course, name='add_course'),
    path('student/enroll/', enroll_student, name='enroll_student'),  # Enroll new student
    path('student/enroll/<int:student_id>/', enroll_student, name='edit_student_enrollment'),  # Edit student enrollment
    path('students/', student_list, name='student_list'),  # List of students
    path('courses/', course_list, name='course_list'),  # Add this line
    path('course/<int:course_id>/', course_detail, name='course_detail'),
    path('grades/', grade_management, name='grade_management'),
]