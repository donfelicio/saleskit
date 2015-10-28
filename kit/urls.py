"""kit URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    url(r'^$', 'reservation.views.home', name='home'),
    url(r'^show', 'show.views.show', name='show'),
    url(r'^res_input', 'reservation.views.res_input', name='res_input'),
    url(r'^help', 'reservation.views.help', name='help'),
    url(r'^logout', 'reservation.views.logout', name='logout'),
    url(r'^login', 'reservation.views.login', name='login'),
    url(r'^load/', 'reservation.views.loadpage', name='load'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^invoice', 'invoice.views.home', name='invoice'),

]

urlpatterns += staticfiles_urlpatterns()

