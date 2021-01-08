from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from ftea import models
# from bootstrap_datepicker_plus import DatePickerInput


class TranslateForm(forms.Form):
    Word_pol = forms.CharField(max_length=500, required=False)
    Word_eng = forms.CharField(max_length=500, required=False)

class ContactForm(forms.Form):
    name = forms.CharField(max_length=500, required=True)
    email = forms.EmailField(max_length=500, required=True)
    message = forms.CharField(max_length=900, required=True)

class TaskForm(forms.ModelForm):
    class Meta:
       model = models.Task
       fields = ('task_name','task_description', 'task_status', 'task_project', 'deadline', 'task_prio',)
       # widgets = {
       #     # 'deadline': DatePickerInput(),  # default date-format %m/%d/%Y will be used
       #     'deadline': DatePickerInput(format='%Y-%m-%d'),  # specify date-frmat
       # }
       deadline = forms.DateField(
           widget=forms.DateInput(
               attrs={
                   'type': 'date',
               }
           )
       )

    def __init__(self, *args, **kwargs):
       user = kwargs.pop('user')
       super(TaskForm, self).__init__(*args, **kwargs)
       self.fields['task_project'].queryset = models.Project.objects.filter(project_user=user)

class DiaryForm(forms.ModelForm):
    class Meta:
       model = models.Diary
       fields = ('diary_name', 'diary_description', 'diary_motto',)

class TaskForm_change_status(forms.ModelForm):
    class Meta:
       model = models.Task
       fields = ('task_status',)

class AddTask(forms.ModelForm):
    class Meta:
       model = models.Task
       fields = ('task_name', 'task_description', 'task_notes', 'deadline', 'task_prio', 'task_project','task_status', 'task_type',)
       # widgets = {
       #     # 'deadline': DatePickerInput(),  # default date-format %m/%d/%Y will be used
       #     'deadline': DatePickerInput(format='%Y-%m-%d'),  # specify date-frmat
       # }

class AddDiary(forms.ModelForm):
    class Meta:
       model = models.Diary
       fields = ('diary_name', 'diary_description', 'diary_motto',)


class ChangeTaskStatus(forms.ModelForm):
    class Meta:
        model = models.Task
        fields = ('task_status', 'id',)
