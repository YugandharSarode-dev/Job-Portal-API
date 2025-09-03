from django.db import transaction
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ViewSet
from job_app.model.category import Category
from utility.response import ApiResponse
from job_app.serializers.category_serializer import CategorySerializer
from utility.utils import get_pagination_resp

class CategoryView(ViewSet, ApiResponse):
    permission_classes = [IsAuthenticated]
    model_class = Category.objects

    @transaction.atomic()
    def create(self, request, *args, **kwargs):
        """Create a category (superuser only)"""
        if request.user.role != 1:
            return ApiResponse.response_unauthorized(self, message=['Only superuser can create category'])

        name = request.data.get('name')
        if not name or not name.strip():
            return ApiResponse.response_bad_request(self, message=['Category name is required'])

        serializer = CategorySerializer(data={'name': name})
        if serializer.is_valid():
            serializer.save()
            return ApiResponse.response_created(
                self,
                data=serializer.data,
                message='Category created successfully'
            )
        else:
            return ApiResponse.response_bad_request(self, message=serializer.errors)
        
    def list(self, request, *args, **kwargs):
        """List all categories (for superuser and employer)"""

        
        try:
            if request.user.role != 1 or 2:
                return ApiResponse.response_unauthorized(self, message=['Only superuser and Employer can list category'])

            query_params = request.query_params
            queryset = self.model_class.all()

            # Sorting
            sort_by = query_params.get('sort_by') or 'id'
            if query_params.get('sort_direction') == 'descending':
                sort_by = '-' + sort_by
            queryset = queryset.order_by(sort_by)

            # Filter by name
            name = query_params.get('name')
            if name:
                queryset = queryset.filter(name__icontains=name)

            response_data = [{'id': obj.id, 'name': obj.name} for obj in queryset]

            paginated_data = get_pagination_resp(response_data, request)
            return ApiResponse.response_ok(self, data=paginated_data)

        except Exception as e:
            return ApiResponse.response_internal_server_error(self, message=[str(e)])

    @transaction.atomic()
    def delete(self, request, *args, **kwargs):
        """Delete a category (superuser only)"""
        if request.user.role != 1:

            return ApiResponse.response_unauthorized(self, message=['Only superuser can delete category'])

        category_id = kwargs.get('id')
        try:
            cat_obj = Category.objects.get(id=category_id)
            cat_obj.delete()
            return ApiResponse.response_ok(self, message='Category deleted successfully')
        except Category.DoesNotExist:
            return ApiResponse.response_not_found(self, message=['Category not found'])
