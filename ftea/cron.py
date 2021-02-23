import requests
from bs4 import BeautifulSoup
from django.core.mail import send_mail, BadHeaderError

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
        ilosc_banerow = 'Ilosc banerow widocznych na stronie to: {}'.format(ilosc_banerow)
        try:
            send_mail('FF - jest git', ilosc_banerow, 'lukasz.szlaszynski@4tea.pl', ['lukasz.szlaszynski@4tea.pl'])
        except:
            send_mail('FF - jest git - error', 'smth goes wrong', 'lukasz.szlaszynski@4tea.pl', ['lukasz.szlaszynski@4tea.pl'])