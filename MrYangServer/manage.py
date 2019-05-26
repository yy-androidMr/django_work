#!/usr/bin/env python
import os
import sys
from pathlib import Path

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MrYangServer.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        # The above import may fail for some other reason. Ensure that the
        # issue is really that Django is missing to avoid masking other
        # exceptions on Python 2.
        try:
            import django
        except ImportError:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            )
        raise
    execute_from_command_line(sys.argv)

p_root = Path(os.path.dirname(os.path.abspath(__file__)))


def root():
    # return os.path.abspath(__file__)
    return p_root
    # return sys.path[0]


def project_root():
    # return os.path.abspath(__file__)
    return os.path.dirname(os.path.abspath(__file__))
    # return sys.path[0]
