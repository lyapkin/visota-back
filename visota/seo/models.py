from django.db import models
from parler.models import TranslatableModel, TranslatedFields

# Create your models here.
class Robots(models.Model):
  text = models.TextField('robots.txt')

  class Meta:
    verbose_name = 'Robots'
    verbose_name_plural = 'Robots'

  def __str__(self) -> str:
    return 'robots.txt'
  

class SEOStaticPage(TranslatableModel):
  order = models.PositiveSmallIntegerField('позиция')
  page = models.CharField(max_length=64, primary_key=True)
  name = models.CharField('страница', max_length=255, unique=True)
  translations = TranslatedFields(
    header = models.CharField("h1", max_length=255, unique=True),
    title = models.CharField("title", max_length=255),
    description = models.TextField('description'),
    noindex_follow = models.BooleanField('<meta name="robots" content="noindex, follow">', default=False)
  )

  def __str__(self):
    return self.name
    
  class Meta:
    verbose_name = "SEO для статических страниц"
    verbose_name_plural = "SEO для статических страниц"
    ordering = ('order',)