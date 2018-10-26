from decimal import Decimal
import json

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Location, Account, PanicLocation, DisasterArea
from .forms import SignUpForm
from .center_detection import *

# Create your views here.


def index(request):
    return render(request, 'index.html')


def map(request):
    locations = Location.objects.all()
    disasters = DisasterArea.objects.all()
    return render(
        request,
        'map.html',
        {'locations': locations, 'disasters': disasters}
    )


def SignUp(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            user = authenticate(username=username, password=password)
            account = Account.objects.create(
                user=user, first_name=first_name, last_name=last_name)

            Location.objects.create(account=account)
            return render(request, 'index.html')

    else:
        form = SignUpForm()

    return render(request, 'signup.html', {'form': form})


def locations(request):
    locations = Location.objects.all()
    return render(
        request,
        'locations.html',
        {'locations': locations}
    )


@csrf_exempt
def api_location(request):

    if request.method == 'POST':
        try:
            print(request.body)
            strData = request.body.decode("utf-8")
            if(strData[0] != '{'):
                strData = '{"' + strData.strip('&').replace('=', '":"').replace('&', '","') + '"}'
            print("strData: " + strData)
            data = json.loads(strData)
            print(data)

            account = get_object_or_404(Account, user__username=data['username'])
            lat = float(data['lat'])
            lng = float(data['lng'])
            intLat = int(lat)
            intLng = int(lng)
            disaster_area = DisasterArea.objects.all().filter(lat=intLat, lng=intLng)

            text = ""
            if (len(disaster_area is not 0)):
                text = "ALERT: possibility of " + disaster_area[0].disaster_type + " is predicted in your area."
            location = get_object_or_404(Location, account=account)
            location.lat = lat
            location.lng = lng
            location.save()

            if (text == ""):
                return HttpResponse("Server: Success")
            else:
                return HttpResponse(text)

        except Exception as e:
            print("Server: Error " + str(e))
            return HttpResponse("Server: Error")
    else:
        return HttpResponse("Server: Error GET request")


@csrf_exempt
def api_panic_location(request):
    if request.method == 'POST':
        try:
            print(request.body)
            strData = request.body.decode("utf-8")
            if(strData[0] != '{'):
                strData = '{"' + strData.strip('&').replace('=', '":"').replace('&', '","') + '"}'
            print("strData: " + strData)
            data = json.loads(strData)
            print(data)
            account = get_object_or_404(Account, user__username=data['username'])
            lat = float(data['lat'])
            lng = float(data['lng'])
            panic_location = PanicLocation.objects.create(account=account, lat=lat, lng=lng)
            return HttpResponse("Server: Success" + str(panic_location))

        except Exception as e:
            print("Server: Error " + str(e))
            return HttpResponse("Server: Error")
    else:
        return HttpResponse("Server: Error GET request")


def map_algo(request):
    feedValue()
    return HttpResponse("Server: Prediction Model Started")
