from django.db import transaction
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from utility.response import ApiResponse
from utility.utils import MultipleFieldPKModelMixin, CreateRetrieveUpdateViewSet, get_serielizer_error
from job_app.model.users import User
from job_app.serializers.user_serializer import UserSerializer    

class UserView(MultipleFieldPKModelMixin, CreateRetrieveUpdateViewSet, ApiResponse):
    serializer_class = UserSerializer
    singular_name = 'User'
    model_class = User.objects
    authentication_classes = []
    permission_classes = []

    search_fields = ['username', 'first_name', 'last_name', 'email']

    def get_permissions(self):
        # Anyone can register a new user
        if self.action == 'create':
            return [AllowAny()]
        # Authenticated for other actions
        return [IsAuthenticated()]

    def get_object(self):
        try:
            pk = self.kwargs.get('id')
            return self.model_class.get(pk=pk)
        except:
            return None

    @transaction.atomic()
    def create(self, request, *args, **kwargs):
        """Register a new User"""
        sp1 = transaction.savepoint()
        try:
            req_data = request.data.copy()
            password = req_data.get("password")
            role = req_data.get('role')
            req_data['role'] = role

            serializer = self.serializer_class(data=req_data)
            if serializer.is_valid():
                user = serializer.save()
                if password:
                    user.set_password(password)
                    user.save()
                transaction.savepoint_commit(sp1)
                return ApiResponse.response_created(
                    self,
                    data=self.serializer_class(user).data,
                    message=self.singular_name + ' created successfully.'
                )

            error_resp = get_serielizer_error(serializer)
            transaction.savepoint_rollback(sp1)
            return ApiResponse.response_bad_request(self, message=error_resp)

        except Exception as e:
            transaction.savepoint_rollback(sp1)
            return ApiResponse.response_internal_server_error(self, message=[str(e)])

    @transaction.atomic()
    def update(self, request, *args, **kwargs):
        """Update logged-in User"""
        sp1 = transaction.savepoint()
        try:
            instance = request.user
            serializer = self.serializer_class(instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                transaction.savepoint_commit(sp1)
                return ApiResponse.response_ok(
                    self,
                    data=serializer.data,
                    message=self.singular_name + ' updated successfully.'
                )

            error_resp = get_serielizer_error(serializer)
            transaction.savepoint_rollback(sp1)
            return ApiResponse.response_bad_request(self, message=error_resp)

        except Exception as e:
            transaction.savepoint_rollback(sp1)
            return ApiResponse.response_internal_server_error(self, message=[str(e)])

    def retrieve(self, request, *args, **kwargs):
        """Get logged-in User by ID"""
        try:
            instance = request.user
            if instance:
                resp_dict = self.transform_single(instance)
                return ApiResponse.response_ok(self, data=resp_dict)

            return ApiResponse.response_not_found(self, message=self.singular_name + ' not found')

        except Exception as e:
            return ApiResponse.response_internal_server_error(self, message=[str(e)])

    def list(self, request, *args, **kwargs):
        """List only logged-in user's details"""
        try:
            instance = request.user
            resp_dict = self.transform_single(instance)
            return ApiResponse.response_ok(self, data=[resp_dict])
        except Exception as e:
            return ApiResponse.response_internal_server_error(self, message=[str(e)])

    def delete(self, request, *args, **kwargs):
        """Delete logged-in User"""
        try:
            instance = request.user
            instance.delete()
            return ApiResponse.response_ok(self, message=self.singular_name + ' deleted')
        except Exception as e:
            return ApiResponse.response_internal_server_error(self, message=[str(e)])

    def transform_single(self, instance):
        return {
            'user_id': instance.id,
            'username': instance.username,
            'first_name': instance.first_name,
            'last_name': instance.last_name,
            'email': instance.email,
            'mobile': instance.mobile,
            'role': instance.role   
        }
