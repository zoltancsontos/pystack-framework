# from peewee import Proxy, Model, Field, PrimaryKeyField, \
#     IntegerField
# import re
#
#
# class PySawForeignKeyField(IntegerField):
#     """
#     Peewee foreign key overrides
#     """
#     def __init__(self, rel_model, related_name=None, on_delete=None,
#                  on_update=None, extra=None, to_field=None, *args, **kwargs):
#         if rel_model != 'self' and not \
#                 isinstance(rel_model, (Proxy, DeferredRelation)) and not \
#                 issubclass(rel_model, Model):
#             raise TypeError('Unexpected value for `rel_model`.  Expected '
#                             '`Model`, `Proxy`, `DeferredRelation`, or "self"')
#         self.rel_model = rel_model
#         self._related_name = related_name
#         self.deferred = isinstance(rel_model, (Proxy, DeferredRelation))
#         self.on_delete = on_delete
#         self.on_update = on_update
#         self.extra = extra
#         self.to_field = to_field
#         super(PySawForeignKeyField, self).__init__(*args, **kwargs)
#
#     def clone_base(self, **kwargs):
#         return super(PySawForeignKeyField, self).clone_base(
#             rel_model=self.rel_model,
#             related_name=self._get_related_name(),
#             on_delete=self.on_delete,
#             on_update=self.on_update,
#             extra=self.extra,
#             to_field=self.to_field,
#             **kwargs)
#
#     def _get_descriptor(self):
#         return RelationDescriptor(self, self.rel_model)
#
#     def _get_id_descriptor(self):
#         return ObjectIdDescriptor(self)
#
#     def _get_backref_descriptor(self):
#         return ReverseRelationDescriptor(self)
#
#     def _get_related_name(self):
#         if self._related_name and callable(self._related_name):
#             return self._related_name(self)
#         return self._related_name or ('%s_set' % self.model_class._meta.name)
#
#     def add_to_class(self, model_class, name):
#         if isinstance(self.rel_model, Proxy):
#             def callback(rel_model):
#                 self.rel_model = rel_model
#                 self.add_to_class(model_class, name)
#             self.rel_model.attach_callback(callback)
#             return
#         elif isinstance(self.rel_model, DeferredRelation):
#             self.rel_model.set_field(model_class, self, name)
#             return
#
#         self.name = name
#         self.model_class = model_class
#         self.db_column = obj_id_name = self.db_column or '%s_id' % self.name
#         if obj_id_name == self.name:
#             obj_id_name += '_id'
#         if not self.verbose_name:
#             self.verbose_name = re.sub('_+', ' ', name).title()
#
#         model_class._meta.add_field(self)
#
#         self.related_name = self._get_related_name()
#         if self.rel_model == 'self':
#             self.rel_model = self.model_class
#
#         if self.to_field is not None:
#             if not isinstance(self.to_field, Field):
#                 self.to_field = getattr(self.rel_model, self.to_field)
#         else:
#             self.to_field = self.rel_model._meta.primary_key
#
#         # TODO: factor into separate method.
#         if model_class._meta.validate_backrefs:
#             def invalid(msg, **context):
#                 context.update(
#                     field='%s.%s' % (model_class._meta.name, name),
#                     backref=self.related_name,
#                     obj_id_name=obj_id_name)
#                 raise AttributeError(msg % context)
#
#             if self.related_name in self.rel_model._meta.fields:
#                 invalid('The related_name of %(field)s ("%(backref)s") '
#                         'conflicts with a field of the same name.')
#             # elif self.related_name in self.rel_model._meta.reverse_rel:
#             #     invalid('The related_name of %(field)s ("%(backref)s") '
#             #             'is already in use by another foreign key.')
#
#             if obj_id_name in model_class._meta.fields:
#                 invalid('The object id descriptor of %(field)s conflicts '
#                         'with a field named %(obj_id_name)s')
#             elif obj_id_name in model_class.__dict__:
#                 invalid('Model attribute "%(obj_id_name)s" would be shadowed '
#                         'by the object id descriptor of %(field)s.')
#
#         setattr(model_class, name, self._get_descriptor())
#         setattr(model_class, obj_id_name,  self._get_id_descriptor())
#         setattr(self.rel_model,
#                 self.related_name,
#                 self._get_backref_descriptor())
#         self._is_bound = True
#
#         model_class._meta.rel[self.name] = self
#         self.rel_model._meta.reverse_rel[self.related_name] = self
#
#     def get_db_field(self):
#         """
#         Overridden to ensure Foreign Keys use same column type as the primary
#         key they point to.
#         """
#         if not isinstance(self.to_field, PrimaryKeyField):
#             return self.to_field.get_db_field()
#         return super(PySawForeignKeyField, self).get_db_field()
#
#     def get_modifiers(self):
#         if not isinstance(self.to_field, PrimaryKeyField):
#             return self.to_field.get_modifiers()
#         return super(PySawForeignKeyField, self).get_modifiers()
#
#     def coerce(self, value):
#         return self.to_field.coerce(value)
#
#     def db_value(self, value):
#         if isinstance(value, self.rel_model):
#             value = value._get_pk_value()
#         return self.to_field.db_value(value)
#
#     def python_value(self, value):
#         if isinstance(value, self.rel_model):
#             return value
#         return self.to_field.python_value(value)
