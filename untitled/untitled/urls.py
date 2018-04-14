# -*- coding: utf-8 -*-
"""untitled URL Configuration

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

from MySite import views

# from django.contrib.staticfiles.urls import staticfiles_urlpatterns
# from django.contrib.staticfiles.urls import static
# from untitled import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^yy/add2/(\d+)/(\d+)/$', views.add2, name='add2'),
    url(r'^yy/new_add2/(\d+)/', views.revers_test_new_add2, name='new_add2'),
    url(r'^yy/html/$', views.template_index),
    url(r'^yy/child_teach/(.+)', views.template_child_teach),
    url(r'^yy/intro/', views.list_action),
    url(r'^yy/show_add2_path/(\d+)/$', views.revers_test_new_add2, name='show_add2_path'),
    url(r'^yy/user_action', views.user_action, name='user_action'),
]
# 对images找不到起不到什么好作用先写着.
# urlpatterns += staticfiles_urlpatterns()
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
