import os
from config import get_config

print('FLASK_ENV is', os.environ.get('FLASK_ENV'))
conf = get_config()
print('Config class:', conf.__name__)

# Try production explicitly
try:
    cfg = get_config('production')
    print('Production config OK')
except Exception as e:
    print('Production config error:', e)
