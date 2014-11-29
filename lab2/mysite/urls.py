from django.conf.urls import patterns, url
#from django.views.generic import TemplateView, ListView

from mysite import views

urlpatterns = patterns('',
    url(r'^$', 'mysite.views.index', name='index'),
    url(r'^(?P<room_id>\d+)/freedates$', 'mysite.views.freedates', name='freedates'),
    url(r'^(?P<room_id>\d+)/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<h_from>\d{1,2})/(?P<h_to>\d{1,2})/reservation$',
     'mysite.views.reservation', name='reservation'),
    url(r'^login$', 'mysite.views.zaloguj', name='login'),
    url(r'^.*login$', 'mysite.views.zaloguj', name='login'),
    url(r'^logout$', 'mysite.views.wyloguj', name='logout'),
    url(r'^.*logout$', 'mysite.views.wyloguj', name='logout'),
    url(r'^search$', 'mysite.views.search', name='search'),
    url(r'^.*/done$', 'mysite.views.zarezerwuj', name='done'),
    url(r'^formularz$', 'mysite.views.formularz', name='formularz'),
    url(r'^newReservation$', 'mysite.views.newReservation', name='newReservation'),
    url(r'^manifest', 'mysite.views.manifest', name='manifest'),
    url(r'^test', 'mysite.views.test', name='test'),
    url(r'^room_details', 'mysite.views.get_room_details', name='get_room_details'),
    url(r'^rooms_list', 'mysite.views.rooms_list', name='rooms_list'),
    url(r'^get_rooms_list', 'mysite.views.get_rooms_list', name='get_rooms_list'),
    url(r'^get_attr_list', 'mysite.views.get_attr_list', name='get_attr_list'),
    url(r'^get_free_list', 'mysite.views.get_free_list', name='get_free_list'),
    url(r'^room_details_free', 'mysite.views.get_room_details_free', name='get_room_details_free'),
    url(r'^book', 'mysiete.views.book', name='book'),
)