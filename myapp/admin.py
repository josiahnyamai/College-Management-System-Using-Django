from django.contrib import admin
from .models import Student, School, Course

#class StudentAdmin(admin.ModelAdmin):
#   list_display = ('registration_no', 'name', 'year', 'course', 'school')  # Show in admin panel
#   list_filter = ('school',)  # Add filtering by school
class StudentAdmin(admin.ModelAdmin):
    list_display = ('registration_no', 'name', 'year', 'school')
    search_fields = ('name', 'registration_no', 'school')

class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'school')
    search_fields = ('name', 'school__name')

class SchoolAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

admin.site.register(Student, StudentAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(School, SchoolAdmin)
