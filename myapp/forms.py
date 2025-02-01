from django import forms
from .models import Student, Course, Grade
from django.contrib.auth.models import User

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['registration_no', 'name', 'year', 'courses', 'school']
        widgets = {
            'school': forms.Select(choices=Student.SCHOOL_CHOICES)
        }


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm password")

    class Meta:
        model = User
        fields = ['username', 'password', 'password2']

    # Check that the passwords match
    def clean_password2(self):
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2        
    

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['school', 'name']


class StudentEnrollmentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'registration_no', 'year', 'courses', 'school', 'courses']  # Include 'courses' for many-to-many field

    courses = forms.ModelMultipleChoiceField(
        queryset=Course.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )


class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ['student', 'course', 'grade']

    # You can limit the dropdown to show only courses that the student is enrolled in
    def __init__(self, *args, **kwargs):
        super(GradeForm, self).__init__(*args, **kwargs)
        if 'student' in self.data:
            student_id = self.data.get('student')
            self.fields['course'].queryset = Course.objects.filter(students__id=student_id)

