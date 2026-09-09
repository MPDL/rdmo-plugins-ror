rdmo-plugins-ror (MaxIT fork - adapted for the SMP catalogue)
================

This plugin implements dynamic option set, that queries the expanded-search endpoint of the [ROR API](https://ror.readme.io/docs/rest-api).


Setup
-----

Install the plugin in your RDMO virtual environment using pip (directly from GitHub):

```bash
pip install git+https://github.com/MPDL/rdmo-plugins-ror
```

Add the `rdmo_ror` app to `INSTALLED_APPS` and the plugin to `OPTIONSET_PROVIDERS` in `config/settings/local.py`:

```python
INSTALLED_APPS += ['rdmo_ror']

...

OPTIONSET_PROVIDERS += [
    ('ror', _('ROR Provider'), 'rdmo_ror.providers.RorProvider')
]
```

The option set provider should now be selectable for option sets in your RDMO installation. For a minimal example catalog, see the files in `xml`.


## Settings for the SMP catalogue

```python
ROR_PROVIDER_URL = 'https://api.ror.org/v2/'

ROR_STORE_NAME = True

ROR_PROVIDER_MAP = [
    {
        'ror': 'https://rdmo.mpdl.mpg.de/terms/domain/project/partner/affiliation/ror-autocomplete',
        'ror_id': 'https://rdmo.mpdl.mpg.de/terms/domain/project/partner/affiliation/ror-id',
        'name': 'https://rdmo.mpdl.mpg.de/terms/domain/project/partner/affiliation'
    }
]
```

In this case, updating the ROR search value for a contributor (`https://rdmo.mpdl.mpg.de/terms/domain/project/partner/affiliation/ror-autocomplete`) will update their ror id and affiliation automatically.


## General example

If a selection of a ROR ID should update other fields, you can add a `ROR_PROVIDER_MAP` in your settings, e.g.:

```python
ROR_PROVIDER_MAP = [
    {
        'ror': 'https://rdmorganiser.github.io/terms/domain/project/partner/ror',
        'alias': 'https://rdmorganiser.github.io/terms/domain/project/partner/id',
        'acronym': 'https://rdmorganiser.github.io/terms/domain/project/partner/id',
        'name': 'https://rdmorganiser.github.io/terms/domain/project/partner/name',
    }
]
```

In this case, a change to the identifier of a partner (`https://rdmorganiser.github.io/terms/domain/project/partner/ror`) will update their name (`https://rdmorganiser.github.io/terms/domain/project/partner/name`) automatically. `ROR_PROVIDER_MAP` is a list of mappings, since multiple ROR ID could be used and should update different other values.

While not required, you can add a custom `User-Agent` to your requests so that the provider can perform statistical analyses and, if you add an email address, might contact you. This can be done by adding the following to your settings.

```python
ROR_PROVIDER_HEADERS = {
    'User-Agent': 'rdmo.example.com/1.0 (mail@rdmo.example.com) rdmo-plugins-ror/1.0'
}
```

By default, the plugin stores the name of the institution and the link to the ROR page as `text` in RDMO (the ROR itself is stored as `external_id`). The name of the institution can be omitted by setting:

```python
ROR_STORE_NAME = False
```
