from django.utils import timezone
from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from ..model.users import User
from ..serializers.login_verify_otp import LoginOtpSerializer
from utility.response import ApiResponse
from utility.utils import generate_token, get_login_response
from utility.utils import MultipleFieldPKModelMixin, CreateRetrieveUpdateViewSet, generate_otp_number
from utility.constants import *

class LoginVerifyView(MultipleFieldPKModelMixin, CreateRetrieveUpdateViewSet, ApiResponse):
    serializer_class = LoginOtpSerializer

    def post(self, request, *args, **kwargs):
        """
        Otp verification
        """
        try:
            data = request.data
            username = data.get('username')

            if not username:
                return ApiResponse.response_bad_request(self, message="Please Enter Valid Username")
                
            try:
                if '@' in username:
                    kwargs = {'email': username, 'is_active': True}
                else:
                    kwargs = {'username': username, 'is_active': True}
                user = User.objects.get(**kwargs)
            except Exception as e:
                print(e)
                return ApiResponse.response_not_found(self, message="User does not exist")
            if not user.login_otp or not user.login_otp_time:
                return ApiResponse.response_bad_request(self, message="OTP expires")
            has_date = (timezone.now() - user.login_otp_time)

            """
            check for 15 minutes only
            """

            if has_date.total_seconds() / 60 > OTP_EXPIRE_MINUTE_TIME:
                return ApiResponse.response_bad_request(self, message="OTP time expires")
            elif user.login_otp == data.get('otp'):
                user.login_otp_time = None
                user.login_otp = None
                user.save()
                """
                Authorize to user
                """
                token = generate_token(request, user)
                resp_dict = get_login_response(user, token)
                return ApiResponse.response_ok(self, data=resp_dict, message="Login successful")

            return ApiResponse.response_bad_request(self, message="OTP not valid")
        except Exception as e:
            return ApiResponse.response_internal_server_error(self, message=[str(e.args[0])])
