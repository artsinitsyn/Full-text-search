from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from documents.views import SearchView


def root_view(request):
    return JsonResponse({"message": "API работает. Используй /api/ для запросов."})

urlpatterns = [
    path('', root_view),  
    path('api/', include('documents.urls')),
    path('api/search/', SearchView.as_view(), name='search'),
]

