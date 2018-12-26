# -*-coding:utf-8 -*-
from __future__ import unicode_literals

from django.db import models


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
    # 文件名称
    name = models.CharField(max_length=100)
    # 父节点
    parent_dir = models.ForeignKey('self', related_name='parent', on_delete=models.CASCADE,
                                   null=True,
                                   blank=True)
    # 自己是否是文件夹
    isdir = models.BooleanField(default=True)
    # 一些标记,存储格式自定义.
    tags = models.CharField(max_length=500, default='')
    # 本地的绝对路径
    abs_path = models.CharField(max_length=500)
    # 相对路径,看各自如何组织
    rel_path = models.CharField(max_length=300)
    # 该文件的根目录类型, movie, pic, doc
    type = models.IntegerField()
    # 有必要给予一个子id.做复杂的父子关系处理
    c_id = models.IntegerField(default=0)

    # # 这是显示等级, 显示不同内容. 不需要,每个功能,独特的level记忆,并不需要dir来处理
    # show_level = models.IntegerField(default=0)

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
    folder_key = models.ForeignKey(Dir, related_name='dir', on_delete=models.CASCADE)
    # 相册名字
    name = models.CharField(max_length=100, default='')
    # 相册简介
    intro = models.CharField(max_length=100, default='')
    # 相册时间
    time = models.CharField(max_length=100, default='')
    # 相册中的指定缩略图
    thum = models.CharField(max_length=100, default='')
    # 展示等级 不需要,dir有展示等级
    level = models.IntegerField(default=0)
    # 其他预留
    param1 = models.CharField(max_length=500, default='')
    param2 = models.CharField(max_length=500, default='')

    def __str__(self):
        return 'id:%s,name:%s,rel_path:%s,intro:%s,time:%s,thum:%s,level:%s,param1:%s,param2:%s' % (
            self.folder_key.c_id, self.name, self.folder_key.rel_path, self.intro, self.time, self.thum,
            self.level,
            self.param1, self.param2)


class MovieInfo(models.Model):
    folder_key = models.ForeignKey(Dir, related_name='movie_dir', on_delete=models.CASCADE)
    # 影片
    name = models.CharField(max_length=200, default='')
    # 影片简介,暂时不需要
    intro = models.CharField(max_length=500, default='')
    # 影片时长:秒
    duration = models.CharField(max_length=100, default='')
    # 影片大小byte
    size = models.CharField(max_length=100, default='')
    # 影片尺寸1280x720
    source_size = models.IntegerField(default=0)
    # 帧率
    fps = models.IntegerField(default=0)
    # 字幕文件
    # 其他预留
    param1 = models.CharField(max_length=500, default='')
    param2 = models.CharField(max_length=500, default='')

    def __str__(self):
        return 'id:%s,name:%s,rel_path:%s,intro:%s,duration:%s,size:%s,source_size:%s,param1:%s,param2:%s' % (
            self.folder_key.c_id, self.name, self.folder_key.rel_path, self.intro, self.duration, self.size,
            self.source_size,
            self.param1, self.param2)


class UpLoadDir(models.Model):
    path = models.CharField(max_length=100, default='')

# models.ImageField
#
# class test(models.Model):
#     f1=1
#
#     def toJSON(self):
#         import json
#         return json.dumps(dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]]))
#
# print(test().toJSON())
