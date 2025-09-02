from drf_yasg.utils import swagger_auto_schema
import json

response_ok = {
    "message": ["Link successfully sent to your email"],
    "code": 200,
    "success": True,
    "data": {"otp": 123456},
}

not_found = {
    "message": [" number not provided or provided Mobile number is incorrect"],
    "code": 404,
    "success": False,
    "data": {},
}
expires = {"message": ["Email not provided or  is incorrect"], "code": 404, "success": False, "data": {}}

swagger_auto_schema = swagger_auto_schema(
    responses={
        "200": json.dumps(response_ok),
        "404": json.dumps(not_found),
        "404": json.dumps(expires),
    },
    operation_id="forget password",
    operation_description='API to forget password \n \n request:: {"email": "anup@gmail.com"}',
)
