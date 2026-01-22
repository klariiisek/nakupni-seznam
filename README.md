

docker compose up --build
# Nákupní seznam (Flask)

Malá Flask aplikace pro správu nákupního seznamu. Umožňuje registraci, přihlášení a práci s položkami, běží na SQLite i PostgreSQL a je připravená pro Docker.

## Co umí

- Přihlášení a registrace s hashovanými hesly
- Přidávání, úprava, mazání a označení položek jako koupených
- Kategorie Zelenina, Ovoce, Ostatni
- Responzivní rozhraní pro mobil i desktop
- Docker Compose konfigurace pro běh s PostgreSQL

## Jak spustit lokálně (SQLite)

1. Závislosti
    ```bash
    pip install -r requirements.txt
    ```
2. Start
    ```bash
    python app.py
    ```
3. Otevři v prohlížeči: http://127.0.0.1:5000

## Jak spustit v Dockeru (PostgreSQL)

1. Postav a spusť kontejnery:
    ```bash
    docker compose up --build
    ```
2. Aplikace poběží na: http://localhost:5000

## Nastavení

Proměnné prostředí:

| Proměnná      | Popis                      | Výchozí hodnota            |
|---------------|----------------------------|----------------------------|
| SECRET_KEY    | Klíč p# � Nákupní seznam Web App

Webová aplikace pro správu nákupního seznamu postavená na Flask frameworku s podporou PostgreSQL a SQLite databáze.

## ✨ Funkce

- 🔐 **Registrace a přihlášení uživatelů** - bezpečná autentizace s hashováním hesel
- ✅ **Správa nákupního seznamu** - přidávání, úprava, mazání a označování jako zakoupené
- 🏷️ **Kategorie položek** - Zelenina, Ovoce, Ostatní
- 📱 **Responzivní design** - moderní UI pro desktop i mobil
- 🐳 **Docker podpora** - snadné nasazení pomocí Docker Compose

## 🚀 Instalace a spuštění

### Lokální spuštění (SQLite)

1. Nainstaluj závislosti:
```bash
pip install -r requirements.txt
```

2. Spusť aplikaci:
```bash
python app.py
```
ro session           | dev-secret-key-change-in-production |
| DATABASE_URL  | URL databáze               | sqlite:///tasks.db         |

Podporované databáze:
- SQLite: sqlite:///tasks.db
- PostgreSQL: postgresql://user:password@host:port/database
- MySQL: mysql://user:password@host:port/database

## Použité technologie

- Flask 3.0, Flask-SQLAlchemy, Flask-Migrate
- SQLAlchemy 2, Werkzeug
- HTML, CSS, Jinja2 šablony
- Docker a Docker Compose

## Stručný přehled adresářů

```
app.py
requirements.txt
Dockerfile
docker-compose.yml
migrations/
templates/
static/
```

## Licence

MIT

