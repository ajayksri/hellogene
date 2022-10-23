#!/usr/bin/env python3

import requests


def test_add_user():
    url = 'http://127.0.0.1:5000/app/hello/v1/user/vijay'
    body = {'name': 'Vijay'}
    response = requests.post(url, json=body)
    assert response.status_code == 200


def test_user_exist():
    # Add user
    url = 'http://127.0.0.1:5000/app/hello/v1/user/vijay'
    body = {'name': 'Vijay'}
    response = requests.post(url, json=body)
    assert response.status_code == 200

    # get request
    response = requests.get(url)
    assert response.status_code == 200
    assert response.json()['data'] == 'Hello Vijay!'

def test_user_not_exist():
    url = 'http://127.0.0.1:5000/app/hello/v1/user/sanjay'
    response = requests.get(url)
    assert response.status_code == 200
    assert response.json()['data'] == 'Hello World!'
