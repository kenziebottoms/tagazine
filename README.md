# Tagazine

![](https://img.shields.io/badge/python-v3.6.0-316391.svg)
![](https://img.shields.io/badge/django-v1.11.13-005237.svg)
![](https://img.shields.io/badge/data-postgres-316391.svg)
![](https://img.shields.io/badge/css_framework-bootstrap-5F2C7C.svg)

A web app for uploading, sharing, reading, and documenting zines.

> ## zine
> ### `zēn` &middot; _noun, informal_
>
> - a magazine, especially a fanzine.
> - a webzine.

---

## Run locally

Assumes the following are already installed:
- `python`
- `pyenv`
- `pip`
- `postgres`

```bash
git clone git@github.com:kenziebottoms/tagazine.git
cd tagazine
sudo pip install -r requirements.txt
pyenv local 3.6.0
psql -c 'create database tagazine;'
python manage.py runserver
```