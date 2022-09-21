from flask import json


def response_json(response):
    return json.loads(response.data.decode('utf8'))


def test_get_user_bob(client):
    response = client.get('user/Bob')

    assert response.status_code == 200
    assert response_json(response)['lname'] == "Newby"


def test_get_user_jim(client):
    response = client.get('user/jim')
    json = response_json(response)

    assert response.status_code == 200
    assert json['lname'] == "Hopper"
    assert not json['lname'] == "Newby"


def test_get_user_not_found(client):
    response = client.get('user/not%20found')

    assert response.status_code == 404
    assert response.data == b"No user found"
