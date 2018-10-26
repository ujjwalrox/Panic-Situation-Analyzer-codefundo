from datetime import timedelta
import numpy as np

from django.utils import timezone

from .models import Account, Location,  PanicLocation, DisasterArea
from .disaster_predictor import predict


# using basic computational geometry algorithm to find center of clustured points

worldMap = np.zeros((182, 362), dtype='int16')
PANIC_LIMIT = 1
PANIC_TIME = 10
panic_blocks = []
user_list = []
point_clusters = {}


def setValue(lat, lng, user_name, tim):
    global point_clusters
    global worldMap
    intLat = 90 + int(lat)
    intLng = 180 + int(lng)

    worldMap[intLat][intLng] += 1
    if (worldMap[intLat][intLng] >= PANIC_LIMIT): # Declare panic
        if ((intLat, intLng) not in point_clusters):
            point_clusters[(intLat, intLng)] = []

            time = ((str(tim).split(' ')[1]).split(':'))
            hour = int(time[0])
            minute = int(time[1])
            sec = int(time[2].split('.')[0])

            point_clusters[(intLat, intLng)].append([lat, lng, hour, minute, sec])
            DisasterArea.objects.create(lat=lat, lng=lng)
        else:
            point_clusters[((intLat, intLng))].append([lat, lng, hour, minute, sec])





def clearMap():
    global point_clusters
    panic_blocks = []
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

    print(point_clusters)
    runModel()


def runModel():
    global point_clusters
    for points, cluster in point_clusters:
        print(point)
        # calling prediction algorithm
        disaster_type = predict(cluster)
        print(disaster_type)