# NOTE: do not try this at home - highly vulnerable ! (SSRF and RCE)
# NOTE: this file should become a simple ssrf example in order to test SSRFmap
# FLASK_APP=example.py flask run

import json
import re
import subprocess

from flask import Flask, abort, request

app = Flask(__name__)


@app.route("/")
def hello():
    return "Simple SSRF Demo App"


# curl -i -X POST -d 'url=http://example.com' http://localhost:5000/form-data
@app.route("/form-data", methods=["POST"])
def curl_post_form_data():
    data = request.values
    content = command("curl {}".format(data.get("url")))
    return content


# curl -i -H "Content-Type: application/json" -X POST -d '{"url": "http://example.com"}' http://localhost:5000/json
@app.route("/json", methods=["POST"])
def curl_post_json():
    data = request.json
    print(data)
    print(data.get("url"))
    content = command("curl {}".format(data.get("url")))
    return content


# curl -v "http://127.0.0.1:5000/query-string?url=http://example.com"
@app.route("/query-string", methods=["GET"])
def curl_get_query_string():
    data = request.values
    content = command("curl {}".format(data.get("url")))
    return content


# curl -X POST -H "Content-Type: application/xml" -d '<run><log encoding="hexBinary">4142430A</log><result>0</result><url>http://google.com</url></run>' http://127.0.0.1:5000/xml
@app.route("/xml", methods=["POST"])
def curl_post_xml():
    data = request.data
    print(data.decode())
    regex = re.compile("url>(.*?)</url")
    try:
        url = regex.findall(data.decode())[0]
        content = command("curl {}".format(url))
        return content
    except Exception as e:
        return e


def command(cmd):
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    return out


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
