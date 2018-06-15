#!/usr/bin/python3

from bs4 import BeautifulSoup
from urllib.request import urlopen, Request


file_name = "data.csv"

f = open(file_name, 'w')

headers = "Название; Ссылка; Категория; Кол-во комментариев; Дата; Картинка\n"

f.write(headers)

for i in range(1, 230):
    url = 'https://aheku.net/?page={}'.format(i)

    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    html = urlopen(req)
    soup = BeautifulSoup(html, 'html.parser')
    articles = soup.find_all('article', {'class': 'card'})

    for article in articles:
        title = article.h4.text

        article_link = article.findAll('h4', {'class': 'caption'})
        link = 'https://aheku.net/' + article_link[0].find('a').get('href')

        article_cat = article.findAll('a')
        if article_cat[1].get('href') == 'news/':
            category = "Новости"
        elif article_cat[1].get('href') == 'events/':
            category = "События"
        elif article_cat[1].get('href') == 'galereya/':
            category = "Галерея"

        article_comments = article.findAll('span', {'class': 'icon icon-comment-1 pull-right'})
        comments = article_comments[0].text.strip()

        article_date = article.findAll('time', {'class': 'pull-left'})
        if len(article_date) == 1:
            date = article_date[0].get('datetime')
        else:
            date = 'nan'

        article_img = article.findAll('img')
        image = "https://aheku.net/" + article_img[0].get('data-original')

        f.write(title + ";" + link + ";" + category + ";" + comments + ";" + date + ";" + image + "\n")

    print('page {} parsed'.format(i))


f.close()