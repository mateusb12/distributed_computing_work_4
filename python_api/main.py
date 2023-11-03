#!/usr/bin/env python

import os
import json
from flask import Flask, request

# Conditionally import redis if REDIS_URL is set
if 'REDIS_URL' in os.environ:
    import redis
    redis_conn = redis.from_url(os.environ["REDIS_URL"])
else:
    redis_conn = None

from linkextractor import extract_links

app = Flask(__name__)

@app.route("/")
def index():
    return "Usage: http://<hostname>[:<prt>]/api/<url>"

@app.route("/api/<path:url>")
def api(url):
    qs = request.query_string.decode("utf-8")
    if qs != "":
        url += "?" + qs

    jsonlinks = None
    # Only use Redis if a connection was established
    if redis_conn:
        jsonlinks = redis_conn.get(url)
    
    if not jsonlinks:
        links = extract_links(url)
        jsonlinks = json.dumps(links, indent=2)
        
        # Only save to Redis if a connection was established
        if redis_conn:
            redis_conn.set(url, jsonlinks)

    response = app.response_class(
        status=200,
        mimetype="application/json",
        response=jsonlinks
    )

    return response

if __name__ == '__main__':
    app.run(host="0.0.0.0")
