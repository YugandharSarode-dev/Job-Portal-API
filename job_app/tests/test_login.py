from django.test import TestCase
from utility.constants import BASE_URL
from oauth2_provider.models import AccessToken
from utility.constants import *
from ..models import User
from django.test import TestCase
from oauth2_provider.models import AccessToken
from django.utils import timezone
import django.utils.timezone
from django.utils.timezone import timedelta
import random
import string
import requests
from json import loads, dumps
from utility.constants import BASE_URL
from utility.test_utility import *
from oauthlib.common import generate_token
from stark_utilities.utilities import random_string_generator
from django.conf import settings
from datetime import date, datetime

class LoginTest(TestCase):
    model_class = User

    @classmethod
    def setUpTestData(self):
        self.user = create_user(SUPERUSER_ROLE)
        
        self.auth_headers = get_auth_dict(self.user)
        self.user.set_password("reset123")

        self.user.save()

    url = BASE_URL + "login/"
        
    data = dict()

    # test add api valid unit test
    def test_add_api_valid(self):
        self.data["username"] = self.user.email
        self.data["password"] = "reset123"
        response = self.client.post(self.url, data=self.data)
        self.assertEqual(response.status_code, 200)

    # test add api invalid unit test
    def test_add_api_empty(self):
        self.data["email"] = " "
        response = self.client.post(self.url, data=self.data)
        self.assertEqual(response.status_code, 400)
