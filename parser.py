## parser.py
import requests
from bs4 import BeautifulSoup
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "websaver.settings")
import django
django.setup()
## BlogData를 import해옵니다
from parsed_data.models import BlogData,KakaopageData,KakaowebtoonData

# 네이버웹툰 크롤링
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

# 카카오페이지 크롤링
def parse_kakaopage():
    req = requests.get('https://page.kakao.com/main?categoryUid=10&subCategoryUid=1002&day=7')
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')
    my_titles = soup.select(
        'div.jsx-3157985592.mainContents.mainContents_pc > div.css-1sna24c > div.css-1saqd06 > div > a > li > div.css-yd766s > div > span'
        )
    #root > div.jsx-3157985592.mainContents.mainContents_pc > div.css-1sna24c > div.css-1saqd06 > div > a:nth-child(130) > li > div.css-yd766s > div > span
    data = {}
    for title in my_titles:
        data[title.text] = title.text
    return data

# 카카오웹툰 크롤링
def parse_kakaowebtoon():
    req = requests.get('https://webtoon.kakao.com/original-webtoon')
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')
    my_titles = soup.select(
        'div > div > div.swiper-container.swiper-container-initialized.swiper-container-horizontal.swiper-container-pointer-events > div > div.swiper-slide.swiper-slide-active > div > div > div > div > div > div.content-start.flex.flex-wrap.-mx-2 > div > div > div > a > div.w-full.absolute.left-0.bottom-10 > picture > img'
        )
    #root > main > div > div > div.swiper-container.swiper-container-initialized.swiper-container-horizontal.swiper-container-pointer-events > div > div.swiper-slide.swiper-slide-active > div > div > div > div > div:nth-child(6) > div.content-start.flex.flex-wrap.-mx-2 > div:nth-child(25) > div > div > a > div.w-full.absolute.left-0.bottom-10 > picture > img
    #root > main > div > div > div.swiper-container.swiper-container-initialized.swiper-container-horizontal.swiper-container-pointer-events > div > div.swiper-slide.swiper-slide-active > div > div > div > div > div:nth-child(3) > div.content-start.flex.flex-wrap.-mx-2 > div:nth-child(5) > div > div > a > div.w-full.absolute.left-0.bottom-10 > picture > img
    data = {}
    for title in my_titles:
        data[title.get('alt')] = title.get('alt')
    return data

## 이 명령어는 이 파일이 import가 아닌 python에서 직접 실행할 경우에만 아래 코드가 동작하도록 합니다.
if __name__=='__main__':
    blog_data_dict = parse_blog()
    kakaopage_data_dict = parse_kakaopage()
    kakaowebtoon_data_dict = parse_kakaowebtoon()
    
    for t, l in blog_data_dict.items():
        BlogData(title=t, link=l).save()
    for t, l in kakaopage_data_dict.items():
        KakaopageData(title=t, link=l).save()
    for t, l in kakaowebtoon_data_dict.items():
        KakaowebtoonData(title=t, link=l).save()