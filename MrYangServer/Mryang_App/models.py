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
        return 'name:%s' % self.name


class Dir(models.Model):
    id = models.AutoField(primary_key=True)
    # 文件名称
    name = models.CharField(max_length=100)
    # 父节点
    parent_dir = models.ForeignKey('self', related_name='parent', on_delete=models.CASCADE,
                                   null=True,
                                   blank=True,
                                   db_index=True)
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
    # 原始路径 绝对路径
    abs_path = models.CharField(max_length=500, default='')
    # 输出路径
    desc_path = models.CharField(max_length=500, default='')
    # 输出相对路径,做显示用.一张图片PicInfo.需要和这个拼接.
    desc_real_path = models.CharField(max_length=500, default='')
    # 相册名称
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


class PicInfo(models.Model):
    gallery_key = models.ForeignKey(GalleryInfo, related_name='gallery', on_delete=models.CASCADE)
    # 都是相对路径. 相对于GalleryInfo
    res = models.CharField(max_length=500, default='')
    # 图片名称, 需要和GalleryInfo.desc_real_path 拼接.做显示用, middle和thum都用这个
    name = models.CharField(max_length=200)
    # 原图片大小.
    size = models.IntegerField(default=0)
    # 原图片尺寸
    width = models.IntegerField(default=0)
    height = models.IntegerField(default=0)


# 在service做转换的时候的src文件进度
class Media(models.Model):
    id = models.AutoField(primary_key=True)
    #   文件绝对路径.
    abs_path = models.CharField(max_length=500, default='')
    # 输出路径
    desc_path = models.CharField(max_length=500, default='')
    # m3u8
    m3u8_path = models.CharField(max_length=500, default='')
    #  nginx访问路径
    nginx_path = models.CharField(max_length=500, default='')
    #  文件md5
    md5 = models.CharField(max_length=100, default='')
    # 时长:秒
    duration = models.IntegerField(default=0)
    # 占用大小: bytes
    size = models.IntegerField(default=0)
    # 文件名
    file_name = models.CharField(max_length=100, default='')
    # 编码格式
    codec_type = models.CharField(max_length=20, default='')
    codec_long_name = models.CharField(max_length=200, default='')

    # 画面尺寸
    width = models.IntegerField(default=0)
    height = models.IntegerField(default=0)

    # 帧率  四舍五入,
    r_frame_rate = models.IntegerField(default=0)
    avg_frame_rate = models.IntegerField(default=0)
    # 该文件当前状态 存在 MediaService.STATE_INIT中
    state = models.IntegerField(default=-1)
    #  父文件夹  理论上不可能是空
    folder_key = models.ForeignKey(Dir, related_name='p_dir', null=True,
                                   blank=True, on_delete=models.CASCADE)
    # 字幕文件
    # 其他预留
    param1 = models.CharField(max_length=500, default='')  # 这里存储m3u8路径
    param2 = models.CharField(max_length=500, default='')  # 这里存储缩略图路径
