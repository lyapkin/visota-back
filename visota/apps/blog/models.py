from django.db import models
from django_ckeditor_5.fields import CKEditor5Field

from common.utils import CustomStorage


class Post(models.Model):
    title = models.CharField("заголовок", max_length=100, unique=True)
    slug = models.SlugField("url", max_length=100, unique=True)
    content = CKEditor5Field("текст статьи", config_name='extends')
    content_concise = models.TextField("краткое описание статьи", max_length=120)
    image_url = models.ImageField("изображение", storage=CustomStorage)
    date = models.DateField("дата", auto_now_add=True)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "пост"
        verbose_name_plural = "посты"