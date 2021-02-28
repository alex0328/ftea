import requests
from bs4 import BeautifulSoup
from django.core.mail import send_mail, BadHeaderError
from .models import LottoNumbers

def my_scheduled_job():
    url = 'https://fabrykaform.pl'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    banery = soup.select('#homepage-banners>div')

    print('______________________________')
    ilosc_banerow = 1
    for idx, i in enumerate(banery):
        ilosc_banerow = idx + 1
    if ilosc_banerow != 7:
        ilosc_banerow = 'Ilosc banerow widocznych na stronie to: {}'.format(ilosc_banerow)
        try:
            send_mail('FF - cos grubo nie tak', ilosc_banerow, 'lukasz.szlaszynski@4tea.pl', ['lukasz.szlaszynski@4tea.pl'])
        except:
            send_mail('FF - cos grubo nie tak', 'smth goes wrong', 'lukasz.szlaszynski@4tea.pl', ['lukasz.szlaszynski@4tea.pl'])
    else:
        pass

def get_lotto_numbers():
    url = 'http://serwis.mobilotto.pl/mapi_v6/index.php?json=getLotto'
    wyniki = requests.get(url)
    na_strone = wyniki.json()
    numerki_to_sort = na_strone['numerki'].split(',')
    numerki = sorted(numerki_to_sort)
    data_losowania = na_strone['data_losowania']
    numer_losowania = na_strone['num_losowania']
    check_if_exist = LottoNumbers.objects.filter(draw_number=numer_losowania).exists()
    if not check_if_exist:
        lotko_to_db = LottoNumbers(draw_date=data_losowania,
                                  draw_number=numer_losowania,
                                  number_1=numerki[0],
                                  number_2=numerki[1],
                                  number_3=numerki[2],
                                  number_4=numerki[3],
                                  number_5=numerki[4],
                                  number_6=numerki[5],
                                  )
        lotko_to_db.save()
        try:
            wyniki_lotto = """
            Wyniki lotto z dnia: {}
            Numer losowania: {}
            Numery: {}, {}, {}, {}, {}, {}
            """.format(data_losowania, numer_losowania, numerki[0], numerki[1], numerki[2], numerki[3], numerki[4], numerki[5])
            send_mail('Wyniki Lotto', wyniki_lotto, 'lukasz.szlaszynski@4tea.pl', ['lukasz.szlaszynski@4tea.pl'])
        except:
            send_mail('Lotko - cos grubo nie tak', 'smth goes wrong', 'lukasz.szlaszynski@4tea.pl', ['lukasz.szlaszynski@4tea.pl'])