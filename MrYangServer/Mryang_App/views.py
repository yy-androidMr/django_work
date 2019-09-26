# -*-coding:utf-8 -*-
import json
import os
from django.contrib import auth
from django.http import HttpResponse, FileResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.views.decorators.gzip import gzip_page

from Mryang_App.controlls import PhotoWallCtrl
from Mryang_App.forms import CreateUserF, LoginUserF, UserAlbumF
from Mryang_App.result.Enums import LOGIN, UPLOAD
from Mryang_App import yquery, forms
from frames import yutils, ypath

# 显示权限
from frames import logger
from frames.xml import XMLBase

COMMON_SHOW = 4
FAMILY = 5
NOT_SEE = 9

dpins = XMLBase.get_base_cfg()
T_COS_MEIDA_ROOT = dpins.cos_media_root.innerText


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
        ypath.create_dirs(yutils.upload_album)
        f = open(os.path.join(yutils.upload_album, img_name), 'wb')
        for chunk in img_file.chunks():
            f.write(chunk)
        f.close()
        print('save suc')
    return render(request, 'upload/gallery/child_item/upload.html')
    # def up_pic_c2(request):


def up_pic2(request):
    return render(request, 'upload/gallery/child_item/up.html')

    # if (request.method == "POST"):
    #     # 提交了表单
    #     uf = forms.upload_f(request.POST, request.FILES)
    #     if uf.is_valid():
    #         # 获取表单信息
    #         pwd = uf.cleaned_data['pwd']
    #         print(pwd)
    #         if not pwd is 'temp1234':
    #             hr = render(request, 'upload/gallery/child_item/upload.html')
    #             hr.set_cookie('login', 'true', max_age=7 * 24 * 60 * 60)
    #             return hr
    #             # 写入数据库
    #             # user = User.objects.get(account=utils.get_s_account())
    #     return to_pic_cmd_login(request)
    # else:
    #     if (check_pic_cmd_login(request)):
    #         return render(request, 'upload/gallery/child_item/upload.html')
    #     return to_pic_cmd_login(request)


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

# def new_move_index(request):
#     json = yquery.dir_2json(yutils.M_FTYPE_MOIVE)
#     info_json = yquery.movie_infos()
#     r = render(request, 'movie/new_index.html', {'json': json, 'info_json': info_json, 'movie_url': movie_url,
#                                                  'out_name': movie_info_cfg[XMLMedia.TAGS.NAME]})
#     return r


def m_index(request):
    return render(request, 'own_index/index.html')


def s_gallery(request):
    json = yquery.pic_level1_2json(COMMON_SHOW)
    return render(request, 'gallery/firstLevel/index-color.html',
                  {'json': json})


def m_gallery(request):
    json = yquery.pic_level1_2json(FAMILY)
    return render(request, 'gallery/firstLevel/index-color.html',
                  {'json': json})


def spe_gallery(request):
    ddd=[{"name": "abc","rel_path": "rel_path","intro": "intro","time": "time","thum": "thum"}]
    print(json.dumps(ddd))
    return render(request, 'gallery/firstLevel/index-color.html',
                  {'json':json.dumps(ddd)})


def dead_gallery(request):
    return HttpResponse(
        r"<!DOCTYPE HTML><html><head><meta charset=\"utf-8\"/></head><title>希望,亦如黎明中的花朵</title><body><table width=100% height=100%><tr> <td><center><font face=\"times\"><span style=\"font-size:100px;color:green;font-family:century\"><a style=\"text-decoration:none;\">我有温暖,亦系极寒孤煞<br>我有梦想,亦似落空黄粱<br>我有痴心,亦如梦醒南柯<br>我有悲伤,亦可传播四方</a></span></font></center></td></tr></table>")
    # json = yquery.dead_2json()
    # return render(request, 'gallery/firstLevel/index-color.html', {'json': json, 'pre_path': '/pic/thum'})


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
            logger.error('非法参数:', dir_id)
    else:
        logger.info('[m_second_gallery]:', dir_id)
        try:
            c_id = int(dir_id)
            json = yquery.pic_level2_2json(c_id, 1)
            return render(request, 'gallery/secondLevel/index.html', {'json': json, 'pre_path': '/pic/middle'})
        except:
            logger.error('[m_second_gallery]没有该id的照片:', dir_id)


def media_moive(request):
    return media_json(request, 'movie')


def media_tv(request):
    return media_json(request, 'tv')


def media_video(request):
    return media_json(request, 'video')


def media_json(request, type):
    p_id = request.GET.get('p')
    if not p_id:
        json = yquery.meida_root(type)
    else:
        try:
            id = int(p_id)
            json = yquery.media_dir(type, id)
        except:
            json = yquery.meida_root(type)

    return HttpResponse(json)


def download_test(request):
    print(os.path.dirname('.'))
    file = open('F:\django_work\MrYangServer\static\media/1.mp4', 'rb')
    response = FileResponse(file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="1.mp4"'
    return response


# 测试用  正常不走这里.
def create_default_photowall(request):
    return HttpResponse(PhotoWallCtrl.batch_create_on_dir())


# 这个可能要走. 但是要设计一下.
def batch_default_photo(request):
    return HttpResponse(PhotoWallCtrl.batch_photo_to_wall())


def photo_wall_list(request):
    return HttpResponse(PhotoWallCtrl.photo_wall_list(1))

def photo_list(request,wall_id):
    return HttpResponse(PhotoWallCtrl.photo_list(wall_id))

    # if (request.method == 'POST'):
    #     request.POST.get('pw_id')
    #     pass