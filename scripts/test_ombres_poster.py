import os
from app import app

os.environ['FLASK_ENV'] = 'testing'

with app.test_client() as client:
    r = client.get('/api/films?mood=peur')
    print('status', r.status_code)
    data = r.get_json()
    print('json response:', data)
    if isinstance(data, list):
        results = data
    else:
        results = data.get('movies', data)
    for m in results:
        if m.get('title') and 'ombres' in m.get('title').lower():
            print('Ombres poster:', m.get('poster_url'))
            break
    else:
        print('No Ombres found in response')
