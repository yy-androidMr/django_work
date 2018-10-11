# coding:utf-8
from django import forms

from Mryang_App.models import User


# error_messages={'required': '请输入用户名'}
class CreateUserF(forms.Form):
    user_name = forms.CharField(max_length=100,
                                label=u'用户名',
                                error_messages={'required': '请输入用户名'}
                                )
    account = forms.CharField(max_length=20)
    pwd = forms.CharField(max_length=200)
    age = forms.IntegerField()

    def flush_to_user(self):
        if (self.is_valid()):
            _user_name = self.cleaned_data['user_name']
            _account = self.cleaned_data['account']
            pwd = self.cleaned_data['pwd']
            age = self.cleaned_data['age']
            User.objects.get(account=_account)
            user = User()
            user.user_name = _user_name
            user.account = _account
            user.pwd = pwd
            user.age = age
            user.save()
            return user


class LoginUserF(forms.Form):
    account = forms.CharField(max_length=20)
    pwd = forms.CharField(max_length=200)

    def check_account(self):
        if (self.is_valid()):
            _account = self.cleaned_data['account']
            _pwd = self.cleaned_data['pwd']
            # noinspection PyBroadException
            try:
                user = User.objects.get(account=_account, pwd=_pwd)
                print('has user,user name=%s' % user.user_name)
                return user
            except:
                # logging.info('abc')
                print('no user')
                return '', ''
                pass

                # def fill_random(self):
                #     user = utils.random_account()
                #     return user


class UserAlbumF(forms.Form):
    album_path = forms.FileField(label=u'上传一张照片',
                                 error_messages={'required': '照片不能为空'})
    name = forms.CharField(max_length=100,
                           label='照片标题')

    def flush_to_album(self):
        if (self.is_valid()):
            album_path = self.cleaned_data['album_path']
            name = self.cleaned_data['name']
            # return user


class upload_f(forms.Form):
    pwd = forms.CharField(max_length=200)

    # def fill_random(self):
    #     user = utils.random_account()
    #     return user
