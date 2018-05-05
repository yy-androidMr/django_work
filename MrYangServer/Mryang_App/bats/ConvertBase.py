# coding=utf-8
import os
import traceback

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MrYangServer.settings')
django.setup()
from Mryang_App.models import Dir


class ConvertBase:
    def walk_call(self, abs_path, rel_path, parent_dir, name, is_dir):
        pass

    def walk_over(self):
        pass

    def flush_dirs(self, source_path, rel_path, is_dir, name, type):
        source_path = source_path.replace('\\', '/')
        self_abs_path = os.path.realpath(source_path).replace('\\', '/')
        # self_abs_path += ('/' if is_dir else '')
        parent_abs_path = os.path.dirname(self_abs_path)
        parent = None
        try:
            parent = Dir.objects.get(abs_path=parent_abs_path)
        except Exception as e:
            print('%s:%s' % (parent_abs_path, e))
            pass

        self.walk_call(self_abs_path, rel_path, parent, name, is_dir)

    def create_dirs(self, media_root, depth_name, type):
        movie_name = depth_name
        movie_root = os.path.join(media_root, movie_name)
        self.flush_dirs(movie_root, movie_name, True, depth_name, type)

        movie_root = movie_root.replace('\\', '/')
        for root, dirs, files in os.walk(movie_root):
            for dir in dirs:
                source_path = os.path.join(root, dir).replace('\\', '/')
                rel_path = source_path[len(movie_root):]
                self.flush_dirs(source_path, rel_path, True, dir, type)

            for file in files:
                source_path = os.path.join(root, file).replace('\\', '/')
                rel_path = source_path[len(movie_root):]
                self.flush_dirs(source_path, rel_path, False, file, type)

    def insert_dirs(self, c_type, root, depth_name):
        Dir.objects.filter(type=c_type).delete()
        self.create_dirs(root, depth_name, c_type)
        self.walk_over()
        pass
