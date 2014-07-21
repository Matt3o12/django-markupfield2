import unittest
from django.db import models
from markupfield2.fields import *
from mock import patch, MagicMock
import markupfield2


class TestMarkup(unittest.TestCase):
    def setUp(self):
        self.markup_field = MagicMock(MarkupField)
        self.markup = Markup(None, raw_value="Raw value", markup_field=self.markup_field)

    def testGetRaw(self):
        self.assertEquals("Raw value", self.markup.raw)

    @patch("django.utils.safestring.mark_safe", new=lambda s: s)
    def testGetRendered(self, s=None):
        self.markup_field.configure_mock(markup_renderer = lambda s: s)

        self.assertEquals("Raw value", self.markup.rendered)

    def testGetUnicode(self):
        self.assertEquals("Raw value", unicode(self.markup))

class TestMarkupFieldDescriptor(unittest.TestCase):
    def setUp(self):
        self.field = MagicMock(MarkupField)
        self.descriptor = MarkupFieldDescriptor(self.field)

    def testGetNoInstance(self):
        self.assertRaises(AttributeError, self.descriptor.__get__, None, None)

    def testGet_no_raw_value(self):
        myModel = MagicMock(models.Model)
        self.field.configure_mock(name="myField")
        myModel.__dict__["myField"] = None # raw value

        self.assertTrue(self.descriptor.__get__(myModel, myModel.__class__) is None)

    @patch("markupfield2.fields.Markup")
    def testGet(self, MarkupMock):
        myModel = MagicMock(models.Model)
        self.field.configure_mock(name="myField")
        myModel.__dict__["myField"] = "Some value"

        markup = self.descriptor.__get__(myModel, myModel.__class__)
        self.assertTrue(isinstance(markup, MagicMock))
        MarkupMock.assert_called_once_with(myModel, raw_value="Some value", markup_field=self.field)


    def testSet(self):
        myModel = MagicMock(models.Model)
        self.field.configure_mock(name="myField")
        self.assertFalse("myField" in myModel.__dict__)

        value = MagicMock(str)
        self.descriptor.__set__(myModel, value)
        self.assertTrue("myField" in myModel.__dict__)
        self.assertTrue(myModel.__dict__["myField"] is value)

    def testSet_markupInstance(self):
        myModel = MagicMock(models.Model)
        self.field.configure_mock(name="myField")
        self.assertFalse("myField" in myModel.__dict__)

        value = MagicMock(Markup)
        rawMock = MagicMock(str)
        value.attach_mock(rawMock, "raw")
        self.descriptor.__set__(myModel, value)
        self.assertTrue("myField" in myModel.__dict__)
        self.assertTrue(myModel.__dict__["myField"] is value.raw)

class TestMarkupField(unittest.TestCase):
    @patch("django.db.models.TextField.__init__", new=lambda *a, **k: None)
    def setUp(self):
        self.markupField = MarkupField("plain")
        self.markupField.test = None

    @patch("django.db.models.TextField.deconstruct")
    def testDeconstruct(self, desconstMock):
        name = MagicMock(str)
        path = MagicMock(str)
        args = []
        kwargs = {}

        desconstMock.return_value = (name, path, args, kwargs)
        result = self.markupField.deconstruct()
        self.assertEquals((name, path, args, {"markup_type": "plain"}), result)

    @patch.object(markupfield2.markup, "get_renderer")
    def testGetMarkup_renderer(self, getRendererMock):
        RendererMock = MagicMock()
        getRendererMock.return_value = RendererMock

        self.assertEquals(RendererMock, self.markupField.markup_renderer)
        getRendererMock.assert_called_once_with("plain")

    @patch("django.db.models.TextField.contribute_to_class", new=lambda *a, **k: None)
    @patch("markupfield2.fields.MarkupFieldDescriptor")
    def testContribute_to_class(self, descriptorMock):
        myModel = MagicMock(models.Model)

        self.markupField.__dict__["name"] = "myField"

        self.markupField.contribute_to_class(myModel, "myField")
        descriptorMock.assert_called_once_with(self.markupField)
        self.assertTrue(hasattr(myModel, "myField"))
        self.assertTrue(isinstance(myModel.myField, MagicMock))
