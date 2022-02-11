import os
from dotenv import load_dotenv

load_dotenv()


class GoogleLoginConstants:
    REDIRECT_URI = os.getenv('REDIRECT_URI')
    GG_CLIENT_SECRET = os.getenv('GG_CLIENT_SECRET')
    GG_REQUEST_TOKEN_URL = os.getenv('GG_REQUEST_TOKEN_URL')
    GG_REQUEST_USERINFO_URL = os.getenv('GG_REQUEST_USERINFO_URL')
