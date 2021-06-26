import cgi
import json
import traceback

from engine import GameEngine

WORLDS = {}


def application(environ, start_response):

    try:
        if environ['REQUEST_METHOD'] == 'POST':
            request_body_size = int(environ.get('CONTENT_LENGTH', '0'))
            request_body = environ['wsgi.input'].read(request_body_size)
            data = json.loads(request_body.decode())

            WORLDS = {}

            world = data['world']
            if world not in WORLDS:
                with open('public/' + world + '/OBJECTS.json') as f:
                    objects = json.load(f)
                with open('public/' + world + '/ROOMS.json') as f:
                    rooms = json.load(f)
                WORLDS['world'] = [objects, rooms]

            world = WORLDS['world']
            game = GameEngine(world[0], world[1])

            game.set_state(data['state'])

            cmd = game.decode_button_command(data['user_command'])
            prs = game.process_command(cmd)

            audio_prs = game.prompts_only(prs)
            text_prs = game.text_only(prs)

            ndata = {
                'text': text_prs,
                'audio': audio_prs,
                'state': game.get_state()
            }

            start_response('200 OK', [('Content-Type', 'application/json')])
            return [json.dumps(ndata).encode()]

        else:
            # If we are running alongside a web server then the server will handle static files.
            # This is for the stand-alone case (like running on the Farmer Says)
            fn = environ['PATH_INFO']
            if fn == '/':
                fn = '/index.html'
            print('*', fn, '*')
            with open('public' + fn, 'rb') as f:
                data = f.read()
            if fn.endswith('.json'):
                start_response('200 OK', [('Content-Type', 'application/json')])
            else:
                start_response('200 OK', [('Content-Type', 'text/html')])
            return [data]
    except Exception:
        with open('ex.txt', 'w') as f:
            f.write(traceback.format_exc())
        raise


if __name__ == '__main__':
    try:
        from wsgiref.simple_server import make_server
        try:
            httpd = make_server('', 80, application)
            print('Serving on port 80...')
        except Exception:
            httpd = make_server('', 8080, application)
            print('Serving on port 8080...')
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('Goodbye.')
