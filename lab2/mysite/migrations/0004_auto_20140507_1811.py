# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        (b'mysite', b'0003_auto_20140507_1806'),
    ]

    operations = [
        migrations.AddField(
            model_name=b'room',
            name=b'attributes',
            field=models.ManyToManyField(to=b'mysite.Attribute', null=True),
            preserve_default=True,
        ),
        migrations.RemoveField(
            model_name=b'attribute',
            name=b'rooms',
        ),
    ]
