from django.db import models
from django.core.exceptions import ValidationError
import datetime, time
from datetime import datetime
from django.db.models import Avg, Max, Min
from collections import defaultdict
import pdb

# Create your models here.

class Attribute(models.Model):
	name = models.CharField(max_length=30, unique=True)
	#rooms = models.ManyToManyField(Room)
	def __unicode__(self):
		return self.name
	def save(self, *args, **kwargs):
		if Attribute.objects.all().count() < 2 :
			s1 = Attribute(name='biala tablica')
			super(Attribute, s1).save(*args, **kwargs)
			s2 = Attribute(name='zielona tablica')
			super(Attribute, s2).save(*args, **kwargs)
		super(Attribute, self).save(*args, **kwargs) 


class Room(models.Model):
        name = models.CharField(max_length=30)
        capacity = models.IntegerField()
        description = models.CharField(max_length=150)
        attributes = models.ManyToManyField(Attribute)
        def __unicode__(self):
        	return self.name

        def save(self, *args, **kwargs):
        	super(Room, self).save(*args, **kwargs)
        	if int(self.capacity) <= 15 and self.attributes.filter(name='biala tablica').count() == 0:
        		a = Attribute.objects.get(name='biala tablica')
        		self.attributes.add(a)
        	if int(self.capacity > 15) and self.attributes.filter(name='zielona tablica').count() == 0:
        		a = Attribute.objects.get(name='zielona tablica')
        		self.attributes.add(a)

		def get_unique_dates(self):
			dates = self.freedate_set.values_list('date', flat=True).distinct().order_by()
			dates = [str(d) for d in dates]
			return dates
		
		def get_free_hours(self, date):
			dates = self.freedate_set.filter(date=date)
			hours = []
			for d in dates:
				h = datetime.combine(datetime.today(), datetime.time(d.From))
				end = datetime.combine(datetime.today(), datetime.time(d.to))
				while h < end:
					hours.append(h.time())
					h += date(hours = 1)
			hours = [str(h)[0:2] for h in hours]
			return hours

        def to_json(self):
        	my_dict = defaultdict(list)
        	# dates = self.get_unique_dates()
        	dates = self.freedate_set.values_list('date', flat=True).distinct().order_by()
        	dates = [str(d) for d in dates]
        	for d in dates:
        		dates2 = self.freedate_set.filter(date=d)
        		hours = []
        		for d2 in dates2:
        			h = datetime.combine(datetime.today(), datetime.time(d2.From))
        			end = datetime.combine(datetime.today(), datetime.time(d2.to))
        			while h < end:
        				hours.append(h.time())
        				h += date(hours = 1)
        				hours = [str(h)[0:2] for h in hours]
        		for h in hours:
        			my_dict[d].append(h)
        			print("to jason", my_dict[d])

        	# print(dict(id = self.id, name = self.name, description = self.description, capacity = self.capacity, 
        	# 	attributes = [ob.__unicode__() for ob in Attribute.objects.filter(room=self)], dates = my_dict))

        	return dict(id = self.id, name = self.name, description = self.description, capacity = self.capacity, 
        		attributes = [ob.__unicode__() for ob in Attribute.objects.filter(room=self)], dates = my_dict)

        

class FreeDate(models.Model):
		room = models.ForeignKey(Room)
		date = models.DateField()
		From = models.IntegerField()
		to = models.IntegerField()
		def __unicode__(self):
			return u'%s' % self.date
		def display_name(self):
			return '%s' % self.date
		def numeric(self):
			d = time.strptime(self.display_name(), "%Y-%m-%d") 
			return '%s' % d 

		def showHours(self):
			l = []
			for f in FreeDate.objects.filter(room_id=self.room_id, date=self.date):
				#print("from: ", f.From, "to: ", f.to, "self.date", self.date, "room", self.room)
				for i in range(f.From, f.to):
					l.append(i)
			l.sort()
			return l

		def clean(self):
			if self.room is not None:
				dates = FreeDate.objects.filter(room=self.room.id)
				for dates in FreeDate.objects.filter(room=self.room.id):
					if dates.date == self.date:
						if dates.From <= self.From:
							if dates.to >= self.to:
								raise ValidationError('Colliding hours.')
			else:
				raise ValidationError('Please choose a room first')
			if self.From < 0 or self.From > 23 or self.From >= self.to:
				raise ValidationError('Wrong time parameters.')
			if self.to < 0 or self.to > 24:
				raise ValidationError('Wrong time parameters.')

		def save(self, *args, **kwargs):
			if self.room is not None:
				print('hello')
				#dates = FreeDate.objects.filter(room=self.room.id
				if FreeDate.objects.filter(room=self.room.id).count() > 0:
					for dates in FreeDate.objects.filter(room=self.room.id):
						print( dates.date == self.date,  dates.date, self.date)
						if dates.date == self.date:
							print(dates.display_name)
							if int(dates.From) <= int(self.From) and int(dates.to) >= int(self.to):
								raise ValidationError('Colliding hours. dates.From <= self.From and dates.to >= self.to')
							elif int(dates.From) >= int(self.From) and int(self.to) > int(dates.From):
								raise ValidationError('Colliding hours. dates.From >= self.From and self.to > dates.From')
							elif int(dates.From) <= int(self.From) and int(self.to) <= int(dates.to):
								raise ValidationError('Colliding hours. dates.From <= self.From and self.to <= dates.to ')
							elif int(self.From) >= int(self.to):
								raise ValidationError('Colliding hours. self.From >= self.to')
							elif self.to < dates.From:
								super(FreeDate, self).save(*args, **kwargs)
							elif self.From > dates.to:
								super(FreeDate, self).save(*args, **kwargs)
							elif int(self.to) == int(dates.From):
								noweTo = dates.to
								dates.delete()
								self.to = noweTo
								print("te same pierwsze", self.to, noweTo)
								super(FreeDate, self).save(*args, **kwargs)
							elif int(self.From) == int(dates.to):
								noweFrom = dates.From
								dates.delete()
								self.From = noweFrom
								print("te same drugie", self.From, noweFrom)
								super(FreeDate, self).save(*args, **kwargs)
						else:
							print("zapisuje, bo inne")
							super(FreeDate, self).save(*args, **kwargs)		
				else:
					print("zapisuje, bo inne")
					super(FreeDate, self).save(*args, **kwargs)
			else:
				raise ValidationError('Please choose a room first')
			if int(self.From) < 0 or int(self.From) > 23 or int(self.From) >= int(self.to):
				raise ValidationError('Wrong time parameters.')
			if int(self.to) < 0 or int(self.to) > 24:
				print(self.to)
				raise ValidationError('Wrong time parameters.')
			




class Reservation(models.Model):
		user = models.CharField(max_length=150)
		room = models.ForeignKey(Room)
		date = models.DateField()
		From = models.IntegerField()
		to = models.IntegerField()
		def __unicode__(self):
			s = str(self.user) + ': ' + str(self.From) + ' - ' + str(self.to)
			return '%s' % s

		def save(self, *args, **kwargs):
			if FreeDate.objects.get(room=self.room.id, date=self.date, From__lte=self.From, to__gte=self.to):
				the_one = FreeDate.objects.get(room=self.room.id, date=self.date, From__lte=self.From, to__gte=self.to)
				room_id = the_one.room
				From = the_one.From
				to = the_one.to
				date = the_one.display_name()
				if (int(From) != int(to)):
					the_one.delete()
					if (int(From) < int(self.From)):
						print("nowe freedate")
						new = FreeDate(room=room_id, date=date, From=From, to=self.From)
						new.save()
					if (int(to) > int(self.to)):
						print("nowe freedate")
						new_date = FreeDate(room=room_id, date=date, From=self.to, to=to)
						new_date.save()
				free_list = list(FreeDate.objects.filter(room=self.room))
				if (len(free_list) == 0):
					room = Room.objects.get(id=self.room.id)
					room.delete()
	        	super(Reservation, self).save(*args, **kwargs) # Call the "real" save() method.







