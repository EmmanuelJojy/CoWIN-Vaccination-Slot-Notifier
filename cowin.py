# -*- coding: utf-8 -*-
"""
Created on Fri May 28 18:45:47 2021

@author: Emmanuel
"""

# UNDER DEVELOPMENT
# REFER main.py

import json, time, playsound, os, threading, datetime
from urllib.request import Request, urlopen
        

class WatchTower(object):
    
    def __init__(self, stateID = 307, ping = 7.5):
        
        assert ping >= 5.0, "Request Limit Vioalation. Potential HTTP 429 ERROR"
        self.ping = ping
        
        self.sID = stateID
        self.url = self.setURL()
    
    def setURL(self):
        l = datetime.date.today().split('-')[::-1]
        date = f"{l[0]}-{l[1]}-{l[2]}"
        
        req = [f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/calendarByDistrict?district_id={self.sID}&date={date}",
               f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id={self.sID}&date={date}"]
        
        return req
    
    def sendReq(url, cycle):
        raw = urlopen(Request(url, headers={'User-Agent': 'Mozilla/5.0'})).read().decode()
        return json.loads(raw)
    
    def formSlot(name, j):
        # # int
        # self.ava = j['available_capacity']
        # self.d01 = j['available_capacity_dose1']
        # self.d02 = j['available_capacity_dose2']
        
        # # str
        # self.nam = name
        # self.dat = j['date']
        # self.age = j['min_age_limit']
        # self.ava = j['available_capacity']
        # self.d01 = j['available_capacity_dose1']
        # self.d02 = j['available_capacity_dose2']
        # self.drg = j['vaccine'] 
        pass