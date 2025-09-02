import json

from drf_yasg.utils import swagger_auto_schema

response_ok = {
    "message": ["OTP is valid"],
    "code": 200,
    "success": True,
    "data": {"new_otp": 123456},
}

user_not_found = {
    "message": ["User does not exist"],
    "code": 404,
    "success": False,
    "data": {},
}
bad_req = {"message": ["OTP time expires"], "code": 400, "success": False, "data": {}}

swagger_auto_schema = swagger_auto_schema(
    responses={
        "200": json.dumps(response_ok),
        "404": json.dumps(user_not_found),
        "400": json.dumps(bad_req),
    },
    operation_id="login-verify-otp",
    operation_description='API to otp verification \n \n request:: {"email": "anup@gmail.com"}',)

