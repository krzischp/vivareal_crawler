from bs4 import BeautifulSoup
from requests import get
import pandas as pd
import itertools
import matplotlib.pyplot as plt
import seaborn as sns

from time import sleep
from random import randint
sns.set()
# pip freeze > requirements.txt

def clean_tag_text(content, feature=""):
    if feature == "price_by_month":
        return content.replace('\n', '').replace("/Mês", '').strip()
    return content.replace('\n', '').strip()


def append_html_cnt_to_list(html_cnt, l, feature=""):
    if html_cnt:
        l.append(clean_tag_text(html_cnt[0].text, feature=feature))
    else:
        l.append(None)


headers = ({'User-Agent':
            'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'})


# sapo = "https://casa.sapo.pt/Venda/Apartamentos/?sa=11&or=10"
domain_name = "https://www.vivareal.com.br"
# sapo = domain_name + "/aluguel/sp/sao-paulo/apartamento_residencial/?__vt=ctaw:h#onde=BR-Sao_Paulo-NULL-Sao_Paulo&tipos=apartamento_residencial"


# response = get(sapo, headers=headers)

# print(response.text[:1000])


# html_soup = BeautifulSoup(response.text, 'html.parser')
id_incr = 1
ids = []
locations = []
access_urls = []
sizes = []
cond_contents = []
prices_by_month = []
prices_condominio = []
whatsapps = []

n_pages = 0
n = 10

for page in range(0,100):
    n_pages += 1
    # page = 5
    viva_url = domain_name + "/aluguel/sp/sao-paulo/?__vt=ctaw:h&pagina=" + str(page) + "#onde=BR-Sao_Paulo-NULL-Sao_Paulo&tipos=apartamento_residencial"
    r = get(viva_url, headers=headers)
    page_html = BeautifulSoup(r.text, 'html.parser')
    house_containers = page_html.find_all('div', class_="property-card__main-content")
    i = 0
    while i < n and house_containers == []:
        r = get(viva_url, headers=headers)
        page_html = BeautifulSoup(r.text, 'html.parser')
        house_containers = page_html.find_all('div', class_="property-card__main-content")
        i += 1

    if house_containers != []:
        for container in house_containers:
            # location and acess link
            ## location
            ids.append(id_incr)
            id_incr += 1
            
            if container.find_all('h2', class_="property-card__header"):
                location_cnt = container.find_all('h2', class_="property-card__header")[0]
                append_html_cnt_to_list(location_cnt.find_all('span'), locations)
            else:
                location_cnt.append(None)
            ## flat page access link
            if container.find_all('a'):
                url = container.find_all('a')[0]
                full_url = domain_name + url.get('href')
                access_urls.append(full_url)
                # url = "https://www.vivareal.com.br/imovel/apartamento-1-quartos-campo-belo-zona-sul-sao-paulo-com-garagem-45m2-venda-RS342000-id-2480816073/"
                ## Get informations on the flat page
                r = get(full_url, headers=headers)
                flat_page_html = BeautifulSoup(r.text, 'html.parser')
                flat_page_container = flat_page_html.find_all('form', class_="new-lead-form__phone js-form-phone")[0]
                append_html_cnt_to_list(flat_page_container.find_all('a', class_="phone-contact__phone--primary"), whatsapps)

            else:
                access_urls.append(None)

            # size in m2
            
            if container.find_all('ul', class_="property-card__details"):
                size_cnt = container.find_all('ul', class_="property-card__details")[0]
                append_html_cnt_to_list(size_cnt.find_all('span'), sizes)
            else:
                sizes.append(None)


            # condominio content
            cond_cnt_list = []
            if container.find_all('ul', class_="property-card__amenities"):
                cond_cnt = container.find_all('ul', class_="property-card__amenities")[0]
                for content in cond_cnt.find_all('li'):
                    cond_cnt_list.append(clean_tag_text(content.text))

                cond_contents.append(cond_cnt_list)
            else:
                cond_contents.append([])


            # prices
            if container.find_all('section', class_="property-card__values"):
                price_cnt = container.find_all('section', class_="property-card__values")[0]
                append_html_cnt_to_list(price_cnt.find_all('div'), prices_by_month, feature="price_by_month")
            else:
                prices_by_month.append(None)

            if price_cnt.find_all('footer'):
                price_cond_cnt = price_cnt.find_all('footer')[0]
                append_html_cnt_to_list(price_cond_cnt.find_all('strong'), prices_condominio)
            else:
                prices_condominio.append(None)


    else:
        break

    sleep(randint(1,2))

print('You scraped {} pages containing {} properties.'.format(n_pages, len(access_urls)))


cols = ['ID', 'Location', 'URL', 'Size (m²)', 'Condominio Content', 'Price By Month', 'Price Condominio', 'Whatsapp Contact']

sao_paulo = pd.DataFrame({'ID': ids,
                           'Location': locations,
                           'URL': access_urls,
                           'Size (m²)': sizes,
                           'Condominio Content': cond_contents,
                           'Price By Month': prices_by_month,
                           'Price Condominio': prices_condominio,
                           'Whatsapp Contact': whatsapps})[cols]

sao_paulo.to_csv('sao_paulo_raw.csv', index=False)
# date ad posted

# short description

# gets all the links

# adding the domain part to the url and remove last letters

# why not get a thumbnail too? it seems to be somewhere between all theses caracs



### TODO
# cleaning process + exploration of the scrapped data
# https://towardsdatascience.com/i-was-looking-for-a-house-so-i-built-a-web-scraper-in-python-part-ii-eda-1effe7274c84


# create an interface for your web scrapper

# send whatsapp message
# https://youtu.be/98OewpG8-yw?t=52