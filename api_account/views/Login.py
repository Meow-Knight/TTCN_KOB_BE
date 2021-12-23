from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password, check_password
from rest_framework import status

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.utils import json

import requests
from rest_framework_simplejwt.tokens import RefreshToken

from api_account.models import Account, Role
from api_account.constants import RoleConstants, GoogleLoginConstants


class LoginView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        user_request_data = request.data
        username = user_request_data.get("username")
        password = user_request_data.get("password")

        account = Account.objects.filter(username=username)
        if account.exists():
            account = account.first()
            if check_password(password, account.password):
                token = RefreshToken.for_user(account)
                response = {'email': account.email, 'access_token': str(token.access_token),
                            'refresh_token': str(token)}
                return Response(response)

        return Response({"details": "Invalid username/password"}, status=status.HTTP_400_BAD_REQUEST)


class MyGoogleLogin(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        data = {
            "redirect_uri": GoogleLoginConstants.REDIRECT_URI,
            "grant_type": "authorization_code",
            "code": request.data.get("code"),
            "client_id": request.data.get("client_id"),
            "client_secret": GoogleLoginConstants.GG_CLIENT_SECRET,
        }
        resp = requests.request(
            'POST',
            GoogleLoginConstants.GG_REQUEST_TOKEN_URL,
            data=data,
        )
        data = json.loads(resp.text)
        payload = {'access_token': data.get("access_token")}  # validate the token
        r = requests.get(GoogleLoginConstants.GG_REQUEST_USERINFO_URL, params=payload)
        data = json.loads(r.text)

        if 'error' in data:
            content = {'message': 'wrong google token or this google token is already expired.'}
            return Response(content)

        account_qs = Account.objects.filter(email=data['email'])
        if not account_qs.exists():
            account = Account()
            account.email = data['email']
            account.first_name = data['given_name']
            account.last_name = data['family_name']
            account.avatar = data.get("picture")
            account.username = 'gg_' + data['email'].split('@')[0]
            account.password = make_password(BaseUserManager().make_random_password())
            user_role = Role.objects.get(name=RoleConstants.USER)
            account.role = user_role
            account.save()
        else:
            account = account_qs.first()

        token = RefreshToken.for_user(account)
        response = {'email': account.email, 'access_token': str(token.access_token), 'refresh_token': str(token)}
        return Response(response)
