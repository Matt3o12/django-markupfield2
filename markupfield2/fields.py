from django.utils.encoding import python_2_unicode_compatible
from . import markup
from django.utils.safestring import mark_safe

from django.db import models

@python_2_unicode_compatible
class Markup(object):
    def __init__(self, instance, raw_value, markup_field):
        self.instance = instance
        self.markup_field = markup_field
        self._raw_value = raw_value

    @property
    def raw(self):
        return self._raw_value

    @property
    def rendered(self):
        return mark_safe(self.markup_field.markup_renderer(self.raw))

    def __str__(self):
        return self.raw

class MarkupFieldDescriptor(object):
    def __init__(self, field):
        self.field = field

    def __get__(self, instance, owner):
        # print "Called: %s; %s; %s; %s;" % (self, instance, type(instance), owner)
        if instance is None:
            raise AttributeError('Can only be accessed via an instance.')

        raw_value = instance.__dict__[self.field.name]
        if raw_value is None:
            return None

        return Markup(instance, raw_value=raw_value, markup_field=self.field)

    def __set__(self, obj, value):
        if isinstance(value, Markup):
            # TODO: When is that called?
            obj.__dict__[self.field.name] = value.raw
        else:
            obj.__dict__[self.field.name] = value

class MarkupField(models.TextField):
    def __init__(self, markup_type, *args, **kwargs):
        super(MarkupField, self).__init__(*args, **kwargs)

        # TODO: Check whether markup_type is valid.
        self.markup_type = markup_type

    def deconstruct(self):
        name, path, args, kwargs = super(MarkupField, self).deconstruct()

        kwargs["markup_type"] = self.markup_type
        return name, path, args, kwargs

    @property
    def markup_renderer(self):
        return markup.get_renderer(self.markup_type)

    def contribute_to_class(self, cls, name, *args, **kwargs):
        super(MarkupField, self).contribute_to_class(cls, name, *args, **kwargs)
        setattr(cls, self.name, MarkupFieldDescriptor(self))
