from django.db import models

# Create your models here.
class Robots(models.Model):
  text = models.TextField('robots.txt')

  class Meta:
    verbose_name = 'Robots'
    verbose_name_plural = 'Robots'

  def __str__(self) -> str:
    return 'robots.txt'