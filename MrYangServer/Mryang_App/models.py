# -*-coding:utf-8 -*-
from __future__ import unicode_literals

from django.db import models


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


# 模型1: 定级文件夹,不定文件名--[展示]:展示最多2级.如有需求变更,需要更新数据库.
# 模型2: 不定文件夹,定文件名 --[展示]:展示不定文件夹,如有需求变更?
class Movie(models.Model):
    # 举例/static/media/movie\depth0\depth3_4\竞技场进入.mp4

    # 竞技场进入.mp4
    name = models.CharField(max_length=100)
    # depth0\depth3_4\竞技场进入.mp4
    nginx_path = models.CharField(max_length=100, primary_key=True)

    # movie\depth0\depth3_4\竞技场进入.mp4
    static_path = models.FileField(upload_to='movie', null=True)
    length = models.CharField(max_length=50, default='0')
    time = models.CharField(max_length=100, default='0')
    #  depth3_4\
    dir = models.CharField(max_length=100, default='')
    # 这个文件的文件夹深度. 0
    depth = models.IntegerField(default=0)

    def __str__(self):
        return 'name:%s, 大小:%s, 时长:%s nginx路径:%s,文件夹深度:%s,文件夹:%s' % (
            self.name, self.length, self.time, self.nginx_path, self.depth, self.dir)


class Dir(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    parent_dir = models.ForeignKey('self', related_name='child', on_delete=models.CASCADE, null=True, blank=True)
    isdir = models.BooleanField(default=True)
    # 一些标记,存储格式自定义.
    tags = models.CharField(max_length=100, default='')
    # 本地的绝对路径
    abs_path = models.CharField(max_length=100)
    # 相对路径,看各自如何组织
    rel_path = models.CharField(max_length=100)
    # 该文件的根目录类型, movie, pic, doc
    type = models.IntegerField()

    def __str__(self):
        parent_dir_name = ''
        if (self.parent_dir is None):
            parent_dir_name = 'None'
        else:
            parent_dir_name = self.parent_dir.name
        return 'name:%s,isDir:%r,parent_dir:%s,tags:%s,abs_path:%s,rel_path:%s,type:%s' % (
            self.name, self.isdir, parent_dir_name, self.tags, self.abs_path, self.rel_path, self.type)
