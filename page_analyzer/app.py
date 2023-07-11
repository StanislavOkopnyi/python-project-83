from flask import Flask, render_template


app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/urls/")
def urls_list():
    sites = []
    return render_template(
        "urls.html",
        sites=sites
    )
