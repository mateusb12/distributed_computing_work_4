#!/usr/bin/env python

import json
from flask import Flask, request
from linkextractor import extract_links
import fix_python_imports
from get_redis_connection import get_redis_connection

app = Flask(__name__)
redis_conn = get_redis_connection()


@app.route("/hello_world")
def hello_world():
    return "Hello World!"


@app.route("/")
def index():
    return "Usage: http://<hostname>[:<prt>]/api/<url>"


@app.route("/api/<path:url>")
def api(url):
    qs = request.query_string.decode("utf-8")
    if qs != "":
        url += "?" + qs

    json_links = None
    if redis_conn:
        json_links = redis_conn.get(url)

    if not json_links:
        links = extract_links(url)
        json_links = json.dumps(links, indent=2)

        if redis_conn:
            redis_conn.set(url, json_links)

    response = app.response_class(
        response=json_links,
        status=200,
        mimetype="application/json"
    )

    return response


if __name__ == '__main__':
    app.run(host="0.0.0.0")
