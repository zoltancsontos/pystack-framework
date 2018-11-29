from peewee import *
from settings.settings import SETTINGS
from datetime import datetime
from playhouse.shortcuts import model_to_dict
import json

database_proxy = Proxy()


class BaseModel(Model):
    """
    Base model definition
    """
    __required_fields__ = []
    initial_data = []

    class Meta:
        database = database_proxy
        schema = SETTINGS['DATABASE']['SCHEMA']

    @staticmethod
    def __find_fk_indexes__(s_model):
        """
        Returns the foreign key index
        :param s_model:
        :return:
        """
        fields = s_model._meta.sorted_fields
        i = 0
        indexes = []
        rel_models = []
        while i < len(fields):
            field = fields[i]
            if isinstance(field, ForeignKeyField):
                indexes.append(i)
                rel_models.append(field.rel_model)
            else:
                rel_models.append(None)
            i += 1
        return indexes, rel_models

    def __prepare_json__(self, single_model):
        """
        Prepares the model to be json serializable
        Args:
            single_model: Model
        Returns: dict
        """
        processed_item = {}
        item_data = {}
        for attr, value in vars(single_model).items():
            if "_data" in attr:
                item_data = value
        fk_indexes, fk_models = self.__find_fk_indexes__(single_model)
        for index, (prop, val) in enumerate(item_data.items()):
            val_ref = val
            if index in fk_indexes:
                model_ref = fk_models[index]
                model_instance = fk_models[index]()
                rel_data = model_instance.get_by_id(model_ref, val)
                val_ref = rel_data
            try:
                processed_item[prop] = json.loads(val_ref)
            except (ValueError, TypeError):
                if isinstance(val, datetime):
                    processed_item[prop] = val.strftime("%Y-%m-%d %H:%M:%S")
                else:
                    processed_item[prop] = val_ref
        return processed_item

    def __is_valid__(self, req=None):
        """
        Checks if model contains all the required properties
        Args:
            req: dictionary
        Returns: boolean
        """
        valid = True
        if req:
            keys = []
            for key in req:
                keys.append(key)
            for prop in self.__required_fields__:
                if prop not in keys:
                    valid = False
                    break
        if not valid:
            raise AttributeError('Missing mandatory model attributes, check model definition')
        return valid

    def __contains_properties__(self, req=None):
        """
        Checks if req properties are valid model props
        Args:
            req: dictionary
        Returns: boolean
        """
        contains_prop = True
        props = req
        if isinstance(req, dict):
            props = list(req.keys())

        if props:
            for item in props:
                model_attr = getattr(self, item, None)
                if model_attr is not None:
                    contains_prop = False
                    break
        if not contains_prop:
            raise AttributeError('Using non-defined model property, please check model definition')
        return contains_prop

    def get_list(self):
        """
        Returns the list of models
        Returns: list<dictionary>
        """
        res = self.select()
        data = []
        for item in res:
            processed_item = BaseModel.__prepare_json__(self, item)
            data.append(processed_item)
        return data

    def get_filtered_list(self, query=None, model=None, page=None, results_no=None):
        """
        Returns a list of models based on filter
        Args:
            model: Class
            query: Dict
            page: integer
            results_no: integer
        Returns: list
        """
        if self.__contains_properties__(query):
            exp_list = []
            for key in query:
                single_prop = getattr(model, key)
                exp_list.append(single_prop == query[key])
            if page is not None and results_no is not None:
                res = self.select().where(*exp_list).paginate(page, results_no)
            else:
                res = self.select().where(*exp_list)
            data = []
            if res:
                for item in res:
                    processed_item = BaseModel.__prepare_json__(self, item)
                    data.append(processed_item)
            return data

    def get_by_id(self, model, pk):
        """
        Returns a single record
        Args:
            model: object
            pk: integer
        Returns: dictionary
        """
        try:
            res = self.get(model.id == pk)
            processed_item = BaseModel.__prepare_json__(self, res)
            item = processed_item
        except DoesNotExist as not_found:
            item = {
                'error': str(not_found)
            }
        return item

    def add(self, item):
        """
        Adds a single item
        Args:
            item: dictionary
        Returns: integer
        """
        if self.__is_valid__(item):
            q = self.insert(**item)
            last_id = q.execute()
            return last_id

    def remove(self, model, pk):
        """
        Removes a single item
        Args:
            model: object
            pk: integer
        Returns:
        """
        q = self.delete().where(model.id == pk)
        q.execute()
        return q

    def change(self, item, model, pk):
        """
        Updates a single item
        Args:
            item: dictionary
            model: object
            pk: integer
        Returns:
        """
        q = self.update(**item).where(model.id == pk)
        q.execute()
        return q

    def to_dict(self):
        """
        Converts results to dictionary
        :return:
        """
        return model_to_dict(self)
