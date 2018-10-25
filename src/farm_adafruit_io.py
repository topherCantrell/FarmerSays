import urllib.request
import json
import time

import credentials # Not checked in ... simple KEY = VALUE module

FARM_CHRIS = 'https://io.adafruit.com/api/v2/topher_cantrell/feeds/quantum-farmer-chris/data'
FARM_GARY  = 'https://io.adafruit.com/api/v2/garydion/feeds/quantum-farmer-gary/data'

TIME_BETWEEN_POLLS = 2 # 2 Seconds

# TODO eat exceptions instead of killing the program

post_headers = {
    'X-AIO-Key': credentials.AIO, 
    'Content-Type':'application/json'
}

last_animal = None

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
        try:
            an = get_last_animal(feed_url)
            if last_animal == None:
                last_animal = an      
                print('First animal '+str(an))          
                continue
            if an['id'] != last_animal['id']:
                last_animal = an
                print('New animal '+str(an))
                return an['value']
            else:
                print('Animal '+str(an)+' is not new')
        except Exception as ex:
            print('Ignoring exception '+str(ex))            
        time.sleep(TIME_BETWEEN_POLLS)

if __name__ == '__main__':
    while True:
        animal = wait_for_new_animal(FARM_CHRIS)
        print(animal)