# Embeddit

A simple oembed meta fetcher which falls back to open graph info when
oembed is not available.

See <http://embeddit.appspot.com/>

## Ask for oEmbed or Open Graph meta info about a url:

    > oe = Embeddit()
    > result = oe.fetch('http://ogp.me')

## Get back a dictionary of that info:

    > result
    {
        u'description': u'The Open Graph protocol enables any web page to become a rich object in a social graph. ',
        u'image': u'http://ogp.me/logo.png',
        'source_type': 'open_graph',
        u'title': u'Open Graph Protocol',
        u'type': u'website',
        u'url': u'http://ogp.me/'
    }

## Also returns json:

    > oe.fetch_json('http://ogp.me')
    '{
        "description": "The Open Graph protocol enables any web page to become a rich object in a social graph. ",
        "title": "Open Graph Protocol",
        "url": "http://ogp.me/",
        "image": "http://ogp.me/logo.png",
        "source_type": "open_graph",
        "type": "website"
    }'

## Included data/endpoints.json is from:

<http://code.google.com/p/python-oembed/>

