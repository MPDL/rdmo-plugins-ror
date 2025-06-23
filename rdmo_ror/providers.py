import re

from django.conf import settings
from django.utils.translation import gettext_lazy as _

import requests

from rdmo.options.providers import Provider

from .handlers import get_name

class RorProvider(Provider):

    search = True
    refresh = True

    widget_props = {
        'noOptionsMessage_text': _('No options found: try a different search term or another language')
    }

    def get_options(self, project, search=None, user=None, site=None):
        if search and len(search) > 2:
            url = getattr(settings, 'ROR_PROVIDER_URL', 'https://api.ror.org/v1/').rstrip('/')
            headers = getattr(settings, 'ROR_PROVIDER_HEADERS', {})

            response = requests.get(url + '/organizations', params={
                'query': self.get_search(search)
                # 'affiliation': self.get_search(search)
            }, headers=headers)

            try:
                data = response.json()
            except requests.exceptions.JSONDecodeError:
                pass
            else:
                if data.get('items'):
                    return [
                        {
                            'id': self.get_id(item),
                            'text': self.get_text(item)
                        } for item in data['items']
                    ]

        # return an empty list by default
        return []

    def get_id(self, item):
        return item.get('id', '').replace('https://ror.org/', '')
    
    def get_text(self, item):
        return '{name} [{id}]'.format(name=get_name(item), id=self.get_id(item))

    def get_search(self, search):
        # reverse get_text to perform the search, remove everything after [
        match = re.match(r'^[^[]+', search)
        if match:
            tokens = match[0].split()
        else:
            tokens = search.split()

        return '+'.join(tokens)