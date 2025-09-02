from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from ..model.users import User
from ..serializers.verify_otp import FindPassSerializer
from rest_framework.generics import CreateAPIView
from utility.utils import generate_otp_number
from utility.response import ApiResponse
from job_app.swagger.verify_otp_swagger import swagger_auto_schema

class VerifyPasswordView(CreateAPIView, ApiResponse):
    serializer_class = FindPassSerializer

    @swagger_auto_schema
    def post(self, request, *args, **kwargs):
        """
        Verify OTP API
        """
        try:
            data = request.data
            try:
                user = User.objects.get(email=data.get('email'), is_active=True)
            except:
                return ApiResponse.response_not_found(self, message="User does not exist")
            
            if not user.otp or not user.otp_time:
                return ApiResponse.response_bad_request(self, message="OTP time expires")
            
            has_date = (timezone.now() - user.otp_time)
            
            if has_date.days >= 1:
                user.otp_time = None
                user.otp = None
                return ApiResponse.response_bad_request(self, message="OTP time expires")
            elif user.otp == data.get('otp'):
                user.otp_time = None
                user.otp = None
                new_otp = generate_otp_number()
                user.new_otp = new_otp
                user.save()
                data = {"new_otp": new_otp}
                return ApiResponse.response_ok(self, message="OTP is valid", data=data)

            return ApiResponse.response_bad_request(self, message="OTP not valid")
        except Exception as e:
            return ApiResponse.response_internal_server_error(self, message=[str(e.args[0])])
