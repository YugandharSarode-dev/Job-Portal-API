import json
from rest_framework.generics import CreateAPIView
from ..model.otp import OTP
from ..model.users import User
from django.conf import settings
from ..serializers.reset_password import ResetPasswordSerializer
from utility.response import ApiResponse
from job_app.swagger.reset_password_swagger import swagger_auto_schema

class ResetPasswordView(CreateAPIView, ApiResponse):
    queryset = User.objects.filter(is_active=False)
    serializer_class = ResetPasswordSerializer

    @swagger_auto_schema
    def post(self, request, *args, **kwargs):
        """
        API for reset password.
        """
        try:
            data = request.data
            try:
                user = User.objects.get(email=data.get('email'), is_active=True)
            except:
                return ApiResponse.response_not_found(self, message="User does not exist")

            if data.get('password') != data.get('confirm_password'):
                return ApiResponse.response_bad_request(self, message="Password and confirm password not match")

            # if str(user.new_otp) != str(data.get('new_otp')):
            #     return ApiResponse.response_bad_request(self, message="Password not change, please send again")
                
            user.set_password(data.get('password'))
            user.otp = None
            user.otp_time = None
            user.new_otp = None
            user.save()
            return ApiResponse.response_ok(self, message="Password changed")
        except Exception as e:
            return ApiResponse.response_internal_server_error(self, message=[str(e.args[0])])
