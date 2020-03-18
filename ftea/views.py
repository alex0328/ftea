import json
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from ftea.forms import TranslateForm
from googletrans import Translator as GoogleTrans
from ftea import models, forms
from django.db.models import Q
from django.core.mail import send_mail, BadHeaderError



# Create your views here.
class Index(View):
    def get(self, request):
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

class Welcome(View):
    def get(self, request):
        return render(request, 'ftea/welcome.html')

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
            all_words = models.Translator.objects.filter(translator_user=request.user)
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