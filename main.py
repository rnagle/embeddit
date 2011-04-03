import fix_path
import urllib
import re

from google.appengine.api import urlfetch
from google.appengine.api.urlfetch import InvalidURLError, DownloadError
from google.appengine.ext.webapp.util import run_wsgi_app

from flask import Flask, Response, render_template, url_for, request
from BeautifulSoup import BeautifulSoup

from django.utils import simplejson as json
encoder = json.JSONEncoder()
decoder = json.JSONDecoder()

app = Flask('embeddit')

invalid_url = {'error': 'Invalid URL'}
unreachable = {'error': 'Failed to reach the URL'}
empty_meta = {'error': 'Found no meta info for that url'}

# --------------------
# API url
@app.route("/fetch/")
def grab_meta():
    url = request.args.get('url', None)
    callback = request.args.get('callback', None)

    response = grab_oembed_meta(url)
    if 'error' in response:
        # No oembed info found.
        # Fall back to open graph
        response = grab_og_meta(url)

    response = encoder.encode(response)

    if callback is not None:
        response = '%s(%s)' % (callback, response)
        return Response(response, mimetype='application/json')
    else:
        return Response(response, mimetype='application/json')

# --------------------
# Demo
@app.route("/")
def demo():
    return render_template('demo.html')

# --------------------
# Grabbers
def grab_oembed_meta(url):
    try:
        f = open('data/endpoints.json', 'r')
        endpoints = decoder.decode(f.read())

        oembed_url = [ep['endpoint_url'] for ep in endpoints 
                        if re.search(ep['url_re'], url)][0]
        params = urllib.urlencode({'url': url})

        try:
            results = urlfetch.fetch('%s?%s' % (oembed_url, params))
            content = decoder.decode(results.content)
            content['source_type'] = 'oembed'
        except ValueError:
            params = urllib.urlencode({'url': url, 'format': 'json'}) # fragile
            results = urlfetch.fetch('%s?%s' % (oembed_url, params))
            content = decoder.decode(results.content)
            content['source_type'] = 'oembed'
        return content
    except IndexError:
        return empty_meta
    except InvalidURLError:
        return invalid_url
    except DownloadError:
        return unreachable

def grab_og_meta(url):
    try:
        results = urlfetch.fetch(url)
        content = results.content
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
    except InvalidURLError:
        return invalid_url
    except DownloadError:
        return unreachable

# --------------------
# WHO RUN IT???
if __name__ == '__main__':
    run_wsgi_app(app)
