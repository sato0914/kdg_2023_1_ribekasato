from django.db import models
from django.utils import timezone # django で日付を管理するためのモジュール

CATEGORY = (('dogs','犬'),('cats','猫'),('other','その他'))

class Post(models.Model):
    title = models.CharField('タイトル', max_length=200)
    text = models.TextField('本文')
    date = models.DateTimeField('日付', default=timezone.now)
    thumbnail = models.ImageField()
    category = models.CharField(
        max_length=100,
        choices= CATEGORY
    )
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    def __str__(self): # Post モデルが直接呼び出された時に返す値を定義
        return self.title # 記事タイトルを返す

class Sirase(models.Model):
    title =models.CharField(max_length=30)
    text = models.TextField()
    thumbnail = models.ImageField()

class Search(models.Model):
  name = models.CharField(max_length=20)
  def __str__(self):
      return self.name
  
class Comment(models.Model):
    """記事に紐づくコメント"""
    name = models.CharField('名前', max_length=255, default='名無し')
    text = models.TextField('本文')
    target = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='対象記事')
    created_at = models.DateTimeField('作成日', default=timezone.now)
 
    def __str__(self):
        return self.text[:20]