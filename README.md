# btp-projet-ia

## Local Development

By default the project will use a local SQLite database for development (dev.db) if PostgreSQL environment variables are not set.

If you want to use PostgreSQL instead of the SQLite fallback, set the following environment variables before starting the app:

- DB_USER
- DB_PASSWORD
- DB_HOST
- DB_PORT (optional, defaults to 5432)
- DB_NAME (optional)

Also install the PostgreSQL driver for Python using pip:

```cmd
pip install psycopg2-binary
```

Start the app (Windows cmd.exe):

```cmd
set FLASK_ENV=development
python app.py
```

Or, to force using your Postgres connection:

```cmd
set DB_USER=postgres
set DB_PASSWORD=password
set DB_HOST=localhost
set FLASK_ENV=development
python app.py
```

This avoids requiring `psycopg2` for simple local development when a local SQLite file is sufficient.