
'''
    This file is a script for adding meters to the sql database
'''

import pandas as pd
import json
import math
import numpy as np
from parkMap.models import Meter


def addMeter(row):
    meter = Meter(
        meter_head = row['METERHEAD'],
        rate_weekday_9A_6P = getRates(row['R_MF_9A_6P']),
        rate_weekday_6P_10P = getRates(row['R_MF_6P_10']),
        rate_sat_9A_6P = getRates(row['R_SA_9A_6P']),
        rate_sat_6P_10P = getRates(row['R_SA_6P_10']),
        rate_sun_9A_6P = getRates(row['R_SU_9A_6P']),
        rate_sun_6P_10P = getRates(row['R_SU_6P_10']),

        time_weekday_9A_6P = getTimeLimit(row['T_MF_9A_6P']),
        time_weekday_6P_10P = getTimeLimit(row['T_MF_6P_10']),
        time_sat_9A_6P = getTimeLimit(row['T_SA_9A_6P']),
        time_sat_6P_10P = getTimeLimit(row['T_SA_6P_10']),
        time_sun_9A_6P = getTimeLimit(row['T_SU_9A_6P']),
        time_sun_6P_10P = getTimeLimit(row['T_SU_6P_10']),

        credit_card = True if row['CREDITCARD'] == "Yes" else False,
        pay_phone = row['PAY_PHONE'],
        lat = getLat(json.loads(row['Geom'])),
        long = getLong(json.loads(row['Geom'])),
        location = row['Geo Local Area'],
        meter_id = row['METERID']
        )
    return meter

def getLat(geom):
    return geom['coordinates'][1]

def getLong(geom):
    return geom['coordinates'][0]

def getTimeLimit(timeStr):
    if (pd.isna(timeStr)):
        return None
    tokens = timeStr.split()
    if ('Hr' in timeStr):
        return float(tokens[0])
    elif('min' in timeStr):
        return float(tokens[0]) / 60
    else:
        return None

def getRates(rateStr):
    if (not pd.isna(rateStr)):
        return float(rateStr[1:])
    return None


# df = pd.read_csv('')
# meters = df.apply(addMeter, axis = 1)
# for m in meters:
#     m.save()