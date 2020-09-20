"""bilibili_react_antd URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from bilibili_react_antd import views
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/auth/manager_login', views.login),
    path(r'api/v1/admin/products/list', views.list_products),
    path(r'api/v1/admin/products', views.products_action),
    path(r'api/v1/admin/products/getOne', views.get_product),
    path(r'api/v1/admin/products/setOne', views.set_product),
    path(r'api/v1/admin/products/delOne', views.del_product),
    path(r'api/v1/common/file_upload', views.upload_avatar),

    path('Auth/Register', views.login_authentication),

    path(r'medias', serve,{'document_root':r'D:\work\django_work\bilibili_react_antd\dir'}),

]
