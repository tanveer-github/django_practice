from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from student_management_app.models import Student, Course, Enrollment
from .serializers import StudentSerializer, CourseSerializer, \
    EnrollmentSerializer


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer


class GPAViewSet(viewsets.ModelViewSet):

    serializer_class = EnrollmentSerializer
    http_method_names = ['get']
    queryset = ''

    @action(detail=False, methods=['GET'], name='calculate')
    def calculate(self, request):

        grading_scheme = [
            {
                'upper_range': 100,
                'lower_range': 85,
                'grade_point': 4.00,
                'grade': 'A'
            },
            {
                'upper_range': 85,
                'lower_range': 80,
                'grade_point': 3.70,
                'grade': 'A-'
            },
            {
                'upper_range': 80,
                'lower_range': 75,
                'grade_point': 3.30,
                'grade': 'B+'
            },
            {
                'upper_range': 75,
                'lower_range': 70,
                'grade_point': 3.00,
                'grade': 'B'
            },
            {
                'upper_range': 70,
                'lower_range': 65,
                'grade_point': 2.70,
                'grade': 'B-'
            },
            {
                'upper_range': 65,
                'lower_range': 61,
                'grade_point': 2.30,
                'grade': 'C+'
            },
            {
                'upper_range': 61,
                'lower_range': 58,
                'grade_point': 2.00,
                'grade': 'C'
            },
            {
                'upper_range': 58,
                'lower_range': 55,
                'grade_point': 1.70,
                'grade': 'C-'
            },
            {
                'upper_range': 55,
                'lower_range': 50,
                'grade_point': 1.00,
                'grade': 'D'
            },
            {
                'upper_range': 50,
                'lower_range': 0,
                'grade_point': 0.00,
                'grade': 'F'
            }
        ]

        roll_no = request.query_params.get('roll_no')
        course_no = request.query_params.get('course_no')

        if not roll_no:
            return Response({'Response': 'Please provide parameters.'})

        if roll_no and course_no:
            try:
                enrollments = Enrollment.objects.get(
                    student__roll_no=roll_no, course__course_no=course_no)
            except Enrollment.DoesNotExist:
                _response = f'Record not found for {roll_no} & {course_no}'
                return Response({'Response': _response})

            if not enrollments:
                _response = f'{roll_no} is not enrolled in {course_no}'
                return Response({'Response': _response})

            for grade in grading_scheme:
                _upper_range = grade['upper_range']
                _lower_range = grade['lower_range']
                _marks = float(enrollments.marks)

                if _lower_range < _marks <= _upper_range:
                    _credit_hour = float(enrollments.course.credit_hours)
                    _grade_weightage = _credit_hour * grade['grade_point']
                    _gpa = round((_grade_weightage / _credit_hour), 1)

                    return Response({f'{roll_no}\'s GPA in {course_no}': _gpa})

        else:
            try:
                enrollments = Enrollment.objects.filter(
                    student__roll_no=roll_no)
            except Enrollment.DoesNotExist:
                _response = f'Record not found for {roll_no}'
                return Response({'Response': _response})

            if not enrollments:
                _response = f'Record not found for {roll_no}'
                return Response({'Response': _response})

            credit_hours = []
            grade_weightages = []

            for grade in grading_scheme:
                for enrollment in enrollments:
                    _upper_range = grade['upper_range']
                    _lower_range = grade['lower_range']
                    _marks = float(enrollment.marks)

                    if _lower_range < _marks <= _upper_range:
                        _credit_hour = float(enrollment.course.credit_hours)
                        _grade_weightage = _credit_hour * grade['grade_point']

                        grade_weightages.append(_grade_weightage)
                        credit_hours.append(_credit_hour)

            _gpa = round(sum(grade_weightages) / sum(credit_hours), 1)
            return Response({'GPA': _gpa})
