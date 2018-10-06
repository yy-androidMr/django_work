# -*-coding:utf-8 -*-
import os
from django.contrib import auth
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.views.decorators.gzip import gzip_page

from Mryang_App.forms import CreateUserF, LoginUserF, UserAlbumF
from Mryang_App.result.Enums import LOGIN, UPLOAD
from Mryang_App import yquery, forms
from frames import yutils

# 显示权限
COMMON_SHOW = 4
FAMILY = 5

NOT_SEE = 9


def hello(request):
    return HttpResponse('hello')


def h5_test(request, param1):
    return render(request, param1 + '.html')


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


# def download_test(request):
#     yutils.download_file()
#     return render(request, 'login.html')

def any_page(request, str):
    return render(request, str)


# 上传照片的控制台
def check_pic_cmd_login(request):
    if 'login' in request.COOKIES:
        value = request.COOKIES['login']
        if None is not value and value == 'true':
            return True
    return False


def to_pic_cmd_login(request):
    return render(request, 'upload/gallery/upload_pic_login.html', {'uf': forms.upload_f()})


# 上传的文件处理
def up_pic_c1(request):
    if not check_pic_cmd_login(request):
        return to_pic_cmd_login(request)
    if request.POST:
        img_file = request.FILES.get("file")
        img_md5 = request.POST['md5']
        print(img_md5)
        img_name = img_file.name
        # path = default_storage.save('tmp/somename.mp3', ContentFile(data.read()))
        yutils.create_dirs(yutils.upload_album)
        f = open(os.path.join(yutils.upload_album, img_name), 'wb')
        for chunk in img_file.chunks():
            f.write(chunk)
        f.close()
        print('save suc')
    return render(request, 'upload/gallery/child_item/upload.html', )
    # def up_pic_c2(request):


def up_pic2(request):
    if (request.method == "POST"):
        # 提交了表单
        uf = forms.upload_f(request.POST, request.FILES)
        if uf.is_valid():
            # 获取表单信息
            pwd = uf.cleaned_data['pwd']
            print(pwd)
            if not pwd is 'temp1234':
                hr = render(request, 'upload/gallery/child_item/upload.html')
                hr.set_cookie('login', 'true', max_age=7 * 24 * 60 * 60)
                return hr
                # 写入数据库
                # user = User.objects.get(account=utils.get_s_account())
        return to_pic_cmd_login(request)
    else:
        if (check_pic_cmd_login(request)):
            return render(request, 'upload/gallery/child_item/upload.html')
        return to_pic_cmd_login(request)


def up_pic(request):
    if (request.method == "POST"):
        # 提交了表单
        uf = forms.upload_f(request.POST, request.FILES)
        if uf.is_valid():
            # 获取表单信息
            pwd = uf.cleaned_data['pwd']
            print(pwd)
            if not pwd is 'temp1234':
                hr = render(request, 'upload/gallery/upload_pic.html')
                hr.set_cookie('login', 'true', max_age=7 * 24 * 60 * 60)
                return hr
                # 写入数据库
                # user = User.objects.get(account=utils.get_s_account())
        return to_pic_cmd_login(request)
    else:
        if (check_pic_cmd_login(request)):
            return render(request, 'upload/gallery/upload_pic.html')
        return to_pic_cmd_login(request)


# ----------------end--------------

def play_video(request):
    # if param1:
    #     return render(request, 'player_2/' + param1)
    # else:

    return render(request, 'movie/video_js.html')


def ck_player(request):
    # if param1:
    #     return render(request, 'player_2/' + param1)
    # else:

    return render(request, 'movie/ck/ck_new.html')


#
# def uploadTest(request):
#     return render(request, 'player_2/video.html', {'medias': Movie.objects.get(showname='abc')})


def move_index(request):
    json = yquery.dir_2json(yutils.M_FTYPE_MOIVE)
    return render(request, 'movie/index.html', {'json': json})


# def pic(request):
#     json = yquery.dir_2json(yutils.M_FTYPE_PIC)
#     return HttpResponse(json, content_type='application/json')
#
#
# def movie(request):
#     json = yquery.dir_2json(yutils.M_FTYPE_MOIVE)
#     return HttpResponse(json, content_type='application/json')


def m_index(request):
    return render(request, 'own_index/index.html')


@gzip_page
def s_gallery(request):
    json = yquery.pic_level1_2json(COMMON_SHOW)
    return render(request, 'gallery/firstLevel/index-color.html', {'json': json, 'pre_path': '/pic/thum'})


@gzip_page
def m_gallery(request):
    json = yquery.pic_level1_2json(FAMILY)
    return render(request, 'gallery/firstLevel/index-color.html', {'json': json, 'pre_path': '/pic/thum'})


@gzip_page
def spe_gallery(request):
    json = yquery.pic_level1_2json(NOT_SEE)
    return render(request, 'gallery/firstLevel/index-color.html', {'json': json, 'pre_path': '/pic/thum'})


@gzip_page
def dead_gallery(request):
    return HttpResponse(
        r"<!DOCTYPE HTML><html><head><meta charset=\"utf-8\"/></head><title>希望,亦如黎明中的花朵</title><body><table width=100% height=100%><tr> <td><center><font face=\"times\"><span style=\"font-size:100px;color:green;font-family:century\"><a style=\"text-decoration:none;\">我有温暖,亦系极寒孤煞<br>我有梦想,亦似落空黄粱<br>我有痴心,亦如梦醒南柯<br>我有悲伤,亦可传播四方</a></span></font></center></td></tr></table>")
    # json = yquery.dead_2json()
    # return render(request, 'gallery/firstLevel/index-color.html', {'json': json, 'pre_path': '/pic/thum'})


@gzip_page
# @ensure_csrf_cookie
def m_second_gallery(request, dir_id):
    if request.method == "POST":
        try:
            page = request.POST.get('page')
            c_id = int(dir_id)
            json = yquery.pic_level2_2json(c_id, page)
            print('[m_second_gallery]:', dir_id, page)
            # return HttpResponse(json)
            return HttpResponse(json, 'content-type=application/x-www-form-urlencoded')
            # render(request, 'gallery/secondLevel/index.html', {'json': json, 'pre_path': '/pic/middle'})
        except:
            print('非法参数:' + dir_id)
    else:
        print('[m_second_gallery]:', dir_id, type(dir_id))
        try:
            c_id = int(dir_id)
            json = yquery.pic_level2_2json(c_id, 1)
            return render(request, 'gallery/secondLevel/index.html', {'json': json, 'pre_path': '/pic/middle'})
        except:
            print('[m_second_gallery]没有该id的照片:' + dir_id)
