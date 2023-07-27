from django.conf import settings
from django.core.files.storage import FileSystemStorage
from storages.backends.s3boto3 import S3Boto3Storage

localStorage = FileSystemStorage(location="/media")

class RemoteStorage(S3Boto3Storage):
    bucket_name = settings.YANDEX_CLIENT_DOCS_BUCKET_NAME
    file_overwrite = True

def select_storage():
    return localStorage if settings.DEBUG else RemoteStorage()