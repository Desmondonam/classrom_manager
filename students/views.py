from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Avg, Count
from .models import Student, Assignment, StudentProgress
from .forms import StudentForm, AssignmentForm, ProgressForm
from .utils import GitHubClassroomService
import csv
from django.http import HttpResponse

def dashboard(request):
    total_students = Student.objects.filter(is_active=True).count()
    total_assignments = Assignment.objects.filter(is_active=True).count()
    avg_score = StudentProgress.objects.filter(score__isnull=False).aggregate(Avg('score'))['score__avg']
    
    recent_students = Student.objects.filter(is_active=True).order_by('-enrollment_date')[:5]
    recent_assignments = Assignment.objects.filter(is_active=True).order_by('-created_at')[:5]
    
    context = {
        'total_students': total_students,
        'total_assignments': total_assignments,
        'avg_score': round(avg_score, 1) if avg_score else 0,
        'recent_students': recent_students,
        'recent_assignments': recent_assignments,
    }
    return render(request, 'students/dashboard.html', context)

def student_list(request):
    students = Student.objects.filter(is_active=True).order_by('last_name', 'first_name')
    return render(request, 'students/student_list.html', {'students': students})

def student_create(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student added successfully!')
            return redirect('student_list')
    else:
        form = StudentForm()
    return render(request, 'students/student_form.html', {'form': form, 'title': 'Add Student'})

def student_update(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student updated successfully!')
            return redirect('student_list')
    else:
        form = StudentForm(instance=student)
    return render(request, 'students/student_form.html', {'form': form, 'title': 'Update Student'})

def student_progress(request, pk):
    student = get_object_or_404(Student, pk=pk)
    progress = StudentProgress.objects.filter(student=student).select_related('assignment')
    return render(request, 'students/student_progress.html', {
        'student': student,
        'progress': progress
    })

def assignment_list(request):
    assignments = Assignment.objects.filter(is_active=True).order_by('-created_at')
    return render(request, 'students/assignment_list.html', {'assignments': assignments})

def assignment_create(request):
    if request.method == 'POST':
        form = AssignmentForm(request.POST)
        if form.is_valid():
            assignment = form.save()
            # Create progress entries for all active students
            students = Student.objects.filter(is_active=True)
            for student in students:
                StudentProgress.objects.create(student=student, assignment=assignment)
            messages.success(request, 'Assignment created successfully!')
            return redirect('assignment_list')
    else:
        form = AssignmentForm()
    return render(request, 'students/assignment_form.html', {'form': form, 'title': 'Create Assignment'})

def export_students_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="students.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Student ID', 'First Name', 'Last Name', 'Email', 'GitHub Username', 'Enrollment Date'])
    
    students = Student.objects.filter(is_active=True)
    for student in students:
        writer.writerow([
            student.student_id,
            student.first_name,
            student.last_name,
            student.email,
            student.github_username,
            student.enrollment_date
        ])
    
    return response