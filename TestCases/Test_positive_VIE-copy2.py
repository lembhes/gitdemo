import json
import pytest
import requests
import time
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

# ----------- Get the ACCESS TOKEN for missing party client credentials ----------------------------#

status_code, json_data = API_Calls.token_api(BASE_URL, VALID_TOKEN_DATA, BASE_TOKEN_PARTYM, CONTENT_TYPE_URL_ENCODED)
ACCESS_TOKEN_PARTYM = json_data['access_token']

# ---------------- GET SUBJECT IDENTIFIER -------------------------------#

status, subject_json = API_Calls.subject_api(BASE_URL, VALID_SUBJECT_DATA, ACCESS_TOKEN,
                                             CONTENT_TYPE_APPLICATION_JSON)

SUB_IDENTIFIER = subject_json['userIdentifier']
print(status)

# ----------------------STORAGE API CALL TO GET STORAGE_SIGNED_URL & FILE_PATH ----------------------------#

VALID_STORAGE_DATA = {
    "fileType": "wav",
    "countryCode": "US",
    "userIdentifier": SUB_IDENTIFIER
}

status_code, response_json = API_Calls.storage_api(BASE_URL, VALID_STORAGE_DATA, ACCESS_TOKEN,
                                                   CONTENT_TYPE_APPLICATION_JSON)

STORAGE_SIGNED_URL = response_json['signedURL']
FILE_PATH = response_json['filePath']

# ____________________UPLOAD THE AUDIO SAMPLE  ____________________________________________#


AUDIO_FILE_PATH = 'C:\\Users\\GS-1431\\Downloads\\shrutiD_audio_30sec.wav'


status_code = API_Calls.upload_sample_file(STORAGE_SIGNED_URL, AUDIO_FILE_PATH)

ASYNC_SCORE_API_DATA ={
    "infer": [
        {
            "type": "Acoustic",
            "version": "v2"
        }
    ],
    "filePath": FILE_PATH,
    "measureName": "mental-fitness"
}


#---------- post score API ----------

status, response_json = API_Calls.post_async_score_api(ASYNC_URL, ASYNC_SCORE_API_DATA , ACCESS_TOKEN,CONTENT_TYPE_APPLICATION_JSON)
print(status, response_json, "trace_score_out")

JOB_ID =response_json ['jobId']
print(JOB_ID)


status, response_json = API_Calls.post_async_score_api(ASYNC_URL, ASYNC_SCORE_API_DATA_V2 , ACCESS_TOKEN,CONTENT_TYPE_APPLICATION_JSON)
print(status, response_json, "trace_score_out")

JOB_ID_v2 =response_json ['jobId']
print(JOB_ID_v2)


status, response_json = API_Calls.post_async_score_api(ASYNC_URL, ASYNC_SCORE_API_DATA_V3 , ACCESS_TOKEN,CONTENT_TYPE_APPLICATION_JSON)
print(status, response_json, "trace_score_out")

JOB_ID_v3 =response_json ['jobId']
print(JOB_ID_v3)

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



# -------------------------------------------------------------------------------------------------------------------
# ------------------------------------------- Test Cases --------------------------------------------------------- #



def test_token_api():
   status, data = API_Calls.token_api(BASE_URL, VALID_TOKEN_DATA, BASE_TOKEN, CONTENT_TYPE_URL_ENCODED)
   assert status == 200
   print(status, data)
   assertion.assert_valid_schema(data, 'token_schema.json')


def test_async_score_v1_api():
    status, score_json_data = API_Calls.post_async_score_api(ASYNC_URL, ASYNC_SCORE_API_DATA ,ACCESS_TOKEN, CONTENT_TYPE_APPLICATION_JSON)
    print(status, score_json_data)
    assert status == 202
    assertion.assert_valid_schema(score_json_data, 'score_3.0_api.json')



def test_async_score_v1_api_access_token_with_Bearer_keyword():
    ACCESS_TOKEN_BEARER = 'Bearer ' + ACCESS_TOKEN
    print(ACCESS_TOKEN_BEARER)
    status, score_json_data = API_Calls.post_async_score_api(ASYNC_URL, ASYNC_SCORE_API_DATA ,ACCESS_TOKEN_BEARER, CONTENT_TYPE_APPLICATION_JSON)
    print(status, score_json_data)
    assert status == 202
    assertion.assert_valid_schema(score_json_data, 'score_3.0_api.json')

def test_async_score_v2_api():
    status, score_json_data = API_Calls.post_async_score_api(ASYNC_URL, ASYNC_SCORE_API_DATA_V2, ACCESS_TOKEN, CONTENT_TYPE_APPLICATION_JSON)
    print(status, score_json_data)
    assert status == 202
    assertion.assert_valid_schema(score_json_data, 'score_3.0_api.json')

def test_async_score_v2_api_access_token_Bearer_keyword():
    ACCESS_TOKEN_BEARER = 'Bearer ' + ACCESS_TOKEN
    print(ACCESS_TOKEN_BEARER)
    status, score_json_data = API_Calls.post_async_score_api(ASYNC_URL, ASYNC_SCORE_API_DATA_V2, ACCESS_TOKEN_BEARER, CONTENT_TYPE_APPLICATION_JSON)
    print(status, score_json_data)
    assert status == 202
    assertion.assert_valid_schema(score_json_data, 'score_3.0_api.json')

def test_async_score_v3_api():
    status, score_json_data = API_Calls.post_async_score_api(ASYNC_URL, ASYNC_SCORE_API_DATA_V3, ACCESS_TOKEN, CONTENT_TYPE_APPLICATION_JSON)
    print(status, score_json_data)
    assert status == 202
    assertion.assert_valid_schema(score_json_data, 'score_3.0_api.json')

def test_async_score_v3_api_with_access_token_Bearer_keyword():
    ACCESS_TOKEN_BEARER = 'Bearer ' + ACCESS_TOKEN
    print(ACCESS_TOKEN_BEARER)
    status, score_json_data = API_Calls.post_async_score_api(ASYNC_URL, ASYNC_SCORE_API_DATA_V3, ACCESS_TOKEN_BEARER, CONTENT_TYPE_APPLICATION_JSON)
    print(status, score_json_data)
    assert status == 202
    assertion.assert_valid_schema(score_json_data, 'score_3.0_api.json')
# copying the test case 178
def test_async_score_v3_api_with_access_token_Bearer_keyword1():
    ACCESS_TOKEN_BEARER = 'Bearer ' + ACCESS_TOKEN
    print(ACCESS_TOKEN_BEARER)
    status, score_json_data = API_Calls.post_async_score_api(ASYNC_URL, ASYNC_SCORE_API_DATA_V3, ACCESS_TOKEN_BEARER, CONTENT_TYPE_APPLICATION_JSON)
    print(status, score_json_data)
    assert status == 202
    assertion.assert_valid_schema(score_json_data, 'score_3.0_api.json')

#copying the test cases 179
def test_async_score_v3_api_with_access_token_Bearer_keyword1():
    ACCESS_TOKEN_BEARER = 'Bearer ' + ACCESS_TOKEN
    print(ACCESS_TOKEN_BEARER)
    status, score_json_data = API_Calls.post_async_score_api(ASYNC_URL, ASYNC_SCORE_API_DATA_V3, ACCESS_TOKEN_BEARER, CONTENT_TYPE_APPLICATION_JSON)
    print(status, score_json_data)
    assert status == 202
    assertion.assert_valid_schema(score_json_data, 'score_3.0_api.json')

    
@pytest.mark.API_VIE
def test_get_async_score_v1_api():
    status, get_score_json =  API_Calls.get_async_score_api(ASYNC_URL,ACCESS_TOKEN,JOB_ID)
    print(JOB_ID)
    print (status,get_score_json)
    assert status == 200
    assertion.assert_valid_schema(get_score_json, 'score_3.0_reponse.json')

def test_get_async_score_v1_api_with_access_token_bearer_keyword():
    ACCESS_TOKEN_BEARER = 'Bearer ' + ACCESS_TOKEN
    print(ACCESS_TOKEN_BEARER)
    status, get_score_json =  API_Calls.get_async_score_api(ASYNC_URL,ACCESS_TOKEN_BEARER,JOB_ID)
    print(JOB_ID)
    print (status,get_score_json)
    assert status == 200
    assertion.assert_valid_schema(get_score_json, 'score_3.0_reponse.json')



def test_get_async_score_v2_api():
    status, get_score_json =  API_Calls.get_async_score_api(ASYNC_URL,ACCESS_TOKEN,JOB_ID)
    print(JOB_ID_v2)
    print (status,get_score_json)
    assert status == 200
    assertion.assert_valid_schema(get_score_json, 'score_3.0_reponse.json')


def test_get_async_score_v2_api_with_access_token_bearer_keyword():
    ACCESS_TOKEN_BEARER = 'Bearer ' + ACCESS_TOKEN
    print(ACCESS_TOKEN_BEARER)
    status, get_score_json =  API_Calls.get_async_score_api(ASYNC_URL,ACCESS_TOKEN_BEARER,JOB_ID)
    print(JOB_ID_v2)
    print (status,get_score_json)
    assert status == 200
    assertion.assert_valid_schema(get_score_json, 'score_3.0_reponse.json')

def test_get_async_score_v3_api():
    status, get_score_json =  API_Calls.get_async_score_api(ASYNC_URL,ACCESS_TOKEN,JOB_ID)
    print(JOB_ID_v3)
    print (status,get_score_json)
    assert status == 200
    assertion.assert_valid_schema(get_score_json, 'score_3.0_reponse.json')


def test_get_async_score_v3_api_with_access_token_bearer_keyword():
    ACCESS_TOKEN_BEARER = 'Bearer ' + ACCESS_TOKEN
    print(ACCESS_TOKEN_BEARER)
    status, get_score_json =  API_Calls.get_async_score_api(ASYNC_URL,ACCESS_TOKEN_BEARER,JOB_ID)
    print(JOB_ID_v3)
    print (status,get_score_json)
    assert status == 200
    assertion.assert_valid_schema(get_score_json, 'score_3.0_reponse.json')


def test_get_voice_feature_by_measure_api():
    status, get_voice_feature_json = API_Calls.get_voice_feature_by_measure_api(BASE_URL,ACCESS_TOKEN)
    print (status,get_voice_feature_json)
    assert status == 200
    assertion.assert_valid_schema(get_voice_feature_json, 'get_voice_feature_by_measure.json')

def test_get_voice_feature_by_measure_api_with_access_token_bearer_keyword():
    ACCESS_TOKEN_BEARER = 'Bearer ' + ACCESS_TOKEN
    print(ACCESS_TOKEN_BEARER)
    status, get_voice_feature_json = API_Calls.get_voice_feature_by_measure_api(BASE_URL,ACCESS_TOKEN_BEARER)
    print (status,get_voice_feature_json)
    assert status == 200
    assertion.assert_valid_schema(get_voice_feature_json, 'get_voice_feature_by_measure.json')


#Need to create and validate this json once got the dev credentials

@pytest.mark.API_VIE
def test_async_score_api_request_body_infer_version_uppercase():
    D_CP = ASYNC_SCORE_API_DATA.copy()
    DATA = helper.update_dictionary(D_CP, version='V1')
    status, data = API_Calls.post_async_score_api(ASYNC_URL, DATA, ACCESS_TOKEN, CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 400

@pytest.mark.API_VIE
def test_async_score_api_request_body_infer_version_lowercase():
    D_CP = ASYNC_SCORE_API_DATA.copy()
    DATA = helper.update_dictionary(D_CP, version='v1')
    status, data = API_Calls.post_async_score_api(ASYNC_URL, DATA, ACCESS_TOKEN, CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 400

@pytest.mark.API_VIE
def test_async_score_api_request_body_infer_type_uppercase():
    D_CP = ASYNC_SCORE_API_DATA.copy()
    DATA = helper.update_dictionary(D_CP, type='ACOUSTIC')
    status, data = API_Calls.post_async_score_api(ASYNC_URL, DATA, ACCESS_TOKEN, CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 400

@pytest.mark.API_VIE
def test_async_score_api_request_body_infer_type_lowercase():
    D_CP = ASYNC_SCORE_API_DATA.copy()
    DATA = helper.update_dictionary(D_CP, version='acoustic')
    status, data = API_Calls.post_async_score_api(ASYNC_URL, DATA, ACCESS_TOKEN, CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 400

################ Negative cases #####################


def test_async_score_api_when_request_contains_no_body():
    status, score_json_data = API_Calls.post_async_score_api(ASYNC_URL, ASYNC_SCORE_NO_DATA_REQUEST ,ACCESS_TOKEN, CONTENT_TYPE_APPLICATION_JSON)
    print(status, score_json_data)
    assert status == 400

def test_async_score_api_invalid_end_point():
    headers1 = {'Authorization': ACCESS_TOKEN, 'Content-Type': CONTENT_TYPE_APPLICATION_JSON}
    INVALID_END_POINT = '/XYZ'
    res = requests.post(url=ASYNC_URL + INVALID_END_POINT, data=json.dumps(ASYNC_SCORE_API_DATA), headers=headers1)
    print(res)
    assert res.status_code == 403


def test_async_score_api_incorrect_ACCESS_TOKEN():
    INCORRECT_ACCESS_TOKEN = 'xyz'
    status, data = API_Calls.post_async_score_api(ASYNC_URL, ASYNC_SCORE_API_DATA, INCORRECT_ACCESS_TOKEN,CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 401
    # ACCESS DENIED
    # status code == 403


def test_async_score_api_expired_access_token():
    status, data = API_Calls.post_async_score_api(ASYNC_URL, ASYNC_SCORE_API_DATA, EXPIRED_ACCESS_TOKEN,CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 401
    # ACCESS DENIED

def test_async_score_api_with_access_token_bearer_in_small_case():
    ACCESS_TOKEN_BEARER1 = 'bearer ' + ACCESS_TOKEN
    print(ACCESS_TOKEN_BEARER1)
    status, data = API_Calls.post_async_score_api(ASYNC_URL, ASYNC_SCORE_API_DATA, ACCESS_TOKEN_BEARER1,CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 401


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
    D_CP = ASYNC_SCORE_API_DATA.copy()
    DATA = helper.update_dictionary(D_CP, infer='')
    status, data = API_Calls.post_async_score_api(ASYNC_URL, DATA, ACCESS_TOKEN,CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 400



def test_async_score_api_request_body_infer_type_blank():
    D_CP = ASYNC_SCORE_API_DATA.copy()
    DATA = helper.update_dictionary(D_CP, type='')

   # print (DATA)
    status, data = API_Calls.post_async_score_api(ASYNC_URL, DATA, ACCESS_TOKEN,CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 400


def test_async_score_api_request_body_infer_version_blank():
    D_CP = ASYNC_SCORE_API_DATA.copy()
    DATA = helper.update_dictionary(D_CP, version='')
    #print(DATA)
    status, data = API_Calls.post_async_score_api(ASYNC_URL, DATA, ACCESS_TOKEN,CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 400


def test_async_score_api_request_body_filePath_blank():
    D_CP = ASYNC_SCORE_API_DATA.copy()
    DATA = helper.update_dictionary(D_CP, filePath='')
    status, data = API_Calls.post_async_score_api(ASYNC_URL, DATA, ACCESS_TOKEN,CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 400

def test_async_score_api_request_body_measureName_blank():
    D_CP = ASYNC_SCORE_API_DATA.copy()
    DATA = helper.update_dictionary(D_CP, measureName='')
    status, data = API_Calls.post_async_score_api(ASYNC_URL, DATA, ACCESS_TOKEN,CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 400



# #-------- Invalid  values  in request -------------------
#

def test_async_score_api_request_body_infer_invalid_value():
    D_CP = ASYNC_SCORE_API_DATA.copy()
    DATA = helper.update_dictionary(D_CP, infer='abc')
    status, data = API_Calls.post_async_score_api(ASYNC_URL, DATA, ACCESS_TOKEN,CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 400



def test_async_score_api_request_body_infer_type_invalid_value():
    D_CP = ASYNC_SCORE_API_DATA.copy()
    DATA = helper.update_dictionary(D_CP, type='testtype')
    status, data = API_Calls.post_async_score_api(ASYNC_URL, DATA, ACCESS_TOKEN,CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 400


def test_async_score_api_request_body_infer_type_invalid_value_check_with_linguistic():
    D_CP = ASYNC_SCORE_API_DATA.copy()
    DATA = helper.update_dictionary(D_CP, type='linguistic')
    status, data = API_Calls.post_async_score_api(ASYNC_URL, DATA, ACCESS_TOKEN,CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 400



def test_async_score_api_request_body_infer_version_invalid_value():
    D_CP = ASYNC_SCORE_API_DATA.copy()
    DATA = helper.update_dictionary(D_CP, version='anystring')
    status, data = API_Calls.post_async_score_api(ASYNC_URL, DATA, ACCESS_TOKEN,CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 400


def test_async_score_api_request_body_filePath_invalid_value():
    D_CP = ASYNC_SCORE_API_DATA.copy()
    DATA = helper.update_dictionary(D_CP, filePath='abc')
    status, data = API_Calls.post_async_score_api(ASYNC_URL, DATA, ACCESS_TOKEN,CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 404

def test_async_score_api_request_body_measureName_invalid_value():
    D_CP = ASYNC_SCORE_API_DATA.copy()
    DATA = helper.update_dictionary(D_CP, measureName='mental-fitness1')
    status, data = API_Calls.post_async_score_api(ASYNC_URL, DATA, ACCESS_TOKEN,CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 404


# #------------------------- invalid data type for any key ---------

def test_async_score_api_request_body_infer_invalid_data_type():
    D_CP = ASYNC_SCORE_API_DATA.copy()
    DATA = helper.update_dictionary(D_CP, infer= '123')
   # print(DATA)
    status, data = API_Calls.post_async_score_api(ASYNC_URL, DATA, ACCESS_TOKEN,CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 400



def test_async_score_api_request_body_infer_type_invalid_data_type():
    D_CP = ASYNC_SCORE_API_DATA.copy()
    DATA = helper.update_dictionary(D_CP, type=101)
    status, data = API_Calls.post_async_score_api(ASYNC_URL, DATA, ACCESS_TOKEN,CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 400


def test_async_score_api_request_body_infer_version_invalid_data_type():
    D_CP = ASYNC_SCORE_API_DATA.copy()
    DATA = helper.update_dictionary(D_CP, version= 22)
    status, data = API_Calls.post_async_score_api(ASYNC_URL, DATA, ACCESS_TOKEN,CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 400


def test_async_score_api_request_body_filePath_invalid_data_type():
    D_CP = ASYNC_SCORE_API_DATA.copy()
    DATA = helper.update_dictionary(D_CP, filePath= 11)
    status, data = API_Calls.post_async_score_api(ASYNC_URL, DATA, ACCESS_TOKEN,CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 400

def test_async_score_api_request_body_measureName_invalid_data_type():
    D_CP = ASYNC_SCORE_API_DATA.copy()
    DATA = helper.update_dictionary(D_CP, measureName= 123)
    status, data = API_Calls.post_async_score_api(ASYNC_URL, DATA, ACCESS_TOKEN,CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 400



#  #--------------key is missing-------------------------#


def test_async_score_api_request_body_infer_key_missing():
    D_CP = ASYNC_SCORE_API_DATA.copy()
    DATA = helper.delete_key(D_CP, 'infer')
    status, data = API_Calls.post_async_score_api(ASYNC_URL, DATA, ACCESS_TOKEN, CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 400


def test_async_score_api_request_body_type_key_missing():
    status, data = API_Calls.post_async_score_api(ASYNC_URL, ASYNC_SCORE_API_DATA_TYPE_KEY_MISSING, ACCESS_TOKEN, CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 400


def test_async_score_api_request_body_version_key_missing():
    status, data = API_Calls.post_async_score_api(ASYNC_URL, ASYNC_SCORE_API_DATA_VERSION_KEY_MISSING, ACCESS_TOKEN, CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 400

def test_async_score_api_request_body_filePath_key_missing():
    D_CP = ASYNC_SCORE_API_DATA.copy()
    DATA = helper.delete_key(D_CP, 'filePath')
    status, data = API_Calls.post_async_score_api(ASYNC_URL, DATA, ACCESS_TOKEN, CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 400

def test_async_score_api_request_body_measureName_key_missing():
    D_CP = ASYNC_SCORE_API_DATA.copy()
    DATA = helper.delete_key(D_CP, 'measureName')
    status, data = API_Calls.post_async_score_api(ASYNC_URL, DATA, ACCESS_TOKEN, CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 400

def test_async_score_api_with_multiple_key_missing():
    D_CP = ASYNC_SCORE_API_DATA.copy()
    for key in range(0, 5):
        DATA = helper.get_random_pairs(D_CP)
        print(DATA)
        status, data = API_Calls.score_api(ASYNC_URL, DATA, ACCESS_TOKEN,
                                           CONTENT_TYPE_APPLICATION_JSON)
        print(status, data)
        assert status == 400


def test_async_score_api_request_body_filePath_with_no_audio_file():
    D_CP = ASYNC_SCORE_API_DATA.copy()
    DATA = helper.update_dictionary(D_CP, filePath=NO_AUDIO_FILE_ON_GIVEN_FILE_PATH)
    status, data = API_Calls.score_api(BASE_URL, DATA, ACCESS_TOKEN,CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 400


def test_async_score_api_request_body_filePath_with_incorrect_file_present():
    D_CP = ASYNC_SCORE_API_DATA.copy()
    DATA = helper.update_dictionary(D_CP, filePath=FILE_PATH_WITH_INVALID_FILE)
    status, data = API_Calls.score_api(BASE_URL, DATA, ACCESS_TOKEN,CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 400

# #---------extra key is added in request------------

def test_async_score_api_request_extra_key_added():
    D_CP = ASYNC_SCORE_API_DATA.copy()
    DATA = helper.update_dictionary(D_CP, test='XYZ')
    status, data = API_Calls.score_api(BASE_URL, DATA, ACCESS_TOKEN,CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 400

#
# #-----------header validation ----------
def test_async_score_api_content_type_header_missing():
    header1 = {'Authorization': ACCESS_TOKEN}
    r = requests.post(ASYNC_URL + ASYNC_SCORE_ENDPOINT, data= ASYNC_SCORE_API_DATA, headers=header1)
    assert r.status_code == 415


def test_async_score_api_contentType_header_value_invalid():
    status, data = API_Calls.score_api(ASYNC_URL, ASYNC_SCORE_API_DATA, ACCESS_TOKEN, CONTENT_TYPE_URL_ENCODED)
    print(status, data)
    assert status == 415

def test_async_score_api_content_type_header_value_missing():
    header1 = {'Authorization': ACCESS_TOKEN, 'Content-Type':''}
    r = requests.post(ASYNC_URL + ASYNC_SCORE_ENDPOINT, data=ASYNC_SCORE_API_DATA, headers=header1)
    assert r.status_code == 415
#
# #---business_cases

def test_async_score_api_when_party_does_not_have_access_to_measure():
    status, score_json_data = API_Calls.post_async_score_api(ASYNC_URL, ASYNC_SCORE_API_DATA_NO_ACCESS_TO_MEASURE , ACCESS_TOKEN, CONTENT_TYPE_APPLICATION_JSON)
    print(status, score_json_data)
    assert status == 403

def test_async_score_api_when_party_tries_to_access_measure_which_is_not_exists():
    status, score_json_data = API_Calls.post_async_score_api(ASYNC_URL, ASYNC_SCORE_API_DATA_INVALID_MEASURE , ACCESS_TOKEN, CONTENT_TYPE_APPLICATION_JSON)
    print(status, score_json_data)
    assert status == 404
#manual verification is done for below case
# def test_async_score_api_when_party_is_not_registered():
#     status, score_json_data = API_Calls.post_async_score_api(ASYNC_URL, ASYNC_SCORE_API_DATA , ACCESS_TOKEN_PARTYM, CONTENT_TYPE_APPLICATION_JSON)
#     print(status, score_json_data)
#     assert status == 404
#
# def test_async_score_api_when_subscription_not_found():
#     status, score_json_data = API_Calls.post_async_score_api(ASYNC_URL, ASYNC_SCORE_API_DATA , ACCESS_TOKEN_SUBSCRIPTION_DELETED, CONTENT_TYPE_APPLICATION_JSON)
#     print(status, score_json_data)
#     assert status == 404

#Not required as not handled

#
# def test_async_score_api_when_file_with_silence():
#     status, score_json_data = API_Calls.post_async_score_api(ASYNC_URL, ASYNC_SCORE_API_DATA_FILE_WITH_SILENCE , ACCESS_TOKEN, CONTENT_TYPE_APPLICATION_JSON)
#     print(status, score_json_data)
#     assert status == 422
#
# def test_async_score_api_when_file_with_beyond_specified_length():
#     status, score_json_data = API_Calls.post_async_score_api(ASYNC_URL, ASYNC_SCORE_API_DATA_FILE_WITH_GREATER_LENGTH , ACCESS_TOKEN, CONTENT_TYPE_APPLICATION_JSON)
#     print(status, score_json_data)
#     assert status == 422

#
# #----------- invalid request type for POST ASYNC SCORE API----



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


# #-----------------------------------------
# #-----------------------------------------
# #  GET ASYNC SCORE API NEGATIVE CASES #
# #-----------------------------------------
# #-----------------------------------------


#---  invalid request type for GET ASYNC SCORE API--#

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

# #----negative cases---#


def test_get_async_score_api_invalid_end_point():
    status, data = API_Calls.get_async_score_api(ASYNC_URL, INVALID_GET_SCORE_ENDPOINT, ACCESS_TOKEN)
    print(status, data)
    assert status == 400

def test_get_async_score_api_invalid_end_point():
    headers_get_score_api = {'Authorization': ACCESS_TOKEN}
    res = requests.get(url=ASYNC_URL + '/XYZ', headers=headers_get_score_api)
    print(res)
    assert res.status_code == 403


def test_get_async_score_api_header_missing():
    res = requests.get(url=ASYNC_URL + GET_ASYNC_SCORE_ENDPOINT)
    print(res)
    assert res.status_code == 401

def test_get_async_score_api_invalid_access_token():
    status, data = API_Calls.get_async_score_api(ASYNC_URL, INCORRECT_ACCESS_TOKEN,JOB_ID)
    print(status, data)
    assert status == 401


def test_get_async_score_api_access_token_with_bearer_in_small_case():
    ACCESS_TOKEN_BEARER1 = 'bearer ' + ACCESS_TOKEN
    print(ACCESS_TOKEN_BEARER1)
    status, data = API_Calls.get_async_score_api(ASYNC_URL, ACCESS_TOKEN_BEARER1,JOB_ID)
    print(status, data)
    assert status == 401


def test_get_async_score_api_invalid_job_id():
    headers_get_score_api = {'Authorization': ACCESS_TOKEN}
    res = requests.get(url=ASYNC_URL + ASYNC_SCORE_ENDPOINT+ INVALID_JOB_ID, headers=headers_get_score_api)
    print(res)
    assert res.status_code == 400


def test_get_async_score_api_access_token_missing():
    headers_get_score_api = {'Authorization': ''}
    res = requests.get(url=ASYNC_URL + GET_ASYNC_SCORE_ENDPOINT, headers=headers_get_score_api)
    print(res)
    assert res.status_code == 401


def test_get_async_score_api_extra_content_type_header_is_added():
    headers_get_score_api = {'Authorization': ACCESS_TOKEN, 'Content-Type': CONTENT_TYPE_APPLICATION_JSON}
    res = requests.get(url=ASYNC_URL + GET_ASYNC_SCORE_ENDPOINT, headers=headers_get_score_api)
    print(res)
    assert res.status_code == 400

def test_get_async_score_api_job_id_blank():
    headers_get_score_api = {'Authorization': ACCESS_TOKEN}

    res = requests.get(url=ASYNC_URL + BLANK_JOB_ID_GET_SCORE_ENDPOINT, headers=headers_get_score_api)
    print (ASYNC_URL+BLANK_JOB_ID_GET_SCORE_ENDPOINT)
    print(res)
    assert res.status_code == 400

def test_get_async_score_api_job_id_as_integer():
    headers_get_score_api = {'Authorization': ACCESS_TOKEN}
    res = requests.get(url=ASYNC_URL + ASYNC_SCORE_ENDPOINT+ JOB_ID_AS_INTEGER, headers=headers_get_score_api)
    print(res)
    assert res.status_code == 400


def test_get_async_score_api_job_id_missing():
    headers_get_score_api = {'Authorization': ACCESS_TOKEN}
    res = requests.get(url=ASYNC_URL + ASYNC_SCORE_ENDPOINT + '/', headers=headers_get_score_api)
    print(res)
    assert res.status_code == 403





#-----------------------------------------
#-----------------------------------------
#  GET VOICE FEATURES BY MEASURE#
#-----------------------------------------
#-----------------------------------------


#---  invalid request type for GET VOICE FEATURE BY MEASURE NAME --#
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

#----negative cases---#


def test_get_voice_feature_by_measure_invalid_end_point():
    headers_get_voice_feature_by_measure_api = {'Authorization': ''}
    res = requests.get(url=BASE_URL + GET_VOICE_FEATURE_MEASURE_ENDPOINT_INVALID,headers=headers_get_voice_feature_by_measure_api)
    print(res)
    assert res.status_code == 403


def test_get_voice_feature_by_measure_invalid_end_point_with_random_input():
    headers_get_voice_feature_by_measure_api = {'Authorization': ACCESS_TOKEN}
    res = requests.get(url=BASE_URL + '/XYZ', headers=headers_get_voice_feature_by_measure_api)
    print(res)
    assert res.status_code == 403


def test_get_voice_feature_by_measure_api_header_missing():
    res = requests.get(url=BASE_URL + GET_VOICE_FEATURE_MEASURE_ENDPOINT)
    print(res)
    assert res.status_code == 401

def test_get_voice_feature_by_measure_api_invalid_access_token():
    headers_get_voice_feature_by_measure_api = {'Authorization': INCORRECT_ACCESS_TOKEN}
    res = requests.get(url=BASE_URL +'/measures/name/'+FEATURE_BY_MEASURE_NAME+'/voice-features',headers=headers_get_voice_feature_by_measure_api)
    print(res)
    assert res.status_code == 401


def test_get_voice_feature_by_measure_api_access_token_with_bearer_in_small_case():
    ACCESS_TOKEN_BEARER1 = 'bearer ' + ACCESS_TOKEN
    print(ACCESS_TOKEN_BEARER1)
    headers_get_voice_feature_by_measure_api = {'Authorization': ACCESS_TOKEN_BEARER1}
    res = requests.get(url=BASE_URL +'/measures/name/'+FEATURE_BY_MEASURE_NAME+'/voice-features',headers=headers_get_voice_feature_by_measure_api)
    print(res)
    assert res.status_code == 401


def test_get_voice_feature_by_measure_api_access_token_missing():
    headers_get_voice_feature_by_measure_api = {'Authorization': ''}
    res = requests.get(url=BASE_URL + GET_VOICE_FEATURE_MEASURE_ENDPOINT_INVALID_MEASURE, headers=headers_get_voice_feature_by_measure_api)
    print(res)
    assert res.status_code == 401


def test_get_voice_feature_by_measure_api_extra_content_type_header_is_added():
    headers_get_voice_feature_by_measure_api = {'Authorization': ACCESS_TOKEN, 'Content-Type': CONTENT_TYPE_APPLICATION_JSON}
    res = requests.get(url=BASE_URL + GET_VOICE_FEATURE_MEASURE_ENDPOINT_INVALID_MEASURE, headers=headers_get_voice_feature_by_measure_api)
    print(res)
    assert res.status_code == 404

def test_get_voice_feature_by_measure_api_invalid_measure_name():
    headers_get_voice_feature_by_measure_api = {'Authorization': ACCESS_TOKEN}
    res = requests.get(url=BASE_URL + GET_VOICE_FEATURE_MEASURE_ENDPOINT_INVALID_MEASURE, headers=headers_get_voice_feature_by_measure_api)
    print(res)
    assert res.status_code == 404


def test_get_voice_feature_by_measure_api_no_access_to_measure():
    headers_get_voice_feature_by_measure_api = {'Authorization': ACCESS_TOKEN}
    res = requests.get(url=BASE_URL + '/measures/name/'+FEATURE_BY_MEASURE_NAME_NO_ACCESS +'/voice-features', headers=headers_get_voice_feature_by_measure_api)
    print(res)
    assert res.status_code == 403


def test_get_voice_feature_by_measure_api_measure_name_is_blank():
    headers_get_voice_feature_by_measure_api = {'Authorization': ACCESS_TOKEN}
    res = requests.get(url=BASE_URL + GET_VOICE_FEATURE_MEASURE_ENDPOINT_BLANK_MEASURE_NAME, headers=headers_get_voice_feature_by_measure_api)
    print(res)
    assert res.status_code == 404


def test_get_voice_feature_by_measure_api_measure_name_is_missing():
    headers_get_voice_feature_by_measure_api = {'Authorization': ACCESS_TOKEN}
    res = requests.get(url=BASE_URL + GET_VOICE_FEATURE_MEASURE_ENDPOINT_MEASURE_NAME_IS_MISSING, headers=headers_get_voice_feature_by_measure_api)
    print(res)
    assert res.status_code == 404


def test_get_voice_feature_by_measure_api_measure_name_is_integer():
    headers_get_voice_feature_by_measure_api = {'Authorization': ACCESS_TOKEN}
    res = requests.get(url=BASE_URL + GET_VOICE_FEATURE_MEASURE_ENDPOINT_MEASURE_NAME_IS_INTEGER, headers=headers_get_voice_feature_by_measure_api)
    print(res)
    assert res.status_code == 404


def test_get_async_score_api():
    status, get_score_json =  API_Calls.get_async_score_api(ASYNC_URL,ACCESS_TOKEN,JOB_ID)
    print(JOB_ID)
    print (status,get_score_json)
    assert status == 200
    assertion.assert_valid_schema(get_score_json, 'score_3.0_reponse.json')
    #VOICE_FEATURE_SCORE_ID = get_score_json['result']['id']
    #print(VOICE_FEATURE_SCORE_ID)



def test_get_async_score_api_with_access_token_bearer_in_small_case():
    ACCESS_TOKEN_BEARER1 = 'bearer ' + ACCESS_TOKEN
    print(ACCESS_TOKEN_BEARER1)
    status, get_score_json =  API_Calls.get_async_score_api(ASYNC_URL,ACCESS_TOKEN_BEARER1,JOB_ID)
    print(JOB_ID)
    print (status,get_score_json)
    assert status == 401
    assertion.assert_valid_schema(get_score_json, 'score_3.0_reponse.json')
    #VOICE_FEATURE_SCORE_ID = get_score_json['result']['id']
    #print(VOICE_FEATURE_SCORE_ID)


time.sleep(50)
# #--------get async voice feature score API-----------#

status, response_json = API_Calls.get_async_score_api(ASYNC_URL,ACCESS_TOKEN,JOB_ID)
print(status, response_json)
VOICE_FEATURE_SCORE_ID = response_json['result']['id']
print(id)

#------ 31-05-2021 -----#
# GET /inference/voice-feature-scores/{voiceFeatureScoreID} #


#--- positive case ---

time.sleep(10)
def test_get_score_by_voice_feature_score_id_api():
    status, get_score_json =  API_Calls.get_score_by_voice_feature_score_id_api(BASE_URL,ACCESS_TOKEN,VOICE_FEATURE_SCORE_ID)
    print(VOICE_FEATURE_SCORE_ID)
    print (status,get_score_json)
    assert status == 200
    assertion.assert_valid_schema(get_score_json, 'get_score_by_voice_feature_json.json')


#--- negative cases ---

def test_get_score_by_voice_feature_score_id_api_post_request(input_url2,get_token):
    headers_get_score_api = {'Authorization': get_token}
    res = requests.post(url=input_url2 + VOICE_FEATURE_SCORE_ENDPOINT + '/' + VOICE_FEATURE_SCORE_ID,headers=headers_get_score_api)
    print(res)
    assert res.status_code == 403


def test_get_score_by_voice_feature_score_id_api_delete_request(input_url2,get_token):
    headers_get_score_api = {'Authorization': get_token}
    res = requests.delete(url=input_url2 + VOICE_FEATURE_SCORE_ENDPOINT + '/' + VOICE_FEATURE_SCORE_ID,headers=headers_get_score_api)
    print(res)
    assert res.status_code == 403

def test_get_score_by_voice_feature_score_id_api_put_request(input_url2,get_token):
    headers_get_score_api = {'Authorization': get_token}
    res = requests.put(url=input_url2 + VOICE_FEATURE_SCORE_ENDPOINT + '/' + VOICE_FEATURE_SCORE_ID,headers=headers_get_score_api)
    print(res)
    assert res.status_code == 403



# #----negative cases---#


def test_get_score_by_voice_feature_score_id_api_invalid_endpoint():
    status, data = API_Calls.get_score_by_voice_feature_score_id_api(BASE_URL, ACCESS_TOKEN, VOICE_FEATURE_SCORE_ID_INVALID)
    print(status, data)
    assert status == 400

def test_get_score_by_voice_feature_score_id_api_invalid_end_point_random_input():
    headers_get_score_api = {'Authorization': ACCESS_TOKEN}
    res = requests.get(url=BASE_URL + '/XYZ', headers=headers_get_score_api)
    print(res)
    assert res.status_code == 403

def test_get_score_by_voice_feature_score_id_api_header_missing():
    res = requests.get(url=BASE_URL + '/inference/voice-feature-scores/'+ VOICE_FEATURE_SCORE_ID)
    print(res)
    assert res.status_code == 401

def test_get_score_by_voice_feature_score_id_api_invalid_access_token():
    status, data = API_Calls.get_score_by_voice_feature_score_id_api(BASE_URL, INCORRECT_ACCESS_TOKEN,VOICE_FEATURE_SCORE_ID)
    print(status, data)
    assert status == 401

def test_get_score_by_voice_feature_score_id_api_access_token_with_bearer_in_small_case():
    ACCESS_TOKEN_BEARER1 = 'bearer ' + ACCESS_TOKEN
    print(ACCESS_TOKEN_BEARER1)
    status, data = API_Calls.get_score_by_voice_feature_score_id_api(BASE_URL, ACCESS_TOKEN_BEARER1,VOICE_FEATURE_SCORE_ID)
    print(status, data)
    assert status == 401


def test_get_score_by_voice_feature_score_id_api_invalid_voice_feature_score_id():
    headers_get_score_api = {'Authorization': ACCESS_TOKEN}
    res = requests.get(url=BASE_URL + VOICE_FEATURE_SCORE_ENDPOINT+ '/'+ VOICE_FEATURE_SCORE_ID_INVALID, headers=headers_get_score_api)
    print(res)
    assert res.status_code == 400


def test_get_score_by_voice_feature_score_id_api_access_token_missing():
    headers_get_score_api = {'Authorization': ''}
    res = requests.get(url=BASE_URL + VOICE_FEATURE_SCORE_ENDPOINT, headers=headers_get_score_api)
    print(res)
    assert res.status_code == 401


def test_get_score_by_voice_feature_score_id_api_extra_content_type_header_is_added():
    headers_get_score_api = {'Authorization': ACCESS_TOKEN, 'Content-Type': CONTENT_TYPE_APPLICATION_JSON}
    res = requests.get(url=BASE_URL + VOICE_FEATURE_SCORE_ENDPOINT+'/'+VOICE_FEATURE_SCORE_ID, headers=headers_get_score_api)
    print(res)
    assert res.status_code == 400

def test_get_score_by_voice_feature_score_id_api_voice_feature_score_id_blank():
    headers_get_score_api = {'Authorization': ACCESS_TOKEN}
    res = requests.get(url=BASE_URL + VOICE_FEATURE_SCORE_ENDPOINT + '/' +'" "', headers=headers_get_score_api)
    print (BASE_URL+VOICE_FEATURE_SCORE_ENDPOINT+'/'+VOICE_FEATURE_SCORE_ID_BLANK)
    print(res)
    assert res.status_code == 400

# def test_get_score_by_voice_feature_score_id_api_voice_feature_score_id_blank():
#     headers_get_score_api = {'Authorization': ACCESS_TOKEN}
#     res = requests.get(url=BASE_URL + VOICE_FEATURE_SCORE_ENDPOINT + '/' +VOICE_FEATURE_SCORE_ID_BLANK, headers=headers_get_score_api)
#     print (BASE_URL+VOICE_FEATURE_SCORE_ENDPOINT+'/'+VOICE_FEATURE_SCORE_ID_BLANK)
#     print(res)
#     assert res.status_code == 400

def test_get_score_by_voice_feature_score_id_api_voice_feature_score_id_as_integer():
    headers_get_score_api = {'Authorization': ACCESS_TOKEN}
    res = requests.get(url=BASE_URL + VOICE_FEATURE_SCORE_ENDPOINT +'/'+VOICE_FEATURE_SCORE_ID_AS_INTEGER, headers=headers_get_score_api)
    print(res)
    assert res.status_code == 400


def test_get_score_by_voice_feature_score_id_api_no_access_to_voice_feature_score_id():
    headers_get_score_api = {'Authorization': ACCESS_TOKEN}
    res = requests.get(url=BASE_URL + VOICE_FEATURE_SCORE_ENDPOINT + '/' + VOICE_FEATURE_SCORE_ID_NO_ACCESS, headers=headers_get_score_api)
    print(res)
    assert res.status_code == 403



# GET /inference/voice-feature-scores #

#--- positive cases ---#


def test_get_voice_feature_scores_api():
    status, get_score_json =  API_Calls.get_voice_feature_scores_api(BASE_URL,ACCESS_TOKEN)
    print (status,get_score_json)
    assert status == 200
    assertion.assert_valid_schema(get_score_json, 'get_voice_feature_scores.json')


def test_get_voice_feature_scores_api():
    ACCESS_TOKEN_BEARER = 'Bearer ' + ACCESS_TOKEN
    print(ACCESS_TOKEN_BEARER)
    status, get_score_json =  API_Calls.get_voice_feature_scores_api(BASE_URL,ACCESS_TOKEN_BEARER)
    print (status,get_score_json)
    assert status == 200
    assertion.assert_valid_schema(get_score_json, 'get_voice_feature_scores.json')

#Working below case through manual
# def test_get_voice_feature_scores_api_all_params():
#     parameters = {'pageIndex':0, 'from': FROM_TIME_ALL, 'to': TO_TIME_ALL, 'userIdentifier': SUB_IDENTIFIER_A}
#     status, get_score_json = API_Calls.get_voice_feature_scores_api_all_params(BASE_URL, ACCESS_TOKEN,SUB_IDENTIFIER)
#     print(status, get_score_json)
#     assert status == 200
#     assertion.assert_valid_schema(get_score_json, 'get_voice_feature_scores.json')


def test_get_voice_feature_scores_api_page_index():
    status, get_score_json = API_Calls.get_voice_feature_scores_api_page_index(BASE_URL, ACCESS_TOKEN)
    print(status, get_score_json)
    assert status == 200
    assertion.assert_valid_schema(get_score_json, 'get_voice_feature_scores.json')

def test_get_voice_feature_scores_api_page_index_access_token_with_bearer():
    ACCESS_TOKEN_BEARER = 'Bearer ' + ACCESS_TOKEN
    print(ACCESS_TOKEN_BEARER)
    status, get_score_json = API_Calls.get_voice_feature_scores_api_page_index(BASE_URL, ACCESS_TOKEN_BEARER)
    print(status, get_score_json)
    assert status == 200
    assertion.assert_valid_schema(get_score_json, 'get_voice_feature_scores.json')


def test_get_voice_feature_scores_api_sub_identifier():
    status, get_score_json = API_Calls.get_voice_feature_scores_api_sub_identifier(BASE_URL, ACCESS_TOKEN,SUB_IDENTIFIER)
    print(status, get_score_json)
    assert status == 200
    assertion.assert_valid_schema(get_score_json, 'get_voice_feature_scores.json')


def test_get_voice_feature_scores_api_sub_identifier_access_token_with_bearer():
    ACCESS_TOKEN_BEARER = 'Bearer ' + ACCESS_TOKEN
    print(ACCESS_TOKEN_BEARER)
    status, get_score_json = API_Calls.get_voice_feature_scores_api_sub_identifier(BASE_URL, ACCESS_TOKEN_BEARER,SUB_IDENTIFIER)
    print(status, get_score_json)
    assert status == 200
    assertion.assert_valid_schema(get_score_json, 'get_voice_feature_scores.json')



def test_get_voice_feature_scores_api_duration():
    status, get_score_json = API_Calls.get_voice_feature_scores_api_duration(BASE_URL, ACCESS_TOKEN)
    print(status, get_score_json)
    assert status == 200
    assertion.assert_valid_schema(get_score_json, 'get_voice_feature_scores.json')

def test_get_voice_feature_scores_api_duration_access_token_with_bearer():
    ACCESS_TOKEN_BEARER = 'Bearer ' + ACCESS_TOKEN
    print(ACCESS_TOKEN_BEARER)
    status, get_score_json = API_Calls.get_voice_feature_scores_api_duration(BASE_URL, ACCESS_TOKEN_BEARER)
    print(status, get_score_json)
    assert status == 200
    assertion.assert_valid_schema(get_score_json, 'get_voice_feature_scores.json')


def test_get_voice_feature_scores_api_pageIndex_duration():
    status, get_score_json = API_Calls.get_voice_feature_scores_api_pageIndex_duration(BASE_URL, ACCESS_TOKEN)
    print(status, get_score_json)
    assert status == 200
    assertion.assert_valid_schema(get_score_json, 'get_voice_feature_scores.json')


def test_get_voice_feature_scores_api_pageIndex_subIdentifier():
    status, get_score_json = API_Calls.get_voice_feature_scores_api_pageIndex_subIdentifier(BASE_URL, ACCESS_TOKEN,SUB_IDENTIFIER)
    print(status, get_score_json)
    assert status == 200
    assertion.assert_valid_schema(get_score_json, 'get_voice_feature_scores.json')


def test_get_voice_feature_scores_api_duration_subIdentifier():
    status, get_score_json = API_Calls.get_voice_feature_scores_api_duration_subIdentifier(BASE_URL, ACCESS_TOKEN,SUB_IDENTIFIER)
    print(status, get_score_json)
    assert status == 200
    assertion.assert_valid_schema(get_score_json, 'get_voice_feature_scores.json')


def test_get_voice_feature_scores_api_sub_identifier_no_data_present():
    status, get_score_json = API_Calls.get_voice_feature_scores_api_sub_identifier(BASE_URL, ACCESS_TOKEN,SUB_IDENTIFIER_NO_DATA)
    print(status, get_score_json)
    assert status == 422
    assertion.assert_valid_schema(get_score_json, 'get_voice_feature_scores.json')


def test_get_voice_feature_scores_api_multiple_subject_identifier(input_url2,get_token):
    headers_get_score_api = {'Authorization': get_token}
    parameters = {'userIdentifier': SUB_IDENTIFIER_VALID1,'userIdentifier': SUB_IDENTIFIER_VALID2}
    res = requests.get(url=BASE_URL + '/inference/voice-feature-scores', headers=headers_get_score_api,params=parameters)
    print(res)
    assert res.status_code == 200

def test_get_voice_feature_scores_api_multiple_pageIndex(input_url2,get_token):
    headers_get_score_api = {'Authorization': get_token}
    parameters = {'pageIndex': 0,'pageIndex':1}
    res = requests.get(url=BASE_URL + '/inference/voice-feature-scores', headers=headers_get_score_api,params=parameters)
    print(res)
    assert res.status_code == 200


def test_get_voice_feature_scores_api_when_no_data_present_for_duration(input_url2,get_token):
    headers_get_score_api = {'Authorization': get_token}
    parameters = {'from': FROM_TIME_NO_DATA,'to': TO_TIME_NO_DATA}
    res = requests.get(url=BASE_URL + '/inference/voice-feature-scores', headers=headers_get_score_api,params=parameters)
    print(res)
    assert res.status_code == 200

def test_get_voice_feature_scores_api_when_to_param_is_before_than_from(input_url2,get_token):
    headers_get_score_api = {'Authorization': get_token}
    parameters = {'to': TO_TIME_ALL,'from': FROM_TIME_ALL}
    res = requests.get(url=BASE_URL + '/inference/voice-feature-scores', headers=headers_get_score_api,params=parameters)
    print(res)
    assert res.status_code == 200

#--- negative cases ---

def test_get_voice_feature_scores_api_post_request(input_url2,get_token):
    headers_get_score_api = {'Authorization': get_token}
    res = requests.post(url=input_url2 + '/inference/voice-feature-scores', headers=headers_get_score_api)
    print(res)
    assert res.status_code == 403

def test_get_voice_feature_scores_api_put_request(input_url2,get_token):
    headers_get_score_api = {'Authorization': get_token}
    res = requests.put(url=input_url2 + '/inference/voice-feature-scores', headers=headers_get_score_api)
    print(res)
    assert res.status_code == 403

def test_get_voice_feature_scores_api_delete_request(input_url2,get_token):
    headers_get_score_api = {'Authorization': get_token}
    res = requests.delete(url=input_url2 + '/inference/voice-feature-scores', headers=headers_get_score_api)
    print(res)
    assert res.status_code == 403


# #----negative cases---#


def test_get_voice_feature_scores_api_invalid_endpoint():
    headers_get_score_api = {'Authorization': ACCESS_TOKEN}
    res = requests.get(url=BASE_URL +'/'+VOICE_FEATURE_SCORE_ENDPOINT_INVALID, headers=headers_get_score_api)
    print(res)
    assert res.status_code == 403

def test_get_voice_feature_scores_api_invalid_endpoint_random_input():
    headers_get_score_api = {'Authorization': ACCESS_TOKEN}
    res = requests.get(url=BASE_URL + '/XYZ', headers=headers_get_score_api)
    print(res)
    assert res.status_code == 403

def test_get_voice_feature_scores_api_header_missing():
    res = requests.get(url=BASE_URL + '/inference/voice-feature-scores')
    print(res)
    assert res.status_code == 401

def test_get_voice_feature_scores_api_invalid_access_token():
    status, data = API_Calls.get_voice_feature_scores_api(BASE_URL, INCORRECT_ACCESS_TOKEN)
    print(status, data)
    assert status == 401

def test_get_voice_feature_scores_api_access_token_with_bearer_in_small_case():
    ACCESS_TOKEN_BEARER1 = 'bearer ' + ACCESS_TOKEN
    print(ACCESS_TOKEN_BEARER1)
    status, data = API_Calls.get_voice_feature_scores_api(BASE_URL, ACCESS_TOKEN_BEARER1)
    print(status, data)
    assert status == 401


def test_get_voice_feature_scores_api_content_type_header_is_added():
    headers_get_score_api = {'Authorization': ACCESS_TOKEN,'Content-Type': CONTENT_TYPE_APPLICATION_JSON}
    res = requests.get(url=BASE_URL + '/inference/voice-feature-scores',headers=headers_get_score_api)
    print(res)
    assert status == 415

#---- pageIndex param validation negative cases  ---- #


def test_get_voice_feature_scores_api_page_index_out_of_bound(input_url2,get_token):
    headers_get_score_api = {'Authorization': get_token}
    parameters = {'pageIndex': 100}
    res = requests.get(url=input_url2 + '/inference/voice-feature-scores', headers=headers_get_score_api,params=parameters)
    print(res)
    assert res.status_code == 422


def test_get_voice_feature_scores_api_page_index_missing(input_url2,get_token):
    headers_get_score_api = {'Authorization': ACCESS_TOKEN}
    parameters = {'pageIndex': ''}
    res = requests.get(url=input_url2 + '/inference/voice-feature-scores', headers=headers_get_score_api,params=parameters)
    print(res)
    assert res.status_code == 400

def test_get_voice_feature_scores_api_page_index_param_typo(input_url2,get_token):
    headers_get_score_api = {'Authorization': get_token}
    parameters = {'pageInndex': 1}
    res = requests.get(url=input_url2 + '/inference/voice-feature-scores', headers=headers_get_score_api,params=parameters)
    print(res)
    assert res.status_code == 400


def test_get_voice_feature_scores_api_page_index_invalid_data(input_url2,get_token):
    headers_get_score_api = {'Authorization': ACCESS_TOKEN}
    parameters = {'pageIndex': 'A'}
    res = requests.get(url=input_url2 + '/inference/voice-feature-scores', headers=headers_get_score_api,params=parameters)
    print(res)
    assert res.status_code == 400


#---- Duration param validation negative cases  ---- #

def test_get_voice_feature_scores_api_from_param_missing(input_url2,get_token):
    headers_get_score_api = {'Authorization': get_token}
    parameters = {'to': TO_TIME_ALL}
    res = requests.get(url=input_url2 + '/inference/voice-feature-scores', headers=headers_get_score_api,params=parameters)
    print(res)
    assert res.status_code == 400

def test_get_voice_feature_scores_api_from_value_missing(input_url2,get_token):
    headers_get_score_api = {'Authorization': get_token}
    parameters = {'from':'','to': TO_TIME_ALL}
    res = requests.get(url=input_url2 + '/inference/voice-feature-scores', headers=headers_get_score_api,params=parameters)
    print(res)
    assert res.status_code == 400

def test_get_voice_feature_scores_api_from_param_has_typos(input_url2,get_token):
    headers_get_score_api = {'Authorization': get_token}
    parameters = {'froom':FROM_TIME_ALL,'to': TO_TIME_ALL}
    res = requests.get(url=input_url2 + '/inference/voice-feature-scores', headers=headers_get_score_api,params=parameters)
    print(res)
    assert res.status_code == 400


def test_get_voice_feature_scores_api_from_greater_than_to(input_url2,get_token):
    headers_get_score_api = {'Authorization': get_token}
    parameters = {'from':TO_TIME_ALL,'to': FROM_TIME_ALL}
    res = requests.get(url=input_url2 + '/inference/voice-feature-scores', headers=headers_get_score_api,params=parameters)
    print(res)
    assert res.status_code == 400


def test_get_voice_feature_scores_api_from_has_incorrect_date_format(input_url2,get_token):
    headers_get_score_api = {'Authorization': get_token}
    parameters = {'from':FROM_TIME_ALL_INCORRECT_DATE_FORMAT,'to': TO_TIME_ALL}
    res = requests.get(url=input_url2 + '/inference/voice-feature-scores', headers=headers_get_score_api,params=parameters)
    print(res)
    assert res.status_code == 400


def test_get_voice_feature_scores_api_from_and_to_has_incorrect_date_format(input_url2,get_token):
    headers_get_score_api = {'Authorization': get_token}
    parameters = {'from':FROM_TIME_ALL_INCORRECT_DATE_FORMAT,'to': TO_TIME_ALL_INCORRECT_DATE_FORMAT}
    res = requests.get(url=input_url2 + '/inference/voice-feature-scores', headers=headers_get_score_api,params=parameters)
    print(res)
    assert res.status_code == 400


def test_get_voice_feature_scores_api_to_has_incorrect_date_format(input_url2,get_token):
    headers_get_score_api = {'Authorization': get_token}
    parameters = {'from':FROM_TIME_ALL ,'to': TO_TIME_ALL_INCORRECT_DATE_FORMAT}
    res = requests.get(url=input_url2 + '/inference/voice-feature-scores', headers=headers_get_score_api,params=parameters)
    print(res)
    assert res.status_code == 400


def test_get_voice_feature_scores_api_to_param_missing(input_url2,get_token):
    headers_get_score_api = {'Authorization': get_token}
    parameters = {'from': FROM_TIME_ALL}
    res = requests.get(url=input_url2 + '/inference/voice-feature-scores', headers=headers_get_score_api,params=parameters)
    print(res)
    assert res.status_code == 400

def test_get_voice_feature_scores_api_to_value_missing(input_url2,get_token):
    headers_get_score_api = {'Authorization': get_token}
    parameters = {'from':FROM_TIME_ALL,'to': ''}
    res = requests.get(url=input_url2 + '/inference/voice-feature-scores', headers=headers_get_score_api,params=parameters)
    print(res)
    assert res.status_code == 400

def test_get_voice_feature_scores_api_to_param_has_typos(input_url2,get_token):
    headers_get_score_api = {'Authorization': get_token}
    parameters = {'froom':FROM_TIME_ALL,'t0o': TO_TIME_ALL}
    res = requests.get(url=input_url2 + '/inference/voice-feature-scores', headers=headers_get_score_api,params=parameters)
    print(res)
    assert res.status_code == 400


def test_get_voice_feature_scores_api_from_to_valid_pageIndex_invalid(input_url2,get_token):
    headers_get_score_api = {'Authorization': get_token}
    parameters = {'from': FROM_TIME_ALL,'to': TO_TIME_ALL,'pageIndex':3}
    res = requests.get(url=input_url2 + '/inference/voice-feature-scores', headers=headers_get_score_api,params=parameters)
    print(res)
    assert res.status_code == 422


def test_get_voice_feature_scores_api_from_to_valid_subjectIdentifier_invalid(input_url2,get_token):
    headers_get_score_api = {'Authorization': get_token}
    parameters = {'from': FROM_TIME_ALL,'to': TO_TIME_ALL,'userIdentifier':SUB_IDENTIFIER_INVALID}
    res = requests.get(url=input_url2 + '/inference/voice-feature-scores', headers=headers_get_score_api,params=parameters)
    print(res)
    assert res.status_code == 422


#---- userIdentifier param validation negative cases  ---- #

def test_get_voice_feature_scores_api_userIdentifier_identifier_missing(input_url2,get_token):
    headers_get_score_api = {'Authorization': get_token}
    parameters = {'userIdentifier':''}
    res = requests.get(url=BASE_URL + '/inference/voice-feature-scores', headers=headers_get_score_api,params=parameters)
    print(res)
    assert res.status_code == 400

def test_get_voice_feature_scores_api_userIdentifier_param_has_typos(input_url2,get_token):
    headers_get_score_api = {'Authorization': get_token}
    parameters = {'userIdentiffier': SUB_IDENTIFIER_VALID1 }
    res = requests.get(url=input_url2 + '/inference/voice-feature-scores', headers=headers_get_score_api,params=parameters)
    print(res)
    assert res.status_code == 400

def test_get_voice_feature_scores_api_userIdentifier_value_invalid(input_url2,get_token):
    headers_get_score_api = {'Authorization': get_token}
    parameters = {'userIdentifier': SUB_IDENTIFIER_INVALID}
    res = requests.get(url=input_url2 + '/inference/voice-feature-scores', headers=headers_get_score_api,params=parameters)
    print(res)
    assert res.status_code == 422

#Verified below case manually
# def test_get_voice_feature_scores_api_one_userIdentifier_value_invalid_and_another_one_is_valid(input_url2,get_token):
#     headers_get_score_api = {'Authorization': get_token}
#     parameters = {'userIdentifier': 'abcd','userIdentifier' : SUB_IDENTIFIER_VALID1}
#     res = requests.get(url=input_url2 + '/inference/voice-feature-scores', headers=headers_get_score_api,params=parameters)
#     print(res)
#     assert res.status_code == 422


