# -*- coding: utf-8 -*-
import random
import sys, os, django

# 导入路径
proj_abs_path = os.path.abspath(os.path.join(sys.argv[0], '../../..'))
sys.path.append(proj_abs_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'QuerySetAPI.settings')
django.setup()
# end
from BlogServer.models import Author, Tag, Article

author_name_list = ['Yang1', 'Yang2', 'MrYang', 'MySite', 'YangYu', 'abc', 'def', 'acd']
article_title_list = ['Django teach', 'python teach', 'html5 teach']


def create_authors():
    for author_name in author_name_list:
        author, createrd = Author.objects.get_or_create(name=author_name)
        if createrd == True:
            author.qq = ''.join(
                str(random.choice(range(10))) for _ in range(9)
            )
            random_addr = ''.join(
                str(random.choice(range(10))) for _ in range(4)
            )
            author.addr = 'address_%s' % (random_addr)
            author.email = '%s@123.com' % (author.qq)
            author.save()


def create_articles_and_tags():
    for article_title in article_title_list:
        tag_name = article_title.split(' ', 1)[0]
        tag, created = Tag.objects.get_or_create(name=tag_name)
        random_author = random.choice(Author.objects.all())
        for i in range(1, 12):
            title = '%s_%s' % (article_title, i)
            article, created = Article.objects.get_or_create(
                title=title, author=random_author, content='%s 这是内容' % title, score=random.randrange(70, 101)

                # defaults={
                #     'author': random_author
                # }
            )
            article.tags.add(tag)


def main():
    create_authors()
    create_articles_and_tags()

    # 代表只能自己运行自己


if __name__ == '__main__':
    main()
    print('done!:')
