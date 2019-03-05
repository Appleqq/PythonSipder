import requests
import re
from bs4 import BeautifulSoup

def get_one_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6)\
         AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return  response.text
    else:
        return None


if __name__ == '__main__':
    url = 'http://maoyan.com/board/4'
    html = get_one_page(url)
    soup = BeautifulSoup(html, 'lxml')
    data = []
    for dd in soup.find_all(name='dd'):
        info = {}
        for title in dd.find_all(text=re.compile('主演')):
            info['title'] = title.string

        for img in dd.find_all(attrs={'class': 'board-img'}):
            info['img'] = img

        for index in dd.find_all(attrs={'class': re.compile('board-index')}):
            info['index'] = index

        for pub_time in dd.find_all(text=re.compile('上映时间')):
            info['pub_time'] = pub_time

        data.append(info)

    print(data)