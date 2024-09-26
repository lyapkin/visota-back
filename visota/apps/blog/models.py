from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from ckeditor.fields import RichTextField
from parler.models import TranslatableModel, TranslatedFields
from common.utils import generate_unique_slug, generate_unique_slug_translated

from common.utils import CustomStorage


class Post(TranslatableModel):
    translations = TranslatedFields(
        title = models.CharField("заголовок", max_length=100, unique=True),
        slug = models.SlugField("url", max_length=250, unique=True, blank=True),
        content = CKEditor5Field("текст статьи", config_name='extends2'),
        # content = RichTextField("текст статьи"),
        content_concise = models.TextField("краткое описание статьи", max_length=120),
        date = models.DateField("дата", auto_now_add=True),
        last_modified = models.DateField(auto_now=True)
    )
    image_url = models.ImageField("изображение", storage=CustomStorage)

    def save(self, *args, **kwargs):
        if not self.slug.strip():
            self.slug = generate_unique_slug_translated(Post, self.title)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "пост"
        verbose_name_plural = "посты"

