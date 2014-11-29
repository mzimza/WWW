from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import transaction, IntegrityError
from django.db.models import Q
from models import Room, FreeDate, Reservation, Attribute
import operator
from operator import itemgetter, attrgetter
from cStringIO import StringIO
from tokenize import generate_tokens
import json
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from collections import defaultdict
from django.core import serializers
import pdb, datetime
from django.core.exceptions import ValidationError



# Create your views here.
from django.http import HttpResponse

def index(request):
	by = request.GET.get('by', '')
	zapytanie = request.GET.get('zapytanie', '')
	attributes = request.GET.getlist('attributes', '')
	allAttr = Attribute.objects.all()
	placeMin = request.GET.get('placeMin', '')
	placeMax = request.GET.get('placeMax', '')
	print('atrybuty', attributes)
	rooms_list = Room.objects.filter(Q(description__contains=zapytanie) | Q(name__contains=zapytanie) | Q(capacity__contains=zapytanie))
	if placeMin != '':
	   	rooms_list = rooms_list.filter(capacity__range=(placeMin, placeMax))
	for a in attributes:
	  	rooms_list = rooms_list.filter(attributes__name=a)

	if by == 'name':
	   	rooms_list = sorted(rooms_list, key=operator.attrgetter('name'))
	elif by == 'capacity':
	   	rooms_list = sorted(rooms_list, key=operator.attrgetter('capacity'))
	paginator = Paginator(rooms_list, 1) # Show 5 contacts per page
	page = request.GET.get('page')
	try:
		rooms = paginator.page(page)
	except PageNotAnInteger:
		rooms = paginator.page(1)
	except EmptyPage:
		rooms = paginator.page(paginator.num_pages)

	pokoj = Room.objects.all()
	wolne = FreeDate.objects.all()
	context = {'rooms_list': rooms, 'zapytanie': zapytanie, 'by' : by, 'placeMin' : placeMin, 'placeMax' : placeMax, 'attributes' : attributes, 'allAttr' : allAttr, 'pokoj' : pokoj, 'wolne' : wolne}
	return render(request, 'mysite/main.html', context)
	
def freedates(request, room_id):
	print("wywoluje")
	free_list = []
	for r in Room.objects.filter(id=room_id):
		free = list(FreeDate.objects.filter(room=r))
		free_list = free_list + free;
	context = {'free_list': free_list }
	return render(request, 'mysite/dates.html', context)

def reservation(request, room_id, year, month, day, h_from, h_to):
	hours_list = []
	search_date =  year + '-' + month + '-' + day
	for h in FreeDate.objects.filter(room_id=room_id, date=search_date, From=h_from, to=h_to):
		hours_list.append(h)
	context = {'hours_list' : hours_list}
	return render(request, 'mysite/reservation.html', context)

def wyloguj(request):
    logout(request)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def zaloguj(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
        else:
            messages.error(request, 'Konto zablokowane')
    else:
        messages.error(request, 'Zle haslo')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
#redirect('/mysite/rooms')


def search(request):
    by = request.GET.get('by', '')
    zapytanie = request.GET.get('zapytanie', '')
    attributes = request.GET.getlist('attributes', '')
    allAttr = Attribute.objects.all()
    placeMin = request.GET.get('placeMin', '')
    placeMax = request.GET.get('placeMax', '')
    print('atrybuty', attributes)
    rooms_list = Room.objects.filter(Q(description__contains=zapytanie) | Q(name__contains=zapytanie) | Q(capacity__contains=zapytanie))
    if placeMin != '':
    #	placeMin = 0
    #if placeMax == '':
    #	placeMax = 1000000
    	rooms_list = rooms_list.filter(capacity__range=(placeMin, placeMax))

    for a in attributes:
		rooms_list = rooms_list.filter(attributes__name=a)

    if by == 'name':
    	rooms_list = sorted(rooms_list, key=operator.attrgetter('name'))
    elif by == 'capacity':
    	rooms_list = sorted(rooms_list, key=operator.attrgetter('capacity'))
    paginator = Paginator(rooms_list, 3) # Show 5 contacts per page
    page = request.GET.get('page')
    try:
        rooms = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        rooms = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        rooms = paginator.page(paginator.num_pages)

    context = {'rooms_list': rooms, 'zapytanie': zapytanie, 'by' : by, 'placeMin' : placeMin, 'placeMax' : placeMax, 'attributes' : attributes, 'allAttr' : allAttr }
    return render(request, 'mysite/search.html', context)

def getfreedates(request):
	context = RequestContext(request)


@transaction.atomic
def book(request):
    json_data = json.dumps({"HTTPRESPONSE":0})
    if request.method == "POST":
        room = Room.objects.get(pk=request.POST['room_id'])
        date = datetime.strptime(request.POST['date'], '%Y-%m-%d')
        hours = json.loads(request.POST['hours'])
        delta = timedelta(hours = 1)

        error = False
        try:
            with transaction.atomic():
                for h in hours:
                    begin = datetime.strptime(h, "%H:%M").time()
                    end = (datetime.combine(dt.today(), begin) + delta).time()
                    reservation = Reservation(
                        user=request.user,
                        room=room,
                        date=date,
                        begin_time=begin,
                        end_time=end
                    )
                    try:
                        reservation.clean()
                    except ValidationError as e:
                        message = begin.__str__()[:5] + "-" + end.__str__()[:5] + " is not available"
                        json_data = json.dumps({"HTTPRESPONSE":0, "ERROR": message})
                        error = True
                        break
                    for t in room.freeterm_set.filter(date=date):
                        if t.begin_time <= begin and t.end_time >= end:
                            break
                    left = FreeTerm(
                        room=room,
                        date=date,
                        begin_time=t.begin_time,
                        end_time=begin
                    )
                    right = FreeTerm(
                        room=room,
                        date=date,
                        begin_time=end,
                        end_time=t.end_time
                    )
                    t.delete()
                    if left.begin_time < left.end_time:
                        left.save()
                    if right.begin_time < right.end_time:
                        right.save()
                    reservation.save()
            if not error:
                json_data = json.dumps({"HTTPRESPONSE":1})

        except IntegrityError:
            messages.error(request, 'Something went wrong')

    return HttpResponse(json_data, mimetype="application/json")

@transaction.atomic
def newReservation(request):
	json_data = json.dumps({"HTTPRESPONSE":0})
	x = 0
	print("new Reservation")
	h = request.POST.get('hours', '')
	r = request.POST['room_id']
	d = request.POST['date']
	print (d)
	#h = request.GET.get('hours', '')
	#r = request.GET['room_id']
	#d = request.GET['date']
	error = False
	for i in h:
		print(i)
	if len(h) == 0:
		messages.error(request, "No hours selected.")
		context = {'result' : 'warning'}
	else:
		context = {'result' : 'info'}
	print(d)
	STRING = 1
	hours = list(token[STRING] for token 
    	in generate_tokens(StringIO(h).readline)
    	if token[STRING])
	for i in hours:
		print(i)
	reserved = []
	for hour in hours:
		x = hour.split('"')
		print("dlugosc", x, len(x))
		if len(x) == 3:
			print("mamy liczbe: ", int(x[1]))
			reserved.append(int(x[1]))
	print("po znajdywaniu", "room_id", r, "date", d)
	free = FreeDate.objects.filter(room_id=r, date=d)
	print("free", free)
	room = Room.objects.get(id=r)
	print("room", room)
	for f in free:
		print("from", str(f.From), "to:", f.to, "date:", f.date)
	try:
		with transaction.atomic():
			for hour in reserved:
				to = hour+1
				print("to", to)
				if Reservation.objects.filter(user=request.user, room=room, date=d, From=hour, to=(hour+1)).count() == 0:
					Reservation.objects.create(user=request.user, room=room, date=d, From=hour, to=to)
					print("udalo sie")
					messages.info(request, 'Your reservation was successful!')
					context = { 'result' : 'success'}
				else:
					print("nope")
					error = True
					messages.error(request, 'Couldn\'t create reservation! This hour isn\'t free anymore.')
					#json_data = json.dumps({"HTTPRESPONSE":0, "ERROR": message})
					# context = { 'result' : 'danger'}
		if not error:
			print ("not error")
			json_data = json.dumps({"HTTPRESPONSE":1})
			x = 1
			print("not error")
		else:
			x = 0

	except IntegrityError, ValidationError:
		messages.error(request, 'Something went wrong')
	print("po except", json_data)
	print (x)
	return JsonResponse({"HTTPRESPONSE": x })
	#return HttpResponse(json_data, mimetype="application/json")	

def formularz(request):
	r = request.POST['room_id']
	reallyFree = []
	even = []
	free = FreeDate.objects.filter(room=r)
	for f in free:
		if f.date not in reallyFree:
			reallyFree.append(f.date)
	for e in reallyFree:
		even.append(FreeDate.objects.filter(room=r, date=e)[0])
		print(e)
	free = sorted(free, key=operator.attrgetter('date'))
	free = sorted(free, key=operator.attrgetter('From'))
	context = {'wolne' : even, 'hours' : free, 'room' : r}
	return render(request, 'mysite/my.html', context)

@transaction.atomic
def zarezerwuj(request):
	id_room = request.POST['roomid']
	From = str(request.POST['From'])
	to = str(request.POST['to'])
	date = str(request.POST['date'])
	mini = str(request.POST['mini'])
	maxi = str(request.POST['maxi'])
	error = 0
	print(From, mini, to, maxi)
	if From == '':
		messages.error(request, 'Fill in starting hour')
		error = 1
		#return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
	elif int(From) < int(mini) or int(to) > int(maxi) or int(From) >= int(to):
		messages.error(request, 'Hours out of range.')
		error = 1
	elif int(From) == int(to):
		messages.error(request, 'Starting hour must be smaller than ending.')
		error = 1
	elif int(From) < 0 or int(to) < 0:
		print(int(From), int(to))
		messages.error(request, 'There is no such hour.')
		error = 1
	elif  int(From) > 23 or int(to) > 24 :
		print(int(From) > 23, int(to))
		messages.error(request, 'There is no such hour.')
		error = 1
	elif to == '':
		messages.error(request, 'Fill in ending hour')
		error = 1
		#return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
	if error == 1:
		return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
	else :
		room = Room.objects.get(name=id_room)
		try:
			with transaction.atomic():
				reservation = Reservation(user=request.user, room=room, date=date, From=From, to=to)
				reservation.save()
		except IntegrityError, ValidationError:
			pass

		if Reservation.objects.get(user=request.user, room=room, date=date, From=From, to=to):
			messages.info(request, 'Your reservation was successful!')
		else:
			messages.error(request, 'Couldn\'t create reservation!')

		return redirect('/mysite/search')
		
def manifest(request):
    return render(request, 'mysite.manifest')

def test(request):
    return render(request, 'mysite/qunittests.html')

@login_required
def rooms_list(request):
    return render(request, 'mysite/searchOff.html')

def get_rooms_list(request):
    my_dict = defaultdict(list)
    print(Room.objects.all().count())
    rooms = serializers.serialize("json", Room.objects.all())
    return HttpResponse(json.dumps(rooms), content_type="application/json")

def get_attr_list(request):
    attributes = serializers.serialize("json", Attribute.objects.all())
    print(serializers.serialize("json", FreeDate.objects.all()))
    return HttpResponse(json.dumps(attributes), content_type="application/json")

def get_free_list(request):
	freedates = serializers.serialize("json", FreeDate.objects.all())
	return HttpResponse(json.dumps(freedates), content_type="application/json")

def get_room_details(request):
    if request.method == "GET":
        room_id = request.GET['room_id']

    room = Room.objects.get(pk=room_id)#.to_json()
    print(room)
    r2 = serializers.serialize("json", [Room.objects.get(pk=room_id)])
    print(r2)
    return HttpResponse(json.dumps(room), content_type="application/json")

def get_room_details_free(request):
    if request.method == "GET":
        room_id = request.GET['room_id']

    room = Room.objects.get(pk=room_id)#.to_json()
    print(room)
    dates = FreeDate.objects.all().filter(room=room)
    d = serializers.serialize("json", dates)
    print (d)
    # r2 = serializers.serialize("json", [Room.objects.get(pk=room_id)])
    # print(r2)
    return HttpResponse(json.dumps(d), content_type="application/json")

