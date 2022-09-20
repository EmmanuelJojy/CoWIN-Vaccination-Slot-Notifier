import json, time, os, threading, datetime
from lzma import CHECK_CRC32
#import playsound
from urllib.request import Request, urlopen

# ADD LOCALITY PIN CODES TO CHECK
# ------------------------------------
wpin = [683572, 683577, 683581, 683574, 683576, 683587, 682315]
# -------------------------------------
warn = 0
spec = False

def alert():
    global warn
    if warn == 0:
        os.system('echo | set /p="9447213133" | clip')
        os.system('start firefox "https://selfregistration.cowin.gov.in/"')
        warn = 1
    for i in range(3):
        pass
        # playsound.playsound('alarm.mp3')
    return None

def displaySlots(data):
    # spacers = [5, 30, 10, 5, 5, 5, 5, 15]
    line = '-' * 105
    def form(l, c = "Sl"):
        # modify order
        print(f"\t{c:<5}{l[0]:<30}{l[6]:<15}{l[1]:^15}{l[2]:^10}{l[3]:^10}{l[4]:^10}{l[5]:^10}")
        
    headers = ["Location", "Date", "Age", "Total", "Dose 1", "Dose 2", "Drug"] 
    print()
    form(headers)
    print(f"\t{line}")
    c = 0
    for i in data:
        form(i, c)
        c += 1
    print()

def watch(): 
    t = None
    timestamp = 1
    l = str(datetime.date.today()).split('-')[::-1]
    date = f"{l[0]}-{l[1]}-{l[2]}"
    while True:
        try:
            # if timestamp % 2:
            #     raw = urlopen(Request(f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/calendarByDistrict?district_id=307&date={date}", headers={'User-Agent': 'Mozilla/5.0'})).read().decode()
            # else:
            #     raw = urlopen(Request(f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id=307&date={date}", headers={'User-Agent': 'Mozilla/5.0'})).read().decode()
            raw = urlopen(Request(f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id=307&date={date}", headers={'User-Agent': 'Mozilla/5.0'})).read().decode()
            d = json.loads(raw) 
            slot, flag = [], False
            print(f"Cycle {timestamp:04d}:  [Scan items: {len(d['centers']):03d}]")    
            for i in d['centers']:
                if spec or i['pincode'] in wpin:
                    for j in i['sessions']:
                        
                        dat = j['date']
                        age = str(j['min_age_limit']) + '+'
                        ava = j['available_capacity']
                        nam = i['name']
                        d01 = j['available_capacity_dose1']
                        d02 = j['available_capacity_dose2']
                        drg = j['vaccine']
                        
                        if ava and d01:
                            slot.append([nam, dat, age, str(ava).zfill(3), str(d01).zfill(3), str(d02).zfill(3), drg])
                            flag = True
                            #   print(f"Slot Active -> [{dat} Age:{age} Avail:{ava:02d}] {nam}")
                            
                            if t == None or not t.is_alive(): # In-consistent!
                                t = threading.Thread(target=alert, daemon=True)
                                t.start()
                            break
            if flag:
                displaySlots(slot)
        except Exception as e:
            print(f"Cycle {timestamp:04d}:  [Scan items: 000]")    
            print("\t--- Request Error --- ")
            print(f"\t>>> {e}")
        
        timestamp += 1
        
        # 100 API calls per 5 minutes
        # safe refresh limit >= 5    
        time.sleep(7.5)

if __name__ == "__main__":
    try:
        print("CoWIN Slot Notifier v1.0")
        print("All Rights Reserved (C) 2021")
        print("@author: Emmanuel Jojy\n\nInitializing System...\n")
        watch()
    except:
        pass
