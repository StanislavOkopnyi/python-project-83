import os
import dotenv
from flask import (
    Flask,
    flash,
    get_flashed_messages,
    redirect,
    render_template,
    request,
    url_for,
)
from validators.url import url as url_validator
from urllib.parse import urlparse
from psycopg2.errors import UniqueViolation

from .database import DB

dotenv.load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

database = DB()


@app.get("/")
def index_get():
    messages = get_flashed_messages(with_categories=True)
    return render_template("index.html", messages=messages)


@app.post("/")
def index_post():
    data = request.form.to_dict()

    # URL validation
    if url_validator(data["url"]) is True:
        parsed_url = urlparse(data["url"])
        data["url"] = f"{parsed_url.scheme}://{parsed_url.netloc}"
    else:
        flash("Некорректный URL =(", "fail")
        return redirect(url_for('index_get'))

    # URL length check
    if len(data["url"]) > 255:
        flash("Слишком длинный URL =(", "fail")
        return redirect(url_for('index_get'))

    # Uniqueness of the URL check
    try:
        database.insert_values_urls(data["url"])
    except UniqueViolation:
        flash("Данный URL был сохранен ранее", "fail")
        return redirect(url_for('index_get'))

    flash("URL сохранен =)", "success")
    return redirect(url_for('index_get'))


@app.route("/urls/")
def urls_list():
    sites = database.get_all_urls()[::-1]
    messages = get_flashed_messages(with_categories=True)
    return render_template(
        "urls.html",
        sites=sites,
        messages=messages,
    )


@app.route("/urls/<id>")
def get_url(id):
    site = database.get_url(id)
    return render_template(
        "url_id.html",
        site=site,
    )
