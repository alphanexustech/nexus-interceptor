from app import app
from datetime import datetime

utc = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
utc_datetime = datetime.utcnow()
api_ip = '127.0.0.1'
port = '5500'
