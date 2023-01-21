# pages/urls.py
from django.urls import path, re_path
from . import views
from django.shortcuts import render


# dobrze chlopcy
# fajnie jakbyscie tu dawali same wyrazenia regularne
# bo to wyglada tak ze
# urls te glowne sa stworzone tam nic nie trzeba ruszac
# tutaj dajecie to co bedzie po /
# przyklad: siemawakacje.pl/city/...
# i tylko tu cos robicie
urlpatterns = [
    re_path(r'^(?P<cityName>[A-Za-zżźćńółęąśŻŹĆĄŚĘŁÓŃ]*)/hotels/$', views.hotelsResponseView),
    re_path(r'^city/($)|^city/(?P<cityName>[A-Za-zżźćńółęąśŻŹĆĄŚĘŁÓŃ]*)/$', views.cityQueryView),
    re_path(r'^($)|(?P<cityName>[A-Za-zżźćńółęąśŻŹĆĄŚĘŁÓŃ]*)/$', views.cityPageView)
]
