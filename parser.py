## parser.py
from unittest import result
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains


from time import sleep
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "websaver.settings")
import django
django.setup()
## BlogData를 import해옵니다
from parsed_data.models import BlogData,KakaopageData,KakaowebtoonData

# 네이버웹툰 크롤링
def parse_blog():
    req = requests.get('https://comic.naver.com/webtoon/weekday')
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')
    my_webtoons = soup.select(
        'div.list_area.daily_all > div > div > ul > li'
        )
    data={}
    for my_webtoon in my_webtoons[:5]:
        
        titleTag = my_webtoon.select_one('a') 
        imageTag = my_webtoon.select_one('div > a > img') 
        print(imageTag.get('title'))
        print(type(imageTag.get('src')))
        
        data[imageTag.get('title')] = [titleTag.get('href'), imageTag.get('src')]
    # print(soup,data)
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
    url = 'https://webtoon.kakao.com/original-webtoon?tab=mon'
    # week = ['#day=mon&tab=day', '#day=tue&tab=day', '#day=wed&tab=day', '#day=thu&tab=day', '#day=fri&tab=day', '#day=sat&tab=day', '#day=sun&tab=day']
    # title_list = [] ; id_list = [] ; author_list = [] ;  day_list = []  ; genre_list = [] ; story_list = [] ; platform_list = []
    # num = 366 # 네이버 웹툰 id가 365까지였음
    # for i in range(7): #월요일부터 일요일까지
    s = Service('./chromedriver')

    URL = url 
    driver = webdriver.Chrome(service=s)
    driver.get(URL) #요일별로 링크 가져옴

    sleep(0.2)
    
    #ActionChains생성
    action = ActionChains(driver)

    #리스트 가져오기
    body = driver.find_elements(By.CSS_SELECTOR, "div.w-full.bottom-0.left-0.absolute.h-full")

    #move_to_element를 이용하여 이동
    for i in range(0, len(body), 15):
        action.move_to_element(body[i]).perform()        
    action.move_to_element(body[-1]).perform()
    
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    my_webtoons = soup.select(
        'div > div > div > a'
        )
    # print(soup, my_webtoons)
    #root > main > div
    #root > main > div > div > div.swiper-container.swiper-container-initialized.swiper-container-horizontal.swiper-container-pointer-events > div > div.swiper-slide.swiper-slide-active > div > div > div > div > div:nth-child(1) > div.content-start.flex.flex-wrap.-mx-2 > div:nth-child(25) > div > div > a > div.w-full.absolute.left-0.bottom-10 > picture > img
    #root > main > div > div > div.swiper-container.swiper-container-initialized.swiper-container-horizontal.swiper-container-pointer-events > div > div.swiper-slide.swiper-slide-active > div > div > div > div > div:nth-child(6) > div.content-start.flex.flex-wrap.-mx-2 > div:nth-child(25)
    # 제목
    #root > main > div > div ~생략~ div:nth-child(25) > div > div > a > div.w-full.absolute.left-0.bottom-10 > picture > img
    #root > main > div > div ~생략~ div:nth-child(5) > div > div > a > div.w-full.absolute.left-0.bottom-10 > picture > img
    # 링크
    #root > main > div > div > div.swiper-container.swiper-container-initialized.swiper-container-horizontal.swiper-container-pointer-events > div > div.swiper-slide.swiper-slide-active > div > div > div > div > div:nth-child(1) > div.content-start.flex.flex-wrap.-mx-2 > div:nth-child(2) > div > div > a
    #root > main > div > div ~생략~ div:nth-child(6) > div.content-start.flex.flex-wrap.-mx-2 > div:nth-child(25) > div > div > a
    # 인물이미지
    #root > main > div > div > div.swiper-container.swiper-container-initialized.swiper-container-horizontal.swiper-container-pointer-events > div > div.swiper-slide.swiper-slide-active > div > div > div > div > div:nth-child(1) > div.content-start.flex.flex-wrap.-mx-2 > div:nth-child(3) > div > div > a > picture:nth-child(2) > img
    #root > main > div > div ~생략~ div:nth-child(25) > div > div > a > picture:nth-child(2) > img
    #root > main > div > div > div.swiper-container.swiper-container-initialized.swiper-container-horizontal.swiper-container-pointer-events > div > div.swiper-slide.swiper-slide-active > div > div > div > div > div:nth-child(1) > div.content-start.flex.flex-wrap.-mx-2 > div:nth-child(2) > div > div > a > picture:nth-child(2) > img
    # 배경이미지
    #root > main > div > div ~생략~ div:nth-child(25) > div > div > a > picture.left-0.top-0.w-full.overflow-hidden.\!absolute.-z-1.origin-top.scale-\[1\.35\] > img
    #root > main > div > div > div.swiper-container.swiper-container-initialized.swiper-container-horizontal.swiper-container-pointer-events > div > div.swiper-slide.swiper-slide-active > div > div > div > div > div:nth-child(1) > div.content-start.flex.flex-wrap.-mx-2 > div:nth-child(1) > div > div > div > a > picture.left-0.top-0.w-full.overflow-hidden.\!absolute.-z-1.origin-top.scale-\[2\.34\] > img
    data = {}
    # image loading complete? yes->sum_t; no->sum_f;
    sum_t=0 
    sum_f=0
    
    for i,my_webtoon in enumerate(my_webtoons):
        print(my_webtoon)
        print()
        if my_webtoon.find('div', 'absolute'):
            print(i)
            sum_t+=1
            if my_webtoon.find('video'):
                titleTag = my_webtoon.select_one('div.w-full.absolute.left-0.bottom-10 > picture > img') 
                linkTag = my_webtoon
                characterimageTag = my_webtoon.select_one('video > source') 
                backgroundimageTag = my_webtoon.select_one('picture:nth-child(2) > img') 
            else:
                titleTag = my_webtoon.select_one('div.w-full.absolute.left-0.bottom-10 > picture > img') 
                linkTag = my_webtoon
                characterimageTag = my_webtoon.select_one('picture:nth-child(2) > img') 
                backgroundimageTag = my_webtoon.select_one('picture:nth-child(1) > img') 
        else:
            sum_f+=1
            continue
        
        print(titleTag.get('alt'))
        print(linkTag.get('href'))
        print(characterimageTag.get('src'))
        print(backgroundimageTag)
        
        data[titleTag.get('alt')] = [linkTag.get('href'), characterimageTag.get('src'),backgroundimageTag.get('src')]
    print("kakaowebtoon")
    print(sum_t, sum_f)
    # input()
    # print(data['미생'])
    # print(soup, my_webtoons, data)
    return data

## 이 명령어는 이 파일이 import가 아닌 python에서 직접 실행할 경우에만 아래 코드가 동작하도록 합니다.
if __name__=='__main__':
    BlogData.objects.all().delete()
    KakaopageData.objects.all().delete()
    KakaowebtoonData.objects.all().delete()
    
    blog_data_dict = parse_blog()
    # kakaopage_data_dict = parse_kakaopage()
    kakaowebtoon_data_dict = parse_kakaowebtoon()
    
    for t, l in blog_data_dict.items():
        BlogData(title=t, link=l[0], image_file=l[1]).save()
    # for t, l in kakaopage_data_dict.items():
    #     KakaopageData(title=t, link=l).save()
    for t, l in kakaowebtoon_data_dict.items():
        KakaowebtoonData(title=t, link=l[0]).save()







    # # test #
    # req = requests.get('https://comic.naver.com/webtoon/weekday')
    # html = req.text
    # soup = BeautifulSoup(html, 'html.parser')
    # my_webtoons = soup.select(
    #     'div.list_area.daily_all > div > div > ul > li'
    #     )
    # #content > div.list_area.daily_all > div > div > ul > li > div > a > img
    # #content > div.list_area.daily_all > div > div > ul > li > div > a > img
    # #content > div.list_area.daily_all > div > div > ul > li > a
    # #content > div.list_area.daily_all > div > div > ul > li > a
    # # print(my_titles[-1].get('title'))
    # data={}
    # for my_webtoon in my_webtoons[:5] :
        
    #     titleTag = my_webtoon.select_one('a') 
    #     imageTag = my_webtoon.select_one('div > a > img') 
    #     print(imageTag.get('title'))
    #     print(type(imageTag.get('src')))
        
    #     data[imageTag.get('title')] = [titleTag.get('href'), imageTag.get('src')]
    # print(data)
    # # data = {}
    # # for title in my_titles:
    # #     data[title.get('title')] = title.get('href')