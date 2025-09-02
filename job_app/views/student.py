import json
import operator
from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from functools import reduce
from django.conf import settings
from simple_search import search_filter
from django.db import transaction

''' utility '''
from utility.response import ApiResponse
from utility.utils import MultipleFieldPKModelMixin, CreateRetrieveUpdateViewSet, get_serielizer_error, get_pagination_resp, transform_list
from utility.constants import *

''' model imports '''
from ..models import Student

''' serializers '''
from ..serializers.student_serializer import StudentSerializer

''' swagger '''
from ..swagger.student_swagger import swagger_auto_schema_list, swagger_auto_schema_post, swagger_auto_schema, swagger_auto_schema_update, swagger_auto_schema_delete, swagger_auto_schema_bulk_delete

class StudentView(MultipleFieldPKModelMixin, CreateRetrieveUpdateViewSet, ApiResponse):
    serializer_class = StudentSerializer
    # authentication_classes = [OAuth2Authentication, ]
    # permission_classes = [IsAuthenticated, ]
    singular_name = 'Student'
    model_class = Student.objects
    
    search_fields = ['name', 'city', 'marks', 'email']

    def get_object(self, pk):
        try:
            return self.model_class.get(pk=pk)
        except:
            return None

    @swagger_auto_schema
    def retrieve(self, request, *args, **kwargs):
        '''
        :To get the single record
        '''
        try:
            # capture data
            get_id = self.kwargs.get('id')

            # process/format on data
            instance = self.get_object(get_id)
            if instance:
                resp_dict = self.transform_single(instance)

                # return success
                return ApiResponse.response_ok(self, data=resp_dict)

            return ApiResponse.response_not_found(self, message=self.singular_name + ' not found')

        except Exception as e:
            return ApiResponse.response_internal_server_error(self, message=[str(e.args[0])])

    @swagger_auto_schema_post
    @transaction.atomic()
    def create(self, request, *args, **kwargs):
        '''
        :To create the new record
        '''
        sp1 = transaction.savepoint()
        try:
            ''' capture data '''
            req_data = request.data

            serializer = self.serializer_class(data=req_data)

            ''' validate serializer '''
            if serializer.is_valid():
                serializer.save()
                serializer_instance = serializer.instance
                
                transaction.savepoint_commit(sp1)

                return ApiResponse.response_created(self, data=req_data,
                                                    message=self.singular_name + ' created successfully.')

            ''' serializer error '''
            error_resp = get_serielizer_error(serializer)
            transaction.savepoint_rollback(sp1)
            return ApiResponse.response_bad_request(self, message=error_resp)

        except Exception as e:
            transaction.savepoint_rollback(sp1)
            return ApiResponse.response_internal_server_error(self, message=[str(e.args[0])])

    @swagger_auto_schema_update
    @transaction.atomic()
    def partial_update(self, request, *args, **kwargs):
        '''
        :To update the existing record
        '''
        sp1 = transaction.savepoint()
        try:
            ''' capture data '''
            req_data = request.data

            get_id = self.kwargs.get('id')
            instance = self.get_object(get_id)

            if instance is None:
                return ApiResponse.response_not_found(self, message=self.singular_name + ' not found')

            ''' validate serializer '''
            serializer = self.serializer_class(instance, data=req_data, partial=True)
            if serializer.is_valid():
                serializer.save()
                serializer_instance = serializer.instance
                
                ''' success response '''
                response_data = self.transform_single(serializer_instance)
                transaction.savepoint_commit(sp1)

                return ApiResponse.response_ok(self, data=response_data, message=self.singular_name + ' updated')

            error_resp = get_serielizer_error(serializer)
            transaction.savepoint_rollback(sp1)
            return ApiResponse.response_bad_request(self, message=error_resp)

        except Exception as e:
            transaction.savepoint_rollback(sp1)
            return ApiResponse.response_internal_server_error(self, message=[str(e.args[0])])

    @swagger_auto_schema_list
    def list(self, request, *args, **kwargs):
        '''
        :To get the all records
        '''
        try:
            # capture data
            query_params = request.query_params

            sort_by = query_params.get('sort_by') or 'id'
            sort_direction = query_params.get('sort_direction') or 'ascending'

            if sort_direction == 'descending':
                sort_by = '-' + sort_by

            obj_list = []
            
            status = query_params.get('status')
            obj_list = [('status__in',[1, 2, 3] )]
            if status:
                status = int(status)
                if status in [1, 2, 3]:
                    obj_list = [('status__in', [status])]
                else:
                    return ApiResponse.response_bad_request(self, message='Invalid status')
                
            gender = query_params.get('gender')
            obj_list = [('gender__in',[1, 2, 3] )]
            if gender:
                gender = int(gender)
                if gender in [1, 2, 3]:
                    obj_list = [('gender__in', [gender])]
                else:
                    return ApiResponse.response_bad_request(self, message='Invalid gender')
            
            
            start_date = query_params.get('start_date')
            end_date = query_params.get('end_date')
            if start_date and end_date:
                from datetime import datetime
                end_date = datetime.strptime(end_date, '%Y-%m-%d')
                end_date = datetime.combine(end_date, datetime.max.time())
                obj_list.append(['created_at__range', [start_date, end_date]])
            
            elif start_date:
                obj_list.append(['created_at__startswith', start_date])

            elif end_date:
                obj_list.append(['created_at__endswith', end_date])
            
            q_list = [Q(x) for x in obj_list]
            queryset = self.model_class.filter(reduce(operator.and_, q_list)).order_by(sort_by)

            '''Search for keyword'''
            if query_params.get('keyword'):
                queryset = queryset.filter(search_filter(self.search_fields, query_params.get('keyword')))

            resp_data = get_pagination_resp(queryset, request)

            response_data = transform_list(self, resp_data.get('data'))

            return ApiResponse.response_ok(self, data=response_data, paginator=resp_data.get('paginator'))
        except Exception as e:
            return ApiResponse.response_internal_server_error(self, message=[str(e.args[0])])

    @swagger_auto_schema_delete
    def delete(self, request, *args, **kwargs):
        '''
        :To delete the single record.
        '''
        try:
            get_id = self.kwargs.get('id')

            ''' get instance '''
            instance = self.get_object(get_id)
            if instance is None:
                return ApiResponse.response_not_found(self, message=self.singular_name + ' not found')

            instance.delete()

            ''' return success '''
            return ApiResponse.response_ok(self, message=self.singular_name + ' deleted')
        except Exception as e:
            return ApiResponse.response_internal_server_error(self, message=[str(e.args[0])])

    @swagger_auto_schema_bulk_delete
    def bulk_delete(self, request, *args, **kwargs):
        '''
        :To delete the multiple record.
        '''
        try:
            ''' capture data '''
            req_data = request.data
            ids = req_data.get('ids')

            if ids is None or type(ids) != list:
                return ApiResponse.response_bad_request(self, message='Please select '+ self.singular_name)

            instances = self.model_class.filter(id__in=ids)

            if not instances:
                return ApiResponse.response_not_found(self, message=self.singular_name + ' not found')

            instances.delete()

            ''' return success '''
            return ApiResponse.response_ok(self, message=self.singular_name + ' deleted.')
        except Exception as e:
            return ApiResponse.response_internal_server_error(self, message=[str(e.args[0])])

    ##Generate the response
    def transform_single(self, instance):
        resp_dict = dict()
        resp_dict['id'] = instance.id
        resp_dict['name'] = instance.name
        resp_dict['city'] = instance.city
        resp_dict['marks'] = instance.marks
        resp_dict['status'] = instance.status
        resp_dict['status_name'] = instance.get_status_display()
        resp_dict['gender'] = instance.gender
        resp_dict['gender_name'] = instance.get_gender_display()
        resp_dict['email'] = instance.email
        resp_dict['created_at'] = instance.created_at
        resp_dict['updated_at'] = instance.updated_at
        return resp_dict
        