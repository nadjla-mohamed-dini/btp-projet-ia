from app import app
c = app.test_client()
rv = c.get('/')
print('status', rv.status_code)
print('len', len(rv.data))
print(rv.data[:200])
