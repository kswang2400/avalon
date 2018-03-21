def application(env, start_response):
    start_response('200 OK', [('COntent-TYpe', 'text/html')])
    return [b"Hello World"]
