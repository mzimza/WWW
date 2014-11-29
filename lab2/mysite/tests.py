from django.test import TestCase
import datetime
from mysite.models import *
from django.core.exceptions import ValidationError

class SimpleTestCase(TestCase):
    def setUp(self):
        Attribute.objects.create(name='krzeslo')
    	Room.objects.create(name='hello', capacity=100, description='takie tam')
    	r = Room.objects.get(name='hello')
    	FreeDate.objects.create(room=r, date='2014-04-09', From=10, to=14)
        
    def test_description(self):
        r1 = Room.objects.get(name="hello")
        self.assertEqual(r1.name, 'hello')
        self.assertEqual(r1.capacity, 100)
        r1 = Room.objects.get(description__contains='tam')
        self.assertEqual(r1.name, 'hello')

    def test_liczba(self):
        self.assertEqual(Room.objects.count(), 1)
        p = Room(name='hello', capacity=100, description='takie tam')
        self.assertEqual(Room.objects.count(), 1)
        p.save()
        self.assertEqual(Room.objects.count(), 2)
        p.delete()
        self.assertEqual(Room.objects.count(), 1)

    def test_freedate(self):
    	r = Room.objects.get(name='hello')
    	t1 = FreeDate.objects.get(room=r)
    	self.assertEqual(t1.date, datetime.date(2014, 4, 9))
        t2 = FreeDate(room=r, date='2014-04-09', From=8, to=11)
    	self.assertEqual(FreeDate.objects.count(), 1)
    	try:
            t2.save()
        except ValidationError:
            pass
    	self.assertEqual(FreeDate.objects.count(), 1)
    	t2 = FreeDate(room=r, date='2014-04-09', From=8, to=10)
        t2.save()
        self.assertEqual(FreeDate.objects.count(), 2)
        t2.delete()
    	x = len(list(FreeDate.objects.filter(room=r)))
    	self.assertEqual(x, 1)
    	t1.delete()
    	x = len(list(FreeDate.objects.filter(room=r)))
    	if x == 0:
    		r.delete()
    		self.assertEqual(Room.objects.count(), 0)
        try:
            t2 = FreeDate(room=r, date='2014-04-09', From=8, to=11)           
    	except ValidationError:
    		pass
        self.assertEqual(FreeDate.objects.count(), 0)

    def test_reserved(self):
    	r = Room.objects.get(name='hello')
        self.assertEqual(Room.objects.filter(name='hello').count(), 1)
        try:
           FreeDate.objects.create(room=r, date='2014-04-09', From=14, to=18)
    	   FreeDate.objects.create(room=r, date='2014-04-09', From=11, to=14)
        except ValidationError:
            pass
        self.assertEqual(FreeDate.objects.filter(room=r, date='2014-04-09').count(), 2)
    	try:
    		res = Reservation(user='kot', room=r, date='2014-04-09', From=9, to=15)
    		#self.fail("Hours out of range.")
    	except ValidationError:
    		pass
    	self.assertEqual(Reservation.objects.count(), 0)
    	self.assertEqual(FreeDate.objects.count(), 2)
        try:
    	   ress = Reservation(user='kot', room=r, date='2014-04-09', From=11, to=12)
           ress.save()
           ress = Reservation(user='kot', room=r, date='2014-04-09', From=14, to=18)
           ress.save()
           ress = Reservation(user='kot', room=r, date='2014-04-09', From=10, to=11)
           ress.save()
           ress = Reservation(user='kot', room=r, date='2014-04-09', From=12, to=14)
           ress.save()
        except ValidationError:
            pass
    	self.assertEqual(FreeDate.objects.count(), 0)
        self.assertEqual(Room.objects.count(), 0)

    def test_boards(self):
        r = Room.objects.get(name='hello')
        self.assertEqual(r.attributes.count(), 1)
        for r in Room.objects.all():
            if r.capacity <= 15:
                self.assertEqual(r.attributes.filter(name="biala tablica").count(), 1)
            if r.capacity > 15:
                self.assertEqual(r.attributes.filter(name="zielona tablica").count(), 1)

    def test_show(self):
        r = Room.objects.get(name='hello')
        t1 = FreeDate.objects.get(room=r)
        t1.showHours()


