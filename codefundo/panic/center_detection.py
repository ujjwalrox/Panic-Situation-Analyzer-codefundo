import time
from django.utils import timezone

import numpy as np
from .models import Account, Location,  PanicLocation

worldMap = np.zeros((182, 362), dtype='int16')
PANIC_LIMIT = 500
panic_blocks = []


def setValue(lat, lng):
    intLat = 90 + int(lat)
    intLng = 180 + int(lng)

    worldMap[intLat][intLng] += 1
    if (worldMap[intLat][intLng] >= PANIC_LIMIT):
        panic_blocks += [intLat, intLng]


def clearMap():
    for i in range(182):
        for j in range(362):
            worldMap[i][j] = 0

def feedValue():
    panic_locations = Location.objects.all()
    currentTime = time.time()
    for location in panic_locations:
        print(location.time)
        if (location.time != None and timezone.now() >= location.time):
            print(timezone.now() - location.time)
        else:
            print("false")
