from django.shortcuts import render, redirect, get_object_or_404
from .models import Student
from .forms import StudentForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegistrationForm
from django.contrib.auth.decorators import login_required

# Login view
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')  # Redirect to student dashboard
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

# Sign-Up View
def user_signup(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Do not commit to DB yet
            user.set_password(form.cleaned_data['password'])  # Hash the password
            user.save()  # Save the user with hashed password
            login(request, user)  # Log in the user immediately after registering
            return redirect('login')  # Redirect to the student list after sign-up
    else:
        form = UserRegistrationForm()
    return render(request, 'signup.html', {'form': form})

# Logout view
def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')


# View to list all student
@login_required
def student_list(request):
    students = Student.objects.all()
    return render(request, 'student_list.html', {'students' : students})

# View to add a new student
@login_required
def student_add(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('student_list')
        
    else:
        form = StudentForm()
    return render(request, 'student_add.html', {'form': form})

# View to edit a student
@login_required
def student_update(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('student_list')
        
    else:
        form = StudentForm(instance=student)
    return render(request, 'student_add.html', {'form': form})

# View to delete a student 
@login_required
def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student.delete()
        return redirect('student_list')
    return render(request, 'student_confirm_delete.html', {'student': student})


from .models import School, Course
from .forms import CourseForm

def course_management(request):
    schools = School.objects.all()
    return render(request, 'course_management.html', {'schools': schools})

def add_course(request, school_id):
    school = get_object_or_404(School, id=school_id)
    
    if request.method == "POST":
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.school = school  # Associate the course with the school
            course.save()
            return redirect('course_management')  # Redirect to the course list

    else:
        form = CourseForm()
    
    return render(request, 'add_course.html', {'form': form, 'school': school})


from .forms import StudentEnrollmentForm

def enroll_student(request, student_id=None):
    student = None
    if student_id:
        student = get_object_or_404(Student, id=student_id)
    else:
        student = Student()

    if request.method == 'POST':
        form = StudentEnrollmentForm(request.POST, instance=student)
        if form.is_valid():
            # Save the student and the selected courses
            student = form.save()
            # Assign the selected courses (if any) to the student
            student.courses.set(form.cleaned_data['courses'])  # Set the many-to-many field
            student.save()  # Save the changes to the student object
            return redirect('student_list')  # Redirect to the student list page
    else:
        form = StudentEnrollmentForm(instance=student)

    return render(request, 'enroll_student.html', {'form': form, 'student': student})

def course_detail(request, course_id):
    # Get the specific course using the course_id
    course = get_object_or_404(Course, id=course_id)
    
    # Get all students enrolled in the course
    students = course.students.all()  # Many-to-many relationship
    
    return render(request, 'course_detail.html', {
        'course': course,
        'students': students
    })


def course_list(request):
    courses = Course.objects.all()
    return render(request, 'course_list.html', {'courses': courses})

from django.shortcuts import render, get_object_or_404, redirect
from .models import Student, Course, Grade
from .forms import GradeForm

def grade_management(request):
    students = Student.objects.all()  # Get all students
    courses = Course.objects.all()  # Get all courses
    
    if request.method == "POST":
        form = GradeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('grade_management')  # Redirect after saving grade
    else:
        form = GradeForm()

    grades = Grade.objects.all()  # Display all grades

    return render(request, 'grade_management.html', {
        'students': students,
        'courses': courses,
        'form': form,
        'grades': grades,
    })