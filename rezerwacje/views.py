from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db.models import Q

from datetime import date

from rezerwacje.models import Room, Booking


def main(request):
    rooms = Room.objects.order_by('name')
    bookings = Booking.objects.filter(date=date.today())
    return render(request, 'html_main', {'rooms': rooms,
                                         'bookings': bookings})


def room_search(request):
    rooms = Room.objects.order_by('name')
    name = request.GET.get("name")
    if name:
        rooms = rooms.filter(name__icontains=name)
    capacity = request.GET.get("capacity")
    if capacity:
        rooms = rooms.filter(capacity__gte=capacity)
    projector = request.GET.get("projector")
    if projector:
        rooms = rooms.filter(projector=True)
    date = request.GET.get("date")
    if date:
        bookings = Booking.objects.filter(date=date)
        for booking in bookings:
            rooms = rooms.exclude(id=booking.room_id_id)
    else:
        bookings = Booking.objects.filter(date=date.today())
    if rooms:
        return render(request, 'html_main', {'rooms': rooms,
                                             'bookings': bookings})
    else:
        message = """Brak wolnych sal dla podanych kryteriów wyszukiwania<br>
                     <a href='/'>Powrót</a>"""
        return HttpResponse(message)


def room_details(request, id):
    id = int(id)
    room = Room.objects.get(pk=id)
    bookings = Booking.objects.filter(room_id=room.id)\
                              .filter(date__gte=date.today())
    return render(request, 'html_room_details', {'room': room,
                                                 'bookings': bookings})


def room_delete(request, id):
    id = int(id)
    room = Room.objects.get(pk=id)
    room.delete()
    return HttpResponseRedirect('/')


@method_decorator(csrf_exempt, name='dispatch')
class RoomNew(View):

    def get(self, request):
        return render(request, 'html_room_addmodify', {})

    def post(self, request):
        name = request.POST.get("name")
        capacity = request.POST.get("capacity")
        if request.POST.get("projector"):
            projector = True
        else:
            projector = False
        Room.objects.create(name=name, capacity=capacity, projector=projector)
        return HttpResponseRedirect('/')


@method_decorator(csrf_exempt, name='dispatch')
class RoomModify(View):

    def get(self, request, id):
        id = int(id)
        room = Room.objects.get(pk=id)
        return render(request, 'html_room_addmodify', {'room': room})

    def post(self, request, id):
        id = int(id)
        room = Room.objects.get(pk=id)
        room.name = request.POST.get("name")
        room.capacity = request.POST.get("capacity")
        if request.POST.get("projector"):
            projector = True
        else:
            projector = False
        room.projector = projector
        room.save()
        return HttpResponseRedirect('/')


@method_decorator(csrf_exempt, name='dispatch')
class ReservationAdd(View):

    def get(self, request, id):
        id = int(id)
        room = Room.objects.get(pk=id)
        bookings = Booking.objects.filter(room_id=room.id)
        return render(request, 'html_reservation_add', {'bookings': bookings})

    def post(self, request, id):
        id = int(id)
        room = Room.objects.get(pk=id)
        date = request.POST.get("date")
        if date < date.today():
            message = """Nieprawidłowy termin<br>
                         <a href='/room/{}'>Powrót</a>"""
            return HttpResponse(message.format(id))
        if Booking.objects.filter(room_id=room, date=date):
            message = """Termin zajęty<br>
                         <a href='/room/{}'>Powrót</a>"""
            return HttpResponse(message.format(id))
        else:
            Booking.objects.create(date=date, room_id=room)
            return HttpResponseRedirect('/')
