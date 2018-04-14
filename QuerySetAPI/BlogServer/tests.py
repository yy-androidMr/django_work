from django.test import TestCase

# Create your tests here.
import os, sys, django

proj_abs_path = os.path.abspath(os.path.join(sys.argv[0], '../..'))
sys.path.append(proj_abs_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'QuerySetAPI.settings')
django.setup()

from django.db.models import Count, Avg, Sum
from BlogServer.models import Article

# vtagValue = Article.objects.all().annotate(count=Count('author')).values('author_id', 'count')
# print(vtagValue)

# print(Article.objects.all().annotate(count=Count('author')).values('author_id', 'count').query)

# a_id = Article.objects.all().values('author_id').annotate(avg_score=Avg('score')).values('author_id','avg_score')
# print(a_id)

# a_id = Article.objects.all().values('author_id').annotate(sum_score=Sum('score')).values('author_id','sum_score')
# print(a_id)

# articles = Article.objects.all().select_related('author')[:10]
# print ("complete sql la")
# a1 = articles[0]
# print ('get a1')
# a1.title
# print  ('get a1 title')
# a1.author.name
# print  ('get author name')
# print(articles[0].tags.name)


# articles = Article.objects.all().prefetch_related('tags')[:10]
# print articles

#
# articles = Article.objects.all().prefetch_related('tags')[:3]
# for a in articles:
#     print 'title is _______________:',a.title,a.tags.all()


# querySet = Article.objects.all().only('content')
# print 'query over'
# print querySet

# queryKey = Article.objects.all().only('content','author')
# print queryKey
# mylabel =  Article().labels
# mylabel =['python','django','yy']
# print mylabel

from BlogServer.models import Article
tempField = Article()
tempField.labels = ['django yy']
tempField.labels.append('custom field yy')
tempField.content = u'i am test custom field content, 11'
tempField.save()