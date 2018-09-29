import urllib.request
import json
import time

import credentials # Not checked in ... simple KEY = VALUE module

FARM_CHRIS = 'https://io.adafruit.com/api/v2/topher_cantrell/feeds/quantum-hdw_farmer_says-chris/data'
FARM_GARY = 'https://io.adafruit.com/api/v2/garydion/feeds/quantum-hdw_farmer_says-gary/data'

TIME_BETWEEN_POLLS = 2 # 2 Seconds

post_headers = {
    'X-AIO-Key': credentials.AIO, 
    'Content-Type':'application/json'
}

last_animal = {'id':''}

def get_last_animal(feed_url):
    req = urllib.request.Request(url=feed_url)
    f = urllib.request.urlopen(req)
    ret =  json.loads(f.read().decode())
    return ret[0]

def post_animal(feed_url,animal):
    data = {'value' : animal}
    d = json.dumps(data).encode()
    req = urllib.request.Request(url=feed_url,headers=post_headers,method='POST',data=d)
    f = urllib.request.urlopen(req)
    ret =  json.loads(f.read().decode())
    return ret

def wait_for_new_animal(feed_url):
    global last_animal
    while True:
        an = get_last_animal(feed_url)
        if an['id'] != last_animal['id']:
            last_animal = an
            return an
        time.sleep(TIME_BETWEEN_POLLS)
        