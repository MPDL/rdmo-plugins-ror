import re

from django.conf import settings
from django.templatetags.static import static
from django.utils.translation import get_language, gettext_lazy as _

import requests

from rdmo.options.providers import Provider

from .handlers import get_name

class RorProvider(Provider):

    search = True
    refresh = True

    def get_options(self, project, search=None, user=None, site=None):
        if search:
            url = getattr(settings, 'ROR_PROVIDER_URL', 'https://api.ror.org/v2/').rstrip('/')
            headers = getattr(settings, 'ROR_PROVIDER_HEADERS', {})

            response = requests.get(url + '/organizations', params={
                'query': self.get_search(search)
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
        return item.get('id', '')
    
    def get_text(self, item):
        ror_id = self.get_id(item)
        ror_name = get_name(item)
        ror_img = static('ror/img/ROR.png')
        ror_link = f'<a href="{ror_id}" target="_blank" ><img height="16" src="{ror_img}" alt="ROR logo" /> {ror_id}</a>'
        # return f'{ror_name} {ror_link}' if ror_name else ror_link
        return f'{ror_name}' if ror_name else ror_link

    def get_search(self, search):
        # reverse get_text to perform the search, remove everything after [
        match = re.match(r'^[^[]+', search)
        if match:
            tokens = match[0].split()
        else:
            tokens = search.split()

        return '+'.join(tokens)