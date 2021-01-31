import json

import django
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView
from datetime import datetime, timedelta, date
from ftea.forms import TranslateForm
from googletrans import Translator as GoogleTrans
from ftea import models, forms
from django.db.models import Q
from django.core.mail import send_mail, BadHeaderError
import pytesseract
from PIL import Image
import os
from jira import JIRA
from ftea import jira_connect, jira_filters
from django.contrib.auth.models import User
import xlwt


# Create your views here.
class Index(View):
    def get(self, request):
        if request.is_ajax():
            pass
        else:
            form = forms.ContactForm
            ctx = {"form": form}
        return render(request, 'ftea/index.html', ctx)

    def post(self, request):
        form = forms.ContactForm(request.POST)
        if form.is_valid():
            name = request.POST.get('name')
            email = request.POST.get('email')
            message = request.POST.get('message')
            email = "Kontakt od: {}, email: {}, wiadomosc: {}".format(name, email, message)
            try:
                send_mail('Kontakt z 4tea.pl', email, 'lukasz.szlaszynski@4tea.pl', ['lukasz.szlaszynski@4tea.pl'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            mess = "Mess sent"
        return render(request, 'ftea/index.html')

class Translator(View):
    def get(self, request):
        translator = GoogleTrans()
        if request.is_ajax():
            if request.GET.get('request_type') == "translator":
                lang_in = ''
                lang_out = ''
                if request.GET.get('lang') == "eng":
                    lang_in = 'en'
                    lang_out = 'pl'
                elif request.GET.get('lang') == "pol":
                    lang_in = 'pl'
                    lang_out = 'en'
                word = translator.translate(request.GET.get('word'), dest=lang_out, src=lang_in)
                print('word')
                ctx = {'word': word.text,
                       'lang': lang_out}
                return HttpResponse(json.dumps(ctx))
            elif request.GET.get('request_type') == "delete_record":
                id_to_delete = request.GET.get("id")
                delete_word = models.Translator.objects.get(id=id_to_delete)
                delete_word.delete()
                ctx = {'status': 200}
                return HttpResponse(json.dumps(ctx))
            elif request.GET.get('request_type') == "add_to_db":
                eng_word = request.GET.get('word_eng')
                pol_word = request.GET.get('word_pol')
                check_if_exist = models.Translator.objects.filter(translator_user=request.user,
                                                                  word_eng=eng_word,
                                                                  word_pol=pol_word).exists()
                if check_if_exist:
                    ctx = {"new_id": "already_exist"}
                else:
                    new_word = models.Translator(translator_user=request.user,
                                                 word_eng=eng_word,
                                                 word_pol=pol_word)
                    new_word.save()
                    new_id = new_word.pk
                    ctx = {"en": eng_word,
                           "pl": pol_word,
                           "new_id": new_id}
                return HttpResponse(json.dumps(ctx))
        else:
            if request.user.is_authenticated:
                all_words = models.Translator.objects.filter(translator_user=request.user)
            else:
                all_words = {}
            ctx = {'all_words': all_words}
            return render(request, 'ftea/translator.html', ctx)

    def post(self, request):
        if request.POST.get('Word_eng') and request.POST.get('Word_pol'):
            pol_word = request.POST.get('Word_pol')
            eng_word = request.POST.get('Word_eng')
            new_word = models.Translator(translator_user=request.user,
                                         word_eng=eng_word,
                                         word_pol=pol_word)
            new_word.save()
        else:
            pass
        all_words = models.Translator.objects.order_by('pk')
        ctx = {'all_words': all_words}
        return render(request, 'ftea/translator.html', ctx)

class Welcome(LoginRequiredMixin, View):
    add_task_form = forms.AddTask
    status_form = forms.ChangeTaskStatus
    template = 'ftea/welcome.html'

    def get(self, request):
        todays_date = date.today()
        next_seven_days = todays_date + timedelta(days=7)
        next_30_days = todays_date + timedelta(days=30)
        last_twenty_days = todays_date - timedelta(days=20)
        first_date = todays_date - timedelta(days=99999)
        yesterday = todays_date - timedelta(days=1)
        #all projects
        projects = models.Project.objects.filter(project_user=request.user)
        #expired Task
        expired_tasks = models.Task.objects.filter(deadline__range=(first_date, yesterday)).filter(
            task_project__project_user=request.user).exclude(task_status='done').exclude(task_status='hold').order_by("deadline")
        #open Task
        open_tasks = models.Task.objects.filter(deadline__range=(todays_date, next_seven_days)).filter(
            task_project__project_user=request.user).exclude(task_status='done').exclude(task_status='hold').order_by("deadline")
        closed_tasks_last_twenty_days = models.Task.objects.filter(deadline__range=(last_twenty_days, todays_date)).filter(
            task_project__project_user=request.user).exclude(task_status='to do').exclude(task_status='in progres').order_by("-updated_at")
        ctx = {
            "projects": projects,
            "expired_tasks": expired_tasks,
            "open_tasks": open_tasks,
            "form": self.add_task_form,
            "status_form": self.status_form,
            "closed_tasks_last_twenty_days": closed_tasks_last_twenty_days
        }
        return render(request, self.template, ctx)

    def post(self, request):
        add_task_form = self.add_task_form(request.POST)
        status_form = self.status_form(request.POST)
        if add_task_form.is_valid():
            p = add_task_form.save()
            return redirect("ftea:welcome")
        if request.POST.get('task_id'):
            task_id = request.POST.get('task_id')
            new_task_status = request.POST.get('task_status')
            task_to_update = models.Task.objects.get(id=task_id)
            task_to_update.task_status = new_task_status
            task_to_update.save()
            return redirect("ftea:welcome")
        return HttpResponse('co poszło nie tak')



class Project_View(LoginRequiredMixin, View):
    def get(self, request, id):
        project = models.Project.objects.filter(id=id)
        ctx = {'project': project}
        return render(request, 'ftea/project.html', ctx)

#addproject/
class ProjectCreate(LoginRequiredMixin, CreateView):
    model = models.Project
    fields = ['project_name','project_description', 'project_status']
    success_url = reverse_lazy("ftea:welcome")

    def form_valid(self, form):
        form.instance.project_user = self.request.user
        return super().form_valid(form)

class Task_View(LoginRequiredMixin, View):
    def get(self, request, id):
        task = models.Task.objects.filter(id=id)
        form_class = forms.TaskForm_change_status
        ctx = {'task': task,
               'form_class': form_class}
        return render(request, 'ftea/task.html', ctx)

    def post(self, request, id):
        #if request.POST.get('Word_eng')
        print(request.POST.get('task_status'))
        change_task_status = models.Task.objects.filter(id=id)
        change_task_status(task_status=request.POST.get('task_status')).save()
        print(change_task_status)
        return HttpResponse("działa")

class TaskCreate(CreateView):
    form_class = forms.TaskForm
    template_name = 'ftea/tasks_form.html'
    success_url = reverse_lazy("ftea:welcome")

    def get_form_kwargs(self):
        kwargs = super(TaskCreate, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.project_user = self.request.user
        return super().form_valid(form)

#dziennik
#wpis tworzenie
class DiaryCreate(CreateView):
    form_class = forms.DiaryForm
    template_name = 'ftea/diary_form.html'
    success_url = reverse_lazy("ftea:welcome")

    def form_valid(self, form):
        form.instance.diary_user = self.request.user
        return super().form_valid(form)

#lista wpisów
class DiaryList(LoginRequiredMixin, View):
    add_diary_form = forms.AddDiary

    def get(self, request):
        diary_list = models.Diary.objects.filter(
            diary_user=request.user)
        ctx = {
            "diary_list": diary_list,
            "form": self.add_diary_form,
        }
        return render(request, 'ftea/diary.html', ctx)


    def post(self, request):
        new_diary = models.Diary(diary_name=request.POST['diary_name'],
                                 diary_description=request.POST['diary_description'],
                                 diary_motto=request.POST['diary_motto'],
                                 diary_user=request.user)
        new_diary.save()
        return redirect("ftea:diary")


class OcrTest(View):
    def get(self, request):
        ctx = {}
        print(os.getcwd())
        img =Image.open('/Users/lukaszszlaszynski/Repos/ftea/ftea/static/ftea/img1/fak4.png')
        text = pytesseract.image_to_string(img)
        print(text)
        return render(request, 'ftea/ocr.html', ctx)

class FF(LoginRequiredMixin, View):
    def get(self, request):
        connection_data = models.Jira_projects.objects.filter(jira_project_user=request.user)
        connection_data_set = [connection_data[0].jira_project_server, connection_data[0].jira_project_login, connection_data[0].jira_project_api_key]
        connector = jira_connect.Jira_connector(connection_data_set[0], connection_data_set[1], connection_data_set[2])
        jira_connection = connector.connect()
        i = jira_connection.search_issues('issuetype in (Bug, Story, Task, Sub-task) order by created DESC', maxResults=None)
        ctx = {
            'issues': i
        }
        return render(request, 'ftea/ff.html', ctx)

class Top_Praca(View):
    def get(self, request):
        if request.user.groups.filter(name__in=['TP']).exists():
            connector_obj = jira_connect.Jira_connector()
            connect = connector_obj.connect(connector_obj.get_connection_data(request))
            filter = connect.search_issues(jira_filters.kadlubowski["all_tasks_tasks"],
                                              maxResults=None)
            all_tasks = connect.search_issues('', maxResults=None)
            all_done = connect.search_issues('issuetype in standardIssueTypes() AND status in (Done) order by created DESC',
                                              maxResults=None)

            projects = connect.projects()
            ctx = {
                'buttons': jira_filters.kadlubowski,
                'project': projects[1],
                'issues': filter,
                'issues_count': len(filter),
                'all_tasks_count': len(all_tasks),
                'all_done': len(all_done),
                'user': request.user
            }
            return render(request, 'ftea/top-praca.html', ctx)
        else:
            return HttpResponse('404')

    def post(self, request):
        filter_value = request.POST['filter']
        connector_obj = jira_connect.Jira_connector()
        connect = connector_obj.connect(connector_obj.get_connection_data(request))
        filter = connect.search_issues(jira_filters.kadlubowski[filter_value],
                                       maxResults=30)
        all_tasks = connect.search_issues('', maxResults=None)
        all_done = connect.search_issues('issuetype in standardIssueTypes() AND status in (Done) order by created DESC',
                                         maxResults=None)
        projects = connect.projects()
        ctx = {
            'buttons': jira_filters.kadlubowski,
            'project': projects[1],
            'issues': filter,
            'issues_count': len(filter),
            'all_tasks_count': len(all_tasks),
            'all_done': len(all_done),
            'user': request.user
        }
        return render(request, 'ftea/top-praca.html', ctx)

class FF(View):
    def get(self, request):
        if request.user.groups.filter(name__in=['FF']).exists():
            connector_obj = jira_connect.Jira_connector()
            connect = connector_obj.connect(connector_obj.get_connection_data(request))
            filter = connect.search_issues(jira_filters.ff["all_tasks_tasks"],
                                              maxResults=30)
            all_tasks = connect.search_issues('', maxResults=None)
            all_done = jira_filters.ff['all_tasks_done']
            projects = connect.projects()
            ctx = {
                'buttons': jira_filters.ff,
                'project': projects[0],
                'issues': filter,
                'issues_count': len(filter),
                'all_tasks_count': len(all_tasks),
                'all_done': len(all_done),
                'user': request.user
            }
            return render(request, 'ftea/ff.html', ctx)
        else:
            return HttpResponse('404')

    def post(self, request):
        filter_value = request.POST['filter']
        connector_obj = jira_connect.Jira_connector()
        connect = connector_obj.connect(connector_obj.get_connection_data(request))
        filter = connect.search_issues(jira_filters.ff[filter_value],
                                       maxResults=30)
        all_tasks = connect.search_issues('', maxResults=None)
        all_done = jira_filters.ff['all_tasks_done']
        projects = connect.projects()
        ctx = {
            'buttons': jira_filters.ff,
            'project': projects[0],
            'issues': filter,
            'issues_count': len(filter),
            'all_tasks_count': len(all_tasks),
            'all_done': len(all_done),
            'user': request.user
        }
        return render(request, 'ftea/ff.html', ctx)
