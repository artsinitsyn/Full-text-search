import os
from django.core.wsgi import get_wsgi_application

# если имя проекта — app (папка, где settings.py), оставляем:
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

application = get_wsgi_application()
