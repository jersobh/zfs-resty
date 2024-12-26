from datetime import datetime, timedelta
import uuid
from aiohttp import web
import jwt
import pam
from config import logger, JWT_SECRET, JWT_ALGORITHM, JWT_EXP_DELTA_SECONDS
import render

async def check_token(request):
    try:
        jwt_token = request.headers.get('Authorization', None)
        payload = jwt.decode(jwt_token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload['session_id']
    except (jwt.DecodeError, jwt.ExpiredSignatureError):
        return False

async def login(request):
    try:
        data = await request.json()
        user = data['username']
        password = data['password']
        if pam.authenticate(user, password):
            payload = {
                'user': user,
                'session_id': str(uuid.uuid4()),
                'exp': datetime.now(datetime.timezone.utc) + timedelta(seconds=JWT_EXP_DELTA_SECONDS)
            }
            jwt_token = jwt.encode(payload, JWT_SECRET, JWT_ALGORITHM)
            return await render.json({'token': jwt_token.decode('utf-8')}, 200)
        else:
            return await render.json({'error': 'Authentication failed'}, 401)
    except Exception as e:
        logger.error(f"Error in auth: {str(e)}")
        return await render.json({'error': str(e)}, 500)

