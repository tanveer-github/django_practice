from django.db import models


class Course(models.Model):
    name = models.CharField(max_length=70)
    course_no = models.CharField(max_length=20)
    credit_hours = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class Student(models.Model):
    name = models.CharField(max_length=70)
    roll_no = models.CharField(max_length=70)
    phone = models.CharField(max_length=20)
    email = models.EmailField(max_length=200)
    address = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    marks = models.CharField(max_length=10)

    class Meta:
        unique_together = ('student', 'course')

    def __str__(self):
        return f'{self.student.name} is enrolled in {self.course.name}'
