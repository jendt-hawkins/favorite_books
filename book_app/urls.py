from django.urls import path
from . import views

urlpatterns = [
    path('', views.form),
    path('registered', views.registered),
    path('logout', views.logout),
    path('login', views.login),
    path('success', views.success),
    path('add_book', views.add_book),
    path('book/<int:book_id>', views.onebook),
    path('favorite/<int:book_id>', views.favorite),
    path('favorites', views.favorites_page),
    path('unfavorite/<int:book_id>', views.unfavorite),
    path('update/<int:book_id>', views.update),
    path('delete/<int:book_id>', views.delete),
]