import datetime
from django.db import models
from django.utils import timezone

# Create your models here.
class Meter(models.Model):
    rate_weekday_9A_6P = models.FloatField('R_MF_9A_6P', null = True)
    rate_weekday_6P_10P = models.FloatField('R_MF_6P_10', null = True)
    rate_sat_9A_6P = models.FloatField('R_SA_9A_6P', null = True)
    rate_sat_6P_10P = models.FloatField('R_SA_6P_10', null = True)
    rate_sun_9A_6P = models.FloatField('R_SU_9A_6P', null = True)
    rate_sun_6P_10P = models.FloatField('R_SU_6P_10', null = True)

    time_weekday_9A_6P = models.FloatField('T_MF_9A_6P', null = True)
    time_weekday_6P_10P = models.FloatField('T_MF_6P_10', null = True)
    time_sat_9A_6P = models.FloatField('T_SA_9A_6P', null = True)
    time_sat_6P_10P = models.FloatField('T_SA_6P_10', null = True)
    time_sun_9A_6P = models.FloatField('T_SU_9A_6P', null = True)
    time_sun_6P_10P = models.FloatField('T_SU_6P_10', null = True)

    credit_card = models.BooleanField('CREDITCARD', null = True)
    pay_phone = models.CharField('PAY_PHONE', max_length = 10)
    lat = models.FloatField('Latitude')
    long = models.FloatField('Longitude')
    location = models.CharField('Geo Local Area', max_length = 140)
    meter_id = models.CharField('METERID', max_length = 10, primary_key= True)

    def __str__(self):
        return "{} MeterID: {}".format(self.location, self.meter_id)
    
    def getPayByPhoneID(self):
        return self.pay_phone
