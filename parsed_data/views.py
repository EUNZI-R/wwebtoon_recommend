from django.shortcuts import render
from django.http import HttpResponse
from parsed_data.models import BlogData,KakaopageData,KakaowebtoonData
import codecs

# Create your views here.
import csv


def psg(request):
# Create the HttpResponse object with the appropriate CSV header.
    print(BlogData.objects.values_list('title','link'))
    response = HttpResponse('text/csv')
    response['Content-Disposition'] = 'attachment; filename=quiz.csv'
# Create the CSV writer using the HttpResponse as the "file"
    # 엑셀에서 글자가 깨져 보임
    # 근데 메모장에서는 깨지지 않음
    # response.write(u'\ufeff')
    # response.write(codecs.BOM_UTF8)
    # https://dasima.xyz/excel-csv-korean-break/
    # csv 저장후 후처리 과정으로 복구 가능
    writer = csv.writer(response)
    writer.writerow(['Webtoon Title', 'link'])
    for (title, link) in BlogData.objects.values_list('title','link'):
        writer.writerow([title, link])

    return response