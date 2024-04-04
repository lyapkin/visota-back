import os
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from urllib.parse import urljoin
from datetime import datetime


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