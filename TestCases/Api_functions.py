import requests
import json

from Variables.variable import *


def token_api(BASE_URL, VALID_TOKEN_DATA, BASE_TOKEN, CONTENT_TYPE_URL_ENCODED):
    headers = {'Authorization': BASE_TOKEN, 'Content-Type': CONTENT_TYPE_URL_ENCODED}
    response = requests.post(url=BASE_URL + TOKEN_END_POINT, data=VALID_TOKEN_DATA, headers=headers)
    return response.status_code, response.json()


def measure_api(BASE_URL, MEASURE_END_POINT, ACCESS_TOKEN):
    headers_get = {'Authorization': ACCESS_TOKEN}
    res_get = requests.get(url=BASE_URL + MEASURE_END_POINT, headers=headers_get)
    return res_get.status_code, res_get.json()


def subject_api(BASE_URL, VALID_SUBJECT_DATA, ACCESS_TOKEN, CONTENT_TYPE_APPLICATION_JSON):
    headers_subject = {'Authorization': ACCESS_TOKEN, 'Content-Type': CONTENT_TYPE_APPLICATION_JSON}
    res = requests.post(url=BASE_URL + SUBJECT_END_POINT, data=json.dumps(VALID_SUBJECT_DATA), headers=headers_subject)
    return res.status_code, res.json()


def measure_id_api(BASE_URL, MEASURE_ID_END_POINT, ACCESS_TOKEN):
    headers_measure_id = {'Authorization': ACCESS_TOKEN}
    res = requests.get(url= BASE_URL + '/measures/' + str(MEASURE_ID_END_POINT), headers= headers_measure_id)
    return res.status_code, res.json()


def storage_api(BASE_URL, VALID_STORAGE_DATA, ACCESS_TOKEN, CONTENT_TYPE_APPLICATION_JSON):
    headers_storage = {'Authorization': ACCESS_TOKEN, 'Content-Type': CONTENT_TYPE_APPLICATION_JSON}
    res = requests.post(url=BASE_URL + STORAGE_END_POINT, data=json.dumps(VALID_STORAGE_DATA), headers=headers_storage)
    return res.status_code, res.json()

#
# def audio_file_upload(STORAGE_SIGNED_URL):
#     with open(r'C:\Users\gsc-30427\Desktop\audio\c45164f2-cdc7-48f9-ad08-0fd621ae3be9_82da7ad9-bdeb-4fe6-bc80-138fdb7038d1_1247_1613_Nikhil_marathi_alz.wav','rb') as filedata:
#         r = requests.put(url= STORAGE_SIGNED_URL, files={'file': filedata})
#         return r.status_code


def score_api(BASE_URL, VALID_SCORE_DATA, ACCESS_TOKEN, CONTENT_TYPE_APPLICATION_JSON):
    headers_scores = {'Authorization': ACCESS_TOKEN, 'Content-Type': CONTENT_TYPE_APPLICATION_JSON}
    res = requests.post(url=BASE_URL + SCORE_END_POINT, data=json.dumps(VALID_SCORE_DATA), headers=headers_scores)
    return res.status_code, res.json()
