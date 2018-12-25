from __future__ import unicode_literals

import threading
import time

from django.apps import AppConfig

class MryangAppConfig(AppConfig):
    name = 'Mryang_App'

    def ready(self):
        print('app ready')
        threads = threading.enumerate()
        for thread in threads:
            print(thread)
