from django.contrib import admin
from ftea.models import Tasks, Diary, Project, Translator


# Register your models here.
admin.site.register(Tasks)
admin.site.register(Diary)
admin.site.register(Project)
admin.site.register(Translator)

