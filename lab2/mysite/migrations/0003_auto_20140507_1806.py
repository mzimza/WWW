# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        (b'mysite', b'0002_attribute'),
    ]

    operations = [
        migrations.AlterField(
            model_name=b'attribute',
            name=b'name',
            field=models.CharField(max_length=30),
        ),
    ]
