from datetime import date, datetime

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

TASK_PRIO = [
    ('low', 'low'),
    ('medium', 'medium'),
    ('high', 'high')
]

TASK_TYPE = [
    ('work', 'work'),
    ('payment', 'payment'),
    ('meeting', 'meeting')
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
    project_status = models.CharField(choices=PROJECT_STATUS, max_length=50, default=PROJECT_STATUS[0][0])

    def __str__(self):
        return self.project_name

class Task(models.Model):
    task_name = models.CharField(max_length=200)
    task_description = models.TextField(blank=True, null=True)
    task_notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deadline = models.DateField(null=True, blank=True)
    task_prio = models.CharField(choices=TASK_PRIO, max_length=50, default=TASK_PRIO[1][1])
    task_project = models.ForeignKey(Project, on_delete=models.CASCADE, blank=True)
    task_status = models.CharField(choices=TASK_STATUS, max_length=50, default=TASK_STATUS[0][0])
    task_type = models.CharField(choices=TASK_TYPE, max_length=50, default=TASK_STATUS[0][0])

    def __str__(self):
        return self.task_name

class Diary(models.Model):
    diary_user = models.ForeignKey(User, on_delete=models.CASCADE)
    diary_name = models.CharField(max_length=200)
    diary_description = models.TextField(blank=True)
    diary_motto = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.diary_name

class Payment_category(models.Model):
    payment_category_user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_category_name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.payment_category_name

class Payment_accounts(models.Model):
    payment_accounts_user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_accounts_name = models.CharField(max_length=200)
    payment_accounts_bank = models.CharField(max_length=200, default=None)
    payment_accounts_number = models.CharField(max_length=200, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Payment(models.Model):
    payment_user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_name = models.CharField(max_length=200)
    payment_description = models.TextField(blank=True)
    payment_cat = models.ForeignKey(Payment_category, on_delete=models.CASCADE)
    payment_account = models.ForeignKey(Payment_accounts, on_delete=models.CASCADE, default=None)
    payment_amount = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.payment_name

class Notes(models.Model):
    note_user = models.ForeignKey(User, on_delete=models.CASCADE)
    note_subject = models.CharField(max_length=200)
    note_description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Jira_projects(models.Model):
    jira_project_user = models.ForeignKey(User, on_delete=models.CASCADE)
    jira_project_server = models.CharField(max_length=200)
    jira_project_login = models.CharField(max_length=200)
    jira_project_api_key = models.CharField(max_length=200)

class LottoNumbers(models.Model):
    draw_date = models.CharField(max_length=20)
    draw_number = models.CharField(max_length=20)
    number_1 = models.CharField(max_length=2, default='0')
    number_2 = models.CharField(max_length=2, default='0')
    number_3 = models.CharField(max_length=2, default='0')
    number_4 = models.CharField(max_length=2, default='0')
    number_5 = models.CharField(max_length=2, default='0')
    number_6 = models.CharField(max_length=2, default='0')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Data: {}, numery: {}, {}, {}, {}, {}, {}".format(self.draw_date, self.number_1, self.number_2, self.number_3, self.number_4, self.number_5, self.number_6)