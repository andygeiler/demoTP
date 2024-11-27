from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_page, name='index-page'),
    path('login/', views.index_page, name='login'),
    path('home/', views.home, name='home'),
    path('buscar/', views.search, name='buscar'),

    path('favourites/', views.getAllFavouritesByUser, name='favourites'),
    path('favourites/add/', views.saveFavourite, name='saveFavourite'),
    path('favourites/delete/', views.deleteFavourite, name='deleteFavourite'),
    path('logout/', views.exit, name='exit'),  # Cerrar sesión
    path('guardar-comentario/', views.guardar_comentario, name='update_comment'),

    path('exit/', views.exit, name='exit'),
]