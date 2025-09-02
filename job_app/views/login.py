from rest_framework.generics import GenericAPIView
from ..models import EmailOrUsernameModelBackend
from ..serializers.login_serializer import LoginSerializer
from ..model.users import User
from utility.utils import generate_token, get_login_response, generate_oauth_token
# from rest_apiresponse.apiresponse import ApiResponse
from job_app.swagger.login_logout_swagger import swagger_auto_schema

import json
import requests
from rest_framework import viewsets, permissions
from rest_framework.generics import GenericAPIView
from ..serializers.login_serializer import LoginSerializer
from ..model.users import User
from rest_framework.response import Response
from utility.response import ApiResponse
from rest_framework.permissions import IsAuthenticated
from datetime import datetime, timedelta
from django.conf import settings
from utility.utils import generate_token, get_login_response, generate_oauth_token
# from ..swagger.login_swagger import swagger_auto_schema
# from ..models import EmailOrMobileModelBackend
from oauth2_provider.settings import oauth2_settings
from utility.constants import *
from utility.constants import MESSAGES

class LoginViewSet(GenericAPIView, ApiResponse, EmailOrUsernameModelBackend):
    serializer_class = LoginSerializer

    @swagger_auto_schema
    def post(self, request, *args, **kwargs):
        """
        API to get logged In.
        """
        try:
            host = request.get_host()
            username = request.data.get('username')
            password = request.data.get('password')

            if not username or not password:
                return ApiResponse.response_bad_request(self, message="Username and Password are required")

            """ authenticate user and generate token """
            user = EmailOrUsernameModelBackend.authenticate(self, username=username, password=password)
            if not user:
                return ApiResponse.response_unauthorized(self, message="Invalid username or password. Please try again.")
            
            token = generate_token(request, user)
            resp_dict = get_login_response(user, token)
            resp_dict['token'] = token
            
            return ApiResponse.response_ok(self, data=resp_dict, message="Login successful")
        except Exception as e:
            print(e)
            return ApiResponse.response_internal_server_error(self, message=[str(e.args[0])])
