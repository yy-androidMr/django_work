# -*- coding: utf-8 -*-
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls.base import reverse
import logging


def template_index(request):
    return render(request, 'MySite/home.html')


def add2(request, a, b):
    c = (int(a) + int(b))
    return HttpResponseRedirect(reverse('new_add2', args=str(c)))
    # c = int(a) + int(b)
    # return HttpResponse('am add2 , my value = ' + str(c))


def revers_test_new_add2(request, c):
    return HttpResponse('am new add2 , my value = ' + str(c))


def template_child_teach(request, last_name):
    # loggers = logging.getLogger('default')
    # loggers.error('Something went wrong!:' + str(last_name))
    return render(request, 'MySite/download/child_teach/' + str(last_name))


def list_action(request):
    intro = u'我是字符串,我从py上传的字符串'
    tutorial_list = ['HTML', 'CSS', 'JQuery', 'python', 'Django']
    info_dict = {'site': 'MrYang', 'content': '什么都会'}
    rang_list = map(str, range(100))
    logic_value = 90

    return render(request, 'MySite/ShowMyIp.html',
                  {'intro': intro, 'TutorialList': tutorial_list, 'info_dict': info_dict, 'rang_list': rang_list,
                   'logic_value': logic_value})


def user_action(request):
    from MySite.models import Blog
    blog_name = Blog.objects.get(name="Yang-blog")
    return render(request, 'MySite/User_action.html', {"blog_name": blog_name.name,"tagline": blog_name.tagline})
