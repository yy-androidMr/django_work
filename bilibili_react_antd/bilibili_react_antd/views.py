from django.http import HttpResponse


def login(request):
    # print('我发起了登录请求')
    # {
    #     "code": "suc",
    #     "token": "abc"
    # }
    return HttpResponse("我收到了你的请求")