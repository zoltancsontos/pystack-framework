from core.base_resource import BaseResource
from falcon import falcon
from helpers.general_helpers import GeneralHelpers
import json
import inspect


class SwaggerConfigHandler(BaseResource):
    """
    TimeSeries resource handler
    """
    model = None
    property_types = [],
    allowed_methods = ['GET']

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

        for route in routes:
            controller = route['controller']
            url = route['url']
            all_members = inspect.getmembers(controller)
            instance_name = controller.__class__.__name__

            if 'Swagger' not in instance_name:
                if instance_name not in used_tag_names and 'Page' not in instance_name:
                    tags.append({
                        'name': instance_name,
                        'description': 'rest api definitions'
                    })
                    used_tag_names.append(instance_name)

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
                            definition_name = method_val().__class__.__name__
                            raw_properties = vars(method_val)
                            non_private_properties = list(filter(lambda i:
                                                                 not i.startswith("__") and
                                                                 not i.startswith("_"),
                                                                 raw_properties))
                            properties = list(filter(lambda i:
                                                     i != 'DoesNotExist' and
                                                     i != 'created' and
                                                     i != 'id', non_private_properties))
                            if definition_name not in definitions:
                                definitions[definition_name] = {
                                    'type': 'object',
                                    'properties': SwaggerConfigHandler.__handle_def_property_list__(properties, method_val)
                                }
                            # handle properties

                if 'Page' not in instance_name:

                    for path_method in path_methods:
                        # handling of uid methods
                        if (path_method == 'get' or
                                path_method == 'put' or
                                path_method == 'patch' or
                                path_method == 'delete') and 'uid' in url:
                            paths[url][path_method] = \
                                SwaggerConfigHandler.__get_path_object__(instance_name, path_method, None)

                        # handling of non uid methods
                        if (path_method == 'get' or
                                path_method == 'post') and 'uid' not in url:
                            paths[url][path_method] = \
                                SwaggerConfigHandler.__get_path_object__(instance_name, path_method, None)

        print(paths)
        print('Model', definitions)

        resp.content_type = "application/json"
        resp.status = falcon.HTTP_200
        resp.body = json.dumps({
            "swagger": "2.0",
            "info": {
                "description": "PySaw app - api documentation",
                "version": "1.0",
                "title": "Api Documentation",
                "termsOfService": "urn:tos",
                "contact": {},
                "license": {
                    "name": "Apache 2.0",
                    "url": "http://www.apache.org/licenses/LICENSE-2.0"
                }
            },
            "host": "localhost:5555",
            "basePath": "/",
            "tags": tags,
            "paths": paths,
            # "definitions": {
            #     "AlertsRes": {
            #         "type": "object",
            #         "properties": {
            #             "actionRequired": {
            #                 "type": "boolean"
            #             },
            #             "completedCount": {
            #                 "type": "integer",
            #                 "format": "int64"
            #             },
            #             "inWorkCount": {
            #                 "type": "integer",
            #                 "format": "int64"
            #             },
            #             "inWorkRecur24Hrs": {
            #                 "type": "integer",
            #                 "format": "int64"
            #             },
            #             "newCount": {
            #                 "type": "integer",
            #                 "format": "int64"
            #             }
            #         }
            #     }
            # }
            "definitions": definitions
        })
        return

    @staticmethod
    def __handle_def_property_list__(properties, class_method):
        data = {}
        for prop in properties:
            data[prop] = {
                "type": "any"
            }
        return data

    @staticmethod
    def __get_path_object__(instance_name, path_method, schema):
        return {
            'tags': [instance_name],
            'summary': path_method,
            'consumes': 'application/json',
            'produces': 'application/json',
            'operationId': path_method + "Using" + path_method.upper(),
            "responses": {
                "200": {
                    "description": "OK",
                    "schema": {
                        "$ref": "#/definitions/{}".format(instance_name.replace('Resource', 'Model'))
                    }
                },
                "401": {
                    "description": "Unauthorized"
                },
                "400": {
                    "description": "Bad Request"
                },
                "404": {
                    "description": "Not Found"
                }
            }
        }
