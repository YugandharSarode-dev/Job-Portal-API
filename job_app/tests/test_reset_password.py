from django.test import TestCase
from utility.constants import BASE_URL
import random
import string
from oauth2_provider.models import AccessToken
from utility.constants import *
from ..models import User
from django.test import TestCase
from django.utils import timezone
from django.utils.timezone import timedelta
import requests
from json import loads, dumps
from utility.test_utility import *
from oauthlib.common import generate_token
from stark_utilities.utilities import random_string_generator
from django.conf import settings
from datetime import date, datetime

"""Model"""
from ..models import User

class ResetPasswordTest(TestCase):
    model_class = User

    @classmethod
    def setUpTestData(self):
        self.user = create_user(SUPERUSER_ROLE)
        
        self.auth_headers = get_auth_dict(self.user)

    url = BASE_URL + "reset_password/"
    data = dict()

    # test reset passward api valid unit test
    def test_reset_password_api_valid(self):
        url = self.url + str("?token=qwert")
        self.data["email"] = self.user.email
        self.data["password"] = "reset123"
        self.data["confirm_password"] = "reset123"
        response = self.client.post(url, data=self.data)
        self.assertEqual(response.status_code, 200)

    # test reset passward api invalid unit test
    def test_add_api_wrong_password(self):
        self.data["email"] = self.user.email
        self.data["password"] = ""
        self.data["confirm_password"] = "reset123"
        response = self.client.post(self.url, data=self.data)
        self.assertEqual(response.status_code, 400)
