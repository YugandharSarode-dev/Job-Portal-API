
from django.test import TestCase
import random
import string
from utility.constants import BASE_URL
from oauth2_provider.models import AccessToken
from utility.constants import *
from django.utils import timezone
import django.utils.timezone
from django.utils.timezone import timedelta
import requests
from json import loads, dumps
from utility.test_utility import *
from oauthlib.common import generate_token
from stark_utilities.utilities import random_string_generator
from django.conf import settings
from datetime import date, datetime

##Model
from ..models import Student


class StudentTest(TestCase):
    model_class =  Student

    @classmethod
    def setUpTestData(self):
        self.user = create_user(SUPERUSER_ROLE)
        self.auth_headers = get_auth_dict(self.user)
        self.user.set_password("reset123")
        self.user.save()
        self.get_instance, created = self.model_class.objects.get_or_create(id=1)
        


    url = BASE_URL + 'student/'
    data = dict()

    #Create add valid test
    def test_add_api_valid(self):
        
        self.data['status'] = 1
        self.data['gender'] = 1
        self.data['email'] = str(random_string_generator()) + '@test.com'
        response = self.client.post(self.url, data=self.data, **self.auth_headers)
        self.assertEqual(response.status_code, 201)

    # #Create add invalid test
    def test_add_api_empty(self):
        self.data = dict()
        response = self.client.post(self.url, data=self.data, **self.auth_headers)
        self.assertEqual(response.status_code, 400)

    # #Update api valid test
    def test_put_for_api_valid(self):
        
        self.data['status'] = 1
        self.data['gender'] = 1
        self.data['email'] = str(random_string_generator()) + '@test.com'
        self.data['id'] = self.get_instance.id
        response = self.client.put(self.url, data=self.data, **self.auth_headers)
        self.assertEqual(response.status_code, 200)

    # #Update api invalid test
    def test_put_for_api_invalid(self):
        
        self.data['status'] = 1
        self.data['gender'] = 1
        self.data['email'] = str(random_string_generator()) + '@test.com'
        self.data['id'] = 110000
        response = self.client.put(self.url, data=self.data, **self.auth_headers)
        self.assertEqual(response.status_code, 404)

    #List api test
    def test_get_api_valid(self):
        response = self.client.get(self.url, **self.auth_headers)
        self.assertEqual(response.status_code, 200)

    #Retrieve api test 
    def test_retrieve_api_valid(self):
        url = self.url + str(self.get_instance.id) + '/'
        response = self.client.get(url, **self.auth_headers)
        self.assertEqual(response.status_code, 200)

    #Retrieve invalid id test
    def test_retrieve_api_invalid(self):
        url = self.url + '50000/'
        response = self.client.get(url, **self.auth_headers)
        self.assertEqual(response.status_code, 404)

    #delete api valid id test
    def test_del_api_valid(self):
        url = self.url + str(self.get_instance.id) + '/'
        response = self.client.delete(url, **self.auth_headers)
        self.assertEqual(response.status_code, 200)

    #delete api invalid id test
    def test_del_api_invalid(self):
        url = self.url + '5000000/'
        response = self.client.delete(url,**self.auth_headers)
        self.assertEqual(response.status_code, 404)
        