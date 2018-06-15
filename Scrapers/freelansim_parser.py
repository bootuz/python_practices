from bs4 import BeautifulSoup
from urllib.request import urlopen, Request


URL = 'https://freelansim.ru/'

file_name = "freelansim_data.csv"
f = open(file_name, 'w')
headers = "title; link; responses; views; cost; suffix; tags\n"
f.write(headers)


def create_bs(link):
    req = Request(link, headers={'User-Agent': 'Mozilla/5.0'})
    html = urlopen(req)
    bs_obj = BeautifulSoup(html, 'html.parser')
    return bs_obj


pag_soup = create_bs(URL)
pag = pag_soup.find('div', {'class': 'pagination'})
last_page = int(pag.findAll('a')[-2].text)

for i in range(1, last_page + 1):

    pag_url = 'https://freelansim.ru/tasks?page={}'.format(i)
    soup = create_bs(pag_url)

    articles = soup.findAll('article', {'class': 'task task_list'})

    for article in articles:
        task_title = article.find('div', {'class': 'task__title'})

        title = task_title.get('title')

        link = URL + task_title.a.get('href')

        task_responses = article.find('span', {'class': 'params__responses icon_task_responses'})
        if task_responses is None:
            response = 0
        else:
            response = int(task_responses.text.split()[0])
        views = int(article.find('span', {'class': 'params__views icon_task_views'}).text.split()[0])

        task_cost = article.find('span', {'class': 'count'})

        if task_cost is None:
            cost = 'Договорная'
            suffix = None
        else:
            cost = task_cost.text.replace(" ", "")
            cost = [s for s in cost if s.isdigit()]
            cost = int(''.join(cost))
            suffix = task_cost.text.split('руб.')[-1].strip()

        task_tags = article.find('div', {'class': 'task__tags'})
        tags = task_tags.findAll('a')
        tag_list = []
        for tag in tags:
            tag_list.append(tag.text)
        tag_str = ','.join(tag_list)

        f.write(title + ";" + link + ";" + str(response) + ";" + str(views) + ";" + str(cost) + ";" + str(suffix) + ";" + tag_str + "\n")
    print('page parsed', i)
