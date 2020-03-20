from django.contrib.auth.models import User
from django.db import models

PROJECT_STATUS = [
    ('new', 'new'),
    ('in progres', 'in progres'),
    ('done', 'done'),
    ('postponed', 'postponed')
]

TASK_STATUS = [
    ('to do', 'to do'),
    ('in progres', 'in progres'),
    ('done', 'done'),
    ('hold', 'hold')
]

class Translator(models.Model):
    translator_user = models.ForeignKey(User, on_delete=models.CASCADE)
    word_eng = models.CharField(max_length=200)
    word_pol = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        words = "Eng: {} - Pol: {}".format(self.word_eng, self.word_pol)
        return words

class Project(models.Model):
    project_user = models.ForeignKey(User, on_delete=models.CASCADE)
    project_name = models.CharField(max_length=50)
    project_description = models.TextField(blank=True, null=True)
    project_notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    project_status = models.CharField(choices=PROJECT_STATUS, max_length=50)

    def __str__(self):
        return self.project_name

class Tasks(models.Model):
    task_user = models.ForeignKey(User, on_delete=models.CASCADE)
    task_name = models.CharField(max_length=200)
    task_description = models.TextField(blank=True, null=True)
    task_notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deadline = models.DateField(null=True, blank=True)
    task_project = models.ForeignKey(Project, on_delete=models.CASCADE, blank=True)
    task_status = models.CharField(choices=TASK_STATUS, max_length=50)

    def __str__(self):
        return self.task_name

class Diary(models.Model):
    diary_user = models.ForeignKey(User, on_delete=models.CASCADE)
    diary_name = models.CharField(max_length=200)
    diary_description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.diary_name

