from datetime import datetime
from django.shortcuts import render
from .models import Bus, Booking
from django.http import JsonResponse
import jwt
from home.models import UserInfo

# Create your views here.

def find(request):
    context = {}
    if request.method == 'POST':
        source = request.POST['source']
        destination = request.POST['destination']
        date_str = request.POST['date']
        
        date = datetime.strptime(date_str, '%Y-%m-%d')
        
        day = date.strftime("%d")
        month = date.strftime("%m")
        year = date.strftime("%Y")

        buses = Bus.objects.filter(source=source.lower(),destination=destination.lower(),date__year=year,
                                   date__month=month,date__day=day)

        if buses:
            for bus in buses:
                bus.rem = bus.nos - bus.booked

            context['buses'] = buses
            context['source'] = source
            context['destination'] = destination
            context['day'] = day
            context['month'] = month
            context['year'] = year
            return render(request, 'buses.html',context)
        else:
            context['error'] = 'No bus found'
            return render(request, 'find.html', context)
    return render(request, 'find.html')

def book(request):

    context = {}
    if request.method == 'POST':
        bus_id = request.POST['bus_id']
        nos = int(request.POST['nos'])
        token = request.COOKIES['access_token']
        
        try:
            token_data = jwt.decode(token, "secret", algorithms=["HS256"])
            email = token_data['email']
            user = UserInfo.objects.get(email=email)
        except Exception as e:
            print("Booking",e)
            return JsonResponse({'error': 'Invalid token'}, status=400)

        
        try:
            # Retrieve the selected bus
            bus = Bus.objects.get(pk=bus_id)
            context['bus_name'] = bus.bus_name
            context['source'] = bus.source
            context['destination'] = bus.destination
            # Check if there are enough available seats
            if bus.nos-bus.booked < nos:
                return render(request, 'buses.html',{'alert':True})

            context['nos'] = nos
            context['price'] = bus.price
            context['cost'] = bus.price * nos
            context['date'] = bus.date
            context['time'] = bus.time
            # Create a new booking record
            booking = Booking.objects.create(
                user_id=user.id,
                bus_id=bus.id,
                nos=nos
            )

            # Update the availability of seats for the selected bus
            bus.booked += nos
            bus.save()

            return render(request, 'book.html', context)

        except Bus.DoesNotExist:
            return JsonResponse({'error': 'Bus not found'}, status=404)
        
    
    return render(request, 'find.html')

def cancel(request):
    if request.method == "POST":
        booking_id = request.POST['booking_id']
        try:
            booking = Booking.objects.get(id=booking_id)
            booking.nos = 0
            booking.status = "C"
            bus = Bus.objects.get(id=booking.bus_id)
            bus.nos = bus.nos + booking.nos
            booking.save()
            bus.save()
            return JsonResponse({'message': 'Booking cancelled successfully'}, status=200)
        except Booking.DoesNotExist:
            return JsonResponse({'error': 'Booking not found'}, status=404)
    return render(request, 'find.html')

def myBookings(request):
    
    token = request.COOKIES['access_token']

    try:
        token_data = jwt.decode(token, "secret", algorithms=["HS256"])
        email = token_data['email']
        user = UserInfo.objects.get(email=email)
    except Exception as e:
        print("myBooking", e)
        return JsonResponse({'error': 'Invalid token'}, status=400)
        
    bookings = Booking.objects.filter(user_id=user.id)
    buses = []

    for booking in bookings:
        bus = Bus.objects.get(id=booking.bus_id)
        bus.nos = booking.nos
        bus.booking_id = booking.id
        bus.user_name = user.first_name + " " + user.last_name
        bus.total_cost  = bus.price * booking.nos
        bus.nos = booking.nos
        bus.status = booking.status
        if bus.status == "B":
            bus.status = "Booked"
        else:
            bus.status = "Cancelled"
        buses.append(bus)
        
    context = {'buses': buses}
    return render(request, 'myBookings.html', context)
    