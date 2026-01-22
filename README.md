# � Nákupní seznam Web App

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

3. Otevři v prohlížeči:
```
http://127.0.0.1:5000
```

### Docker spuštění (PostgreSQL)

1. Spusť pomocí Docker Compose:
```bash
docker compose up --build
```

2. Otevři v prohlížeči:
```
http://localhost:5000
```

## ⚙️ Konfigurace

Aplikace podporuje konfiguraci pomocí proměnných prostředí:

| Proměnná | Popis | Výchozí hodnota |
|----------|-------|-----------------|
| `SECRET_KEY` | Tajný klíč pro session | `dev-secret-key-change-in-production` |
| `DATABASE_URL` | URL databáze | `sqlite:///shopping.db` |

### Podporované databáze
- **SQLite**: `sqlite:///shopping.db`
- **PostgreSQL**: `postgresql://user:password@host:port/database`
- **MySQL**: `mysql://user:password@host:port/database`

## 🛠️ Použité technologie

- **Backend**: Flask 3.0, Flask-SQLAlchemy, Flask-Migrate
- **Databáze**: PostgreSQL / SQLite
- **Frontend**: HTML5, CSS3, Jinja2 šablony
- **Kontejnerizace**: Docker, Docker Compose
- **Bezpečnost**: Werkzeug (hashování hesel)

## 📁 Struktura projektu

```
shopping-list/
├── app.py                 # Hlavní Flask aplikace
├── requirements.txt       # Python závislosti
├── Dockerfile            # Docker konfigurace
├── docker-compose.yml    # Docker Compose konfigurace
├── .gitignore            # Git ignore soubor
├── .env.example          # Příklad konfigurace prostředí
├── .github/
│   └── workflows/
│       └── docker-publish.yml  # GitHub Actions pro Docker
├── migrations/           # Databázové migrace (Alembic)
│   ├── alembic.ini
│   ├── env.py
│   └── versions/
├── templates/            # Jinja2 šablony
│   ├── base.html         # Základní šablona
│   ├── login.html        # Přihlášení
│   ├── register.html     # Registrace
│   ├── dashboard.html    # Nákupní seznam
│   ├── add_item.html     # Přidání položky
│   ├── edit_item.html    # Úprava položky
│   └── macros.html       # Makra pro šablony
└── static/
    └── css/
        └── style.css     # Styly
```

## 📝 Licence

MIT

