# Embeddit

A simple oembed meta fetcher which falls back to open graph info when
oembed is not available.

## Ask for oEmbed or Open Graph meta info about a url:

    > oe = Embeddit()
    > result = oe.fetch('http://vimeo.com/33211636')

## Get back a dictionary of that info:

    > result
    {
        u'count': u'22906',
        u'description': u'During 3 years (2008-2011) i have been drawing 12 drawing of animation every day, it make one second of film. I had no plans what so ever before starting the first drawing. And then, each of the folowing days, I took the 3 last drawing from the day before...',
        u'image': u'http://b.vimeocdn.com/ts/225/276/225276903_640.jpg',
        u'site_name': u'Vimeo',
        u'source_type': 'open_graph',
        u'title': u'12 Drawings a Day - 12 Dessins par Jour',
        u'type': u'article',
        u'url': u'http://vimeo.com/33211636',
        u'video': u'http://vimeo.com/moogaloop.swf?clip_id=33211636',
        u'video:height': u'360',
        u'video:type': u'application/x-shockwave-flash',
        u'video:width': u'640'
    }

## Also returns json:

    > oe.fetch_json('http://vimeo.com/33211636')
    '{
        "count": "22906",
        "site_name": "Vimeo",
        "description": "During 3 years (2008-2011) i have been drawing 12 drawing of animation every day, it make one second of film. I had no plans what so ever before starting the first drawing. And then, each of the folowing days, I took the 3 last drawing from the day before...",
        "title": "12 Drawings a Day - 12 Dessins par Jour",
        "url": "http://vimeo.com/33211636",
        "image": "http://b.vimeocdn.com/ts/225/276/225276903_640.jpg",
        "video:type": "application/x-shockwave-flash",
        "video:height": "360",
        "source_type": "open_graph",
        "video": "http://vimeo.com/moogaloop.swf?clip_id=33211636",
        "video:width": "640",
        "type": "article"
    }'

## Included data/endpoints.json is from:

<http://code.google.com/p/python-oembed/>

