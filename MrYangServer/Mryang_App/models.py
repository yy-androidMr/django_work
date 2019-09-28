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


# class GalleryInfo(models.Model):
#     # folder_key = models.ForeignKey(Dir, related_name='dir', on_delete=models.CASCADE)
#     # 原始路径 绝对路径
#     # abs_path = models.CharField(max_length=500, default='')
#     # 源的相对路径.
#     src_real_path = models.CharField(max_length=500, default='', unique=True)
#
#     mulit_path = models.ManyToManyField('MPath')
#     # 输出相对路径,做显示用.一张图片PicInfo.需要和这个拼接.
#     desc_real_path = models.CharField(max_length=500, unique=True)
#     # 相册名称
#     name = models.CharField(max_length=100, default='')
#     # 相册简介
#     intro = models.CharField(max_length=100, default='')
#     # 相册时间
#     time = models.CharField(max_length=100, default='')
#     # 相册中的指定缩略图
#     thum = models.CharField(max_length=100, default='')
#     # 展示等级 不需要,dir有展示等级
#     level = models.IntegerField(default=0)
#     # 显示该相册
#     hidden = models.BooleanField(default=False)
#     # 其他预留
#     param1 = models.CharField(max_length=500, default='')
#     param2 = models.CharField(max_length=500, default='')
#
#     def __str__(self):
#         return 'id:%s,name:%s,intro:%s,time:%s,thum:%s,level:%s,param1:%s,param2:%s' % (
#             self.src_real_path, self.name, self.intro, self.time, self.thum,
#             self.level, self.param1, self.param2)


# class PicInfo(models.Model):
#     gallery_key = models.ForeignKey(GalleryInfo, related_name='gallery', on_delete=models.CASCADE)
#     # mpath = models.
#     # src中的文件绝对路径.
#     src_abs_path = models.CharField(max_length=500)
#
#     src_name = models.CharField(max_length=50, default='')
#     # desc_root_dir = models.ForeignKey(Dir, related_name='dir', on_delete=models.CASCADE)
#     # 这是文件的md5值!!暂时没用到.
#     src_md5 = models.CharField(max_length=50, default='')
#     # 图片名称, 需要和desc_mpath/GalleryInfo.desc_real_path 拼接.做显示用, middle和thum都用这个,没有后缀.要加
#     # 是src_name的md5化
#     desc_name = models.CharField(max_length=100)
#     # 图片后缀. 如果是gif. thum后缀是jpg, middle后缀是gif. webp没有后缀.
#     ext = models.CharField(max_length=20, default='')
#     # 原图片大小.
#     size = models.IntegerField(default=0)
#     # 缩放后大小
#     m_size = models.IntegerField(default=0)
#     # 原图片尺寸
#     width = models.IntegerField(default=0)
#     height = models.IntegerField(default=0)
#     # 缩放后的图片尺寸
#     m_width = models.IntegerField(default=0)
#     m_height = models.IntegerField(default=0)
#     # 该文件当前状态 存在 PicHelp.STATE_INIT中
#     state = models.IntegerField(default=-1)
#     # 是否是gif
#     is_gif = models.BooleanField(default=False)
#     # 分目录的外键 做显示用 其他的用不着吧
#     desc_mpath = models.ForeignKey('MPath', related_name='desc_mpath', on_delete=models.DO_NOTHING, null=True,
#                                    blank=True)
#     src_mpath = models.ForeignKey('MPath', related_name='src_mpath', on_delete=models.CASCADE)
#
#     def __eq__(self, other):
#         if other.src_file_md5 and other.src_path:
#             eq_bool = other.src_file_md5 == self.src_md5 and other.src_path == self.src_name
#             return eq_bool
#         return super().__eq__(other)
#
#     def __hash__(self):
#         return super().__hash__()


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


# 路径存储.
class MPath(models.Model):
    id = models.AutoField(primary_key=True)
    # # 文件夹绝对路径.
    # path = models.CharField(max_length=500, default='', unique=True)
    # 该文件夹类型: 0 无意义, 1 src, 2 desc
    type = models.IntegerField(default=0, verbose_name=u'文件夹的类型(1.src,2.desc)')
    # 使用优先级.相同的话根据id排序 0为最低
    level = models.IntegerField(default=0, verbose_name=u'放置优先级,数字越大优先级越高')
    # 剩余多少M 就不填了
    drive_memory_mb = models.IntegerField(default=8192, verbose_name=u'磁盘剩余空间小于此数值时,不选择此路径')
    dir = models.OneToOneField(Dir, on_delete=models.CASCADE)
    # dir = models.ForeignKey(Dir, related_name='dir_info', on_delete=models.CASCADE, unique=True)
    # 预留  param1: dir__abs_path的md5值
    param1 = models.CharField(max_length=500, default='')
    param2 = models.CharField(max_length=500, default='')


class PhotoWall(models.Model):
    # folder_key = models.ForeignKey(Dir, related_name='dir', on_delete=models.CASCADE)
    # 原始路径 绝对路径
    # abs_path = models.CharField(max_length=500, default='')
    # d原始名称
    name = models.CharField(max_length=100, default='')
    # 修改后的显示昵称
    nick = models.CharField(max_length=100, default='')
    # 相册简介
    intro = models.CharField(max_length=100, default='')
    # 相册时间
    time = models.CharField(max_length=100, default='')
    # 相册中的指定缩略图
    thum_photo = models.ForeignKey('Photo', related_name='photo', on_delete=models.SET_NULL, null=True,
                                   blank=True)
    # 展示等级 不需要,dir有展示等级
    level = models.IntegerField(default=0)
    # 显示该相册
    hidden = models.BooleanField(default=False)
    # 其他预留
    param1 = models.CharField(max_length=500, default='')
    param2 = models.CharField(max_length=500, default='')

    def __str__(self):
        return 'id:%s,name:%s,intro:%s,time:%s,thum:%s,level:%s,param1:%s,param2:%s' % (
            self.id, self.name, self.intro, self.time, self.thum_photo_id,
            self.level, self.param1, self.param2)


class Photo(models.Model):
    # gallery_key = models.ForeignKey(GalleryInfo, relatedk_name='gallery', on_delete=models.CASCADE)
    # src中的文件绝对路径.
    src_abs_path = models.CharField(max_length=500)

    # 这是文件的md5值!!暂时没用到.
    src_md5 = models.CharField(max_length=50, default='')
    #  desc_mpath + desc_dir + src_md5 +  ext  显示拼接
    #  输出,在middle,thum下的的相对路径, 之前设想通过拼接.  23个文件,减少12k.如果后续有问题.则需要调整.
    desc_rela_path = models.CharField(max_length=100)
    # 图片后缀. 如果是gif. thum后缀是jpg, middle后缀是gif. webp没有后缀.
    ext = models.CharField(max_length=20, default='')
    # 原图片大小.
    src_size = models.IntegerField(default=0)
    # 缩放后大小
    mid_size = models.IntegerField(default=0)
    # 原图片尺寸
    src_width = models.IntegerField(default=0)
    src_height = models.IntegerField(default=0)
    # 缩放后的图片尺寸
    mid_width = models.IntegerField(default=0)
    mid_height = models.IntegerField(default=0)
    # 该文件当前状态 存在 PicHelp.STATE_INIT中
    state = models.IntegerField(default=-1)
    # 是否是gif
    is_gif = models.BooleanField(default=False)
    # 分目录的外键 做显示用 其他的用不着吧
    # src_dir=models.ForeignKey(Dir, related_name='src_dir', on_delete=models.DO_NOTHING, null=True,
    #                                blank=True)
    # desc_dir=models.ForeignKey(Dir, related_name='desc_dir', on_delete=models.DO_NOTHING, null=True,
    #                                blank=True)
    desc_mpath = models.ForeignKey('MPath', related_name='min_mpath', on_delete=models.DO_NOTHING, null=True,
                                   blank=True)
    src_mpath = models.ForeignKey('MPath', related_name='src_mpath', on_delete=models.DO_NOTHING, null=True,
                                  blank=True)
    photo_wall = models.ForeignKey(PhotoWall, related_name='photo_wall', on_delete=models.DO_NOTHING, null=True,
                                   blank=True)
    #创建时间和修改时间
    ctime = models.IntegerField(default=-1)
    mtime = models.IntegerField(default=-1)

    def __eq__(self, other):
        # if other.src_file_md5 and other.src_path:
        #     eq_bool = other.src_file_md5 == self.src_md5 and other.src_path == self.src_name
        #     return eq_bool
        return super().__eq__(other)

    def __hash__(self):
        return super().__hash__()
