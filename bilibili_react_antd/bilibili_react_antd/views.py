import json

from django.http import HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie

from bilibili_react_antd import utils

cur_products = [
    {
        'name': '香皂',
        'price': 3,
        'id': 1
    }, {
        'name': '特仑苏',
        'price': 50,
        'id': 2
    },
    {
        'name': 'iphoneX',
        'price': 9998,
        'id': 3
    }
]


def auth(request):
    if (utils.check_token(request.META.get("HTTP_AUTHORIZATION"))):
        return None
    return {"message": "尚未登录", 'code': 'err'}


def login(request):
    res_info = {}
    if (request.method == 'POST'):
        if request.body:
            data_json = json.loads(request.body)
            userName = data_json.get('userName', None)
            passWord = data_json.get('passWord', None)
            if (userName is None or passWord is None):
                res_info['code'] = '请输入账户名或者密码'
                res_info['code'] = 'err'
            else:

                res_info['token'] = utils.create_token(userName)
                res_info['code'] = 'suc'
    else:
        res_info['code'] = 'err!!!'
    return HttpResponse(json.dumps(res_info))


def list_products(request):
    auth_res = auth(request)
    if auth_res is not None:
        return HttpResponse(json.dumps(auth_res))
    # print(utils.check_token(request.META.get("HTTP_AUTHORIZATION")))
    res_info = {'code': 'suc'}
    need_pages = request.GET.get('page', 1)
    res_info['totalCount'] = 30
    res_info['pages'] = need_pages
    if need_pages is '1':
        res_info['products'] = cur_products
    else:
        res_info['products'] = [
            {
                'name': need_pages + '香皂',
                'price': 3,
                'id': 4,
                'coverImage':'http://localhost:9000/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_158632004322.png'
            }, {
                'name': need_pages + '特仑苏',
                'price': 50,
                'id': 5
            },
            {
                'name': need_pages + 'iphoneX',
                'price': 9998,
                'id': 6
            }
        ]
    # if(request.method=='POST'):
    #     if request.body:
    #         data_json = json.loads(request.body)
    #         userName = data_json.get('userName',None)
    #         passWord = data_json.get('passWord',None)
    #         if(userName is None or passWord is None):
    #             res_info['code']='请输入账户名或者密码'
    #             res_info['code']='err'
    #         else:
    #
    #             res_info['token'] = utils.create_token(userName)
    #             res_info['code'] = 'suc'
    # else:
    #     res_info['code']='err!!!'
    return HttpResponse(json.dumps(res_info))


@ensure_csrf_cookie
def login_authentication(request):
    if request.method != "POST":
        return HttpResponse()


def products_action(request):
    auth_res = auth(request)
    if auth_res is not None:
        return HttpResponse(json.dumps(auth_res))

    res_info = {'code': 'suc'}
    data_json = json.loads(request.body)
    product_name = data_json.get('name', None)
    product_price = data_json.get('price', None)
    cur_products.append({'name': product_name,
                         'price': product_price,
                         'id': 99})

    # res_info['totalCount'] = 30
    # res_info['pages'] = need_pages
    return HttpResponse(json.dumps(res_info))


def get_product(request):
    # auth_res = auth(request)
    # if auth_res is not None:
    #     return HttpResponse(json.dumps(auth_res))
    id = request.GET.get('id', 1)

    res_info = {'code': 'suc'}

    for item in cur_products:
        if item['id'] is int(id):
            res_info['product']=item
            break
            #就是这个
    return HttpResponse(json.dumps(res_info))



def set_product(request):

    auth_res = auth(request)
    if auth_res is not None:
        return HttpResponse(json.dumps(auth_res))

    res_info = {'code': 'suc'}
    data_json = json.loads(request.body)
    product_name = data_json.get('name', None)
    product_price = data_json.get('price', None)
    product_id = int(request.GET.get('id', -1))
    if product_id != -1:
        for item in cur_products:
            if item['id']  == product_id:
                item['name']=product_name
                item['price']=product_price
    # cur_products[]

    # res_info['totalCount'] = 30
    # res_info['pages'] = need_pages
    return HttpResponse(json.dumps(res_info))


def del_product(request):

    auth_res = auth(request)
    if auth_res is not None:
        return HttpResponse(json.dumps(auth_res))

    res_info = {'code': 'suc'}
    product_id = int(request.GET.get('id', -1))
    if product_id != -1:
        for item in cur_products:
            if item['id']  == product_id:
                cur_products.remove(item)
    # cur_products[]

    # res_info['totalCount'] = 30
    # res_info['pages'] = need_pages
    return HttpResponse(json.dumps(res_info))



def upload_avatar(request):
    res_info = {}
    if request.method== 'POST':
        myFile = request.FILES.get('file',None)
        if not myFile:
            res_info['code']='error'
            return HttpResponse(json.dumps(res_info))
        destination = open(r'D:\work\django_work\bilibili_react_antd/dir/'+myFile.name,'wb+')
        for chunk in myFile.chunks():
            destination.write(chunk)
        destination.close()
        res_info['code'] = 'suc'

        return HttpResponse(json.dumps(res_info))