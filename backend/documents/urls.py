from django.urls import path
from .views import SearchView, BookDetailView

urlpatterns = [
    path("search/", SearchView.as_view(), name="search"),
    path("book/<pk>/", BookDetailView.as_view(), name="book_detail"),
]

