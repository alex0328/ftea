from django.conf.urls import url
from django.urls import path, re_path
from ftea import views


app_name = 'ftea'
urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('welcome/', views.Welcome.as_view(), name='welcome'),
    path('project/<int:id>', views.Project_View.as_view(), name='project'),
    path('addproject/', views.ProjectCreate.as_view(), name='add_project'),
    path('task/<int:id>', views.Task_View.as_view(), name='task'),
    path('addtask/', views.TaskCreate.as_view(), name='add_task'),
    path('adddiary/', views.DiaryCreate.as_view(), name='add_diary'),
    path('diary/', views.DiaryList.as_view(), name='diary'),
    path('translator/', views.Translator.as_view(), name='translator'),
    path('ocr/', views.OcrTest.as_view(), name='ocr'),
    path('top-praca/', views.Top_Praca.as_view(), name='top-praca'),
    path('ff/', views.FF.as_view(), name='ff'),
    path('ff-ajax/', views.FF_ajax.as_view(), name='ff-ajax'),
    path('ff-banners/', views.FF_banners.as_view(), name='ff-banners'),
    path('lotko/', views.Lotko.as_view(), name='lotko'),
    ]