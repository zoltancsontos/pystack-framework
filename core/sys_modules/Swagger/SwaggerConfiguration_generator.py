from core.base_resource import BaseResource
from falcon import falcon
from helpers.general_helpers import GeneralHelpers
from settings.settings import SETTINGS
import json


class SwaggerConfigurationGenerator(BaseResource):
    """
    Swagger configuration generator
    """
    excluded_prop_fields = ['id', 'created']

    python_to_swagger_type_mapping = {
        'bool': 'boolean',
        'int': 'integer',
        'long': 'integer',
        'float': 'number',
        'str': 'string',
        'tuple': 'array',
        'list': 'array',
        'dict': 'object'
    }

    non_uid_methods = ['GET', 'POST']
    uid_methods = ['GET', 'PUT', 'DELETE', 'PATCH']

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
    exclude_keywords = [
        'Page',
        'Swagger'
    ]

    @falcon.after(BaseResource.conn.close)
    def on_get(self, req=None, resp=None, uid=0):

        this = SwaggerConfigurationGenerator
        swagger_settings = SETTINGS['SWAGGER_CONFIG']
        app_url = self.__get_app_url__(req)
        app_routes = GeneralHelpers.get_app_routes()

        resp.content_type = 'application/json'
        resp.status = falcon.HTTP_200
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
            'tags': this.__get_tags__(app_routes),
            'paths': this.__get_paths__(app_routes),
            'definitions': this.__get_definitions__(app_routes)
        })

    @staticmethod
    def __get_tags__(app_routes):
        """
        Returns the swagger config tags
        :return: object
        """
        classes_used = []
        tags = []
        this = SwaggerConfigurationGenerator
        for route in app_routes:
            url, cls = this.__extract_route_parts__(route)
            res_name = cls.__class__.__name__
            if not this.__should_be_excluded__(res_name) and res_name not in classes_used:
                tags.append({
                    'name': res_name,
                    'description': 'rest service definition for url {}'.format(url)
                })
                classes_used.append(res_name)
        return tags

    @staticmethod
    def __get_paths__(app_routes):
        """
        Returns the swagger config paths
        :return: object
        """
        this = SwaggerConfigurationGenerator
        paths = {}
        urls_used = []
        for route in app_routes:
            url, cls = this.__extract_route_parts__(route)
            res_name = cls.__class__.__name__
            if not this.__should_be_excluded__(res_name):
                if url not in urls_used:
                    paths[url] = {}
                    urls_used.append(url)
                allowed_methods = getattr(cls.__class__, 'allowed_methods')
                model = getattr(cls.__class__, 'model')
                property_types = getattr(cls.__class__, 'property_types')
                use_property_types = len(property_types) != 0
                paths = this.__assign_methods_to_path__(url, paths, allowed_methods,
                                                        res_name, model.__name__, use_property_types)

        return paths

    @staticmethod
    def __assign_methods_to_path__(url, paths, allowed_methods, res_name, model_name, use_property_types = False):
        this = SwaggerConfigurationGenerator
        model = model_name

        if use_property_types:
            model = res_name + 'RequestModel'

        for method in allowed_methods:
            # Handle the crud methods with uid
            if method in ['GET', 'PUT', 'PATCH', 'DELETE'] and 'uid' in url:
                paths[url][method.lower()] = {
                    'parameters': this.__get_parameters_for_res__(True, model, method),
                    'tags': [res_name],
                    'summary': method.lower(),
                    'consumes': [BaseResource.default_content_type],
                    'produces': [BaseResource.default_content_type],
                    'responses': this.__get_path_responses__(model_name, method)
                }
            # Handle the crud methods without uid
            if method in ['GET', 'POST'] and 'uid' not in url:
                paths[url][method.lower()] = {
                    'parameters': this.__get_parameters_for_res__(False, model, method),
                    'tags': [res_name],
                    'summary': method.lower(),
                    'consumes': [BaseResource.default_content_type],
                    'produces': [BaseResource.default_content_type],
                    'responses': this.__get_path_responses__(model_name, method)
                }

        return paths

    @staticmethod
    def __get_parameters_for_res__(use_uid, model_name, method):
        """
        Returns parameters for uid type resource
        :param use_uid: Boolean
        :param model_name: str
        :param method: str
        :return: list
        """
        param_list = []
        if use_uid:
            param_list.append({
                'in': 'path',
                'name': 'uid',
                'type': 'integer',
                'required': True,
                'description': 'matching uid of resource'
            })
        if method != 'GET' and method != 'DELETE':
            param_list.append({
                'in': 'body',
                'name': model_name,
                'description': '',
                'schema': {
                    '$ref': '#/definitions/{}'.format(model_name)
                }
            })
        return param_list

    @staticmethod
    def __get_path_responses__(response_name, method):
        """
        Returns the matching path responses
        :param response_name: str
        :param method: str
        :return: dict
        """
        data = {
            "200": {
                "description": "OK",
                "schema": {
                    "$ref": "#/definitions/{}".format(response_name)
                }
            },
            "204": {
                "description": "No content"
            },
            "400": {
                "description": "Bad Request"
            },
            "401": {
                "description": "Unauthorized"
            },
            "404": {
                "description": "Not Found"
            }
        }
        if method != 'GET' and method != 'DELETE':
            data['201'] = {
                "description": "Created"
            }
        return data

    @staticmethod
    def __get_definitions__(app_routes):
        """
        Returns the swagger config definitions
        :return:  object
        """
        definitions = {}
        used_definitions = []
        this = SwaggerConfigurationGenerator
        for route in app_routes:
            url, cls = this.__extract_route_parts__(route)
            model, request = this.__extract_model_and_request_body__(cls)
            if model:
                model_name = model.__name__
                if model_name not in used_definitions:
                    definitions[model_name] = this.__get_model_properties_list__(model)
                    used_definitions.append(model_name)
            if len(request) != 0:
                model_name = cls.__class__.__name__ + 'RequestModel'
                if model_name not in used_definitions:
                    definitions[model_name] = this.__create_request_obj__definition(request)
                    used_definitions.append(model_name)

        return definitions

    @staticmethod
    def __get_model_properties_list__(model):
        """
        Extracts the model properties and map them to matching swagger types
        :param model: object
        :return: dict
        """
        this = SwaggerConfigurationGenerator
        data = {
            'type': 'object',
            'properties': {}
        }
        prop_list = this.__get_property_list_with_types__(model, True)
        for prop in prop_list:
            prop_name = prop['prop_name']
            item_type = prop['type']
            data['properties'][prop_name] = {
                'type': item_type
            }
        return data

    @staticmethod
    def __create_request_obj__definition(request_obj):
        """
        Creates the request object definitions
        :param request_obj: dict
        :return: dict
        """
        this = SwaggerConfigurationGenerator
        data = {
            'type': 'object',
            'properties': {}
        }
        for prop in request_obj:
            if 'key' in prop and 'type' in prop:
                prop_name = prop['key']
                type_df = prop['type']
                prop_type = 'object' if type_df not in this.python_to_swagger_type_mapping else \
                    this.python_to_swagger_type_mapping[type_df]
                data['properties'][prop_name] = {
                    'type': prop_type
                }
        return data

    @staticmethod
    def __get_property_list_with_types__(item_class, is_model=False):
        """
        Returns the property list of a given class
        :param item_class: object
        :param is_model: boolean
        :return: list
        """
        this = SwaggerConfigurationGenerator
        props = []
        raw_properties = vars(item_class)
        non_private_properties = list(filter(lambda i:
                                             not i.startswith('__') and
                                             not i.startswith('_'),
                                             raw_properties))
        for item in non_private_properties:
            if item not in this.excluded_prop_fields:
                attr_type = getattr(item_class, item)
                attr_type_name = attr_type.__class__.__name__
                if 'type' not in attr_type_name \
                        and 'BackrefAccessor' not in attr_type_name \
                        and attr_type_name != 'list':
                    props.append({
                        'prop_name': item,
                        'type': this.model_property_type_mapping[attr_type_name] if is_model else attr_type_name
                    })

        return props

    @staticmethod
    def __extract_route_parts__(route):
        """
        Extracts the url prats
        :param route: dict
        :return:
        """
        url, cls = route['url'], route['controller']
        return url, cls

    @staticmethod
    def __should_be_excluded__(class_name):
        """
        Checks if a resource should be excluded
        :param class_name: str
        :return: boolean
        """
        this = SwaggerConfigurationGenerator
        for keyword in this.exclude_keywords:
            if keyword in class_name:
                return True
        return False

    @staticmethod
    def __extract_model_and_request_body__(cls):
        """
        Tries to extract the model and property_types class properties
        :param cls: object
        :return: model, request_body
        """
        model = getattr(cls, 'model')
        request_body = getattr(cls, 'property_types')
        return model, request_body

    @staticmethod
    def __get_app_url__(req):
        app_host = req.host
        app_port = ':' + str(req.port) if req.port is not None else ''
        app_url = '{0}{1}'.format(app_host, app_port)
        return app_url
