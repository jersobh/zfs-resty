import jwt
from datetime import datetime, timedelta
from config import JWT_SECRET, JWT_ALGORITHM, JWT_EXP_DELTA_SECONDS

def create_jwt(user):
    payload = {
        'user': user,
        'session_id': str(uuid.uuid4()),
        'exp': datetime.utcnow() + timedelta(seconds=JWT_EXP_DELTA_SECONDS)
    }
    return jwt.encode(payload, JWT_SECRET, JWT_ALGORITHM)
