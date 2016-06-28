import os
import re
import json
import requests
import fnmatch

from urllib import urlencode
from BeautifulSoup import BeautifulSoup

_ROOT = os.path.abspath(os.path.dirname(__file__))

invalid_url = {'error': 'Invalid URL'}
unreachable = {'error': 'Failed to reach the URL'}
empty_meta = {'error': 'Found no meta info for that url'}


class Embeddit(dict):

    url = None
    fetched = False

    def __init__(self, url=None, *args, **kwargs):
        if url:
            self.url = url
            self.fetch()

    def fetch(self, force=False):
        if self.fetched and not force:
            return self

        response = self.fetch_oembed_meta()

        if 'error' in response:
            # No oembed info found.
            # Fall back to open graph
            response = self.fetch_og_meta()

        self.clear()
        self.update(response)
        self.fetched = True

        return response

    def to_json(self):
        if not self.fetched:
            self.fetch()
        return json.dumps(self)

    def fetch_oembed_meta(self):
        try:
            f = open(get_data('providers.json'), 'r')
            providers = json.loads(f.read())
            oembed_url = None

            for provider in providers:
                for endpoint in provider.get('endpoints', []):
                    for schema in endpoint.get('schemes', []):
                        if not schema.startswith('http://*') or not schema.startswith('https://*'):
                            schema = schema.replace('http://', 'http://*')
                            schema = schema.replace('https://', 'https://*')
                        if fnmatch.fnmatch(self.url, schema):
                            oembed_url = endpoint.get('url')
                            break

                if not oembed_url:
                    provider_urls = [
                        provider.get('provider_url'),
                        provider.get('provider_url').replace('http://', 'https://')
                    ]
                    for provider_url in provider_urls:
                        if fnmatch.fnmatch(self.url,  provider_url + "*"):
                            oembed_url = provider.get('endpoints')[0].get('url')
                            break

            if not oembed_url:
                return invalid_url

            params = urlencode({'url': self.url})

            try:
                results = requests.get('%s?%s' % (oembed_url.replace('{format}', 'json'), params))
                content = json.loads(results.content)
                content[u'source_type'] = 'oembed'
            except ValueError:
                params = urlencode({'url': self.url, 'format': 'json'})
                results = requests.get('%s?%s' % (oembed_url, params))
                content = json.loads(results.content)
                content[u'source_type'] = 'oembed'
            return content
        except IndexError:
            return empty_meta
        except requests.exceptions.InvalidSchema:
            return invalid_url
        except requests.exceptions.HTTPError:
            return unreachable

    def fetch_og_meta(self):
        try:
            results = requests.get(self.url)
            soup = BeautifulSoup(results.content)
            meta = soup.findAll('meta')

            content = {}
            for tag in meta:
                if tag.has_key('property'):
                    if re.search('og:', tag['property']) is not None:
                        key = re.sub('og:', '', tag['property'])
                        content[key] = tag['content']

            if content == {}:
                return empty_meta
            else:
                content[u'source_type'] = 'open_graph'
                return content
        except requests.exceptions.InvalidSchema:
            return invalid_url
        except requests.exceptions.HTTPError:
            return unreachable


def get_data(path):
    return os.path.join(_ROOT, 'data', path)
