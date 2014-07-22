from django.template.base import Template
from django.template.context import Context
from django.test import TestCase
from django.utils.html import linebreaks, escape, urlize
from markupfield2.fields import MarkupField
from .models import SimpleModel

class TestSimpleModel(TestCase):
    def testPlainRender(self):
        myModel = SimpleModel.objects.create(
            plainField = "Hello world.\n<b>test</b>."
        )

        template = Template("{{ model.plainField.rendered }}")
        context = Context({"model": myModel})
        expected = "<p>Hello world.<br />&lt;b&gt;test&lt;/b&gt;.</p>"
        self.assertEquals(expected, template.render(context))

    def testHTMLRender(self):
        myModel = SimpleModel.objects.create(
            htmlField = "I'm some <b>HTML</b>\ntext :)"
        )

        template = Template("{{ model.htmlField.rendered }}")
        context = Context({"model": myModel})
        expected = "I'm some <b>HTML</b>\ntext :)"
        self.assertEquals(expected, template.render(context))

