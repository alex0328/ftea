from django.contrib import admin
from ftea.models import Task, Diary, Project, Translator, Payment_category, Payment, Payment_accounts


# Register your models here.
admin.site.register(Task)
admin.site.register(Diary)
admin.site.register(Payment_category)
admin.site.register(Payment_accounts)
admin.site.register(Payment)
admin.site.register(Project)
admin.site.register(Translator)


