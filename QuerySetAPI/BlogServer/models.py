from __future__ import unicode_literals
from django.db import models

# Create your models here.
from django.utils.encoding import python_2_unicode_compatible

from BlogServer.LIstField import ListField


@python_2_unicode_compatible
class Author(models.Model):
    name = models.CharField(max_length=50)
    qq = models.CharField(max_length=20)
    addr = models.TextField()
    email = models.EmailField()

    def __str__(self):
        return u'%s--%s' % (self.name, self.qq)


@python_2_unicode_compatible
class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Article(models.Model):
    labels = ListField()
    tags = models.ManyToManyField(Tag)
    title = models.CharField(max_length=50)
    author = models.ForeignKey(Author)
    content = models.TextField(null=True, blank=True)
    score = models.IntegerField(default=0)

    def __str__(self):
        return u'%s--%s' % (self.title, self.score)
