import os
import dotenv
import requests
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

from page_analyzer.parser import Parser
from page_analyzer.database import PostgresConnection
from page_analyzer.repository import URLRepository, URLChecksRepository


dotenv.load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

url_repo = URLRepository(PostgresConnection)
checks_repo = URLChecksRepository(PostgresConnection)


@app.get("/")
def index_get(url: str = "", code: int = 200):
    messages = get_flashed_messages(with_categories=True)
    return render_template("index.html", messages=messages, url=url), code


@app.post("/urls")
def urls_post():
    data = request.form.to_dict()

    # URL validation
    if url_validator(data["url"]):
        url_parser = urlparse(data["url"])
        url = f"{url_parser.scheme}://{url_parser.netloc}"
    else:
        flash("Некорректный URL", "fail")
        return index_get(data["url"], 422)

    # URL length check
    if len(url) > 255:
        flash("Некорректный URL", "fail")
        return index_get(data["url"], 422)

    # Uniqueness of the URL check
    try:
        url_repo.add_url(url)
    except UniqueViolation:
        flash("Страница уже существует", "fail")
        return redirect(url_for("get_url", id=url_repo.get_id_from_url(url)))

    id = url_repo.get_id_from_url(url)
    flash("Страница успешно добавлена", "success")
    return redirect(url_for('get_url', id=id))


@app.route("/urls")
def urls_list():
    sites = checks_repo.get_urls_with_checks()[::-1]
    messages = get_flashed_messages(with_categories=True)
    return render_template(
        "urls.html",
        sites=sites,
        messages=messages,
    )


@app.route("/urls/<id>")
def get_url(id):
    site = url_repo.get_url(id)
    checks = checks_repo.get_checks(id)
    messages = get_flashed_messages(with_categories=True)
    return render_template(
        "url_id.html",
        site=site,
        checks=checks,
        messages=messages
    )


@app.post("/urls/<id>/checks")
def url_check(id):
    site_url = url_repo.get_url(id).name

    # try:
    site_res = requests.get(site_url)
    assert site_res.status_code == 200
    parser = Parser(site_res)
    checks_repo.add_check(id, site_res.status_code,
                          parser.h1, parser.title,
                          parser.meta_description)
    flash("Страница успешно проверена", "success")
    # except Exception:
    #     flash("Произошла ошибка при проверке", "fail")

    return redirect(url_for('get_url', id=id))
