# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name=b'Room',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                (b'name', models.CharField(max_length=30)),
                (b'capacity', models.IntegerField()),
                (b'description', models.CharField(max_length=150)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name=b'FreeDate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                (b'room', models.ForeignKey(to=b'mysite.Room', to_field='id')),
                (b'date', models.DateField()),
                (b'From', models.IntegerField()),
                (b'to', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name=b'Reservation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                (b'user', models.CharField(max_length=150)),
                (b'room', models.ForeignKey(to=b'mysite.Room', to_field='id')),
                (b'date', models.DateField()),
                (b'From', models.IntegerField()),
                (b'to', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
