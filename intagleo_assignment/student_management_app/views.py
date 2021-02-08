from django.shortcuts import render

from student_management_app.models import Student, Enrollment, Course


def students(request):
    context = {
        'students': Student.objects.all()
    }
    return render(request, 'students.html', context)


def courses(request):
    context = {
        'courses': Course.objects.all()
    }
    return render(request, 'courses.html', context)


def enrollments(request):
    context = {
        'enrollments': Enrollment.objects.all()
    }
    return render(request, 'enrollments.html', context)
