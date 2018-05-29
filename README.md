# Tagazine

A web app for uploading, sharing, reading, and documenting zines.

> ## zine
> ### `zēn` &middot; _noun, informal_
>
> - a magazine, especially a fanzine.
> - a webzine.

---

## Run locally

Assumes the following are already installed:
- python
- pip
- postgres

```bash
git clone git@github.com:kenziebottoms/tagazine.git
cd tagazine
sudo pip install -r requirements.txt
psql -c 'create database tagazine;'
python manage.py runserver
```