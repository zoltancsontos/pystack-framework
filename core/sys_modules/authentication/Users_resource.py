from core.base_resource import BaseResource
from core.sys_modules.authentication.Users_model import UsersModel
from core.sys_modules.authentication.UserServices import UserServices
from core.sys_modules.authentication.UsersPermissions_model import UsersPermissionsModel
from core.sys_modules.authentication.PermissionGroups_model import PermissionGroupsModel
from falcon import falcon
import json


class UsersResource(BaseResource):
    """
    Users resource handler
    """
    model = UsersModel
    permissions_model = UsersPermissionsModel
    property_types = []
    allowed_methods = ['GET']
    transient_properties = ['password']

    @falcon.after(BaseResource.conn.close)
    def on_get(self, req=None, resp=None, uid=0):
        """
        Returns the filtered user data
        :param req:
        :param resp:
        :param uid:
        :return:
        """
        token = None if 'token' not in req.cookies else req.cookies['token']
        content_type = '' if req.content_type is None else req.content_type
        if token is not None:
            payload = UserServices.get_data_from_token(token)
            if payload:
                payload_data = payload['payload']
                user_id = payload_data['user_id']
                try:
                    db_data = self.permissions_model.select()\
                        .join(PermissionGroupsModel, on=(PermissionGroupsModel.id == UsersPermissionsModel.id))\
                        .where(UsersPermissionsModel.user == user_id)
                except self.model.DoesNotExist:
                    db_data = None
                    BaseResource.conn.close()
                if db_data is not None:

                    user_details = {}
                    groups = []

                    for db_item in db_data:
                        parsed_data = db_item.to_dict()
                        groups.append(parsed_data['group']['group_name'])
                        user_details = parsed_data['user']

                    for transient in self.transient_properties:
                        del user_details[transient]

                    data = {
                        'permissions': groups,
                        'user_details': user_details
                    }

                    resp.content_type = "application/json"
                    resp.status = falcon.HTTP_200
                    resp.body = (json.dumps(data, indent=4, sort_keys=True, default=str))
                    return
            BaseResource.conn.close()
            raise falcon.HTTPBadRequest('Ooops', 'something went wrong...')
        else:
            if 'json' not in content_type:
                BaseResource.conn.close()
                raise falcon.HTTPTemporaryRedirect('/login')
            else:
                BaseResource.conn.close()
                raise falcon.HTTPUnauthorized('Access denied', 'in order to continue please log in')


