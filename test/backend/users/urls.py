from django.urls import path
from django.contrib import admin
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseNotAllowed
from django.views.generic import TemplateView

from api.views import *
from users.views import *

urlpatterns = [

    # Base views
    path('home/', view_accueil, name='home'),
    path('perso/', view_perso, name='perso'),
    path('perso-content/', view_perso, name='perso-content'),
	
    # Settings
    path('settings/', view_setting, name='settings'),
    path('setting_change_username/', setting_change_username, name='setting_change_username'),
    path('setting_change_image/', setting_change_image, name='setting_change_image'),
    path('setting_change_password/', setting_change_password, name='setting_change_password'),

    # Friend list
    path('friend/', friend_list, name='friend_list'),
    path('add_friend/<int:user_id>/', add_friend, name='add_friend'),
    # path('user_search/', search_users, name='user_search'),
]
