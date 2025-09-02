from django.db import transaction
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

# Utilities
from utility.response import ApiResponse
from utility.utils import (
    MultipleFieldPKModelMixin,
    CreateRetrieveUpdateViewSet,
    get_pagination_resp,
    get_serielizer_error,
)

# Models and serializers
from job_app.model.job import Job
from job_app.model.application import Application
from job_app.serializers.job_serializer import JobSerializer
from job_app.serializers.application_serializer import ApplicationSerializer


class JobView(MultipleFieldPKModelMixin, CreateRetrieveUpdateViewSet, ApiResponse):
    serializer_class = JobSerializer
    singular_name = 'Job'
    model_class = Job.objects
    permission_classes = [IsAuthenticated]
    search_fields = ['title', 'description', 'category', 'location']

    def get_object(self):
        """Get single job posted by logged-in employer"""
        try:
            pk = self.kwargs.get('id')
            return self.model_class.filter(pk=pk, posted_by=self.request.user).first()
        except:
            return None

    def retrieve(self, request, *args, **kwargs):
        """Get single Job by ID"""
        try:
            instance = self.get_object()
            if instance:
                resp_dict = self.transform_single(instance)
                return ApiResponse.response_ok(self, data=resp_dict)

            return ApiResponse.response_not_found(self, message=self.singular_name + ' not found')
        except Exception as e:
            return ApiResponse.response_internal_server_error(self, message=[str(e)])

    @transaction.atomic()
    def create(self, request, *args, **kwargs):
        """Employer can create a Job"""
        sp1 = transaction.savepoint()
        try:
            req_data = request.data.copy()
            req_data['posted_by'] = request.user.id

            serializer = self.serializer_class(data=req_data)
            if serializer.is_valid():
                serializer.save()
                transaction.savepoint_commit(sp1)
                return ApiResponse.response_created(
                    self,
                    data=serializer.data,
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
        """Update Job if it belongs to employer"""
        sp1 = transaction.savepoint()
        try:
            instance = self.get_object()
            if not instance:
                return ApiResponse.response_not_found(self, message=self.singular_name + ' not found')

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

    def list(self, request, *args, **kwargs):
        """List all active jobs (for job seekers)"""
        try:
            query_params = request.query_params
            # For job seekers, list jobs with status active (1)
            queryset = self.model_class.filter(status=1)  # status=1 is active

            # Sorting
            sort_by = query_params.get('sort_by') or 'id'
            if query_params.get('sort_direction') == 'descending':
                sort_by = '-' + sort_by
            queryset = queryset.order_by(sort_by)

            # Filters
            category = query_params.get('category')
            if category:
                queryset = queryset.filter(category__iexact=category)

            location = query_params.get('location')
            if location:
                queryset = queryset.filter(location__icontains=location)

            keyword = query_params.get('keyword')
            if keyword:
                queryset = queryset.filter(Q(title__icontains=keyword) | Q(description__icontains=keyword))

            response_data = [self.transform_single(obj) for obj in queryset]

            paginated_data = get_pagination_resp(response_data, request)
            return ApiResponse.response_ok(self, data=paginated_data)

        except Exception as e:
            return ApiResponse.response_internal_server_error(self, message=[str(e)])


    def delete(self, request, *args, **kwargs):
        """Delete Job if it belongs to employer"""
        try:
            instance = self.get_object()
            if not instance:
                return ApiResponse.response_not_found(self, message=self.singular_name + ' not found')

            instance.delete()
            return ApiResponse.response_ok(self, message=self.singular_name + ' deleted')

        except Exception as e:
            return ApiResponse.response_internal_server_error(self, message=[str(e)])

    @action(detail=True, methods=['get'])
    def applications(self, request, *args, **kwargs):
        """Get all applications for a specific job (employer only)"""
        try:
            job = self.get_object()
            if not job:
                return ApiResponse.response_not_found(self, message='Job not found')

            queryset = Application.objects.filter(job=job)

            # Pagination
            paginated_data = get_pagination_resp(queryset, request)
            response_data = [self.transform_application(app) for app in paginated_data['data']]

            return ApiResponse.response_ok(self, data=response_data, paginator=paginated_data.get('paginator'))

        except Exception as e:
            return ApiResponse.response_internal_server_error(self, message=[str(e)])

    def transform_single(self, instance):
        """Transform single Job record into response dict"""
        return {
            'job_id': instance.id,
            'title': instance.title,
            'description': instance.description,
            'category': instance.category,
            'skills': [skill.name for skill in instance.skills.all()],
            'location': instance.location,
            'status': instance.status,
            'posted_by': instance.posted_by.id if instance.posted_by else None,
            'created_at': instance.created_at,
            'updated_at': instance.updated_at,
        }

    def transform_application(self, instance):
        """Transform Application object for job applications list"""
        return {
            'application_id': instance.id,
            'job_id': instance.job.id,
            'job_title': instance.job.title,
            'status': instance.status,
            'status_name': instance.get_status_display(),
            'applied_by': {
                'id': instance.applied_by.id,
                'username': instance.applied_by.username
            },
            'applied_at': instance.created_at
        }
