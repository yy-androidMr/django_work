from django.db import models

# Create your models here.
__author__ = 'junxi'



class OAuthQQ(models.Model):
    """QQ and User Bind"""
    # user = models.ForeignKey(UserProfile)  # 关联用户信息表
    qq_openid = models.CharField(max_length=64)  # QQ的关联OpenID

    # def __str__(self):
    #    return self.user