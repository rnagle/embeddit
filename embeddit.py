import re

from urllib import urlencode
from urllib2 import urlopen, HTTPError, URLError

from BeautifulSoup import BeautifulSoup
import json as json

encoder = json.JSONEncoder()
decoder = json.JSONDecoder()

invalid_url = {'error': 'Invalid URL'}
unreachable = {'error': 'Failed to reach the URL'}
empty_meta = {'error': 'Found no meta info for that url'}

class Embeddit:

    def fetch(self, url):
        response = self.fetch_oembed_meta(url)
        if 'error' in response:
            # No oembed info found.
            # Fall back to open graph
            response = self.fetch_og_meta(url)
        return response

    def fetch_json(self, url):
        response = self.fetch(url)
        return encoder.encode(response)

    def fetch_oembed_meta(self, url):
        try:
            f = open('data/endpoints.json', 'r')
            endpoints = decoder.decode(f.read())

            oembed_url = [ep['endpoint_url'] for ep in endpoints
                            if re.search(ep['url_re'], url)][0]
            params = urlencode({'url': url})

            try:
                results = urlopen('%s?%s' % (oembed_url, params))
                content = decoder.decode(results.read())
                content['source_type'] = 'oembed'
            except ValueError:
                params = urlencode({'url': url, 'format': 'json'}) # fragile
                results = urlopen('%s?%s' % (oembed_url, params))
                content = decoder.decode(results.read())
                content['source_type'] = 'oembed'
            return content
        except IndexError:
            return empty_meta
        except URLError:
            return invalid_url
        except HTTPError:
            return unreachable

    def fetch_og_meta(self, url):
        try:
            results = urlopen(url)
            content = results.read()
            soup = BeautifulSoup(content)

            meta = soup.findAll('meta')

            content = {}
            for tag in meta:
                if tag.has_key('property'):
                    if re.search('og:', tag['property']) is not None:
                        content[re.sub('og:', '', tag['property'])] = tag['content']

            if content == {}:
                return empty_meta
            else:
                content['source_type'] = 'open_graph'
                return content
        except URLError:
            return invalid_url
        except HTTPError:
            return unreachable

