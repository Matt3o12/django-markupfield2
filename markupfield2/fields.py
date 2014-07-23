from django.forms.fields import ChoiceField
from django.utils.encoding import python_2_unicode_compatible
from . import markup
from django.utils.safestring import mark_safe

from django.db import models

@python_2_unicode_compatible
class Markup(object):
    def __init__(self, instance, raw_value, markup_field):
        """
        Markup is responsible for rendering the raw values and
        providing the raw values if necessary.
        The instance

        :param instance: models.Model
        :param raw_value: string
        :param markup_field: MarkupField
        """
        self.instance = instance
        self.markup_field = markup_field
        self._raw_value = raw_value

    @property
    def raw(self):
        """
        Return the raw, unrendered value.

        :return: returns the raw, unrendered value
        :rtype: string
        """
        return self._raw_value

    @property
    def rendered(self):
        """
        Return the rendered value.

        :return:
        :rtype: SafeData
        """

        return mark_safe(self.markup_field.markup_renderer(self.raw))

    def __str__(self):
        """
        Returns the raw data.
        """
        return self.raw

class MarkupFieldDescriptor(object):
    def __init__(self, field):
        """
        The descriptor for the markup field.

        :param field: the field to use.
        """
        self.field = field

    def __get__(self, instance, owner):
        """

        :return: None if there isn't a raw value.
        :rtype: Markup or None
        :raise: AttributeError if not accessed via an instance.
        """
        print type(instance)
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
        """
        Creates a new Markup Field.

        :param markup_type: string markup_type to use.
        :param args: Same as models.TextField
        :param kwargs: Same as models.TextField
        """
        super(MarkupField, self).__init__(*args, **kwargs)

        # TODO: Check whether markup_type is valid.
        self.markup_type = markup_type

    def deconstruct(self):
        name, path, args, kwargs = super(MarkupField, self).deconstruct()

        kwargs["markup_type"] = self.markup_type
        return name, path, args, kwargs

    @property
    def markup_renderer(self):
        """
        Return the renderer (html, plain, markdown) to use to render
        the value.

        :return: the renderer to use
        """
        return markup.get_renderer(self.markup_type)

    def contribute_to_class(self, cls, name, *args, **kwargs):
        """
        Adds MarkupFieldDescriptor to the class.
        Also calls its parent's method.
        """
        super(MarkupField, self).contribute_to_class(cls, name, *args, **kwargs)
        setattr(cls, self.name, MarkupFieldDescriptor(self))
