from django.db import models

class Student(models.Model):
    SCHOOL_CHOICES = [
        ('Education', 'School of Education'),
        ('Law', 'School of Law'),
        ('Business', 'School of Business'),
        ('Engineering', 'School of Engineering'),
        ('Medicine', 'School of Medicine'),
        ('IT', 'School of IT & Computer Science'),
    ]

    registration_no = models.CharField(max_length=200, unique=True)
    name = models.CharField(max_length=250)
    year = models.IntegerField()
    courses = models.ManyToManyField('Course', related_name='students')  # Many-to-many relationship with Course
    school = models.CharField(max_length=50, choices=SCHOOL_CHOICES, default='Education')

    def __str__(self):
        return f"{self.registration_no} - {self.name} ({self.get_school_display()})"


class School(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Course(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name="courses")
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.school.name})"

class Grade(models.Model):
    GRADE_CHOICES = [
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
    ]
    
    student = models.ForeignKey('Student', on_delete=models.CASCADE, related_name="grades")
    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name="grades")
    grade = models.CharField(max_length=1, choices=GRADE_CHOICES)
    
    def __str__(self):
        return f"{self.student.name} - {self.course.name}: {self.grade}"



