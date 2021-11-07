from django.shortcuts import render,redirect, HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
import math
from datetime import date
import time
from django.template.loader import render_to_string, get_template
from django.conf import settings
from django.core.mail import EmailMessage
from django.contrib import messages
from django.contrib.auth.models import User

# Create your views here.

def index(request):

    dests = Destination.objects.all()
    destsWithOffer = Destination.objects.filter(offer=True)
    # print(destsWithOffer)
    testimonials = Contact.objects.filter(subject = "testimonial")
    # print(testimonials)
    # print(testimonials.count())
    return render(request, 'index.html', {'dests': dests, 'testimonials':testimonials, 'testimonialCount':testimonials.count(), 'destsWithOffer': destsWithOffer.count()})


def about(request):
    return render(request, 'about.html')

def services(request):

    dests = Destination.objects.all()
    return render(request, 'destinations.html', {'dests': dests})


def contact(request):
    if request.method == 'POST':
        yourName = request.POST['yourName']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']

        # if request.user.is_authenticated:
        #     con = Contact(yourName=yourName, email=email, subject=subject, message=message)
        #     con.save()
        #     return redirect('contact')
        # else:
        #     return redirect('login')

        c = Contact(yourName=yourName, email=email, subject=subject, message=message)
        c.save()

        return redirect('contact')

    else:
        return render(request, 'contact.html')



def destination_details(request,id):
    dest = Destination.objects.get(id=id)
    # print(dest)
    # print("Price = ", dest.price)
    # print("Loc = ", dest.name)

    request.session['name'] = dest.name
    request.session['price'] = dest.price
    request.session['day'] = dest.days
    # print(request.session['name'])
    # print(request.session['price'])
    # print("Days = ", request.session['day'])

    return render(request,'destination_details.html',{'dest':dest})


def booking(request, id):
    destinationName = request.session['name']
    destinationPrice = request.session['price']
    # print(destinationName)
    # print(destinationPrice)

    if request.method == 'POST':
        firstName = request.POST['firstName']
        lastName = request.POST['lastName']
        fromCity = request.POST['fromCity']
        toCity = request.POST['toCity']
        depatureDate = request.POST['depatureDate']
        days = request.POST['days']
        noOfRooms = int(request.POST['noOfRooms'])
        noOfAdults = int(request.POST['noOfAdults'])
        noOfChildren = int(request.POST['noOfChildren'])
        email = request.POST['email']
        phoneNo = request.POST['phoneNo']
        totalAmount = int(request.POST['totalAmount'])

        request.session['fname'] = firstName
        request.session['lname'] = lastName
        request.session['to_city'] = toCity
        request.session['from_city'] = fromCity
        request.session['depature_date'] = depatureDate
        request.session['arrival_date'] = days
        request.session['no_of_rooms'] = noOfRooms
        request.session['no_of_adults'] = noOfAdults
        request.session['no_of_children'] = noOfChildren
        request.session['email'] = email
        request.session['phone_no'] = phoneNo
        request.session['total_amount'] = totalAmount

        requiredRooms = 1
        if noOfAdults/3 > 1:
            requiredRooms = math.ceil(noOfAdults/3)

        if noOfRooms < requiredRooms:
            noOfRooms = requiredRooms - noOfRooms
            messages.info(request, 'For adding more travellers, Please add' + str(noOfRooms) +' more rooms')
            return redirect('booking', id)

        if noOfRooms > noOfAdults:
            messages.info(request, 'Minimum 1 Adult is required per Room')
            return redirect('booking', id)

        if (noOfAdults + noOfChildren)/4 > 1:
            requiredRooms = math.ceil((noOfAdults + noOfChildren)/4)

        if noOfRooms < requiredRooms:
            noOfRooms = requiredRooms - noOfRooms
            messages.info(request, 'For adding more travellers, Please add'+ str(noOfRooms) + 'more rooms')
            return redirect('booking',id)

        noOfRooms = requiredRooms
        request.session['no_of_rooms'] = noOfRooms
        # print("No of rooms = ", noOfRooms)
        # print("Working")
        # book = Booking(firstName=firstName, lastName=lastName, fromCity=fromCity, toCity=toCity, depatureDate=depatureDate, arrivalDate=arrivalDate, noOfRooms=noOfRooms, noOfAdults=noOfAdults, noOfChildren=noOfChildren, email=email,phoneNo=phoneNo, totalAmount=totalAmount)

        # book.save()
        return redirect('receipt')
    else:
        return render(request, 'booking.html')

@login_required(login_url='/accounts/login')
def receipt(request):
    first_name = request.session.get('fname')
    # print(first_name)
    last_name = request.session.get('lname')
    # print(last_name)

    tour_amount = int(request.session.get('total_amount')) #Per person
    # print(tour_amount)
    adults = int(request.session.get('no_of_adults'))
    # print(adults)
    rooms = int(request.session.get('no_of_rooms'))
    # print(rooms)
    children = int(request.session.get('no_of_children'))
    # print(adults)
    if rooms > 1:
        totalCost = tour_amount*adults + tour_amount*children/2 + rooms*tour_amount/4
    else:

        totalCost = tour_amount*adults + tour_amount*children/2

    request.session['total_amount'] =str(totalCost)

    # print(totalCost)
    request.session['total_amount'] = tour_amount

    today = date.today()

    t = time.localtime()
    currentTime = time.strftime("%H:%M:%S", t)
    return render(request,'receipt.html',{'totalCost':totalCost, 'date':today, 'currentTime':currentTime})



def search(request):

    # dests = Destination.objects.all()
    query = request.GET['query']
    # budget = request.GET['budget']
    price = Destination.objects.all()
    # print(price.price)
    # print(query)
    # print("Price = ", budget)
    dests = Destination.objects.filter(name__icontains = query)
    # print(dests)
    # dests = Destination.objects.filter(price__lt = budget)
    # print(dests)

    return render(request, 'search.html', {'dests' : dests, 'query':query})
    # return HttpResponse('This is search')

def confirm_booking(request):
    if request.method == 'POST':
        fullName = request.POST['fullName']
        fromCity = request.POST['fromCity']
        toCity = request.POST['toCity']
        depatureDate = request.POST['depatureDate']
        arrivalDate = request.POST['days']
        noOfRooms= int(request.POST['noOfRooms'])
        noOfAdults  = int(request.POST['noOfAdults'])
        noOfChildren = int(request.POST['noOfChildren'])
        email = request.POST['email']
        phoneNo = request.POST['phoneNo']
        amountPerPerson = request.POST['amountPerPerson']
        totalAmount = float(request.POST['totalAmount'])
        userName = request.user.username


        books = ConfirmBooking(fullName=fullName, fromCity=fromCity, toCity=toCity,
                       depatureDate=depatureDate, days=arrivalDate, noOfRooms=noOfRooms, noOfAdults=noOfAdults,
                       noOfChildren=noOfChildren, email=email, phoneNo=phoneNo, amountPerPerson=amountPerPerson,
                       totalAmount=totalAmount, userName=userName)
        books.save()

        message = render_to_string('order_placed_body.html', {'fullName':fullName, 'fromCity':fromCity, 'toCity':toCity, 'depatureDate':depatureDate,'arrivalDate':arrivalDate,'noOfRooms':noOfRooms,'noOfAdults':noOfAdults,'noOfChildren':noOfChildren,'email':email,'phoneNo':phoneNo,'amountPerPerson':amountPerPerson, 'totalAmount':totalAmount})
        msg = EmailMessage(
            'Tripology',
            message,
            settings.EMAIL_HOST_USER,
            [request.user.email]
        )
        msg.content_subtype = "html"  # Main content is now text/html
        msg.send()

        # print("Mail successfully sent")

        # print("User Added")

        return redirect('/')
    else:
        return render(request,'booking.html')

@login_required(login_url='/accounts/login')
def orderHistory(request):

    bookings = ConfirmBooking.objects.filter(userName = request.user.username)
    destinations = Destination.objects.all()

    return render(request, 'orderHistory.html', {'bookings':bookings, 'destinations':destinations})

def delete_destination(request, id):

    if request.method == 'POST':

        message = render_to_string('order_cancel_body.html', {'orderId':id})
        msg = EmailMessage(
            'Tripology',
            message,
            settings.EMAIL_HOST_USER,
            [request.user.email]
        )
        msg.content_subtype = "html"  # Main content is now text/html
        msg.send()

        ConfirmBooking.objects.filter(id=id).delete()


        return redirect('orderHistory')