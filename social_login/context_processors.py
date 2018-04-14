# -*- coding: utf-8 -*-

from socialoauth import socialsites
from socialoauth.utils import import_oauth_class

from .utils import LazyList

# add 'social_login.context_processors.social_sites' in TEMPLATE_CONTEXT_PROCESSORS
# then in template, you can get this sites via {% for s in social_sites %} ... {% endfor %}
# Don't worry about the performance,
# `social_sites` is a lazy object, it readly called just access the `social_sites`


def social_sites(request):
    def _social_sites():
        def make_site(s):
            s = import_oauth_class(s)()
            return {
                'site_id': s.site_id,
                'site_name': s.site_name,
                'site_name_zh': s.site_name_zh,
                'authorize_url': s.authorize_url,
            }
        return [make_site(s) for s in socialsites.list_sites()]
    
    return {'social_sites': LazyList(_social_sites)}
