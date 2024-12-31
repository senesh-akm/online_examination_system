from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('student', 'Student'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
    groups = models.ManyToManyField(
        Group,
        related_name="custom_user_groups",
        blank=True,
        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
        verbose_name="groups",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="custom_user_permissions",
        blank=True,
        help_text="Specific permissions for this user.",
        verbose_name="user permissions",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Exam(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    duration = models.IntegerField(help_text="Duration in minutes")
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Question(models.Model):
    QUESTION_TYPES = (
        ('MCQ', 'Multiple Choice'),
        ('SA', 'Short Answer'),
    )
    exam = models.ForeignKey(Exam, related_name='questions', on_delete=models.CASCADE)
    type = models.CharField(max_length=3, choices=QUESTION_TYPES)
    question_text = models.TextField()
    options = models.JSONField(blank=True, null=True, help_text="Applicable for MCQs")
    correct_answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class QuestionBank(models.Model):
    topic = models.CharField(max_length=255)
    type = models.CharField(max_length=3, choices=Question.QUESTION_TYPES)
    question_text = models.TextField()
    options = models.JSONField(blank=True, null=True)
    correct_answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class StudentExam(models.Model):
    exam = models.ForeignKey(Exam, related_name='student_exams', on_delete=models.CASCADE)
    student = models.ForeignKey(User, related_name='exams', on_delete=models.CASCADE)
    score = models.FloatField(blank=True, null=True)
    submitted = models.BooleanField(default=False)
    submitted_at = models.DateTimeField(blank=True, null=True)


class Result(models.Model):
    exam = models.ForeignKey(Exam, related_name='results', on_delete=models.CASCADE)
    student = models.ForeignKey(User, related_name='results', on_delete=models.CASCADE)
    score = models.FloatField()
    feedback = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)