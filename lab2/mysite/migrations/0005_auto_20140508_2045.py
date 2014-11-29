# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


def forwards_func(apps, schema_editor):
    # We get the model from the versioned app registry;
    # if we directly import it, it'll be the wrong version
    Room = apps.get_model("mysite", "Room")
    for room in Room.objects.all():
        if room.capacity <= 15:
            room.attributes.add('bialaTabilca')
        else:
            room.attributes.add('zielonaTablica')


class Migration(migrations.Migration):

    dependencies = [
        (b'mysite', b'0004_auto_20140507_1811'),
    ]

    operations = [
         migrations.RunPython(
            forwards_func,
        ),
        migrations.AlterField(
            model_name=b'room',
            name=b'attributes',
            field=models.ManyToManyField(to=b'mysite.Attribute'),
        ),
        migrations.AlterField(
            model_name=b'attribute',
            name=b'name',
            field=models.CharField(unique=True, max_length=30),
        ),
    ]


