import json
import requests
import pytest
from TestCases import API_Calls
from TestCases.Support import assertion
from Variables.variable import *
from TestCases.Support import helper
from jsonschema import validate
from collections import Mapping, MutableMapping
#
#
# # ---------------- Get the Base64 --------------------------------#

base64secrets = helper.get_base64secrets(CLIENT_ID, CLIENT_SECRET)
print(base64secrets)

BASE_TOKEN = 'Basic ' + base64secrets


# # ---------------- Get the Base64  for dummy API --------------------------------#

base64secrets = helper.get_base64secrets(CLIENT_ID_dummy, CLIENT_SECRET_dummy)
print(base64secrets)

BASE_TOKEN_DUMMY = 'Basic ' + base64secrets

# # ----------- Get the ACCESS TOKEN ----------------------------#

status_code, json_data = API_Calls.token_api(BASE_URL, VALID_TOKEN_DATA, BASE_TOKEN, CONTENT_TYPE_URL_ENCODED)
ACCESS_TOKEN = json_data['access_token']


# # ---------------- Get the Base64  for party deleted client credentials--------------------------------#

base64secrets = helper.get_base64secrets(CLIENT_ID_PARTYM, CLIENT_SECRET_PARTYM)
print(base64secrets)

BASE_TOKEN_PARTYM = 'Basic ' + base64secrets

# # ----------- Get the ACCESS TOKEN for party deleted client credentials ----------------------------#

status_code, json_data = API_Calls.token_api(BASE_URL, VALID_TOKEN_DATA, BASE_TOKEN_PARTYM, CONTENT_TYPE_URL_ENCODED)
ACCESS_TOKEN_PARTYM = json_data['access_token']

# # # ----------- Get the ACCESS TOKEN DUMMY API  ----------------------------#
#
# status_code, json_data = API_Calls.token_api(BASE_URL, VALID_TOKEN_DATA, BASE_TOKEN_DUMMY, CONTENT_TYPE_URL_ENCODED)
# ACCESS_TOKEN_DUMMY = json_data['access_token']

# ----------- Get the JOB_ID to be stored from post request ----------------------------#
status_code,json_data =API_Calls.async_score_api(ASYNC_URL,ACCESS_TOKEN_DUMMY,CONTENT_TYPE_APPLICATION_JSON)
JOB_ID = json_data['jobId']

# #-----------------------
ASYNC_SCORE_API_DATA ={
    "infer": [
        {
            "type": "ACOUSTIC",
            "version": "v1"
        }
    ],
    "filePath": "s3://dev-sondeplatform2-us-subject-metadata/b1e664dd-0b64-49a5-8224-d6e0e349c09a/voice-samples/de7de039-6d8f-40f7-8d2a-7fb27e8a1d7a.wav",
    "measureName": "dummy"
}
#
#print(ASYNC_SCORE_API_DATA['infer'][0]['type'])



def test_async_score_api_when_request_contains_no_body():
    status, score_json_data = API_Calls.async_score_api(ASYNC_URL, ASYNC_SCORE_NO_DATA_REQUEST ,ACCESS_TOKEN_DUMMY, CONTENT_TYPE_APPLICATION_JSON)
    print(status, score_json_data)
    assert status == 400

def test_async_score_api_invalid_end_point():
    headers1 = {'Authorization': ACCESS_TOKEN_DUMMY, 'Content-Type': CONTENT_TYPE_APPLICATION_JSON}
    INVALID_END_POINT = '/XYZ'
    res = requests.post(url=ASYNC_URL + INVALID_END_POINT, data=json.dumps(ASYNC_SCORE_API_DATA), headers=headers1)
    print(res)
    assert res.status_code == 403


def test_async_score_api_incorrect_ACCESS_TOKEN():
    INCORRECT_ACCESS_TOKEN = 'xyz'
    status, data = API_Calls.async_score_api(ASYNC_URL, ASYNC_SCORE_API_DATA, INCORRECT_ACCESS_TOKEN,CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 401
    # ACCESS DENIED
    # status code == 403


def test_async_score_api_expired_access_token():
    status, data = API_Calls.async_score_api(ASYNC_URL, ASYNC_SCORE_API_DATA, EXPIRED_ACCESS_TOKEN,CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 401
    # ACCESS DENIED


def test_async_score_api_missing_authorization():
    headers = {'Content-Type': CONTENT_TYPE_APPLICATION_JSON}
    res = requests.post(url=ASYNC_URL + ASYNC_SCORE_ENDPOINT, data=json.dumps(ASYNC_SCORE_API_DATA), headers=headers)
    print(res)
    assert res.status_code == 401


def test_async_score_api_blank_auth_key():
    headers = {'Authorization': '', 'Content-Type': CONTENT_TYPE_APPLICATION_JSON}
    res = requests.post(url=ASYNC_URL + ASYNC_SCORE_ENDPOINT, data=json.dumps(ASYNC_SCORE_API_DATA), headers=headers)
    print(res)
    assert res.status_code == 401



def test_async_score_api_request_body_infer_blank():
    D_CP = ASYNC_SCORE_API_DATA['infer'].copy()
    D = helper.update_dictionary(D_CP, infer='')
    DATA = {'infer': D}
    status, data = API_Calls.async_score_api(ASYNC_URL, DATA, ACCESS_TOKEN_DUMMY,CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 400



def test_async_score_api_request_body_infer_type_blank():
    D_CP = ASYNC_SCORE_API_DATA['infer'].copy()
    D = helper.update_dictionary(D_CP, type='')
    DATA = {'infer': D}
   # print (DATA)
    status, data = API_Calls.async_score_api(ASYNC_URL, DATA, ACCESS_TOKEN_DUMMY,CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 400


def test_async_score_api_request_body_infer_version_blank():
    D_CP = ASYNC_SCORE_API_DATA['infer'].copy()
    D = helper.update_dictionary(D_CP, version='')
    DATA = {'infer': D}
    #print(DATA)
    status, data = API_Calls.async_score_api(ASYNC_URL, DATA, ACCESS_TOKEN_DUMMY,CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 400


def test_async_score_api_request_body_filePath_blank():
    D_CP = ASYNC_SCORE_API_DATA.copy()
    DATA = helper.update_dictionary(D_CP, filePath='')
    status, data = API_Calls.async_score_api(ASYNC_URL, DATA, ACCESS_TOKEN_DUMMY,CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 400

def test_async_score_api_request_body_measureName_blank():
    D_CP = ASYNC_SCORE_API_DATA.copy()
    DATA = helper.update_dictionary(D_CP, measureName='')
    status, data = API_Calls.async_score_api(ASYNC_URL, DATA, ACCESS_TOKEN_DUMMY,CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 400



# #-------- Invalid  values  in request -------------------
#

def test_async_score_api_request_body_infer_invalid_value():
    D_CP = ASYNC_SCORE_API_DATA.copy()
    DATA = helper.update_dictionary(D_CP, infer='abc')
    status, data = API_Calls.async_score_api(ASYNC_URL, DATA, ACCESS_TOKEN_DUMMY,CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 404



def test_async_score_api_request_body_infer_type_invalid_value():
    D_CP = ASYNC_SCORE_API_DATA.copy()
    DATA = helper.update_dictionary(D_CP, type='testtype')
    status, data = API_Calls.async_score_api(ASYNC_URL, DATA, ACCESS_TOKEN_DUMMY,CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 404


def test_async_score_api_request_body_infer_type_invalid_value_check_with_linguistic():
    D_CP = ASYNC_SCORE_API_DATA.copy()
    DATA = helper.update_dictionary(D_CP, type='linguistic')
    status, data = API_Calls.async_score_api(ASYNC_URL, DATA, ACCESS_TOKEN_DUMMY,CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 404



def test_async_score_api_request_body_infer_version_invalid_value():
    D_CP = ASYNC_SCORE_API_DATA.copy()
    DATA = helper.update_dictionary(D_CP, version='anystring')
    status, data = API_Calls.async_score_api(ASYNC_URL, DATA, ACCESS_TOKEN_DUMMY,CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 404


def test_async_score_api_request_body_filePath_invalid_value():
    D_CP = ASYNC_SCORE_API_DATA.copy()
    DATA = helper.update_dictionary(D_CP, filePath='s3://dev-sondeplatform2-us-subject-metadata/b1e664dd-0b64-49a5-8224-d6e0e349c09abcdefg/voice-samples/de7de039-6d8f-40f7-8d2a-7fb27e8a1d7a.wav')
    status, data = API_Calls.async_score_api(ASYNC_URL, DATA, ACCESS_TOKEN_DUMMY,CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 404

def test_async_score_api_request_body_measureName_invalid_value():
    D_CP = ASYNC_SCORE_API_DATA.copy()
    DATA = helper.update_dictionary(D_CP, measureName='mental-fitness1')
    status, data = API_Calls.async_score_api(ASYNC_URL, DATA, ACCESS_TOKEN_DUMMY,CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 404


# #------------------------- invalid data type for any key ---------
@pytest.mark.API_VIE
def test_async_score_api_request_body_infer_invalid_data_type():
    D_CP = ASYNC_SCORE_API_DATA.copy()
    DATA = helper.update_dictionary(D_CP, infer= '123')
   # print(DATA)
    status, data = API_Calls.async_score_api(ASYNC_URL, DATA, ACCESS_TOKEN_DUMMY,CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 400



def test_async_score_api_request_body_infer_type_invalid_data_type():
    D_CP = ASYNC_SCORE_API_DATA.copy()
    DATA = helper.update_dictionary(D_CP, type=101)
    status, data = API_Calls.async_score_api(ASYNC_URL, DATA, ACCESS_TOKEN_DUMMY,CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 400


def test_async_score_api_request_body_infer_version_invalid_data_type():
    D_CP = ASYNC_SCORE_API_DATA.copy()
    DATA = helper.update_dictionary(D_CP, version= 22)
    status, data = API_Calls.async_score_api(ASYNC_URL, DATA, ACCESS_TOKEN_DUMMY,CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 400


def test_async_score_api_request_body_filePath_invalid_data_type():
    D_CP = ASYNC_SCORE_API_DATA.copy()
    DATA = helper.update_dictionary(D_CP, filePath= 11)
    status, data = API_Calls.async_score_api(ASYNC_URL, DATA, ACCESS_TOKEN_DUMMY,CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 400

def test_async_score_api_request_body_measureName_invalid_data_type():
    D_CP = ASYNC_SCORE_API_DATA.copy()
    DATA = helper.update_dictionary(D_CP, measureName= '["respiratory-symptoms-risk"]')
    status, data = API_Calls.async_score_api(ASYNC_URL, DATA, ACCESS_TOKEN_DUMMY,CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 400



#  #--------------key is missing-------------------------#


def test_async_score_api_request_body_infer_key_missing():
    D_CP = ASYNC_SCORE_API_DATA.copy()
    DATA = helper.delete_key(D_CP, 'infer')
    status, data = API_Calls.async_score_api(ASYNC_URL, DATA, ACCESS_TOKEN_DUMMY, CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 400


def test_async_score_api_request_body_type_key_missing():
    D_CP = ASYNC_SCORE_API_DATA.copy()
    DATA = helper.delete_key(D_CP, 'type')
    status, data = API_Calls.async_score_api(ASYNC_URL, DATA, ACCESS_TOKEN_DUMMY, CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 400


def test_async_score_api_request_body_version_key_missing():
    D_CP = ASYNC_SCORE_API_DATA.copy()
    DATA = helper.delete_key(D_CP, 'version')
    status, data = API_Calls.async_score_api(ASYNC_URL, DATA, ACCESS_TOKEN_DUMMY, CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 400

def test_async_score_api_request_body_filePath_key_missing():
    D_CP = ASYNC_SCORE_API_DATA.copy()
    DATA = helper.delete_key(D_CP, 'filePath')
    status, data = API_Calls.async_score_api(ASYNC_URL, DATA, ACCESS_TOKEN_DUMMY, CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 400

def test_async_score_api_request_body_measureName_key_missing():
    D_CP = ASYNC_SCORE_API_DATA.copy()
    DATA = helper.delete_key(D_CP, 'measureName')
    status, data = API_Calls.async_score_api(ASYNC_URL, DATA, ACCESS_TOKEN_DUMMY, CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 400

def test_async_score_api_with_multiple_key_missing():
    D_CP = ASYNC_SCORE_API_DATA.copy()
    for key in range(0, 5):
        DATA = helper.get_random_pairs(D_CP)
        status, data = API_Calls.score_api(ASYNC_URL, DATA, ACCESS_TOKEN_DUMMY,
                                           CONTENT_TYPE_APPLICATION_JSON)
        print(status, data)
        assert status == 400


def test_async_score_api_request_body_filePath_with_no_audio_file():
    D_CP = ASYNC_SCORE_API_DATA.copy()
    DATA = helper.update_dictionary(D_CP, filePath=NO_AUDIO_FILE_ON_GIVEN_FILE_PATH)
    status, data = API_Calls.score_api(BASE_URL, DATA, ACCESS_TOKEN_DUMMY,CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 400


def test_async_score_api_request_body_filePath_with_incorrect_file_present():
    D_CP = ASYNC_SCORE_API_DATA.copy()
    DATA = helper.update_dictionary(D_CP, filePath=FILE_PATH_WITH_INVALID_FILE)
    status, data = API_Calls.score_api(BASE_URL, DATA, ACCESS_TOKEN_DUMMY,CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 400

# #---------extra key is added in request------------

def test_async_score_api_request_extra_key_added():
    D_CP = ASYNC_SCORE_API_DATA.copy()
    DATA = helper.update_dictionary(D_CP, test='XYZ')
    status, data = API_Calls.score_api(BASE_URL, DATA, ACCESS_TOKEN_DUMMY,CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 400

#
# #-----------header validation ----------
def test_async_score_api_content_type_header_missing():
    header1 = {'Authorization': ACCESS_TOKEN_DUMMY}
    r = requests.post(ASYNC_URL + ASYNC_SCORE_ENDPOINT, data=VALID_SCORE_DATA, headers=header1)
    assert r.status_code == 415


def test_async_score_api_contentType_header_value_invalid():
    status, data = API_Calls.score_api(ASYNC_URL, VALID_SCORE_DATA, ACCESS_TOKEN_DUMMY, CONTENT_TYPE_URL_ENCODED)
    print(status, data)
    assert status == 415

def test_async_score_api_content_type_header_value_missing():
    header1 = {'Authorization': ACCESS_TOKEN_DUMMY, 'Content-Type':''}
    r = requests.post(ASYNC_URL + ASYNC_SCORE_ENDPOINT, data=VALID_SCORE_DATA, headers=header1)
    assert r.status_code == 415
#
# #---business_cases

def test_async_score_api_when_party_does_not_have_access_to_measure():
    status, score_json_data = API_Calls.async_score_api(ASYNC_URL, ASYNC_SCORE_API_DATA_NO_ACCESS_TO_MEASURE , ACCESS_TOKEN_DUMMY, CONTENT_TYPE_APPLICATION_JSON)
    print(status, score_json_data)
    assert status == 403

def test_async_score_api_when_party_tries_to_access_measure_which_is_not_exists():
    status, score_json_data = API_Calls.async_score_api(ASYNC_URL, ASYNC_SCORE_API_DATA_INVALID_MEASURE , ACCESS_TOKEN_DUMMY, CONTENT_TYPE_APPLICATION_JSON)
    print(status, score_json_data)
    assert status == 403

def test_async_score_api_when_party_is_not_registered():
    status, score_json_data = API_Calls.async_score_api(ASYNC_URL, ASYNC_SCORE_API_DATA , ACCESS_TOKEN_PARTYM, CONTENT_TYPE_APPLICATION_JSON)
    print(status, score_json_data)
    assert status == 404
#
# def test_async_score_api_when_subscription_not_found():
#     status, score_json_data = API_Calls.async_score_api(ASYNC_URL, ASYNC_SCORE_API_DATA , ACCESS_TOKEN_SUBSCRIPTION_DELETED, CONTENT_TYPE_APPLICATION_JSON)
#     print(status, score_json_data)
#     assert status == 404


def test_async_score_api_when_file_with_silence():
    status, score_json_data = API_Calls.async_score_api(ASYNC_URL, ASYNC_SCORE_API_DATA_FILE_WITH_SILENCE , ACCESS_TOKEN_DUMMY, CONTENT_TYPE_APPLICATION_JSON)
    print(status, score_json_data)
    assert status == 422

def test_async_score_api_when_file_with_beyond_specified_length():
    status, score_json_data = API_Calls.async_score_api(ASYNC_URL, ASYNC_SCORE_API_DATA_FILE_WITH_GREATER_LENGTH , ACCESS_TOKEN_DUMMY, CONTENT_TYPE_APPLICATION_JSON)
    print(status, score_json_data)
    assert status == 422

#
# #----------- invalid request type for POST ASYNC SCORE API

def test_async_score_api_put_request(ASYNC_URL, DATA, ACCESS_TOKEN_DUMMY, CONTENT_TYPE_APPLICATION_JSON):
    headers_scores = {'Authorization': ACCESS_TOKEN_DUMMY, 'Content-Type': CONTENT_TYPE_APPLICATION_JSON}
    res = requests.put(url=ASYNC_URL + ASYNC_SCORE_ENDPOINT, data=json.dumps(DATA), headers=headers_scores)
    print(res)
    assert res.status_code == 403



def test_async_score_api_get_request(ASYNC_URL, DATA, ACCESS_TOKEN_DUMMY, CONTENT_TYPE_APPLICATION_JSON):
    headers_scores = {'Authorization': ACCESS_TOKEN_DUMMY, 'Content-Type': CONTENT_TYPE_APPLICATION_JSON}
    res = requests.get(url=ASYNC_URL + ASYNC_SCORE_ENDPOINT, data=json.dumps(DATA), headers=headers_scores)
    print(res)
    assert res.status_code == 403


def test_async_score_api_delete_request(ASYNC_URL, DATA, ACCESS_TOKEN_DUMMY, CONTENT_TYPE_APPLICATION_JSON):
    headers_scores = {'Authorization': ACCESS_TOKEN_DUMMY, 'Content-Type': CONTENT_TYPE_APPLICATION_JSON}
    res = requests.delete(url=ASYNC_URL + ASYNC_SCORE_ENDPOINT, data=json.dumps(DATA), headers=headers_scores)
    print(res)
    assert res.status_code == 403

# #-----------------------------------------
# #-----------------------------------------
# #  GET ASYNC SCORE API NEGATIVE CASES #
# #-----------------------------------------
# #-----------------------------------------
#

#---  invalid request type for GET ASYNC SCORE API--#
def test_get_async_score_api_post_request(ASYNC_URL,JOB_ID,ACCESS_TOKEN_DUMMY):
    headers_get_score_api = {'Authorization': ACCESS_TOKEN_DUMMY}
    res = requests.post(url=ASYNC_URL + GET_ASYNC_SCORE_ENDPOINT,headers=headers_get_score_api)
    print(res)
    assert res.status_code == 403


def test_get_async_score_api_put_request(ASYNC_URL,JOB_ID,ACCESS_TOKEN_DUMMY):
    headers_get_score_api = {'Authorization': ACCESS_TOKEN_DUMMY}
    res = requests.put(url=ASYNC_URL + GET_ASYNC_SCORE_ENDPOINT,headers=headers_get_score_api)
    print(res)
    assert res.status_code == 403

def test_get_async_score_api_delete_request(ASYNC_URL,JOB_ID,ACCESS_TOKEN_DUMMY):
    headers_get_score_api = {'Authorization': ACCESS_TOKEN_DUMMY}
    res = requests.delete(url=ASYNC_URL + GET_ASYNC_SCORE_ENDPOINT,headers=headers_get_score_api)
    print(res)
    assert res.status_code == 403
#
# #----negative cases---#


def test_get_async_score_api_invalid_end_point():
    status, data = API_Calls.get_async_score_api(ASYNC_URL, INVALID_GET_SCORE_ENDPOINT, ACCESS_TOKEN_DUMMY)
    print(status, data)
    assert status == 400

def test_get_async_score_api_invalid_end_point():
    headers_get_score_api = {'Authorization': ACCESS_TOKEN_DUMMY}
    res = requests.get(url=ASYNC_URL + '/XYZ', headers=headers_get_score_api)
    print(res)
    assert res.status_code == 403


def test_get_async_score_api_header_missing():
    res = requests.get(url=ASYNC_URL + GET_ASYNC_SCORE_ENDPOINT)
    print(res)
    assert res.status_code == 401

def test_get_async_score_api_invalid_access_token():
    status, data = API_Calls.get_async_score_api(ASYNC_URL,JOB_ID, INVALID_ACCESS_TOKEN)
    print(status, data)
    assert status == 401


def test_get_async_score_api_invalid_job_id():
    headers_get_score_api = {'Authorization': ACCESS_TOKEN_DUMMY}
    res = requests.get(url=ASYNC_URL + ASYNC_SCORE_ENDPOINT+ INVALID_JOB_ID, headers=headers_get_score_api)
    print(res)
    assert res.status_code == 404


def test_get_async_score_api_access_token_missing():
    headers_get_score_api = {'Authorization': ''}
    res = requests.get(url=ASYNC_URL + GET_ASYNC_SCORE_ENDPOINT, headers=headers_get_score_api)
    print(res)
    assert res.status_code == 401


def test_get_async_score_api_extra_content_type_header_is_added():
    headers_get_score_api = {'Authorization': ACCESS_TOKEN_DUMMY, 'Content-Type': CONTENT_TYPE_APPLICATION_JSON}
    res = requests.get(url=ASYNC_URL + GET_ASYNC_SCORE_ENDPOINT, headers=headers_get_score_api)
    print(res)
    assert res.status_code == 404

def test_get_async_score_api_job_id_blank():
    headers_get_score_api = {'Authorization': ACCESS_TOKEN_DUMMY}
    res = requests.get(url=ASYNC_URL + ASYNC_SCORE_ENDPOINT+ BLANK_JOB_ID, headers=headers_get_score_api)
    print(res)
    assert res.status_code == 400

def test_get_async_score_api_job_id_as_integer():
    headers_get_score_api = {'Authorization': ACCESS_TOKEN_DUMMY}
    res = requests.get(url=ASYNC_URL + ASYNC_SCORE_ENDPOINT+ JOB_ID_AS_INTEGER, headers=headers_get_score_api)
    print(res)
    assert res.status_code == 400


def test_get_async_score_api_job_id_missing():
    headers_get_score_api = {'Authorization': ACCESS_TOKEN_DUMMY}
    res = requests.get(url=ASYNC_URL + ASYNC_SCORE_ENDPOINT, headers=headers_get_score_api)
    print(res)
    assert res.status_code == 400





#-----------------------------------------
#-----------------------------------------
#  GET VOICE FEATURES BY MEASURE#
#-----------------------------------------
#-----------------------------------------


#---  invalid request type for GET VOICE FEATURE BY MEASURE NAME --#
def test_get_voice_feature_by_measure_post_request(TEST_URL,FEATURE_BY_MEASURE_NAME,ACCESS_TOKEN_DUMMY):
    headers_get_voice_feature_by_measure_api = {'Authorization': ACCESS_TOKEN_DUMMY}
    res = requests.post(url=TEST_URL + GET_VOICE_FEATURE_MEASURE_ENDPOINT,headers=headers_get_voice_feature_by_measure_api)
    print(res)
    assert res.status_code == 403

def test_get_voice_feature_by_measure_put_request(TEST_URL,FEATURE_BY_MEASURE_NAME,ACCESS_TOKEN_DUMMY):
    headers_get_voice_feature_by_measure_api = {'Authorization': ACCESS_TOKEN_DUMMY}
    res = requests.put(url=TEST_URL + GET_VOICE_FEATURE_MEASURE_ENDPOINT,headers=headers_get_voice_feature_by_measure_api)
    print(res)
    assert res.status_code == 403

def test_get_voice_feature_by_measure_delete_request(TEST_URL,FEATURE_BY_MEASURE_NAME,ACCESS_TOKEN_DUMMY):
    headers_get_voice_feature_by_measure_api = {'Authorization': ACCESS_TOKEN_DUMMY}
    res = requests.delete(url=TEST_URL + GET_VOICE_FEATURE_MEASURE_ENDPOINT,headers=headers_get_voice_feature_by_measure_api)
    print(res)
    assert res.status_code == 403

#----negative cases---#


def test_get_voice_feature_by_measure_invalid_end_point():
    status, data = API_Calls.get_voice_feature_by_measure_api(TEST_URL, GET_VOICE_FEATURE_MEASURE_ENDPOINT_INVALID, ACCESS_TOKEN_DUMMY)
    print(status, data)
    assert status == 400

def test_get_voice_feature_by_measure_invalid_end_point_with_random_input():
    headers_get_voice_feature_by_measure_api = {'Authorization': ACCESS_TOKEN_DUMMY}
    res = requests.get(url=TEST_URL + '/XYZ', headers=headers_get_voice_feature_by_measure_api)
    print(res)
    assert res.status_code == 403


def test_get_voice_feature_by_measure_api_header_missing():
    res = requests.get(url=TEST_URL + GET_VOICE_FEATURE_MEASURE_ENDPOINT)
    print(res)
    assert res.status_code == 401

def test_get_voice_feature_by_measure_api_invalid_access_token():
    status, data = API_Calls.get_voice_feature_by_measure_api(TEST_URL,FEATURE_BY_MEASURE_NAME, INVALID_ACCESS_TOKEN)
    print(status, data)
    assert status == 401


def test_get_voice_feature_by_measure_api_access_token_missing():
    headers_get_voice_feature_by_measure_api = {'Authorization': ''}
    res = requests.get(url=TEST_URL + GET_VOICE_FEATURE_MEASURE_ENDPOINT_INVALID_MEASURE, headers=headers_get_voice_feature_by_measure_api)
    print(res)
    assert res.status_code == 401


def test_get_voice_feature_by_measure_api_extra_content_type_header_is_added():
    headers_get_voice_feature_by_measure_api = {'Authorization': ACCESS_TOKEN_DUMMY, 'Content-Type': CONTENT_TYPE_APPLICATION_JSON}
    res = requests.get(url=TEST_URL + GET_VOICE_FEATURE_MEASURE_ENDPOINT_INVALID_MEASURE, headers=headers_get_voice_feature_by_measure_api)
    print(res)
    assert res.status_code == 404

def test_get_voice_feature_by_measure_api_invalid_measure_name():
    headers_get_voice_feature_by_measure_api = {'Authorization': ACCESS_TOKEN_DUMMY}
    res = requests.get(url=TEST_URL + GET_VOICE_FEATURE_MEASURE_ENDPOINT_INVALID_MEASURE, headers=headers_get_voice_feature_by_measure_api)
    print(res)
    assert res.status_code == 404


def test_get_voice_feature_by_measure_api_no_access_to_measure():
    headers_get_voice_feature_by_measure_api = {'Authorization': ACCESS_TOKEN_DUMMY}
    res = requests.get(url=TEST_URL + GET_VOICE_FEATURE_MEASURE_ENDPOINT_NO_ACCESS_MEASURE, headers=headers_get_voice_feature_by_measure_api)
    print(res)
    assert res.status_code == 403


def test_get_voice_feature_by_measure_api_measure_name_is_blank():
    headers_get_voice_feature_by_measure_api = {'Authorization': ACCESS_TOKEN_DUMMY}
    res = requests.get(url=TEST_URL + GET_VOICE_FEATURE_MEASURE_ENDPOINT_BLANK_MEASURE_NAME, headers=headers_get_voice_feature_by_measure_api)
    print(res)
    assert res.status_code == 404


def test_get_voice_feature_by_measure_api_measure_name_is_missing():
    headers_get_voice_feature_by_measure_api = {'Authorization': ACCESS_TOKEN_DUMMY}
    res = requests.get(url=TEST_URL + GET_VOICE_FEATURE_MEASURE_ENDPOINT_MEASURE_NAME_IS_MISSING, headers=headers_get_voice_feature_by_measure_api)
    print(res)
    assert res.status_code == 404


def test_get_voice_feature_by_measure_api_measure_name_is_integer():
    headers_get_voice_feature_by_measure_api = {'Authorization': ACCESS_TOKEN_DUMMY}
    res = requests.get(url=TEST_URL + GET_VOICE_FEATURE_MEASURE_ENDPOINT_MEASURE_NAME_IS_INTEGER, headers=headers_get_voice_feature_by_measure_api)
    print(res)
    assert res.status_code == 404