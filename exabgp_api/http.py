from flask import Flask, request
from sys import stdout


app = Flask(__name__)
app.logger = None


@app.route("/", methods=["POST"])
def command():
    cmd = request.form["command"]
    app.logger.info(cmd)
    stdout.write("%s\n" % cmd)
    stdout.flush()

    return "%s\n" % cmd


def api(host, port, logger):
    app.logger = logger
    app.run(host=host, port=port)
