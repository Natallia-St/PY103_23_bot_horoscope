import requests
import bs4


total_horo_list =[]
# Создание функции
def parsing_av_site(link_):
    # Создание списков для каждого вида спаршенной информации

    # Скачиваем страницу по ссылке
    url_ = link_
    r = requests.get(url_)
    print(r.status_code)
    # Из скаченной HTML страницы делаем суп для дальнейшего получения нужной информации
    soup = bs4.BeautifulSoup(r.text, 'html.parser')
    total_horo_teg = soup.find_all(class_="article__item article__item_alignment_left article__item_html")
    for all_info in total_horo_teg:
        total_horo = all_info.text
        total_horo_1 = total_horo.replace("\n", " ")
        total_horo_list.append(total_horo_1)
    print(total_horo_list)

parsing_av_site("https://horo.mail.ru/")
















# from bs4 import BeautifulSoup
# import asyncio
# import aiohttp

# pars_list = []
#
#
# async def fetch(session, url):
#     async with session.get(url) as response:
#         return await response.text()
#
#
# async def parser(html):
#     soup = BeautifulSoup(html, 'lxml')
#
#     links_ = soup.find_all('a', class_='listing-item__link')
#     link_list = [('https://cars.av.by' + link.get('href')) for link in links_]
#
#     bs_prices_byn = soup.find_all('div', class_='listing-item__price')
#     price_byn_list = [price_byn.text for price_byn in bs_prices_byn]
#
#     bs_prices_usd = soup.find_all('div', class_='listing-item__priceusd')
#     price_usd_list = [price_usd.text.replace("≈", "").replace(" ", "").replace("$", "") for price_usd in bs_prices_usd]
#
#     options_ = soup.find_all('div', class_='listing-item__params')
#     options_list = [param.text for param in options_]
#
#     pars_list.append([{'Ссылка': link_list[num],
#                        'Цена в BYN': price_byn_list[num],
#                        'Характеристики': options_list[num],
#                        'Цена в USD': price_usd_list[num]
#                        } for num in range(0, len(price_usd_list))])
#     print(pars_list)
#
#
# async def download(url):
#     async with aiohttp.ClientSession() as session:
#         html = await fetch(session, url)
#         await parser(html)
#
#
# urls = [f'https://cars.av.by/filter?brands[0][brand]=545&brands[0][model]=1980&brands[0][generation]=3808&brands[1]' \
#         f'[brand]=545&brands[1][model]=1980&brands[1][generation]=3809&page={i}' for i in range(1, 3)]
#
# loop = asyncio.get_event_loop()
# tasks = [asyncio.ensure_future(download(url)) for url in urls]
# tasks = asyncio.gather(*tasks)
# loop.run_until_complete(tasks)
#
#
# # https://horo.mail.ru/prediction/pisces/today/
#
