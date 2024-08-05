1. Clone the repository

```bash
    git clone https://github.com/Aravindhan-Master/SocialNetwork.git
```

2. Create a virtual environment

```bash
    python -m venv venv
```

3. Activate the virtual environment

```bash
    venv\Scripts\activate
```

4. Install dependencies

```bash
    pip install -r requirements.txt
```

5. Add these in .env file

```bash
    DJANGO_SECRET_KEY=django_secret_key

    DEBUG=True

    DATABASE_ENGINE=django.db.backends.postgresql
    DATABASE_NAME=accuknox
    DATABASE_PASSWORD=password
    DATABASE_HOST=localhost
    DATABASE_USER=postgres
    DATABASE_PORT=5432
```

6. Migrate database schema

```bash
    python manage.py makemigrations main
    python manage.py migrate
```

7. Start server

```bash
    python manage.py runserver
```

POSTMAN COLLECTION LINK:

```bash
    https://www.postman.com/aravindhan-2003/workspace/aravindhan/collection/37437613-d335e733-c5a9-4b0e-9288-0162096cd861
```