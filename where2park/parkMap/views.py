from django.shortcuts import render
from django.http import HttpResponse
from .models import Meter
from datetime import datetime
import math
import json

def index(request):
    context = {'hi'}
    return render(request, 'parkMap/index.html')

def detail(request, meter_id):
    return HttpResponse("You're looking at meter %s." % meter_id)

def getMeterRate(request, meter_id):
    meter = Meter.objects.filter(meter_id = meter_id)[0]
    now = datetime.now()
    hour = now.hour
    weekday = now.weekday()

    rate = 0.0
    if (weekday >= 0 and weekday <=4):  
        if (hour >= 9 and hour < 18):
            rate = meter.rate_weekday_9A_6P
        elif (hour >= 18 and hour < 22):
            rate = meter.rate_weekday_6P_10P
    elif (weekday == 5):
        if (hour >= 9 and hour < 18):
            rate = meter.rate_sat_9A_6P
        elif (hour >= 18 and hour < 22):
            rate = meter.rate_sat_6P_10P
    elif (weekday == 6):
        if (hour >= 9 and hour < 18):
            rate = meter.rate_sun_9A_6P
        elif (hour >= 18 and hour < 22):
            rate = meter.rate_sun_6P_10P

    return HttpResponse("The rate of meter {} at current time is {}".format(meter_id, rate))


'''
    Get meters that are within *threshold(km)* distance to the location (lat, long),
    up to 20 meters.
    Filter by the location first.
'''
def getClosestMeters(request, lat, lon, threshold):
    meters = Meter.objects.all()
    lat = float(lat)
    lon = float(lon)
    threshold = float(threshold)
    distance = dict()
    for meter in meters:
        dist = getDistance(lat, lon, meter.lat, meter.long)
        if (dist <= threshold):
            distance[meter.meter_id] = dist
    distance = sorted(distance.items(), key=lambda x: x[1])
    result = json.dumps(distance[:20])
    return HttpResponse(result)




'''
    Compute ecludian distance between location1 and location2
'''
def getDistance(lat1, lon1, lat2, lon2):
    R = 6373.0 #radius of the Earth
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c

    return distance