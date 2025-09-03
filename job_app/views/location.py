from django.db import transaction
from rest_framework.permissions import IsAuthenticated
from job_app.model.location import Location
from job_app.serializers.location_serializer import LocationSerializer
from utility.response import ApiResponse
from utility.utils import CreateRetrieveUpdateViewSet, get_pagination_resp

class LocationView(CreateRetrieveUpdateViewSet, ApiResponse):
    serializer_class = LocationSerializer
    singular_name = 'Location'
    model_class = Location.objects
    permission_classes = [IsAuthenticated]

    def get_object(self):
        try:
            pk = self.kwargs.get('id')
            return self.model_class.filter(pk=pk).first()
        except:
            return None

    @transaction.atomic()
    def create(self, request, *args, **kwargs):
        if request.user.role != 1:  
            return ApiResponse.response_unauthorized(self, message=['Only superuser can create location'])

        name = request.data.get('name')
        if not name or not name.strip():
            return ApiResponse.response_bad_request(self, message=['Location name is required'])

        serializer = self.serializer_class(data={'name': name})
        if serializer.is_valid():
            serializer.save()
            return ApiResponse.response_created(self, data=serializer.data, message='Location created successfully')

        return ApiResponse.response_bad_request(self, message=[str(serializer.errors)])
    
    def list(self, request, *args, **kwargs):
        """List all Locations (for superuser and employer)"""
        try:
            if request.user.role != 1 or 2:
                return ApiResponse.response_unauthorized(self, message=['Only superuser and Employer can list Locations'])
            
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


    def delete(self, request, *args, **kwargs):
        if request.user.role != 1:
            return ApiResponse.response_unauthorized(self, message=['Only superuser can delete location'])

        instance = self.get_object()
        if not instance:
            return ApiResponse.response_not_found(self, message='Location not found')

        instance.delete()
        return ApiResponse.response_ok(self, message='Location deleted successfully')
