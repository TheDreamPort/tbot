from django.apps import AppConfig
from django.db.models.signals import post_delete


class RestAPIConfig(AppConfig):
    name = 'rest_api'
