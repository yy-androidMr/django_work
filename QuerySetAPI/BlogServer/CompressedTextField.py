# -*- coding: utf-8 -*-
from django.db import models
# 估计是拿来用数据库编码转换的
class CompressedTextField(models.TextField):

    def from_db_value(self,value, expression,connection,context):
        if not value:
            return value
        try:
            return value.decode('base64').decode('bz2').decode('utf-8')
        except Exception:
            return value

    def to_python(self,value):
        if not value:
            return value
        try:
            return value.decode('base64').decode('bz2').decode('utf-8')
        except Exception:
            return value

    def get_prep_value(self,value):
        if not value:
            return value
        try:
            return value.decode('base64')
        except Exception:
            try:
                return value.decode('bz2').decode('utf-8').decode('base64')
            except Exception:
                return value