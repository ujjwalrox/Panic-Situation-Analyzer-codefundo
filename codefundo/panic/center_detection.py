from datetime import timedelta
import numpy as np

from django.utils import timezone

from .models import Account, Location,  PanicLocation

worldMap = np.zeros((182, 362), dtype='int16')
PANIC_LIMIT = 500
panic_blocks = []


def setValue(lat, lng):
    intLat = 90 + int(lat)
    intLng = 180 + int(lng)

    worldMap[intLat][intLng] += 1
    if (worldMap[intLat][intLng] >= PANIC_LIMIT):
        if ([intLat, intLng] not in panic_blocks):
            panic_blocks += [intLat, intLng]


def clearMap():
    for i in range(182):
        for j in range(362):
            worldMap[i][j] = 0


def feedValue():
    clearMap()
    panic_locations = PanicLocation.objects.all()
    currentTime = timezone.now()
    for location in panic_locations:
        if (location.time is not None and (currentTime - location.time) <= timedelta(minutes=10)):
            setValue(location.lat, location.lng)

    runModel()


def runModel():
    for panic in panic_blocks:
        # create a list and pass to models:
        pass
