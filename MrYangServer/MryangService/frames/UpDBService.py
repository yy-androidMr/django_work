#
# class DLInfo(models.Model):
#     src_mpath = models.ForeignKey('MPath', related_name='src_mpath', on_delete=models.DO_NOTHING, null=True,
#                                   blank=True)
#     # 下载的相对路径
#     rela_path = models.CharField(max_length=500)
#     # 当前
#     state = models.IntegerField(default=-1)
#     # url.  需要判断是否是m3u8
#     url = models.CharField(max_length=500)
#     # 文件类型 mp4  m3u8
#     file_type = models.IntegerField(default=-1)
#     # 该文件名. 需要有后缀.
#     file_name = models.CharField(max_length=200)
