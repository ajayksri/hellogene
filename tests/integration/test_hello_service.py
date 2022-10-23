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


def test_user_exist_random_name():
    # Add user
    url = 'http://127.0.0.1:5000/app/hello/v2/user/jay'
    given_names = ['Vijay', 'Sanjay', 'Dhanajay']
    for a_given_name in given_names:
        body = {'name': a_given_name}
        response = requests.post(url, json=body)
        assert response.status_code == 200

    # get request
    response = requests.get(url)
    assert response.status_code == 200

    name_returned = response.json()['data']
    name_returned = name_returned.split()[1]
    name_returned = name_returned.split('!')[0]

    assert name_returned in given_names
