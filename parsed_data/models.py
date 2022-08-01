## parsed_data/models.py
from django.db import models


class BlogData(models.Model):
    title = models.CharField(max_length=200)
    link = models.URLField()

    def __str__(self):
        return self.title
    
class KakaopageData(models.Model):
    title = models.CharField(max_length=200)
    link = models.URLField()

    def __str__(self):
        return self.title

class KakaowebtoonData(models.Model):
    title = models.CharField(max_length=200)
    link = models.URLField()

    def __str__(self):
        return self.title