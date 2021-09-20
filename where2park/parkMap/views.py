from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.forms.models import model_to_dict
from .models import Meter
from datetime import datetime
import math
import json

METER_NUM_DISPLAY = 40

def test(request):
    return render(request, 'parkMap/test.html')

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
    up to *METER_NUM_DISPLAY* meters.
    Filter by the location first.
'''
def getNearestMeters(request):
    lat = 49.282730
    lon = -123.120735
    threshold = 10
    meters = Meter.objects.all()
    lat = float(lat)
    lon = float(lon)
    threshold = float(threshold)
    distance = dict()
    result = dict()
    for meter in meters:
        dist = getDistance(lat, lon, meter.lat, meter.long)
        if (dist <= threshold):
            distance[meter.meter_id] = dist

    meterList = sorted(distance.items(), key=lambda x: x[1])
    f = open('./parkMap/token.txt', 'r')
    token = f.read()
    f.close()
    meterList = [Meter.objects.filter(meter_id = x[0])[0] for x in meterList[:METER_NUM_DISPLAY]]
    result =  {
        'closest_meters':meterList, 
        'mapbox_access_token': token,
        'center_lat': lat,
        'center_long': lon,
        } 
    return render(request, 'parkMap/meters.html',result)
    # return render(request, 'parkMap/meters.html',result)

def getNearestMetersJSON(request, lat, lon, threshold):
    meters = Meter.objects.all()
    lat = float(lat)
    lon = float(lon)
    threshold = float(threshold)
    distance = dict()
    result = dict()
    for meter in meters:
        dist = getDistance(lat, lon, meter.lat, meter.long)
        if (dist <= threshold):
            distance[meter.meter_id] = dist

    meterList = sorted(distance.items(), key=lambda x: x[1])
    f = open('./parkMap/token.txt', 'r')
    token = f.read()
    f.close()
    meterObjList = [Meter.objects.filter(meter_id = x[0])[0] for x in meterList[:METER_NUM_DISPLAY]]
    meterList = [model_to_dict(x) for x in meterObjList]
    for idx, meter in enumerate(meterList):
        meter['curr_rate'] = meterObjList[idx].getCurrentRate();

    result =  {
        'closest_meters': meterList, 
        'mapbox_access_token': token,
        'center_lat': lat,
        'center_long': lon,
        } 
    return JsonResponse(json.dumps(result), safe=False)

'''
    Compute ecludian distance between location1(lat1, lon1) and location2(lat2, lon2)
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