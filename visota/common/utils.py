import os
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from urllib.parse import urljoin
from datetime import datetime
from django.utils.text import slugify
from unidecode import unidecode


class CustomStorage(FileSystemStorage):
    """
    Кастомное расположение для медиа файлов редактора
    """
    def get_folder_name(self):
        return datetime.now().strftime('%Y/%m/%d')

    def get_valid_name(self, name):
        return name

    def _save(self, name, content):
        folder_name = self.get_folder_name()
        name = os.path.join(folder_name, self.get_valid_name(name))
        return super()._save(name, content)

    location = os.path.join(settings.MEDIA_ROOT, 'uploads')
    base_url = urljoin(settings.MEDIA_URL, 'uploads/')


def upload_product_img_to(instance, filename):
    return 'images/products/{product}/{filename}'.format(product=instance.product.slug, filename=filename)


def upload_product_file_to(instance, filename):
    return 'images/products/{product}/docs/{filename}'.format(product=instance.product.slug, filename=filename)


def generate_unique_slug(klass, field):
    origin_slug = slugify(unidecode(field))
    unique_slug = origin_slug
    numb = 1
    while klass.objects.filter(slug=unique_slug).exists():
        unique_slug = f'{origin_slug}-{numb}'
        numb += 1
    return unique_slug

def generate_unique_slug_translated(klass, field):
    origin_slug = slugify(unidecode(field))
    unique_slug = origin_slug
    numb = 1
    while klass.objects.translated(slug=unique_slug).exists():
        unique_slug = f'{origin_slug}-{numb}'
        numb += 1
    return unique_slug