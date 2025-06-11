from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

import requests

from rdmo.domain.models import Attribute
from rdmo.projects.models import Value

def get_name(item):
    names = item.get('names', [])
    if len(names) > 0:
        ror_display_name = next((n['value'] for n in names if 'ror_display' in n['types']), names[0]['value'])
        return ror_display_name
    
    return ''

@receiver(post_save, sender=Value)
def value_handler(sender, request=None, instance=None, **kwargs):
    # check for ROR_PROVIDER_MAP
    if not getattr(settings, 'ROR_PROVIDER_MAP', None):
        return

    # check if we are importing fixtures
    if kwargs.get('raw'):
        return

    # check if this value instance has an external_id
    if not instance.external_id:
        return

    # loop over ROR_PROVIDER_MAP and check if the value instance attribute is found
    for attribute_map in settings.ROR_PROVIDER_MAP:
        if 'ror' in attribute_map and instance.attribute.uri == attribute_map['ror']:
            # query the orcid api for the record for this orcid
            try:
                url = getattr(settings, 'ROR_PROVIDER_URL', 'https://api.ror.org/v1/').rstrip('/')
                headers = getattr(settings, 'ROR_PROVIDER_HEADERS', {})

                response = requests.get(f'{url}/organizations/{instance.external_id}', headers=headers)
                response.raise_for_status()

                data = response.json()
            except (requests.exceptions.RequestException, requests.exceptions.HTTPError):
                return
            
            if 'ror_id' in attribute_map:
                Value.objects.update_or_create(
                    project=instance.project,
                    attribute=Attribute.objects.get(uri=attribute_map['ror_id']),
                    set_prefix=instance.set_prefix,
                    set_index=instance.set_index,
                    defaults={
                        'text': data.get('id')
                    }
                )

            if 'name' in attribute_map:
                Value.objects.update_or_create(
                    project=instance.project,
                    attribute=Attribute.objects.get(uri=attribute_map['name']),
                    set_prefix=instance.set_prefix,
                    set_index=instance.set_index,
                    defaults={
                        'text': get_name(data)
                    }
                )
