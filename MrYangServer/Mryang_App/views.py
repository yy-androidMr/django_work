# -*-coding:utf-8 -*-
import urllib

from django.contrib import auth
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from Mryang_App.forms import CreateUserF, LoginUserF, UserAlbumF
from Mryang_App.models import Dir
from Mryang_App.result.Enums import LOGIN, UPLOAD
from Mryang_App import yutils, yquery


def hello(request):
    return HttpResponse('hello')


def login(request):
    return HttpResponse('hello2')


def h5_test(request, param1):
    return render(request, param1 + '.html')


def h5_demo(request):
    return render(request, 'tpmo_506_tinker/index.html')


def h5_307(request):
    return render(request, 'cpts_307_mq/index.html')


def h5_23(request):
    return render(request, 'dstp_23_picxa/index1.html')


def login(request):
    if (request.method == 'POST'):
        auth.authenticate()
        f_user = LoginUserF(request.POST)
        user = f_user.check_account()
        if user:
            response = redirect('../login/')
            response.set_cookie(yutils.S_NAME, user.user_name, yutils.LOGIN_TIME_OUT)
            response.set_cookie(yutils.S_ACCOUNT, user.account, yutils.LOGIN_TIME_OUT)
            return response
        else:
            return render(request, 'login.html', {'f_user': f_user, 'err': LOGIN.NO_ACCOUNT})
    else:
        if yutils.is_login_c(request.COOKIES):
            return redirect('../upload/')
        else:
            f_user = LoginUserF()
            # user = f_user.fill_random()
            return render(request, 'login.html', {'f_user': f_user})


def regist(request):
    if (request.method == 'POST'):
        f_user = CreateUserF(request.POST, request.FILES)
        user = f_user.flush_to_user()
        if user:
            response = redirect('../login/')
            return response
        else:
            f_user = CreateUserF()
            return render(request, 'regist.html', {'f_user': f_user, 'err': f_user.errors})
    else:
        f_user = CreateUserF()
        return render(request, 'regist.html', {'f_user': f_user})


def upload_file(request):
    # 检查登录状态
    if yutils.is_login_c(request.COOKIES):
        if (request.method == "POST"):
            # 提交了表单
            uf = UserAlbumF(request.POST, request.FILES)
            if uf.is_valid():
                # 获取表单信息
                headimg = uf.cleaned_data['headImg']
                # 写入数据库
                # user = User.objects.get(account=utils.get_s_account())
        else:
            uf = UserAlbumF()
        return render(request, 'upload_img.html', {'uf': uf})
    else:
        # 如果没有登录,返回登录界面.
        return redirect('../login/', {'err': UPLOAD.NO_LOGIN})


def download_test(request):
    yutils.download_file()
    return render(request, 'login.html')


def show_gallery(request):
    return render(request, 'player_2/index.html', {'movie_dir': Dir.objects.get(type=yutils.M_FTYPE_MOIVE)})


def play_video(request, nginxPath):
    # if param1:
    #     return render(request, 'player_2/' + param1)
    # else:

    return render(request, 'player_3/video.html', {'nginxPath': urllib.parse.unquote(nginxPath)})


#
# def uploadTest(request):
#     return render(request, 'player_2/video.html', {'medias': Movie.objects.get(showname='abc')})


def player_3(request):
    json = yquery.dir_2json(yutils.M_FTYPE_MOIVE)
    return render(request, 'player_3/index.html', {'json': json})


def pic(request):
    json = yquery.dir_2json(yutils.M_FTYPE_PIC)
    return HttpResponse(json, content_type='application/json')


def movie(request):
    json = yquery.dir_2json(yutils.M_FTYPE_MOIVE)
    return HttpResponse(json, content_type='application/json')


def yy_all(request, path):
    return render(request, path + '.html')


def m_index(request):
    return render(request,  'own_index/index.html')

def m_gallery(request):
    return render(request,'gallery/firstLevel/index-color.html')


