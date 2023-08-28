### Hexlet tests and linter status:
[![Actions Status](https://github.com/StanislavOkopnyi/python-project-83/workflows/hexlet-check/badge.svg)](https://github.com/StanislavOkopnyi/python-project-83/actions)
[![Tests and linter check](https://github.com/StanislavOkopnyi/python-project-83/actions/workflows/linter-check.yml/badge.svg)](https://github.com/StanislavOkopnyi/python-project-83/actions/workflows/linter-check.yml)
[![Maintainability](https://api.codeclimate.com/v1/badges/245e175be7539bfa1a23/maintainability)](https://codeclimate.com/github/StanislavOkopnyi/python-project-83/maintainability)

<a>https://page-analyzer-okopnyi.up.railway.app/<a>

Анализатор страниц - это сайт, который анализирует указанные страницы на SEO-пригодность по аналогии с PageSpeed Insights

Бэкенд сайта сделан на базе фреймворка Flask, в качестве базы данных используется PostgreSQL

Для развертывания сайта локально нужно:
1) Установить poetry ` pip install poetry `
2) Установить зависимости ` make install `
3) Запустить docker контейнер с базой данных ` sudo docker-compose up -d `
4) Создать .env файл 
```
# DB connection settings
DATABASE_URL=postgresql://postgres:postgres@localhost:50432/postgres
# Flask secret-key
SECRET_KEY= (секретный ключ)
```
5) Запустить  dev-сервер ` make dev `


