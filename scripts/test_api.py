from app import app

with app.test_client() as c:
    rv = c.get('/api/films?value=75')
    print('status:', rv.status_code)
    print('json:', rv.get_json())