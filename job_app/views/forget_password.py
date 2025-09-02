import datetime
from ..model.users import User
from rest_framework.generics import CreateAPIView
from django.conf import settings
from random import randint
from django.template.loader import render_to_string
from django.core.mail import send_mail, EmailMessage
from utility.utils import generate_otp_number
from utility.utils import encrypt, send_common_email
from random import randint
import urllib.request
from django.utils import timezone
from utility.constants import *

import json
import datetime
from random import randint
from rest_framework.generics import CreateAPIView
from django.conf import settings
from utility.response import ApiResponse
from random import randint
from django.template.loader import render_to_string
from django.core.mail import send_mail, EmailMessage
from utility.utils import generate_otp_number




"""serializer"""
from ..serializers.forget_password import (
    ForgetPasswordSerializer,
)

"""swagger"""
from ..swagger.forget_password_swagger import swagger_auto_schema

class ForgotPasswordView(CreateAPIView, ApiResponse):
    """
    API Used For validating email and generating OTP.
    """

    queryset = User.objects.all().values("email")
    serializer_class = ForgetPasswordSerializer

    def create_email_body(self, user, link):
        context = {"link": link, "logo_url": settings.FRONT_END_URL + "images/login-logo.png"}
        message = render_to_string("forget_password.html", context)
        return message

    @swagger_auto_schema
    def post(self, request, *args, **kwargs):
        try:
            data = request.data.copy()

            """ Check Eamil NUll"""
            if not data.get("email"):
                return ApiResponse.response_bad_request(self, message=MESSAGES["email_not_provided"])
                # return ApiResponse.response_bad_request(self, message='Email not provided')

            is_user = User.objects.filter(email=data.get("email"), status=1).first()
            if is_user:
                user = is_user

                """ Create hash"""
                random_str = str(randint(100000, 999999))
                email = user.email + random_str
                encrypt_email = encrypt(email).decode("ascii")

                """Save hash in model"""
                user.email_hash = encrypt_email
                user.hash_expires = timezone.now()
                user.save()

                # email body
                subject = MESSAGES["forget_password_email_subject"]

                """Create Link"""

                # link = FORGET_PASSWORD_URL + urllib.parse.quote_plus(encrypt_email)
                if data.get("is_local"):
                    link = settings.BASE_URL + "password/reset/" + urllib.parse.quote_plus(encrypt_email)
                else:
                    link = settings.FRONT_END_URL + "password/reset/" + urllib.parse.quote_plus(encrypt_email)

                message = self.create_email_body(user, link)
                email_to = user.email
                from_emails = settings.FROM_EMAIL
                try:
                # send email
                    send_common_email(subject, message, email_to, from_emails)
                except:
                    pass

                return ApiResponse.response_ok(self, message="Link successfully sent to yor Email.")
            else:
                return ApiResponse.response_bad_request(self, message="User with this Email does not exist.")
        except Exception as e:
            print(e)
            return ApiResponse.response_internal_server_error(self, message=[str(e.args[0])])
