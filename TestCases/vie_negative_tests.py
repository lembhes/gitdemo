import json
import pytest
import requests
from TestCases import API_Calls
from TestCases.Support import assertion
from Variables.variable import *
from TestCases.Support import helper

# ---------------- Get the Base64 --------------------------------#

base64secrets = helper.get_base64secrets(CLIENT_ID_Shruti, CLIENT_SECRET_Shruti)
print(base64secrets)

BASE_TOKEN = 'Basic ' + base64secrets


# ---------------- Get the Base64  for dummy API --------------------------------#

base64secrets = helper.get_base64secrets(CLIENT_ID_PARTYM, CLIENT_SECRET_PARTYM)
print(base64secrets)

BASE_TOKEN_PARTYM = 'Basic ' + base64secrets

# ----------- Get the ACCESS TOKEN ----------------------------#

status_code, json_data = API_Calls.token_api(BASE_URL, VALID_TOKEN_DATA, BASE_TOKEN, CONTENT_TYPE_URL_ENCODED)
ACCESS_TOKEN = json_data['access_token']

@pytest.fixture
def input_url1():
   input = ASYNC_URL
   return input

@pytest.fixture
def input_url2():
   input = BASE_URL
   return input

@pytest.fixture()
def get_token():
    status_code, json_data = API_Calls.token_api(BASE_URL, VALID_TOKEN_DATA, BASE_TOKEN, CONTENT_TYPE_URL_ENCODED)
    ACCESS_TOKEN = json_data['access_token']
    return  ACCESS_TOKEN


@pytest.fixture
def input_data():
   input = ASYNC_SCORE_API_DATA
   return input

@pytest.fixture
def get_header():
   content_type = CONTENT_TYPE_APPLICATION_JSON
   return content_type


def test_async_score_api_put_request(input_url1, input_data,get_token , get_header):
    headers_scores = {'Authorization': get_token, 'Content-Type': get_header}
    res = requests.put(url=input_url1 + ASYNC_SCORE_ENDPOINT, data=json.dumps(input_data), headers=headers_scores)
    print(res)
    assert res.status_code == 403

def test_async_score_api_get_request(input_url1, input_data, get_token, get_header):
    headers_scores = {'Authorization': get_token, 'Content-Type': get_header}
    res = requests.get(url=input_url1 + ASYNC_SCORE_ENDPOINT, data=json.dumps(input_data), headers=headers_scores)
    print(res)
    assert res.status_code == 403

def test_async_score_api_delete_request(input_url1, input_data, get_token, get_header):
    headers_scores = {'Authorization': get_token, 'Content-Type': get_header}
    res = requests.delete(url=input_url1 + ASYNC_SCORE_ENDPOINT, data=json.dumps(input_data), headers=headers_scores)
    print(res)
    assert res.status_code == 403


def test_get_async_score_api_post_request(input_url1,get_token):
    headers_get_score_api = {'Authorization': get_token}
    res = requests.post(url=input_url1 + GET_ASYNC_SCORE_ENDPOINT,headers=headers_get_score_api)
    print(res)
    assert res.status_code == 403


def test_get_async_score_api_put_request(input_url1,get_token):
    headers_get_score_api = {'Authorization': get_token}
    res = requests.put(url=input_url1 + GET_ASYNC_SCORE_ENDPOINT,headers=headers_get_score_api)
    print(res)
    assert res.status_code == 403

def test_get_async_score_api_delete_request(input_url1,get_token):
    headers_get_score_api = {'Authorization': get_token}
    res = requests.delete(url=input_url1 + GET_ASYNC_SCORE_ENDPOINT,headers=headers_get_score_api)
    print(res)
    assert res.status_code == 403


def test_get_voice_feature_by_measure_post_request(input_url2,get_token):
    headers_get_voice_feature_by_measure_api = {'Authorization': get_token}
    res = requests.post(url=input_url2 + GET_VOICE_FEATURE_MEASURE_ENDPOINT,headers=headers_get_voice_feature_by_measure_api)
    print(res)
    assert res.status_code == 403

def test_get_voice_feature_by_measure_put_request(input_url2,get_token):
    headers_get_voice_feature_by_measure_api = {'Authorization': get_token}
    res = requests.put(url=input_url2 + GET_VOICE_FEATURE_MEASURE_ENDPOINT,headers=headers_get_voice_feature_by_measure_api)
    print(res)
    assert res.status_code == 403

def test_get_voice_feature_by_measure_delete_request(input_url2,get_token):
    headers_get_voice_feature_by_measure_api = {'Authorization': get_token}
    res = requests.delete(url=input_url2 + GET_VOICE_FEATURE_MEASURE_ENDPOINT,headers=headers_get_voice_feature_by_measure_api)
    print(res)
    assert res.status_code == 403