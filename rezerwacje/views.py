from django.db.models.fields import CharField
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from rezerwacje.models import Room, Booking
from django.views.decorators.csrf import csrf_exempt
from datetime import date

html_begin = """
<html>
    <body>
        <div align="center">
"""
html_end = """
        </div>
    </body>
</html
"""
html_form = """
        <form action='' method="POST">
            <label>Nazwa:
            <input type="text" name="name" value={}>
            </label><br>
            <label>Pojemność:
            <input type="text" name="capacity" value={}>
            </label><br>
            <label>Rzutnik:
            <input type="checkbox" name="projector" {}>
            </label><br>
            <input type="submit" value="Wyślij">
        </form>
"""

def main(request):
    response = HttpResponse()
    response.write(html_begin)
    response.write("""
<table borderwidth=1px bordercolor='black'>
<tr><td colspan='3'>Nazwa sali</td><td>Status</td></tr>
""")
    rooms = Room.objects.all()
    for room in rooms:
        bookings = Booking.objects.filter(date=date.today()).filter(room_id=room.id)
        if bookings:
            status = "Zajęta"
        else:
            status = "Wolna"
        response.write("""
        <tr><td><a href='/room/{0}'>{1}</a></td>
        <td><a href='/modify/{0}'>Edytuj</a></td>
        <td><a href='/room/delete/{0}'>Usuń</a></td>
        <td>{2}</td></tr>
        """.format(room.id, room.name, status))
    response.write("""
    <tr><td colspan='4'><a href='/room/new'>Dodaj salę</a></td></tr></table>
    """)
    response.write(html_end)
    return response


def room_details(request, id):
    id = int(id)
    response = HttpResponse()
    response.write(html_begin)
    room = Room.objects.get(pk=id)
    bookings = Booking.objects.filter(room_id=room.id)
    if room.projector:
        projector = "Tak"
    else:
        projector = "Nie"
    response.write("""
    <table borderwidth=1px bordercolor='black'>
    <tr><td>Nazwa sali</td><td>Pojemność</td><td>Projektor</td><td>Daty:</td></tr>
    """)
    response.write("""
    <tr>
    <td>{}</td>
    <td>{}</td>
    <td>{}</td>
    <td><a href='/room/modify/{}'>Dodaj rezerwację</a></td></tr>
    """.format(room.name, room.capacity, projector, room.id))
    for booking in bookings:
        response.write("""
        <tr><td colspan='3'></td><td>{}</td>
        """.format(booking.date))
    response.write(html_end)
    return response


def delete_room(request, id):
    response = HttpResponse()
    id = int(id)
    room = Room.objects.get(pk=id)
    room.delete()
    return HttpResponseRedirect('/')


@csrf_exempt
def new_room(request):
    response = HttpResponse()
    if request.method == 'GET':
        html = html_begin + html_form + html_end
        response.write(html.format("", "", ""))
        return response
    else:
        name = request.POST.get("name")
        capacity = request.POST.get("capacity")
        if request.POST.get("projector"):
            projector = True
        else:
            projector = False
        Room.objects.create(name=name, capacity=capacity, projector=projector)
        return HttpResponseRedirect('/')


@csrf_exempt
def modify_room(request, id):
    response = HttpResponse()
    id = int(id)
    room = Room.objects.get(pk=id)
    if request.method == 'GET':
        html = html_begin + html_form + html_end
        if room.projector:
            response.write(html.format(room.name, room.capacity, "checked"))
        else:
            response.write(html.format(room.name, room.capacity, ""))
        return response
    else:
        room.name = request.POST.get("name")
        room.capacity = request.POST.get("capacity")
        if request.POST.get("projector"):
            projector = True
        else:
            projector = False
        room.projector = projector
        room.save()
        return HttpResponseRedirect('/')

def add_reservation(request, id):
    room = Room.objects.get(pk=id)
    if request.method == 'GET':
        id = int(id)
        bookings = Booking.objects.filter(room_id=room.id)
        response = HttpResponse()
        response.write(html_begin)
        response.write("""
<form action='' method="POST">
    <label>Data:
    <input type="date" name="date">
    </label>
    <input type="submit" value="Wyślij">
</form>
""")
        response.write("""
<table borderwidth=1px bordercolor='black'>
<tr><td>Daty rezerwacji:</td></tr>
""")
        for booking in bookings:
            response.write("<tr><td>{}</td></tr>".format(booking.date))
        response.write("</table>" + html_end)
        return response
    else:
        date = request.POST.get("date")
        try:
            book = Booking.objects.get(room_id=room, date=date)
        except:
            return HttpResponse("Termin zajęty")




