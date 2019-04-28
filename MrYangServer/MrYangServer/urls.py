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

from django.conf.urls.static import static
from frames import TmpUtil

# 检查路径.
# TmpUtil.check_tmp_paths()
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # 上传照片的控制台
    url(r'^upp/$', views.up_pic),
    url(r'^up/pic/a', views.up_pic_c1),
    url(r'^up/pic', views.up_pic2),
    # ----------end---------------

    url(r'^$', views.new_move_index),
    url(r'^own/$', views.m_index),
    url(r'^sg/$', views.s_gallery),
    url(r'^mg/$', views.m_gallery),
    url(r'^speg/$', views.spe_gallery),
    url(r'^g2/([0-9]+)$', views.m_second_gallery),

    url(r'^h5/(.*)/$', views.h5_test),
    url(r'^download/$', views.download_test),
    url(r'tttt/',views.test_json),
    # static(res_url, document_root=res_root)
    # url(r'^any/(.*)/$', views.any_page),
]
# from django.conf.urls.static import static
#
urlpatterns += static(views.res_url, document_root=views.res_root)
