from datetime import timedelta
import numpy as np

from django.utils import timezone

from .models import Account, Location,  PanicLocation, DisasterArea

worldMap = np.zeros((182, 362), dtype='int16')
PANIC_LIMIT = 1
PANIC_TIME = 50
panic_blocks = []
user_list = []


def setValue(lat, lng, user_name, time):
    global panic_blocks
    intLat = 90 + int(lat)
    intLng = 180 + int(lng)

    worldMap[intLat][intLng] += 1
    if (worldMap[intLat][intLng] >= PANIC_LIMIT):
        if ([intLat, intLng] not in panic_blocks):
            panic_blocks.append([user_name, intLat, intLng, time])
            DisasterArea.objects.create(lat=intLat, lng=intLng)


def clearMap():
    global worldMap
    for i in range(182):
        for j in range(362):
            worldMap[i][j] = 0


def feedValue():
    clearMap()
    global user_list
    panic_locations = PanicLocation.objects.all()
    currentTime = timezone.now()
    for location in panic_locations:
        user_name = location.account.user.username
        time = location.time
        if (currentTime - location.time) <= timedelta(minutes=PANIC_LIMIT):
            setValue(location.lat, location.lng, user_name, time)

    print(panic_blocks)
    runModel()


def runModel():
    global panic_blocks
    for panic in panic_blocks:
        # create a list and pass to models:
        pass
