from django.urls import path, re_path
from ftea import views


app_name = 'ftea'
urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('welcome/', views.Welcome.as_view(), name='welcome'),
    path('translator/', views.Translator1.as_view(), name='translator'),
    ]