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
from job_app.model.application import Application
from job_app.serializers.application_serializer import ApplicationSerializer


class ApplicationView(MultipleFieldPKModelMixin, CreateRetrieveUpdateViewSet, ApiResponse):
    serializer_class = ApplicationSerializer
    singular_name = 'Application'
    model_class = Application.objects
    permission_classes = [IsAuthenticated]
    search_fields = ['job__title', 'status']

    def get_object(self):
        """Get single application of logged-in user"""
        try:
            pk = self.kwargs.get('id')
            return self.model_class.filter(pk=pk, applicant=self.request.user).first()
        except:
            return None

    @transaction.atomic()
    def create(self, request, *args, **kwargs):
        """Apply for a Job"""
        sp1 = transaction.savepoint()
        try:
            req_data = request.data.copy()
            # Force applicant to be logged-in user
            req_data['applicant'] = request.user.id

            serializer = self.serializer_class(data=req_data)
            if serializer.is_valid():
                serializer.save()
                transaction.savepoint_commit(sp1)
                return ApiResponse.response_created(
                    self,
                    data=serializer.data,
                    message='Applied for job successfully.'
                )

            error_resp = get_serielizer_error(serializer)
            transaction.savepoint_rollback(sp1)
            return ApiResponse.response_bad_request(self, message=error_resp)

        except Exception as e:
            transaction.savepoint_rollback(sp1)
            return ApiResponse.response_internal_server_error(self, message=[str(e)])

    @transaction.atomic()
    def update(self, request, *args, **kwargs):
        """Allow applicant to update their own application (e.g., resume)"""
        sp1 = transaction.savepoint()
        try:
            instance = self.get_object()
            if not instance:
                return ApiResponse.response_not_found(self, message='Application not found')

            req_data = request.data.copy()
            # Prevent modifying applicant, or status
            req_data.pop('applicant', None)
            req_data.pop('status', None)

            serializer = self.serializer_class(instance, data=req_data, partial=True)
            if serializer.is_valid():
                serializer.save()
                transaction.savepoint_commit(sp1)
                return ApiResponse.response_ok(
                    self,
                    data=serializer.data,
                    message='Application updated successfully'
                )

            error_resp = get_serielizer_error(serializer)
            transaction.savepoint_rollback(sp1)
            return ApiResponse.response_bad_request(self, message=error_resp)

        except Exception as e:
            transaction.savepoint_rollback(sp1)
            return ApiResponse.response_internal_server_error(self, message=[str(e)])

    @action(detail=True, methods=['patch'], url_path='update-status')
    def update_status(self, request, *args, **kwargs):
        """Employer can accept or reject an application"""
        try:
            pk = self.kwargs.get('id')
            instance = self.model_class.filter(pk=pk, job__posted_by=request.user).first()
            if not instance:
                return ApiResponse.response_not_found(self, message='Application not found')

            status = request.data.get('status')
            if status not in ['2', '3']:
                return ApiResponse.response_bad_request(self, message='Invalid status')

            # Update the status
            instance.status = status
            instance.save()

            return ApiResponse.response_ok(
                self,
                data=self.transform_single(instance),
                message=f'Application Status Updated successfully'
            )

        except Exception as e:
            return ApiResponse.response_internal_server_error(self, message=[str(e)])



    def list(self, request, *args, **kwargs):
        """List applications based on user role"""
        try:
            query_params = request.query_params
            user = request.user

            # Check user role
            if user.role == 3:  # Job seeker / applicant
                queryset = self.model_class.filter(applicant=user)
            elif user.role == 2:  # Employer
                queryset = self.model_class.filter(job__posted_by=user)
            else:
                queryset = self.model_class.none()  # Superuser or other roles, return empty

            # Optional filters
            job_id = query_params.get('job_id')
            if job_id:
                queryset = queryset.filter(job_id=job_id)

            status = query_params.get('status')
            if status:
                queryset = queryset.filter(status=status)

            keyword = query_params.get('keyword')
            if keyword:
                queryset = queryset.filter(Q(job__title__icontains=keyword))

            # Sorting
            sort_by = query_params.get('sort_by') or 'created_at'
            if query_params.get('sort_direction') == 'descending':
                sort_by = '-' + sort_by
            queryset = queryset.order_by(sort_by)

            # Pagination
            paginated_data = get_pagination_resp(queryset, request)
            response_data = [self.transform_single(obj) for obj in paginated_data['data']]

            return ApiResponse.response_ok(self, data=response_data, paginator=paginated_data.get('paginator'))

        except Exception as e:
            return ApiResponse.response_internal_server_error(self, message=[str(e)])


    def delete(self, request, *args, **kwargs):
        """Delete applied job"""
        try:
            instance = self.get_object()
            if not instance:
                return ApiResponse.response_not_found(self, message='Application not found')

            instance.delete()
            return ApiResponse.response_ok(self, message='Application deleted successfully')

        except Exception as e:
            return ApiResponse.response_internal_server_error(self, message=[str(e)])

    def transform_single(self, instance):
        """Transform application object into response"""
        return {
            'applicant_id': instance.applicant.id,
            'applicant_name': instance.applicant.username,
            'application_id': instance.id,
            'job_id': instance.job.id,
            'job_title': instance.job.title,
            'status': instance.get_status_display(),
            'status_name': instance.get_status_display(),
            'applied_at': instance.created_at
        }
