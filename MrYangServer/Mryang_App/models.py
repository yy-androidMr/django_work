# -*-coding:utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import json


# Create your models here.
class User(models.Model):
    token = models.CharField(max_length=100, primary_key=True)
    user_name = models.CharField(max_length=100)
    account = models.CharField(max_length=20)
    pwd = models.CharField(max_length=200)
    age = models.IntegerField(default=0)
    regist_time = models.DateField(auto_now_add=True)
    modify_time = models.DateField(auto_now=True)

    def __str__(self):
        return 'token:%s,user_name:%s,account:%s,pwd:%s' % (self.token, self.user_name, self.account, self.pwd)


class UserAlbum(models.Model):
    user_token = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=100)
    video_path = models.FileField(upload_to='video/', null=True)
    album_path = models.FileField(upload_to='album/', null=True)
    upload_time = models.DateField(auto_now_add=True)
    modify_time = models.DateField(auto_now=True)

    def __str__(self):
        return 'name:%s' % (self.name)


class Dir(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    parent_dir = models.ForeignKey('self', related_name='parent', on_delete=models.CASCADE, null=True, blank=True)
    isdir = models.BooleanField(default=True)
    # 一些标记,存储格式自定义.
    tags = models.CharField(max_length=100, default='')
    # 本地的绝对路径
    abs_path = models.CharField(max_length=100)
    # 相对路径,看各自如何组织
    rel_path = models.CharField(max_length=100)
    # 该文件的根目录类型, movie, pic, doc
    type = models.IntegerField()
    # 有必要给予一个子id.做复杂的父子关系处理
    c_id = models.IntegerField(default=0)
    # 这是显示等级, 显示不同内容.
    show_level = models.IntegerField(default=0)

    def __str__(self):
        if self.parent_dir is None:
            parent_dir_name = 'None'
        else:
            parent_dir_name = self.parent_dir.name
        return 'id:%s,name:%s,isDir:%r,parent_dir:%s,tags:%s,rel_path:%s,type:%s,c_id:%s' % (
            self.id, self.name, self.isdir, parent_dir_name, self.tags, self.rel_path, self.type, self.c_id)


    # def to_json(self):
    #     map = {'c_id': self.c_id, 'rel_path': self.rel_path}
    #     # print([f.name for f in self._meta.fields])
    #     return json.dumps(dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]]))


class GalleryInfo(models.Model):
    # 对应Dir的c_id
    id = models.AutoField(primary_key=True)
    # 相册对应的文件夹名称
    dir_name = models.CharField(max_length=100, default='')
    # 相册名字
    name = models.CharField(max_length=100, default='')
    # 相册简介
    intro = models.CharField(max_length=100, default='')
    # 相册时间
    time = models.CharField(max_length=100, default='')
    # 相册中的指定缩略图
    thum = models.CharField(max_length=100, default='')
    # 展示等级
    level = models.CharField(max_length=100, default='')
    # 其他预留
    param1 = models.CharField(max_length=100, default='')
    param2 = models.CharField(max_length=100, default='')

    def __str__(self):
        return 'id:%s,dir_name:%s,name:%s,intro:%s,time:%s,thum:%s,level:%s,param1:%s,param2:%s' % (
            self.id, self.dir_name, self.name, self.intro, self.time, self.thum, self.level, self.param1, self.param2)

    def dict(self):
        dic = dict([(attr, getattr(self,attr)) for attr in [f.name for f in self._meta.fields]])
        # return dicts
        # self.param2
        # getattr
        return dic


class UpLoadDir(models.Model):
    path = models.CharField(max_length=100, default='')

#
# class test(models.Model):
#     f1=1
#
#     def toJSON(self):
#         import json
#         return json.dumps(dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]]))
#
# print(test().toJSON())
