import jwt

# Secrets
from config.secrets import sessionSecret, issuerSecret

def verify(token):
    token = token.split('Bearer ')[1]
    try:
        decoded_token = jwt.decode(token, sessionSecret, algorithms=['HS256'])
    except Exception as e:
        print(e)
        return [False]

    if not decoded_token or decoded_token['iss'] != issuerSecret:
        return [False]
    else:
        return [True, decoded_token]

def authenticate_user(token):
    verfication_result = verify(token)
    if verfication_result[0]: # 0th position is True or False
        return verfication_result[1]['sub'] # user_id
    else:
        return False
