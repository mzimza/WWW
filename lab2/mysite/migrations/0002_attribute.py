# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        (b'mysite', b'0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name=b'Attribute',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                (b'name', models.CharField(unique=True, max_length=30)),
                (b'rooms', models.ManyToManyField(to=b'mysite.Room')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
