from django.contrib import admin
from .models import Student, Assignment, StudentProgress

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['student_id', 'first_name', 'last_name', 'email', 'github_username', 'is_active']
    list_filter = ['is_active', 'enrollment_date']
    search_fields = ['student_id', 'first_name', 'last_name', 'email']

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ['title', 'due_date', 'max_points', 'is_active']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title', 'description']

@admin.register(StudentProgress)
class StudentProgressAdmin(admin.ModelAdmin):
    list_display = ['student', 'assignment', 'status', 'score', 'submission_date']
    list_filter = ['status', 'assignment']
    search_fields = ['student__first_name', 'student__last_name', 'assignment__title']