from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Student(models.Model):
    student_id = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    github_username = models.CharField(max_length=50, blank=True)
    enrollment_date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.student_id})"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

class Assignment(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    github_repo_template = models.CharField(max_length=200, blank=True)
    due_date = models.DateTimeField()
    max_points = models.IntegerField(default=100)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.title

class StudentProgress(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    github_repo_url = models.URLField(blank=True)
    submission_date = models.DateTimeField(null=True, blank=True)
    score = models.IntegerField(
        null=True, 
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    status = models.CharField(
        max_length=20,
        choices=[
            ('not_started', 'Not Started'),
            ('in_progress', 'In Progress'),
            ('submitted', 'Submitted'),
            ('graded', 'Graded'),
        ],
        default='not_started'
    )
    notes = models.TextField(blank=True)
    
    class Meta:
        unique_together = ['student', 'assignment']
    
    def __str__(self):
        return f"{self.student.full_name} - {self.assignment.title}"
