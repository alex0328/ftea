import json

from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from ftea.forms import TranslateForm
from googletrans import Translator as GoogleTrans
from ftea import models
from django.db.models import Q



# Create your views here.
class Index(View):
    def get(self, request):
        return render(request, 'ftea/index.html')

class Welcome(View):
    def get(self, request):
        return render(request, 'ftea/welcome.html')

class Translator(View):
    def get(self, request):
        if request.is_ajax():
            return HttpResponse(json.dumps(ctx))
        else:
            all_words = models.Translator.objects.all()
            ctx = {'all_words': all_words}
            return render(request, 'ftea/translator.html', ctx)

    def post(self, request):
        pol_word = 'pol'
        eng_word = 'eng'
        all_words = 'all'
        print(request.POST)
        if 'check_meaning' in request.POST:
            translator = GoogleTrans()
            if request.POST.get('Word_eng') and request.POST.get('Word_pol'):
                print("oba")
                models.Translator.objects.all()
                all_words = models.Translator.objects.all()
                ctx = {"all_words": all_words}
                if request.is_ajax():
                    print(request.POST)
                    print('ajax pierwszejszy')
                    return HttpResponse(json.dumps(ctx))
                else:
                    print(request.POST)
                    print('nie ajax')
                    return render(request, 'ftea/translator.html', ctx)
            elif request.POST.get('Word_pol'):
                print("pol")
                post_content = request.POST['Word_pol']
                word = translator.translate(post_content, dest='en', src='pl')
                pol_word = request.POST.get('Word_pol')
                eng_word = word.text
            elif request.POST.get('Word_eng'):
                print("eng_word")
                post_content = request.POST['Word_eng']
                word = translator.translate(post_content, dest='pl', src='en')
                eng_word = request.POST.get('Word_eng')
                pol_word = word.text
            else:
                print("żodyn")
                if request.is_ajax():
                    print(request.POST)
                    print('ajax pierwszy')
                    print(HttpResponse("nic"))
                    return HttpResponse("nic")
                else:
                    all_words = models.Translator.objects.all()
                    ctx = {"all_words": all_words}
                    print(request.POST)
                    print('nie ajax')
                    return render(request, 'ftea/translator.html', ctx)
        elif 'add_to_db' in request.POST:
            if request.POST.get('Word_eng') and request.POST.get('Word_pol'):
                print(request.user)
                pol_word = request.POST.get('Word_pol')
                eng_word = request.POST.get('Word_eng')
                check_word = models.Translator.objects.filter(Q(translator_user=request.user) & Q(word_eng=eng_word) & Q(word_pol=pol_word))
                if check_word:
                    print("już jest")
                else:
                    new_word = models.Translator(translator_user=request.user,
                                                 word_eng=eng_word,
                                                 word_pol=pol_word)
                    new_word.save()
                all_words = models.Translator.objects.all()
                ctx = {"all_words": all_words}
                if request.is_ajax():
                    print(request.POST)
                    print('ajax przedostatni')
                    print(HttpResponse(json.dumps(ctx)))
                    return HttpResponse(json.dumps(ctx))
                else:
                    print(request.POST)
                    print('nie ajax')
                    return render(request, 'ftea/translator.html', ctx)
            all_words = models.Translator.objects.all()
        ctx = {"pol_word": pol_word,
               "eng_word": eng_word,
               "all_words": all_words,
               }
        if request.is_ajax():
            print(request.POST)
            print('ajax ostatni')
            print(HttpResponse(json.dumps(ctx)))
            return HttpResponse(json.dumps(ctx))
        else:
            print(request.POST)
            print('nie ajax')
            return render(request, 'ftea/translator.html', ctx)


class Translator1(View):
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
                ctx = {'word': word.text,
                       'lang': lang_out}
                return HttpResponse(json.dumps(ctx))
            elif request.GET.get('request_type') == "delete_record":
                print(request.GET)
                id_to_delete = request.GET.get("id")
                print(id_to_delete)
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
            all_words = models.Translator.objects.order_by('word_eng')
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