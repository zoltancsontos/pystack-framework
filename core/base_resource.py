from falcon import *
from core.db_adapter import mysql_adapter
import json
from settings.settings import SETTINGS


class BaseResource(object):
    """
    REST API Resource base class
    """
    model = None
    conn = mysql_adapter
    default_content_type = "application/json"
    property_types = []
    allowed_methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
    transient_properties = []
    expected_request_body = None
    group_access = SETTINGS['PERMISSIONS']['GROUPS']

    def __bad_request__(self, resp, props):
        """
        Returns a bad request
        Args:
            resp: object
            props: dictionary
        Returns:
        """
        resp.status = falcon.HTTP_400
        resp.content_type = self.default_content_type
        body = {
            'message': 'Invalid request: Missing property or type mismatch',
            'errors': props
        }
        resp.body = (json.dumps(body))

    def __method_not_allowed__(self, resp):
        """
        Returns a method not allowed status
        :param resp: object
        :return:
        """
        resp.status = falcon.HTTP_405
        resp.content_type = self.default_content_type
        body = {
            'message': 'Method not allowed'
        }
        resp.body = (json.dumps(body))

    def __check_if_method_allowed(self, method, resp):
        """
        Checks if the requested method is allowed if not return the matching error
        :param method: string
        :param resp: object
        :return:
        """
        if method not in self.allowed_methods:
            self.__method_not_allowed__(resp)
        else:
            return True

    @staticmethod
    def __get_prop_by_key__(src, key):
        """
        Returns dictionary from property_types based on key
        Args:
            src: list
            key: string
        Returns: dictionary
        """
        found_item = None
        for item in src:
            if item['key'] == key:
                found_item = item
                break
        return found_item

    def __process_property_types(self):
        """
        Process the property list
        Returns: list, list
        """
        props = []
        prop_types = []
        for prop in self.property_types:
            props.append(prop['key'])
            prop_types.append(prop['type'])
        return props, prop_types

    def __process_mandatory_property_types__(self):
        """
        Process the mandatory property types list
        Returns: list, list
        """
        # Order the mandatory props
        mandatory_props = []
        prop_types = []
        for prop in self.property_types:
            if prop['required']:
                mandatory_props.append(prop['key'])
                prop_types.append(prop['type'])
        return mandatory_props, prop_types

    @staticmethod
    def __process_request_properties__(req_data):
        """
        Process the request data properties
        Args:
            req_data: dictionary
        Returns:
        """
        request_props = []
        request_types = []
        for req in req_data:
            request_props.append(req)
            request_types.append(type(req_data[req]))
        return request_props, request_types

    def __props_exists__(self, req_data, resp):
        """
        Checks if the properties from the request exists in the validation fields
        Args:
            req_data:
            resp:
        Returns:
        """
        valid_request = True
        prop_list = []

        props, prop_types = self.__process_property_types()
        request_props, request_types = self.__process_request_properties__(req_data)

        for i, key in enumerate(request_props):

            if key not in props:
                valid_request = False
                prop_list.append({
                    'prop': key,
                    'reason': 'invalid or not specified property'
                })
                break

            prop_definition = self.__get_prop_by_key__(self.property_types, key)
            if prop_definition['type'] != request_types[i]:
                valid_request = False
                prop_list.append({
                    'prop': key,
                    'reason': 'expected ' + str(prop_types[i]) + ' got ' + str(request_types[i])
                })
                break
        if not valid_request:
            self.__bad_request__(resp, prop_list)
        return valid_request

    def __has_mandatory_props__(self, req_data, resp):
        """
        Validates if the request contains all the mandatory model property types
        Args:
            req_data: dictionary
            resp: object
        Returns:
        """
        valid_request = True
        prop_list = []

        if len(self.property_types) != 0:

            # Order the mandatory props
            mandatory_props, prop_types = self.__process_mandatory_property_types__()

            # Order the request props
            request_props, request_types = self.__process_request_properties__(req_data)

            # Check if we have all the mandatory properties
            for i, val in enumerate(mandatory_props):
                if val not in request_props:
                    valid_request = False
                    prop_list.append({
                        'prop': val,
                        'reason': 'missing'
                    })
                    break

            # Check if the types are matching
            if valid_request:
                for i, val in enumerate(request_props):
                    req_type = request_types[i]
                    orgn_def = self.__get_prop_by_key__(self.property_types, val)
                    if orgn_def['type'] != req_type:
                        valid_request = False
                        prop_list.append({
                            'prop': val,
                            'reason': 'expected ' + str(prop_types[i]) + ' got ' + str(request_types[i])
                        })
                        break

            if not valid_request:
                self.__bad_request__(resp, prop_list)
        return valid_request

    def __process_transient_fields__(self, body):
        """
        Removes fields that are marked transient
        :param body:
        :return:
        """
        if len(self.transient_properties) != 0:
            if 'message' not in body:
                for transient_prop in self.transient_properties:
                    if transient_prop in body:
                        del body[transient_prop]
        return body

    @falcon.after(conn.close)
    def on_get(self, req=None, resp=None, uid=0):
        """
        Default GET method handler
        Args:
            req: object
            resp: object
            uid: integer
        Returns:
        """
        if self.__check_if_method_allowed("GET", resp):
            if self.model is not None:
                if req.params:
                    page = None if 'page' not in req.params else req.params['page']
                    results_no = None if 'results' not in req.params else req.params['results']
                    data = self.model().get_filtered_list(query=req.params,
                                                          model=self.model,
                                                          page=page,
                                                          results_no=results_no)
                    resp.status = falcon.HTTP_200
                elif uid != 0:
                    q = self.model().get_by_id(self.model, uid)
                    if 'error' in q:
                        resp.status = falcon.HTTP_404
                        data = {
                            'message': 'item with id {id} doesn\'t exist'.format(id=uid)
                        }
                    else:
                        resp.status = falcon.HTTP_200
                        data = q
                else:
                    data = list(map(self.__process_transient_fields__, self.model().get_list()))
                    resp.status = falcon.HTTP_200
                body = data
            else:
                resp.status = falcon.HTTP_400
                body = {
                    'message': 'Missing resource model'
                }
            body = self.__process_transient_fields__(body)
            resp.content_type = self.default_content_type
            resp.body = (json.dumps(body, indent=4, sort_keys=True, default=str))

    @falcon.after(conn.close)
    def on_post(self, req, resp):
        """
        REST API default post method handler
        Args:
            req: object
            resp: object
        Returns:
        """
        if self.__check_if_method_allowed("POST", resp):
            req_body = req.stream.read().decode('utf-8')
            content = json.loads(req_body, encoding='utf-8')
            if self.__has_mandatory_props__(content, resp):
                last_id = self.model().add(content)
                content['id'] = last_id
                resp.status = falcon.HTTP_201
                resp.content_type = "application/json"
                content = self.__process_transient_fields__(content)
                resp.body = (json.dumps(content))

    @falcon.after(conn.close)
    def on_patch(self, req, resp, uid=0):
        """
        REST API default PATCH method handler
        Args:
            req: object
            resp: object
            uid: integer
        Returns:
        """
        if self.__check_if_method_allowed("PATCH", resp):
            req_body = req.stream.read().decode('utf-8')
            req_data = json.loads(req_body, encoding='utf-8')

            if self.__props_exists__(req_data, resp):

                content = self.model().get_by_id(self.model, uid)
                if 'error' not in content:
                    self.model().change(req_data, self.model, uid)
                    resp.status = falcon.HTTP_200
                else:
                    content = {
                        'message': 'resource with {id} doesn\'t exists'.format(id=uid)
                    }
                    resp.status = falcon.HTTP_404

                # Update the response object
                for key in req_data:
                    if key in content:
                        content[key] = req_data[key]

                resp.content_type = 'application/json'
                content = self.__process_transient_fields__(content)
                resp.body = (json.dumps(content))

    @falcon.after(conn.close)
    def on_put(self, req, resp, uid=0):
        """
        REST API default PUT method handler
        Args:
            req: object
            resp: object
            uid: integer
        Returns:
        """
        if self.__check_if_method_allowed("PUT", resp):
            resp.status = falcon.HTTP_400
            req_body = req.stream.read().decode('utf-8')
            req_data = json.loads(req_body, encoding='utf-8')

            content = {
                'message': 'missing id parameter, eg. PUT /resource/{id}'
            }
            if self.__has_mandatory_props__(req_data, resp) and uid != 0:
                if self.__has_mandatory_props__(req_data, resp):
                    self.model().change(req_data, self.model, uid)
                    resp.status = falcon.HTTP_201
                resp.content_type = "application/json"
                content = self.__process_transient_fields__(content)
                resp.body = (json.dumps(req_data))
            if uid == 0:
                content = self.__process_transient_fields__(content)
                resp.body = (json.dumps(content))

    @falcon.after(conn.close)
    def on_delete(self, req, resp, uid=0):
        """
        REST API default DELETE method handler
        Args:
            req: object
            resp: object
            uid: number
        Returns:
        """
        if self.__check_if_method_allowed("DELETE", resp):
            item_id = 0
            if 'id' in req.params:
                item_id = req.params['id']
            elif uid != 0:
                item_id = uid
            if item_id != 0:
                self.model().remove(self.model, item_id)
            resp.status = falcon.HTTP_204
            resp.content_type = "application/json"
