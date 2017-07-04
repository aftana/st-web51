def app(environ, start_response):
    raw_uri = str(environ.get('RAW_URI'))
    raw_uri = raw_uri[2:]
    params = raw_uri.split('&')
	
    data = ''
    for param in params:
        data += param + '\r\n'
	
    start_response("200 OK", [
	  ("Content-Type", "text/plain"),
	  ("Content-Length", str(len(data)))
	])
	return iter([data])