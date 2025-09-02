from drf_yasg.utils import swagger_auto_schema
import json

response_ok = {"message": ["Password changed"], "code": 200, "success": True, "data": {}}

not_found = {"message": ["User does not exist"], "code": 404, "success": False, "data": {}}

bad_req = {"message": ["Password and confirm password not match"], "code": 400, "success": False, "data": {}}

swagger_auto_schema = swagger_auto_schema(
    responses={
        "200": json.dumps(response_ok),
        "400": json.dumps(bad_req),
        "404": json.dumps(not_found),
    },
    operation_id="reset password",
    operation_description='API to reset password \n \n requests::   {"email":"anup@gmail.com","password": "123456","confirm_password": "123456"}',)
