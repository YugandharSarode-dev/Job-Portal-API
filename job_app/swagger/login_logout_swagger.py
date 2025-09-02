from drf_yasg.utils import swagger_auto_schema
import json

login = {
    "message": [
        "Login successful"
    ],
    "code": 200,
    "success": True,
    "data": {
        "id": 1,
        "first_name": "anup",
        "last_name": "shourya",
        "email": "anup@gmail.com",
        "mobile": "7898002213",
        "username": "",
        "group": None,
        "token": {
            "access_token": "5bJTRbqtYmVmw9wBKBGnyWjR9KWIuy",
            "token_type": "Bearer",
            "expires_in": 36000,
            "refresh_token": "Grg3RcqeR3P9pYv0oGRNg6anmwDnBY",
            "scope": {
                "read": "Read scope"
            }
        }
    }
}

invalid_login = {
    "message": [
        "Invalid username or password. Please try again."
    ],
    "code": 403,
    "success": False,
    "data": {}
}

logout = {
    "message": [
        "Logout successful"
    ],
    "code": 200,
    "success": True,
    "data": []
}

swagger_auto_schema_logout = swagger_auto_schema(
    responses={
        "200": json.dumps(logout),
    },
    operation_id="logout ",
    operation_description="API to logout",
)

swagger_auto_schema = swagger_auto_schema(
    responses={
        "200": json.dumps(login),
        "403": json.dumps(invalid_login),
    },
    operation_id="login",
    operation_description='API to login \n \n request::   {"username": "anup@gmil.com","password": "123456"}',)
