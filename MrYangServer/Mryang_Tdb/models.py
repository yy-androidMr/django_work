from Mryang_App.apps import MryangAppConfig
from django.db import models
from Mryang_App.models import Dir as Main_Dir
from Mryang_App.models import GalleryInfo as Main_GalleryInfo

from frames import yutils


# from Mryang_App import models
#
# models.dir_foregin_name = MryangAppConfig.name + '.TDir'




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

    def __str__(self):
        if self.parent_dir is None:
            parent_dir_name = 'None'
        else:
            parent_dir_name = self.parent_dir.name
        return 'id:%s,name:%s,isDir:%r,parent_dir:%s,tags:%s,rel_path:%s,type:%s,c_id:%s' % (
            self.id, self.name, self.isdir, parent_dir_name, self.tags, self.rel_path, self.type, self.c_id)

    class Meta:
        db_table = MryangAppConfig.name + '_' + Main_Dir.__name__.lower()


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

    class Meta:
        db_table = MryangAppConfig.name + '_' + Main_GalleryInfo.__name__.lower()
