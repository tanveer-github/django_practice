from django.urls import path, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register('student', views.StudentViewSet)
router.register('course', views.CourseViewSet)
router.register('enrollment', views.EnrollmentViewSet)
router.register('gpa', views.GPAViewSet, basename='gpa')

urlpatterns = [
    path('', include(router.urls))
]
