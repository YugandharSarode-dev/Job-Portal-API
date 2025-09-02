import requests
from django.conf import settings
from utility.role import user_role_super_admin
from utility.utils import *
from ..model.users import User
from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from rest_framework.permissions import IsAuthenticated
from ..serializers.login_serializer import LoginSerializer
from utility.utils import MultipleFieldPKModelMixin, CreateRetrieveUpdateViewSet
from utility.utils import revoke_oauth_token
from utility.response import ApiResponse

class ImpersonateView(MultipleFieldPKModelMixin, CreateRetrieveUpdateViewSet, ApiResponse):
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [OAuth2Authentication, ]
    serializer_class = LoginSerializer
    singular_name = "Login"
    model_class = User.objects

    def get_object(self, pk):
        try:
            return self.model_class.get(pk=pk)
        except:
            return None

    """ User impersonate """

    def retrieve(self, request, **kwargs):
        """
        API to impersonate to other user only for admin.
        """
        try:
            id = self.kwargs.get('id')
            if not user_role_super_admin(request.user):
                return ApiResponse.response_unauthorized(self)
            
            self.old_user = request.user
            user = self.get_object(id)
            if user:
                """
                Authorize to user
                """
                token = generate_token(request, user)
                resp_dict = get_login_response(user, token)
                
                """LOGOUT OLDUSER"""
                if resp_dict:
                    try:
                        response = revoke_oauth_token(request)
                    except:
                        pass
                return ApiResponse.response_ok(self, data=resp_dict, message="Login successful")

            return ApiResponse.response_ok(self, data=[], message="User not found")
        except Exception as e:
            return ApiResponse.response_internal_server_error(self, message=[str(e.args[0])])
