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

## Using TMDB for posters
The app can enrich movies by fetching posters from The Movie DB (TMDB) when a poster isn't already stored in the database.
To enable this, set the `TMDB_API_KEY` environment variable with your TMDB API key before starting the app:

```cmd
set TMDB_API_KEY=your_tmdb_api_key
```

When a movie returned by `/api/films` is missing `poster_url`, the server will try to fetch the poster from TMDB and return a full `poster_url` using TMDB images.

## Responsive features - Frontend
The mood slider UI was updated to be responsive and mobile-friendly:
- The card layout now uses percentage widths and adapts to small screens.
- Emoji buttons shrink on mobile and remain accessible (keyboard controls + `aria-pressed`).
- Film recommendations are displayed in a responsive grid and support horizontal scrolling on narrow screens (carousel-like behavior).

If you want to enable TMDB poster enrichment, set `TMDB_API_KEY` before starting the app. On small devices, posters are lazy-loaded for better performance.