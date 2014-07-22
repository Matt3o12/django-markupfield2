from django.db import models
from markupfield2.fields import MarkupField


class SimpleModel(models.Model):
    plainField = MarkupField(markup_type="plain")
    htmlField = MarkupField(markup_type="html")

