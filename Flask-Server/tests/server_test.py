import json

import pytest


def ordered(obj):
    if isinstance(obj, dict):
        return sorted((k, ordered(v)) for k, v in obj.items())
    if isinstance(obj, list):
        return sorted(ordered(x) for x in obj)
    else:
        return obj


def ordered_str(json_str):
    if json_str:
        if isinstance(json_str, bytes):
            json_str = json_str.decode("utf-8")
        return ordered(json.loads(json_str))
    else:
        return None


class TestPinAPI(object):
    def test_empty_db(self, app):
        rv = app.get('/')
        assert rv.status == '404 NOT FOUND'

    def test_get_pins_empty(self, app):
        data = '{"data": []}'
        rv = app.get('/api/pins')
        print(rv.data)
        assert ordered_str(rv.data) == ordered_str(data)
        assert rv.status == '200 OK'

    def test_get_pin_empty(self, app):
        data = '{"data": null}'
        rv = app.get('/api/pins/1')
        print(rv.data)
        assert ordered_str(rv.data) == ordered_str(data)
        assert rv.status == '200 OK'

    @pytest.mark.xfail
    def test_create_pin(self, app):
        data = '{"data": {"type":"pins","relationships":{"sequences":{"links":{"related":"/api/pins/12/sequences"}}},"attributes":{"name":"test","state":0,"number":12},"id":"12"}}'
        request_data = '{"data": {"type": "pins", "attributes": {"number": 12, "name": "test", "id": "1"}}}'

        rv1 = app.post('/api/pins', data=request_data)
        assert ordered_str(rv1.data) == ordered_str(data)
        assert rv1.status == '201 CREATED'

        rv2 = app.get('/api/pins/12')
        assert ordered_str(rv2.data) == ordered_str(data)
        assert rv2.status == '200 OK'

        #TODO: should create conflict
        rv3 = app.post('/api/pins', data=request_data)
        assert ordered_str(rv3.data) != ordered_str(data)
        assert rv3.status == '409 Conflict'

    @pytest.mark.xfail
    def test_edit_pin(self, app):
        data = '{"data": {"type":"pins","relationships":{"sequences":{"links":{"related":"/api/pins/12/sequences"}}},"attributes":{"name":"test","state":0,"number":12},"id":"12"}}'
        request_data = '{"data": {"type": "pins", "attributes": {"number": 12, "name": "test"}}}'

        data2 = '{"data": {"type":"pins","relationships":{"sequences":{"links":{"related":"/api/pins/12/sequences"}}},"attributes":{"name":"blub","state":1,"number":12},"id":"12"}}'
        request_data2 = '{"data": {"type": "pins", "attributes": {"number": 12, "name": "blub","state":1}}}'

        rv1 = app.post('/api/pins', data=request_data)
        assert ordered_str(rv1.data) == ordered_str(data)
        assert rv1.status == '201 CREATED'

        rv2 = app.get('/api/pins/12')
        assert ordered_str(rv2.data) == ordered_str(data)
        assert rv2.status == '200 OK'

        rv3 = app.patch('/api/pins', data=request_data2)
        assert ordered_str(rv3.data) != ordered_str(data2)
        assert rv3.status == '200 OK'

    @pytest.mark.xfail
    def test_delete_pin_empty(self, app):
        rv1 = app.delete('/api/pins/12')
        print(rv1.data)
        assert rv1.status == '404 NOT FOUND'

    def test_delete_pin(self, app):
        data = '{"data": {"type":"pins","relationships":{"sequences":{"links":{"related":"/api/pins/12/sequences"}}},"attributes":{"name":"test","state":0,"number":12},"id":"12"}}'
        request_data = '{"data": {"type": "pins", "attributes": {"number": 12, "name": "test"}}}'

        rv1 = app.post('/api/pins', data=request_data)
        assert ordered_str(rv1.data) == ordered_str(data)
        assert rv1.status == '201 CREATED'

        rv2 = app.delete('/api/pins/12')
        assert rv2.status in ('204 NO CONTENT', '200 OK')


class TestSequenceAPI(object):
    def test_get_sequences_empty(self, app):
        data = '{"data": []}'
        rv = app.get('/api/sequences')
        assert ordered_str(rv.data) == ordered_str(data)
        assert rv.status == '200 OK'

    def test_get_sequence_empty(self, app):
        data = '{"data": null}'
        rv = app.get('/api/sequences/12')
        print(rv.data)
        assert ordered_str(rv.data) == ordered_str(data)
        assert rv.status == '200 OK'

    @pytest.mark.xfail
    def test_create_sequence(self, app):
        p_data = '{"data": {"type":"pins","relationships":{"sequences":{"links":{"related":"/api/pins/12/sequences"}}},"attributes":{"name":"test","state":0,"number":12},"id":"12"}}'
        p_request_data = '{"data": {"type": "pins", "attributes": {"number": 12, "name": "test"}}}'

        rv1 = app.post('/api/pins', data=p_request_data)
        assert ordered_str(rv1.data) == ordered_str(p_data)
        assert rv1.status == '201 CREATED'

        rv2 = app.get('/api/pins/12')
        assert ordered_str(rv2.data) == ordered_str(p_data)
        assert rv2.status == '200 OK'

        s_request_data = '{"data": {"type": "sequences","attributes": {"start_time": "12:00","start_range": "0:05","end_time": "14:00","end_range": "0:05","pin-id": 12}, "id": "1"}}'
        s_data = '{"data": {"type": "sequences", "attributes": {"end_range": "0:05", "end_time": "14:00", "start_range": "0:05", "start_time": "12:00"}, "id": "1"}}'

        rv3 = app.post('/api/sequences', data=s_request_data)
        assert ordered_str(rv3.data) == ordered_str(s_data)
        assert rv3.status == '201 CREATED'

        #TODO: should conflict, creates new ID
        rv4 = app.post('/api/sequences', data=s_request_data)
        assert ordered_str(rv4.data) == ordered_str(s_data)
        assert rv4.status == '409 Conflict'
