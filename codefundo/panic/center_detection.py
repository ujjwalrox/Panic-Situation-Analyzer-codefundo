from datetime import timedelta
import numpy as np
import threading

from django.utils import timezone

from .models import Account, Location,  PanicLocation, DisasterArea, Threshold
from .disaster_predictor import predict


# using computational geometry algorithm to find center of clustured points

worldMap = np.zeros((182, 362), dtype='int16')
CONSTANTS = Threshold.objects.all()[0]
PANIC_LIMIT = CONSTANTS.panic_limit
PANIC_TIME = CONSTANTS.panic_time
panic_blocks = []
user_list = []
point_clusters = {}


def setValue(lat, lng, user_name, tim):
    global point_clusters
    global worldMap
    intLat = 90 + int(lat)
    intLng = 180 + int(lng)

    worldMap[intLat][intLng] += 1
    if (worldMap[intLat][intLng] >= PANIC_LIMIT):  # Declare panic
        if ((intLat, intLng) not in point_clusters):
            point_clusters[(intLat-90, intLng-180)] = []

            time = ((str(tim).split(' ')[1]).split(':'))
            hour = int(time[0])
            minute = int(time[1])
            sec = int(time[2].split('.')[0])

            point_clusters[(intLat-90, intLng-180)].append([lat, lng, hour, minute, sec])
            disaster_area = DisasterArea.objects.all().filter(lat=intLat-90, lng=intLng-180)
            if (len(disaster_area) == 0):
                DisasterArea.objects.create(lat=intLat-90, lng=intLng-180)
        else:
            point_clusters[(intLat-90, intLng-180)].append([lat, lng, hour, minute, sec])





def clearMap():
    global point_clusters
    point_clusters = {}
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
        if ((currentTime - location.time).total_seconds() <= PANIC_TIME):
            setValue(location.lat, location.lng, user_name, time)

    print(point_clusters)
    runModel(point_clusters)


def runModel(point_clusters):
    for point, cluster in point_clusters.items():
        print(point)
        print(cluster)
        # calling prediction algorithm
        disaster_type = predict(cluster)
        print(disaster_type)
        disaster_area = DisasterArea.objects.all().filter(lat=point[0], lng=point[1])[0]
        disaster_area.disaster_type = disaster_type
        disaster_area.save()
