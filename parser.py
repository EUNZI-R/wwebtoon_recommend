## parser.py
import requests
from bs4 import BeautifulSoup
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "websaver.settings")
import django
django.setup()
## BlogData를 import해옵니다
from parsed_data.models import BlogData

def parse_blog():
    req = requests.get('https://comic.naver.com/webtoon/weekdayList?week=thu')
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')
    my_titles = soup.select(
        'div.list_area.daily_img > ul > li > dl > dt > a'
        )
    data = {}
    for title in my_titles:
        data[title.get('title')] = title.get('href')
    return data

## 이 명령어는 이 파일이 import가 아닌 python에서 직접 실행할 경우에만 아래 코드가 동작하도록 합니다.
if __name__=='__main__':
    blog_data_dict = parse_blog()
    for t, l in blog_data_dict.items():
        BlogData(title=t, link=l).save()