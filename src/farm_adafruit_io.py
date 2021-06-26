import json
import time
import urllib.request

import credentials  # Not checked in

FARM_CHRIS = 'https://io.adafruit.com/api/v2/topher_cantrell/feeds/quantum-farmer-chris/data'
FARM_GARY = 'https://io.adafruit.com/api/v2/garydion/feeds/quantum-farmer-gary/data'

TIME_BETWEEN_POLLS = 2  # 2 Seconds

last_animal = None


def get_last_animal():

    if not credentials.IO_FROM:
        return None

    headers = {
        'X-AIO-Key': credentials.IO_FROM['key'],
        'Content-Type': 'application/json'
    }
    req = urllib.request.Request(url=credentials.IO_FROM['feed'], headers=headers)

    f = urllib.request.urlopen(req)
    ret = json.loads(f.read().decode())
    return ret[0]


def post_animal(animal):

    if not credentials.IO_TO:
        return

    data = {'value': animal}
    d = json.dumps(data).encode()
    headers = {
        'X-AIO-Key': credentials.IO_TO['key'],
        'Content-Type': 'application/json'
    }
    req = urllib.request.Request(url=credentials.IO_TO['feed'], headers=headers, method='POST', data=d)
    f = urllib.request.urlopen(req)
    ret = json.loads(f.read().decode())
    return ret


def wait_for_new_animal():
    global last_animal
    while True:
        try:
            an = get_last_animal()
            if last_animal is None:
                last_animal = an
                # print('First animal ' + str(an))
                continue
            if an['id'] != last_animal['id']:
                last_animal = an
                # print('New animal ' + str(an))
                return an['value']
            else:
                # print('Animal ' + str(an) + ' is not new')
                pass
        except Exception:
            # print('Ignoring exception ' + str(ex))
            pass
        time.sleep(TIME_BETWEEN_POLLS)


if __name__ == '__main__':

    while True:
        animal = wait_for_new_animal()
        print(animal)
