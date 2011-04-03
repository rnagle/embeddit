# Embeddit

A (mostly working) oembed and open graph meta fetcher api.

See <http://embeddit.appspot.com/>

## Ask for oEmbed or Open Graph meta info about a url:
    
    http://embeddit.appspot.com/fetch/?url=http%3A//ogp.me

## Get back a json representation of that info:

    {
        "url": "http:\/\/opengraphprotocol.org\/",
        "image": "http:\/\/opengraphprotocol.org\/open_graph_protocol_logo.png",
        "type": "website",
        "description": "The Open Graph protocol enables any 
        web page to become a rich object in a social graph.",
        "title": "Open Graph Protocol"
    }

## Made to run on App Engine:

But, it uses Flask <http://flask.pocoo.org/>

So it should be simple to refactor and deploy elsewhere.

## Included data/endpoints.json is from:

<http://code.google.com/p/python-oembed/>

