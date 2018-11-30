from core.base_resource import BaseResource
from falcon import falcon
import json

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
            "tags": [{
                "name": "alerts-controller",
                "description": "Alerts Controller"
            }],
            "paths": {
                "/alerts/": {
                    "get": {
                        "tags": ["alerts-controller"],
                        "summary": "get",
                        "operationId": "getUsingGET",
                        "consumes": ["application/json"],
                        "produces": ["*/*"],
                        "responses": {
                            "200": {
                                "description": "OK",
                                "schema": {
                                    "$ref": "#/definitions/AlertsRes"
                                }
                            },
                            "401": {
                                "description": "Unauthorized"
                            },
                            "403": {
                                "description": "Forbidden"
                            },
                            "404": {
                                "description": "Not Found"
                            }
                        }
                    }
                }
            },
            "definitions": {
                "AlertsRes": {
                    "type": "object",
                    "properties": {
                        "actionRequired": {
                            "type": "boolean"
                        },
                        "completedCount": {
                            "type": "integer",
                            "format": "int64"
                        },
                        "inWorkCount": {
                            "type": "integer",
                            "format": "int64"
                        },
                        "inWorkRecur24Hrs": {
                            "type": "integer",
                            "format": "int64"
                        },
                        "newCount": {
                            "type": "integer",
                            "format": "int64"
                        }
                    }
                }
            }
        })
        return
