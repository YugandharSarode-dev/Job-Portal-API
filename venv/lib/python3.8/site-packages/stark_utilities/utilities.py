import requests
from django.core.validators import validate_email
from django.core.paginator import Paginator
from django.conf import settings
from random import randint
from rest_framework.generics import GenericAPIView
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from django.shortcuts import get_object_or_404
from cryptography.fernet import Fernet
from django.utils import timezone
from django.utils.timezone import make_aware
from oauthlib.oauth2.rfc6749.tokens import random_token_generator
from oauth2_provider.models import AccessToken, Application, RefreshToken
from oauth2_provider.settings import oauth2_settings
from datetime import datetime, timedelta, date
import pytz
import shortuuid

def generate_otp_number(OTP_LENGTH=6):
    """ generate otp number """
    try:
        OTP_LENGTH = settings.OTP_LENGTH
    except:
        pass

    range_start = 10 ** (OTP_LENGTH - 1)
    range_end = (10 ** OTP_LENGTH) - 1
    return randint(range_start, range_end)

class CreateRetrieveUpdateViewSet(
    GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
):
    """ mixins to handle request url """
    pass


class MultipleFieldPKModelMixin(object):
    """
    Class to override the default behaviour for .get_object for models which have retrieval on fields
    other  than primary keys.
    """

    lookup_field = []
    lookup_url_kwarg = []

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        get_args = {field: self.kwargs[field] for field in self.lookup_field if field in self.kwargs}

        get_args.update({"pk": self.kwargs[field] for field in self.lookup_url_kwarg if field in self.kwargs})
        return get_object_or_404(queryset, **get_args)

def is_valid_email(email):
    """ email validations """
    try:
        validate_email(email)
    except:
        return False
    return True

def get_serielizer_error(serializer, with_key=True):
    """ handle serializer error """
    msg_list = []
    try:
        mydict = serializer.errors
        for key in sorted(mydict.keys()):
            msg = ''
            
            if with_key:
                msg = key + " : "
            
            msg += str(mydict.get(key)[0])

            msg_list.append(msg)
    except:
        msg_list = ["Invalid format"]
    return msg_list

def get_pagination_resp(data, request):
    """ pagination response """
    page_response = {
        "total_count": None, 
        "total_pages": None, 
        "current_page": None, 
        "limit": None
    }

    where_array = request.query_params

    if where_array.get("type") == "all":
        return {
            "data": data, 
            "paginator": page_response
        }

    page = where_array.get("page") if where_array.get("page") else 1

    try:
        PAGE_SIZE = settings.PAGE_SIZE
    except:
        PAGE_SIZE = 10

    limit = where_array.get("limit") if where_array.get("limit") else settings.PAGE_SIZE
    
    paginator = Paginator(data, limit)
    
    data = paginator.get_page(page).object_list
    
    current_page = paginator.num_pages

    if int(current_page) < int(page):
        return {"data": [], "paginator": paginator.get("paginator")}

    page_response['total_count'] = paginator.count
    page_response['total_pages'] = paginator.num_pages
    page_response['current_page'] =  page
    page_response['limit'] =  limit
    
    paginator = {"paginator": page_response}

    response_data = {"data": data, "paginator": paginator.get("paginator")}
    return response_data

def string_to_date(string_time):
    """ string to date """
    try:
        naive_datetime = datetime.strptime(string_time, "%Y-%m-%d")
        aware_datetime = make_aware(naive_datetime)
        return aware_datetime.date()
    except:
        return e

def convert_timestamp_to_date(timestamp):
    """ timestamp to date """
    try:
        naive_datetime = datetime.fromtimestamp(timestamp)
        aware_datetime = make_aware(naive_datetime)
        return aware_datetime.date()
    except:
        return None

def encrypt(text):
    """ encryption of text"""
    try:
        cipher_suite = Fernet(settings.S_KEY)
    except:
        raise Exception('Add S_KEY in settings to encrypt string.')

    text = text.encode("utf-8")
    cipher_text = cipher_suite.encrypt(text)
    return cipher_text

def decrypt(text):
    """ decryption text """
    try:
        cipher_suite = Fernet(settings.S_KEY)
    except:
        raise Exception('Add S_KEY in settings to encrypt string.')

    plain_text = cipher_suite.decrypt(text)
    plain_text = plain_text.decode("utf-8")
    return plain_text

def generate_token(request, user):
    """ login token generations """
    expire_seconds = oauth2_settings.user_settings["ACCESS_TOKEN_EXPIRE_SECONDS"]
    scopes = oauth2_settings.user_settings["SCOPES"]

    application = Application.objects.first()
    expires = datetime.now() + timedelta(seconds=expire_seconds)
    access_token = AccessToken.objects.create(
        user=user,
        application=application,
        token=random_token_generator(request),
        expires=expires,
        scope=scopes,
    )

    refresh_token = RefreshToken.objects.create(
        user=user, token=random_token_generator(request), access_token=access_token, application=application
    )

    token = {
        "access_token": access_token.token,
        "token_type": "Bearer",
        "expires_in": expire_seconds,
        "refresh_token": refresh_token.token,
        "scope": scopes,
    }
    return token

""" token generations by oauth """
def generate_oauth_token(host, username, password):
    try:
        client_id = settings.CLIENT_ID
    except:
        raise Exception('Add CLIENT_ID in settings.')

    try:
        client_secret = settings.CLIENT_SECRET
    except:
        raise Exception('Add CLIENT_SECRET in settings.')

    try:
        SERVER_PROTOCOLS = settings.SERVER_PROTOCOLS
    except:
        raise Exception('Add SERVER_PROTOCOLS in settings.')

    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    payload = {
        "grant_type": "password",
        "username": username,
        "password": password,
        "client_id": client_id,
        "client_secret": client_secret,
    }
    return requests.post(SERVER_PROTOCOLS + host + "/o/token/", data=payload, headers=headers)

def revoke_oauth_token(request):
    """ revoke token """
    try:
        client_id = settings.CLIENT_ID
    except:
        raise Exception('Add CLIENT_ID in settings.')

    try:
        client_secret = settings.CLIENT_SECRET
    except:
        raise Exception('Add CLIENT_SECRET in settings.')
    
    try:
        SERVER_PROTOCOLS = settings.SERVER_PROTOCOLS
    except:
        raise Exception('Add SERVER_PROTOCOLS in settings.')

    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    payload = {
        "token": request.META["HTTP_AUTHORIZATION"][7:],
        "token_type_hint": "access_token",
        "client_id": client_id,
        "client_secret": client_secret,
    }

    # host request
    host = request.get_host()
    response = requests.post(
        SERVER_PROTOCOLS + host + "/o/revoke_token/", data=payload, headers=headers
    )
    return response

def get_otp_expirity():
    """ set otp expiry time """
    return timezone.now() + timedelta(minutes=15)

def transform_list(self, data):
    return map(self.transform_single, data)

def utc_to_time(naive, timezone="Asia/Calcutta"):
    if naive:
        return naive.replace(tzinfo=pytz.utc).astimezone(pytz.timezone(timezone))
    else:
        return ""

def min_to_hr_conversion(estimation):
    duration = ""
    if estimation:
        arr_duration = str(timedelta(minutes=estimation)).split(":")
        try:
            if int(arr_duration[0]) != 0:
                duration += str(arr_duration[0]) + " Hrs"
        except:
            days = arr_duration[0].split(", ")
            if days[0]:
                duration += str(days[0])

            if days[1]:
                duration += " " + str(days[1]) + " Hrs"

        if int(arr_duration[1]) != 0:
            duration += " " + str(arr_duration[1]) + " Mins"

    return duration

def check_email(email, regex="^[\w.+\-]+@starkdigital\.net$"):
    import re

    match = re.match(regex, email)
    if match:
        return True

    return False

def get_notification_time(temp_time, language="en"):
    now_time = timezone.now()
    diff_time = now_time - temp_time
    if diff_time.days < 1:

        return "today"

    elif diff_time.days < 14:
        if diff_time.days < 2:
            return "yesterday"
        return_time = str(diff_time.days)
        return return_time + " day ago" if return_time == "1" else return_time + " days ago"

    elif diff_time.days < 60:
        return_time = str(diff_time.days // 8)
        return return_time + " week ago" if return_time == "1" else return_time + " weeks ago"

    return_time = str(diff_time.days // 30)
    return return_time + " month ago" if return_time == "1" else return_time + " months ago"

import calendar

def find_day(date):
    date = datetime.strptime(str(date), "%Y-%m-%d").date()
    dayname = datetime.strptime(str(date), "%Y-%m-%d").weekday()
    return calendar.day_name[dayname]

def get_slug(slug_name, date=None):
    from django.utils import timezone

    now = timezone.now()
    if date:
        timestamp = int(datetime.timestamp(date))
    else:
        timestamp = int(datetime.timestamp(now))

    get_slug_name = slug_name.replace(" ", "-").lower() + "-" + str(timestamp)
    return get_slug_name

def int_to_time(time):
    if int(time) < 12:
        time = time + ":00 am"
    elif int(time) == 12:
        time = time + ":00 pm"
    elif int(time) < 24:
        time = str(int(time) - 12) + ":00 pm"
    else:
        time = str(int(time) - 12) + ":00 am"

    return time

def random_string_generator(length=6):
    short_code = shortuuid.ShortUUID().random(length=length)
    return short_code