"""MrYangServer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from Mryang_App import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # url(r'^login/',views.login),
    # url(r'^h5/(.*)/$', views.h5_test),
    # url(r'^h5_demo/', views.h5_demo),
    # url(r'^h5_307/', views.h5_307),
    # url(r'^h5_23/', views.h5_23),
    # url(r'^upload/', views.upload_file),
    # url(r'^regist/', views.regist),
    # url(r'^login/', views.login),
    # url(r'^download/', views.download_test),
    # url(r'^$', views.show_gallery),
    url(r'^video/(.*)/$', views.play_video),
    url(r'^$', views.player_3),
    # url(r'^index/$', views.yy_index),
    url(r'^i/(.*)$', views.yy_all),
    url(r'^aj_pic/$', views.pic),
    url(r'^aj_mov/$', views.movie),
    url(r'^own/$', views.m_index),
    url(r'^gallery/$', views.m_gallery),
]
