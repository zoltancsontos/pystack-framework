from core.base_resource import BaseResource
from falcon import falcon
from helpers.general_helpers import GeneralHelpers
from settings.settings import SETTINGS
import json
import inspect


class SwaggerConfigHandler(BaseResource):
    """
    Swagger configuration generator
    """
    model = None
    allowed_methods = ['GET']
    url_blacklist = [
        '/',
        '/login'
    ]
    group_access = ['ADMIN', 'DEVELOPER']
    model_property_type_mapping = {
        'IntegerField': 'integer',
        'BigIntegerField': 'integer',
        'SmallIntegerField': 'integer',
        'AutoField': 'integer',
        'BigAutoField': 'integer',
        'IdentityField': 'integer',
        'FloatField': 'number',
        'DoubleField': 'number',
        'DecimalField': 'number',
        'CharField': 'string',
        'FixedCharField': 'string',
        'TextField': 'string',
        'BlobField': 'object',
        'BitField': 'integer',
        'BigBitField': 'integer',
        'UUIDField': 'string',
        'BinaryUUIDField': 'object',
        'DateTimeField': 'string',
        'DateField': 'string',
        'TimeField': 'string',
        'TimestampField': 'integer',
        'IPField': 'integer',
        'BooleanField': 'boolean',
        'BareField': 'object',
        'ForeignKeyField': 'integer'
    }

    @falcon.after(BaseResource.conn.close)
    def on_get(self, req=None, resp=None, uid=0):
        """
        Handles the swagger config generation
        :param req:
        :param resp:
        :param uid:
        :return:
        """
        routes = GeneralHelpers.get_app_routes()
        tags = []
        used_tag_names = []
        paths = {}
        definitions = {}
        model_names = {}
        expected_request_types = []

        for route in routes:
            controller = route['controller']
            url = route['url']
            all_members = inspect.getmembers(controller)
            instance_name = controller.__class__.__name__

            if 'Swagger' not in instance_name and url not in self.url_blacklist:
                SwaggerConfigHandler.__process_tags__(instance_name, used_tag_names, tags)

                paths[url] = {}
                path_methods = []

                if len(all_members) != 0:
                    for member in all_members:
                        method_name = member[0]
                        method_val = member[1]
                        if 'allowed_methods' in method_name:
                            for val in method_val:
                                path_methods.append(val.lower())
                        if 'model' in method_name:
                            definition_name = method_val.__name__ if inspect.isclass(method_val) \
                                else method_val.__class__.__name__
                            if definition_name is not None and inspect.isclass(method_val):
                                raw_properties = vars(method_val)
                                non_private_properties = list(filter(lambda i:
                                                                     not i.startswith('__') and
                                                                     not i.startswith('_'),
                                                                     raw_properties))
                                properties = list(filter(lambda i:
                                                         i != 'DoesNotExist' and
                                                         i != 'created' and
                                                         i != 'id', non_private_properties))
                                if definition_name not in definitions:
                                    definitions[definition_name] = {
                                        'type': 'object',
                                        'properties': SwaggerConfigHandler.__handle_def_property_list__(properties,
                                                                                                        method_val)
                                    }
                                model_names[url] = {
                                    'model': definition_name,
                                    'expected_request_body': None
                                }

                        if 'property_types' in method_name:
                            if method_val is not None:
                                if url not in expected_request_types:
                                    expected_request_types.append({
                                        'url': url,
                                        'value': method_val
                                    })

                if 'Page' not in instance_name:
                    for expected_type in expected_request_types:
                        item_url = expected_type['url']
                        if item_url in model_names:
                            model_names[item_url]['expected_request_body'] = expected_type['value']
                    SwaggerConfigHandler.__handle_path_methods__(path_methods, url, model_names, instance_name, paths)

        resp.content_type = 'application/json'
        resp.status = falcon.HTTP_200

        app_host = req.host
        app_port = ':' + str(req.port) if req.port is not None else ''
        app_url = '{0}{1}'.format(app_host, app_port)

        swagger_settings = SETTINGS['SWAGGER_CONFIG']

        BaseResource.conn.close()
        resp.body = json.dumps({
            'swagger': '2.0',
            'info': {
                'description': swagger_settings['DOCUMENTATION_DESCRIPTION'],
                'version': SETTINGS['APP_VERSION'],
                'title': swagger_settings['DOCUMENTATION_TITLE'],
                'termsOfService': swagger_settings['TERMS_AND_CONDITIONS_URL'],
                'contact': {},
                'license': {
                    'name': 'Apache 2.0',
                    'url': 'http://www.apache.org/licenses/LICENSE-2.0'
                }
            },
            'host': app_url,
            'basePath': '/',
            'tags': tags,
            'paths': paths,
            'definitions': definitions
        })
        return

    @staticmethod
    def __handle_path_methods__(path_methods, url, model_names, instance_name, paths):
        """
        Handles the path method assignment
        :param path_methods:
        :param url:
        :param model_names:
        :param instance_name:
        :param paths:
        :return:
        """
        for path_method in path_methods:
            # handling of uid methods
            expected_request_body = model_names[url]['expected_request_body']
            used_model_name = model_names[url]['model'] if url in model_names else ''
            if (path_method == 'get' or
                path_method == 'put' or
                path_method == 'patch' or
                path_method == 'delete') and 'uid' in url:
                paths[url][path_method] = \
                    SwaggerConfigHandler.__get_path_object__(instance_name, path_method, used_model_name,
                                                             True, expected_request_body)

            # handling of non uid methods
            if (path_method == 'get' or
                path_method == 'post') and 'uid' not in url:
                paths[url][path_method] = \
                    SwaggerConfigHandler.__get_path_object__(instance_name, path_method, used_model_name,
                                                             False, expected_request_body)

    @staticmethod
    def __process_tags__(instance_name, used_tag_names, tags):
        """
        Process the tag values
        :param instance_name:
        :param used_tag_names:
        :param tags:
        :return:
        """
        if instance_name not in used_tag_names and 'Page' not in instance_name:
            tags.append({
                'name': instance_name,
                'description': 'rest service definition'
            })
            used_tag_names.append(instance_name)

    @staticmethod
    def __handle_def_property_list__(properties, class_method):
        data = {}
        type_mapping = SwaggerConfigHandler.model_property_type_mapping
        for prop in properties:
            prop_class = getattr(class_method, prop)
            field_name = prop_class.__class__.__name__
            mapped_type = 'object' if field_name not in type_mapping else type_mapping[field_name]
            data[prop] = {
                'type': mapped_type
            }
        return data

    @staticmethod
    def __get_path_object__(instance_name, path_method, schema, uid=None, expected_request_body=None):
        uid_operation_id = "Uid" if uid is not None else ""
        request_body_methods = ['post', 'put', 'patch', 'delete']
        data = {
            'tags': [instance_name],
            'summary': path_method,
            'consumes': ['application/json'],
            'produces': ['application/json'],
            'operationId': path_method + instance_name.replace('Resource', '') +
                            uid_operation_id + 'Using' + path_method.upper(),
            'responses': {
                '200': {
                    'description': 'OK',
                    'schema': {
                        '$ref': '#/definitions/{}'.format(schema)
                    }
                },
                '201': {
                    'description': 'Created',
                },
                '204': {
                    'description': 'No content',
                },
                '401': {
                    'description': 'Unauthorized'
                },
                '400': {
                    'description': 'Bad Request'
                },
                '404': {
                    'description': 'Not Found'
                }
            }
        }
        if uid:
            data['parameters'] = [{
                'in': 'path',
                'name': 'uid',
                'type': 'integer',
                'required': True,
                'description': 'matching uid of the resource'
            }]
        if path_method in request_body_methods:
            if expected_request_body is None:
                param = {
                    'in': 'body',
                    'name': schema,
                    'description': '',
                    'schema': {
                        '$ref': '#/definitions/{}'.format(schema)
                    }
                }
            else:
                param = {
                    'in': 'body',
                    'name': schema,
                    'description': '',
                    'schema': {
                        'type': 'object',
                        'required': [],
                        'properties': {}
                    }
                }
                for item in expected_request_body:
                    if item['required']:
                        param['schema']['required'].append(item['key'])
                    param['schema']['properties'][item['key']] = {
                        'type': SwaggerConfigHandler.__convert_python_type_to_json_type__(item['type'])
                    }
            if uid:
                data['parameters'].append(param)
            else:
                data['parameters'] = [param]
        return data

    @staticmethod
    def __convert_python_type_to_json_type__(python_type):
        if python_type == 'str':
            return 'string'
        return 'object'
