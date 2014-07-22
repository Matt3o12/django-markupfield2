# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import markupfield2.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SimpleModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('plainField', markupfield2.fields.MarkupField(markup_type=b'plain')),
                ('htmlField', markupfield2.fields.MarkupField(markup_type=b'html')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
