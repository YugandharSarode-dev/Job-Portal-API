
from drf_yasg.openapi import Parameter, IN_QUERY, IN_PATH
from drf_yasg.utils import swagger_auto_schema
import json

response_list = {
    'message': [
        'Ok'
    ],
    'code': 200,
    'success': True,
    'data': []
}

response_get = {
    'message': [
        'Ok'
    ],
    'code': 200,
    'success': True,
    'data': {}
}

response_post = {
    'message': [
        'Products created'
    ],
    'code': 201,
    'success': True,
    'data': {}
}


response_update = {
    'message': [
        'Products updated'
    ],
    'code': 200,
    'success': True,
    'data': {}
}

response_delete = {
    'message': [
        'Products deleted'
    ],
    'code': 200,
    'success': True,
    'data': {}
}

response_unauthenticate = {
    'message': [
        "Authentication credentials were not provided."
    ],
    'code': 403,
    'success': True,
    'data': {}
}

response_unauthorized = {
    'message': [
        "Unauthorized"
    ],
    'code': 401,
    'success': True,
    'data': {}

}

response_bad_request = {
    'message': [
        'Products already exists.'
    ],
    'code': 400,
    'success': True,
    'data': {}
}

response_not_found = {
    'message': [
        'Products not found'
    ],
    'code': 404,
    'success': True,
    'data': {}
}

swagger_auto_schema_list = swagger_auto_schema(
    manual_parameters=[
        Parameter('sort_by', IN_QUERY, description='sort by id', type='int'),
        Parameter('sort_direction', IN_QUERY, description='sort_direction in ascending,descending', type='char'),
        Parameter('id', IN_QUERY, description='id parameter', type='char'),
        Parameter('keyword', IN_QUERY, description='keyword paramater', type='char'),
        Parameter('page', IN_QUERY, description='page no. paramater', type='int'),
        Parameter('limit', IN_QUERY, description='limit paramater', type='int'),
        Parameter('type', IN_QUERY, description='All result set type=all', type='char'),
        Parameter('status', IN_QUERY, description='status paramater', type='char'),

        Parameter('start_date', IN_QUERY, description='start_date paramater', type='char'),

        Parameter('end_date', IN_QUERY, description='end_date paramater', type='char'),

    ],
    responses={
        '200': json.dumps(response_list),
        '403': json.dumps(response_unauthenticate),
        '401': json.dumps(response_unauthorized),
        '404': json.dumps(response_not_found)
    },

    operation_id='list products',
    operation_description='API to list products data',
)

swagger_auto_schema_post = swagger_auto_schema(
    responses={
        '201': json.dumps(response_post),
        '403': json.dumps(response_unauthenticate),
        '401': json.dumps(response_unauthorized),
        '400': json.dumps(response_bad_request),
        '404': json.dumps(response_not_found),
    },

    operation_id='Create products',
    operation_description='API to add new products request::  {}',
)

swagger_auto_schema_update = swagger_auto_schema(
    responses={
        '200': json.dumps(response_update),
        '403': json.dumps(response_unauthenticate),
        '401': json.dumps(response_unauthorized),
        '400': json.dumps(response_bad_request),
        '404': json.dumps(response_not_found),
    },

    operation_id='update products',
    operation_description='API to update products',
)

swagger_auto_schema_delete = swagger_auto_schema(
    responses={
        '200': json.dumps(response_delete),
        '403': json.dumps(response_unauthenticate),
        '401': json.dumps(response_unauthorized),
        '404': json.dumps(response_not_found),
    },

    operation_id='delete products',
    operation_description='API to delete products',
)

swagger_auto_schema_bulk_delete = swagger_auto_schema(
    responses={
        '200': json.dumps(response_delete),
        '403': json.dumps(response_unauthenticate),
        '401': json.dumps(response_unauthorized),
        '404': json.dumps(response_not_found),
    },

    operation_id='delete products',
    operation_description='API to bulk delete products',
)

swagger_auto_schema = swagger_auto_schema(
    responses={
        '200': json.dumps(response_get),
        '403': json.dumps(response_unauthenticate),
        '401': json.dumps(response_unauthorized),
        '404': json.dumps(response_not_found),
    },

    operation_id='Fetch products',
    operation_description='API to fetch products',
)
    