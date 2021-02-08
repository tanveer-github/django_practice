from django.urls import path, include

from student_management_app import views

urlpatterns = [
    path('', views.students, name='students'),
    path('courses', views.courses, name='courses'),
    path('enrollments', views.enrollments, name='enrollments'),
    path('api/', include('student_management_app.api.urls'), name='student-api')
]
