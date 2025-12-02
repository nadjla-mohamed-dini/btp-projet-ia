import os
from app import app

# For test, ensure no TMDB key set so we see fallback behavior
os.environ.pop('TMDB_API_KEY', None)

with app.test_client() as c:
    r = c.get('/api/films?value=0')
    print('status', r.status_code)
    data = r.get_json()
    print('count', len(data))
    for d in data:
        print(d.get('title'), 'poster', d.get('poster_url')[:80])
