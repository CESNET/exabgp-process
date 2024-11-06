import json
from flask import Flask, request
from sys import stdout


app = Flask(__name__)
app.logger = None


@app.route("/", methods=["POST"])
def command():
    cmd = request.form["command"]
    route = json.loads(cmd)
    app.logger.info(cmd)
    stdout.write("%s\n" % route["command"])
    stdout.flush()

    return "%s\n" % cmd


def api(host, port, logger):
    app.logger = logger
    app.run(host=host, port=port)
