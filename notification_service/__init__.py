from dotenv import load_dotenv
import os
from .celery import app as celery_app

load_dotenv()
__all__ = ('celery_app',)