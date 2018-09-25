import urllib.request
import json

FARM_CHRIS = 'https://io.adafruit.com/api/v2/topher_cantrell/feeds/quantum-farmer-chris/data'
FARM_GARY = 'https://io.adafruit.com/api/v2/garydion/feeds/quantum-farmer-gary/data'

with open('credentials.json') as f:
    config = json.load(f)

post_headers = {
    'X-AIO-Key': config['AIO'], 
    'Content-Type':'application/json'
}

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

#post_animal(FARM_CHRIS,'Bat')
#print(get_last_animal(FARM_CHRIS))
