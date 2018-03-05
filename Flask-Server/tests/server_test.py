import json

def ordered(obj):
    """order json objects
    """
    if isinstance(obj, dict):
        return sorted((k, ordered(v)) for k, v in obj.items())
    if isinstance(obj, list):
        return sorted(ordered(x) for x in obj)
    else:
        return obj




class TestServer(object):

    def test_empty_db(self, app):
        rv = app.get('/')
        assert rv.status == '404 NOT FOUND'

    def test_get_pins_empty(self, app):
        data = b'{"data": []}'
        rv = app.get('/api/pins')
        print(rv.data)
        assert ordered(rv.data) == ordered(data)

    def test_get_sequences_empty(self, app):
        data = b'{"data": []}'
        rv = app.get('/api/sequences')
        print(rv.data)
        assert ordered(rv.data) == ordered(data)

    def test_get_pin_404(self, app):
        data = b'{"errors": [{"status": "401", "code": 401, "title": "Authentication Error", "detail": "The token is not provided!", "source": {"pointer": "http://localhost/api/pins"}}]}'
        rv = app.get('/api/pins/1')
        print(rv.data)
        assert ordered(rv.data) == ordered(data)
