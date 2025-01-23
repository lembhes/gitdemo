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
BASE_TOKEN = 'Basic ' + base64secrets
print(base64secrets)

# ---------------- Get the Base64 No access --------------------------------#

base64secrets = helper.get_base64secrets(CLIENT_ID_NOACCESS_TRANSCRIPTION, CLIENT_SECRET_NOACCESS_TRANSCRIPTION)
BASE_TOKEN_NO_ACCESS = 'Basic ' + base64secrets
print(base64secrets)

# ----------- Get the ACCESS TOKEN ----------------------------#

status_code, json_data = API_Calls.token_api(BASE_URL, VALID_TOKEN_DATA, BASE_TOKEN, CONTENT_TYPE_URL_ENCODED)
ACCESS_TOKEN = json_data['access_token']
print(ACCESS_TOKEN)

# ----------- Get the ACCESS TOKEN no Access ----------------------------#

status_code, json_data = API_Calls.token_api(BASE_URL, VALID_TOKEN_DATA, BASE_TOKEN, CONTENT_TYPE_URL_ENCODED)
ACCESS_TOKEN_NOACCESS_FOR_TRANSCRIPTION = json_data['access_token']
print(ACCESS_TOKEN_NOACCESS_FOR_TRANSCRIPTION)

# ---------------- GET SUBJECT IDENTIFIER -------------------------------#

status, subject_json = API_Calls.subject_api(BASE_URL, VALID_SUBJECT_DATA, ACCESS_TOKEN,
                                             CONTENT_TYPE_APPLICATION_JSON)

SUB_IDENTIFIER = subject_json['userIdentifier']

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
FILE_PATH_ENCODED = helper.urlEncoder(FILE_PATH)
print(FILE_PATH_ENCODED)

# ____________________UPLOAD THE AUDIO SAMPLE  ____________________________________________#


#AUDIO_FILE_PATH = 'C:\\Users\\GS-1329\\Downloads\\30sec.wav'

AUDIO_FILE_PATH = 'C:\\Users\\GS-1431\\Downloads\\shrutiD_audio_30sec.wav'

status_code = API_Calls.upload_sample_file(STORAGE_SIGNED_URL, AUDIO_FILE_PATH)



#----- post request body ----#

ASYNC_TRANSCRIPTION_API_DATA ={
    "filePath": FILE_PATH
}
INVALID_ASYNC_TRANSCRIPTION_API_DATA ={
    "filePathh": FILE_PATH
}

ASYNC_TRANSCRIPTION_API_DATA_EXTRA_KEY = {
"filePath": FILE_PATH,
 "Test" : "ABC"
}


#---------- post transcriptions API to get job Id  ----------

# status, response_json = API_Calls.post_async_transcriptions_api(ASYNC_URL, ASYNC_TRANSCRIPTION_API_DATA, ACCESS_TOKEN,CONTENT_TYPE_APPLICATION_JSON)
# print(status, response_json, "trace_score_out")
# ASYNC_JOB_ID =response_json['jobId']
# print (ASYNC_JOB_ID)

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
   input = ASYNC_TRANSCRIPTION_API_DATA
   return input

@pytest.fixture
def get_header():
   content_type = CONTENT_TYPE_APPLICATION_JSON
   return content_type


@pytest.fixture
def get_async_endpoint():
   get_end_point = '/transcriptions/'
   return get_end_point

@pytest.fixture()
def get_job_id():
    status, transcriptions_json_data = API_Calls.post_async_transcriptions_api(ASYNC_URL, ASYNC_TRANSCRIPTION_API_DATA,
                                                                               ACCESS_TOKEN,
                                                                               CONTENT_TYPE_APPLICATION_JSON)
    print(status, transcriptions_json_data)
    ASYNC_JOB_ID=transcriptions_json_data['jobId']
    return  ASYNC_JOB_ID

# ----------------------TEST CASES Positive ---------------------------------------#

def test_post_async_transcriptions_api():
    status, transcriptions_json_data = API_Calls.post_async_transcriptions_api(ASYNC_URL, ASYNC_TRANSCRIPTION_API_DATA,ACCESS_TOKEN,  CONTENT_TYPE_APPLICATION_JSON)
    print(status, transcriptions_json_data)
    assert status == 202
    assertion.assert_valid_schema(transcriptions_json_data, 'post_transcription.json')


time.sleep(10)
def test_post_async_transcriptions_api_secondtime():
    status, transcriptions_json_data = API_Calls.post_async_transcriptions_api(ASYNC_URL, ASYNC_TRANSCRIPTION_API_DATA, ACCESS_TOKEN,                                                                    CONTENT_TYPE_APPLICATION_JSON)
    print(status, transcriptions_json_data)
    assert status == 200
    assertion.assert_valid_schema(transcriptions_json_data, 'post_transcription.json')


time.sleep(30)
def test_get_async_transcription_api():
    status, get_score_json =  API_Calls.get_async_transcription_api(ASYNC_URL,ACCESS_TOKEN,str(get_job_id))
    print(status, get_score_json)
    assert status_code == 200
    assertion.assert_valid_schema(get_score_json, 'get_transcription.json')


###########  transcript update changes as below  ###########
def test_get_audio_file_transcription():
    status, response = API_Calls.get_audio_file_transcription(BASE_URL, FILE_PATH_ENCODED_SAVED, ACCESS_TOKEN)
    print(FILE_PATH_ENCODED_SAVED)
    print(status, response)
    assert status == 200
    assertion.assert_valid_schema(response, 'get_audio_file_transcription.json')


# def test_get_transcriptions_without_file_path():
#     status, response = API_Calls.get_transcriptions(BASE_URL,ACCESS_TOKEN)
#     # print(API_Calls.get_audio_file_transcription(BASE_URL, FILE_PATH_ENCODED_SAVED, ACCESS_TOKEN))
#     print(FILE_PATH_ENCODED_SAVED)
#     print(status, response)
#     assert status == 200
#     assertion.assert_valid_schema(response, 'get_transcriptions.json')

def test_get_transcriptions_with_single_file_path():
    status, response = API_Calls.get_transcriptions(BASE_URL,ACCESS_TOKEN)
    print(FILE_PATH_ENCODED_SAVED)
    print(status, response)
    assert status == 200
    assertion.assert_valid_schema(response, 'get_transcriptions.json')



#filePathlist = ['s3%3A%2F%2Fqa-sondeplatformlive-us-subject-metadata%2Fff1c04e0-0bb6-4861-ab6d-faf857e44f90%2Fvoice-samples%2F905ab7c6-fd3d-4209-9c21-90f8bbe1915d.wav','s3%3A%2F%2Fqa-sondeplatformlive-us-subject-metadata%2Fff1c04e0-0bb6-4861-ab6d-faf857e44f90%2Fvoice-samples%2Fddb577dd-15d2-41d0-a137-db77bedb1c12.wav']

filePathlist1 = ['s3%3A%2F%2Fqa-sondeplatformlive-us-subject-metadata%2Fff1c04e0-0bb6-4861-ab6d-faf857e44f90%2Fvoice-samples%2F6f4ab68a-c6fa-4af2-88dc-2f71d7e71f21.wav','s3%3A%2F%2Fqa-sondeplatformlive-us-subject-metadata%2Fff1c04e0-0bb6-4861-ab6d-faf857e44f90%2Fvoice-samples%2F4c39d1a1-bb97-4820-afc2-281f48fbb645.wav','s3%3A%2F%2Fqa-sondeplatformlive-us-subject-metadata%2Fff1c04e0-0bb6-4861-ab6d-faf857e44f90%2Fvoice-samples%2F905ab7c6-fd3d-4209-9c21-90f8bbe1915d.wav','s3%3A%2F%2Fqa-sondeplatformlive-us-subject-metadata%2Fff1c04e0-0bb6-4861-ab6d-faf857e44f90%2Fvoice-samples%2Fddb577dd-15d2-41d0-a137-db77bedb1c12.wav']

#filePaths = 's3%3A%2F%2Fqa-sondeplatformlive-us-subject-metadata%2Fff1c04e0-0bb6-4861-ab6d-faf857e44f90%2Fvoice-samples%2F6f4ab68a-c6fa-4af2-88dc-2f71d7e71f21.wav,s3%3A%2F%2Fqa-sondeplatformlive-us-subject-metadata%2Fff1c04e0-0bb6-4861-ab6d-faf857e44f90%2Fvoice-samples%2F4c39d1a1-bb97-4820-afc2-281f48fbb645.wav,s3%3A%2F%2Fqa-sondeplatformlive-us-subject-metadata%2Fff1c04e0-0bb6-4861-ab6d-faf857e44f90%2Fvoice-samples%2F905ab7c6-fd3d-4209-9c21-90f8bbe1915d.wav,s3%3A%2F%2Fqa-sondeplatformlive-us-subject-metadata%2Fff1c04e0-0bb6-4861-ab6d-faf857e44f90%2Fvoice-samples%2Fddb577dd-15d2-41d0-a137-db77bedb1c12.wav'
comma_separated_params = []
for file_path in filePathlist1:
    #encoded_file_path = encode_file_path(file_path)
    comma_separated_params.append(file_path)
file_paths = ','.join(comma_separated_params)
params = {'filePath' : file_paths}
#print(file_paths)



def test_get_transcriptions_with_multiple_file_paths():
    #headers = {'Authorization': ACCESS_TOKEN}
    parameters ={'filePath' : file_paths}
    status, response = API_Calls.get_transcriptions(BASE_URL, ACCESS_TOKEN)
    assert status==200
    assertion.assert_valid_schema(response,'get_transcriptions.json')

#--------------------POST Transcription Negative TC ---------------------------------------#

# POST -> No request body
def test_post_async_transcriptions_api_when_request_contains_no_body():
    status, score_json_data = API_Calls.post_async_transcriptions_api(ASYNC_URL, ASYNC_TRANSCRIPTION_NO_DATA_REQUEST ,ACCESS_TOKEN, CONTENT_TYPE_APPLICATION_JSON)
    print(status, score_json_data)
    assert status == 400

# POST -> Invalid end point
def test_post_async_transcriptions_api_invalid_end_point():
    headers1 = {'Authorization': ACCESS_TOKEN, 'Content-Type': CONTENT_TYPE_APPLICATION_JSON}
    INVALID_END_POINT = '/XYZ'
    res = requests.post(url=ASYNC_URL + INVALID_END_POINT, data=json.dumps(ASYNC_TRANSCRIPTION_API_DATA), headers=headers1)
    print(res)
    assert res.status_code == 403

# POST -> Incorrect access token
def test_post_async_transcriptions_api_incorrect_ACCESS_TOKEN():
    INCORRECT_ACCESS_TOKEN = 'xyz'
    status, data = API_Calls.post_async_transcriptions_api(ASYNC_URL, ASYNC_TRANSCRIPTION_API_DATA, INCORRECT_ACCESS_TOKEN,CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 401

# POST -> Expired access token
def test_post_async_transcriptions_api_expired_access_token():
    status, data = API_Calls.post_async_transcriptions_api(ASYNC_URL, ASYNC_TRANSCRIPTION_API_DATA, EXPIRED_ACCESS_TOKEN,CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 401

# POST -> Missing authorization
def test_post_async_transcriptions_api_missing_authorization():
    headers = {'Content-Type': CONTENT_TYPE_APPLICATION_JSON}
    res = requests.post(url=ASYNC_URL + TRANSCRIPTION_ENDPOINT, data=json.dumps(ASYNC_TRANSCRIPTION_API_DATA), headers=headers)
    print(res)
    assert res.status_code == 401

# POST -> Missing authorization key value
def test_post_async_transcriptions_api_blank_auth_key():
    headers = {'Authorization': '', 'Content-Type': CONTENT_TYPE_APPLICATION_JSON}
    res = requests.post(url=ASYNC_URL + TRANSCRIPTION_ENDPOINT, data=json.dumps(ASYNC_TRANSCRIPTION_API_DATA), headers=headers)
    print(res)
    assert res.status_code == 401

# POST -> request body filePath parameter name invalid
def test_post_async_transcriptions_api_request_body_filePath_keyname_invalid():
    status, data = API_Calls.post_async_transcriptions_api(ASYNC_URL, INVALID_ASYNC_TRANSCRIPTION_API_DATA, ACCESS_TOKEN, CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 400

# POST -> request body filePath parameter with incorrect file
def test_post_async_transcriptions_api_request_body_filePath_with_incorrect_file_present():
    D_CP = ASYNC_TRANSCRIPTION_API_DATA.copy()
    DATA = helper.update_dictionary(D_CP, filePath=FILE_PATH_INVALID_FILE_TRANSCRIPTION)
    status, data = API_Calls.post_async_transcriptions_api(ASYNC_URL, DATA, ACCESS_TOKEN,CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 404

# POST -> request body filePath parameter name missing
def test_post_async_transcriptions_api_request_body_filePath_key_missing():
    D_CP = ASYNC_TRANSCRIPTION_API_DATA.copy()
    DATA = helper.delete_key(D_CP, 'filePath')
    status, data = API_Calls.post_async_transcriptions_api(ASYNC_URL, DATA, ACCESS_TOKEN, CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 400

# POST -> request body filePath parameter value not in correct format (.wav)
def test_post_async_transcriptions_request_body_filePath_invalid_data_type():
    D_CP = ASYNC_TRANSCRIPTION_API_DATA.copy()
    DATA = helper.update_dictionary(D_CP, filePath= 11)
    status, data = API_Calls.post_async_transcriptions_api(ASYNC_URL, DATA, ACCESS_TOKEN,CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 400

# POST -> request body filePath parameter value not in correct format not url (123 or abc or abc123)
def test_post_async_transcriptions_api_request_body_filePath_invalid_value():
    D_CP = ASYNC_TRANSCRIPTION_API_DATA.copy()
    DATA = helper.update_dictionary(D_CP, filePath='abc')
    status, data = API_Calls.post_async_transcriptions_api(ASYNC_URL, DATA, ACCESS_TOKEN,CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 400

# POST -> request body filePath parameter value is missing
def test_post_async_transcriptions_api_request_body_filePath_blank():
    D_CP = ASYNC_TRANSCRIPTION_API_DATA.copy()
    DATA = helper.update_dictionary(D_CP, filePath='')
    status, data = API_Calls.post_async_transcriptions_api(ASYNC_URL, DATA, ACCESS_TOKEN,CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 400

# POST -> request body filePath with no audio
def test_post_async_transcriptions_api_request_body_filePath_with_no_audio_file():
    D_CP = ASYNC_TRANSCRIPTION_API_DATA.copy()
    DATA = helper.update_dictionary(D_CP, filePath=VALID_FILE_PATH_MISSING_FILE)
    status, data = API_Calls.post_async_transcriptions_api(ASYNC_URL, DATA, ACCESS_TOKEN,CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 404

# POST -> request body has extra key added
def test_post_async_transcriptions_api_request_extra_key_added():
    D_CP = ASYNC_TRANSCRIPTION_API_DATA.copy()
    DATA = helper.update_dictionary(D_CP, test='XYZ')
    print(DATA)
    status, data = API_Calls.post_async_transcriptions_api(ASYNC_URL, DATA, ACCESS_TOKEN,CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 400

# POST -> request body content-type header missing

def test_post_async_transcriptions_api_content_type_header_missing():
    header1 = {'Authorization': ACCESS_TOKEN}
    res = requests.post(url=ASYNC_URL + TRANSCRIPTION_ENDPOINT, data=json.dumps(ASYNC_TRANSCRIPTION_API_DATA),
                        headers=header1)
    print(res)
    assert res.status_code == 400

# POST -> request body content-type header invalid

def test_post_async_transcriptions_api_contentType_header_value_invalid():
    status, data = API_Calls.post_async_transcriptions_api(ASYNC_URL, ASYNC_SCORE_API_DATA, ACCESS_TOKEN, CONTENT_TYPE_URL_ENCODED)
    print(status, data)
    assert status == 415

# POST -> request body content-type header value is missing
def test_post_async_transcriptions_api_content_type_header_value_missing():
    header1 = {'Authorization': ACCESS_TOKEN, 'Content-Type':''}
    res = requests.post(url=ASYNC_URL + TRANSCRIPTION_ENDPOINT, data=json.dumps(ASYNC_TRANSCRIPTION_API_DATA),
                        headers=header1)
    print(res)
    assert res.status_code == 415

#POST -> Do not have permission to access voice transcriptions feature

def test_post_async_transcriptions_api_party_donot_have_access_to_voice_transcriptions():
    D_CP = ASYNC_TRANSCRIPTION_API_DATA.copy()
    DATA = helper.update_dictionary(D_CP, filePath=NO_ACCESS_TO_FILE_PATH_FOR_TRANSCRIPTION)
    print(DATA)
    status, data = API_Calls.post_async_transcriptions_api(ASYNC_URL, DATA, ACCESS_TOKEN, CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 403

# POST -> Invalid request with GET / PUT / DELETE

def test_post_async_transcriptions_api_put_request(input_url1, input_data,get_token , get_header):
    headers = {'Authorization': get_token, 'Content-Type': get_header}
    res = requests.put(url=input_url1 + TRANSCRIPTION_ENDPOINT, data=json.dumps(input_data),
                        headers=headers)
    print(res)
    assert res.status_code == 403

def test_post_async_transcriptions_api_get_request(input_url1, input_data, get_token, get_header):
    headers = {'Authorization': get_token, 'Content-Type': get_header}
    res = requests.get(url=input_url1 + TRANSCRIPTION_ENDPOINT, data=json.dumps(input_data),
                        headers=headers)
    print(res)
    assert res.status_code == 403

def test_post_async_transcriptions_api_delete_request(input_url1, input_data, get_token, get_header):
    headers = {'Authorization': get_token, 'Content-Type': get_header}
    res = requests.delete(url=input_url1 + TRANSCRIPTION_ENDPOINT, data=json.dumps(input_data),
                        headers=headers)
    print(res)
    assert res.status_code == 403


# --------------------GET Transcription Negative TC ---------------------------------------#

# GET -> Invalid end point

def test_get_async_transcriptions_api_invalid_end_point_random_string_at_last():
    headers_get_transcriptions_api = {'Authorization': ACCESS_TOKEN}
    res = requests.get(url=ASYNC_URL + '/XYZ', headers=headers_get_transcriptions_api)
    print(res)
    assert res.status_code == 403


def test_get_async_transcriptionse_api_header_missing():
    res = requests.get(url=ASYNC_URL + GET_TRANSCRIPTION_ENDPOINT + str(get_job_id))
    print(res)
    assert res.status_code == 401

def test_get_async_transcriptions_api_invalid_access_token():
    status, data = API_Calls.get_async_transcription_api(ASYNC_URL, INCORRECT_ACCESS_TOKEN,str(get_job_id))
    print(status, data)
    assert status == 401


def test_get_async_transcriptions_api_invalid_job_id():
    headers_get_transcriptions_api = {'Authorization': ACCESS_TOKEN}
    res = requests.get(url=ASYNC_URL + INVALID_ASYNC_JOB_ID_GET_TRANSCRIPTION_ENDPOINT, headers=headers_get_transcriptions_api)
    print(res)
    assert res.status_code == 400

def test_get_async_transcriptions_api_invalid_job_id_minor_change():
    headers_get_transcriptions_api = {'Authorization': ACCESS_TOKEN}
    res = requests.get(url=ASYNC_URL + '/transcriptions/' + INVALID_JOB_ID_MINOR_CHANGE, headers=headers_get_transcriptions_api)
    print(res)
    assert res.status_code == 404


def test_get_async_transcriptions_party_has_no_access_to_job_id():
    headers_get_transcriptions_api = {'Authorization': ACCESS_TOKEN}
    res = requests.get(url=ASYNC_URL + '/transcriptions/' + NO_ACCESS_TO_JOB_ID, headers=headers_get_transcriptions_api)
    print(ASYNC_URL + '/transcriptions/' + NO_ACCESS_TO_JOB_ID)
    print(res)
    assert res.status_code == 401

def test_get_async_transcriptions_api_access_token_missing():
    headers_get_transcriptions_api = {'Authorization': ''}
    res = requests.get(url=ASYNC_URL + GET_TRANSCRIPTION_ENDPOINT + str(get_job_id), headers=headers_get_transcriptions_api)
    print(res)
    assert res.status_code == 401


def test_get_async_transcriptions_api_extra_content_type_header_is_added():
    headers_get_transcriptions_api = {'Authorization': ACCESS_TOKEN, 'Content-Type': CONTENT_TYPE_URL_ENCODED}
    res = requests.get(url=ASYNC_URL + GET_TRANSCRIPTION_ENDPOINT + str(get_job_id) , headers=headers_get_transcriptions_api)
    print(res)
    assert res.status_code == 415

def test_get_async_transcriptions_api_job_id_blank():
    headers_get_transcriptions_api = {'Authorization': ACCESS_TOKEN}
    res = requests.get(url=ASYNC_URL + BLANK_JOB_ID_GET_TRANSCRIPTION_ENDPOINT, headers=headers_get_transcriptions_api)
    print (ASYNC_URL+BLANK_JOB_ID_GET_TRANSCRIPTION_ENDPOINT)
    print(res)
    assert res.status_code == 400

def test_get_async_transcriptions_api_job_id_as_integer():
    headers_get_transcriptions_api = {'Authorization': ACCESS_TOKEN}
    res = requests.get(url=ASYNC_URL + '/transcriptions/'+ ASYNC_JOB_ID_AS_INTEGER, headers=headers_get_transcriptions_api)
    print(res)
    assert res.status_code == 400


def test_get_async_transcriptions_api_job_id_missing():
    headers_get_transcriptions_api = {'Authorization': ACCESS_TOKEN}
    res = requests.get(url=ASYNC_URL + MISSING_GET_TRANSCRIPTION_ENDPOINT , headers=headers_get_transcriptions_api)
    print(res)
    assert res.status_code == 403

def test_get_async_transcriptions_api_post_request(input_url1,get_token):
    headers_get_transcriptions_api = {'Authorization': get_token}
    res = requests.post(url=input_url1 + GET_TRANSCRIPTION_ENDPOINT + str(get_job_id),headers=headers_get_transcriptions_api)
    print(res)
    assert res.status_code == 403


def test_get_async_transcriptions_api_put_request(input_url1,get_token):
    headers_get_transcriptions_api = {'Authorization': get_token}
    res = requests.put(url=input_url1 + GET_TRANSCRIPTION_ENDPOINT + str(get_job_id),headers=headers_get_transcriptions_api)
    print(res)
    assert res.status_code == 403

def test_get_async_transcriptions_api_delete_request(input_url1,get_token):
    headers_get_transcriptions_api = {'Authorization': get_token}
    res = requests.delete(url=input_url1 + GET_TRANSCRIPTION_ENDPOINT + str(get_job_id),headers=headers_get_transcriptions_api)
    print(res)
    assert res.status_code == 403

# --------------------GET File Transcription Negative TC ---------------------------------------#

# GET -> Invalid end point
def test_get_audio_file_transcription_api_invalid_end_point():
    headers_get_transcriptions_api = {'Authorization': ACCESS_TOKEN}
    res = requests.get(url=BASE_URL +'/storage/files/'+ FILE_PATH_ENCODED + '/XYZ', headers=headers_get_transcriptions_api)
    print(res)
    assert res.status_code == 403


def test_get_audio_file_transcription_api_header_missing():
    res = requests.get(url=BASE_URL +'/storage/files/'+ FILE_PATH_ENCODED + '/transcriptions')
    print(res)
    assert res.status_code == 401

def test_get_audio_file_transcription_api_invalid_access_token():
    status, data = API_Calls.get_audio_file_transcription(BASE_URL, FILE_PATH_ENCODED,INCORRECT_ACCESS_TOKEN)
    print(status, data)
    assert status == 401


def test_get_audio_file_transcription_api_invalid_filePath():
    headers_get_transcriptions_api = {'Authorization': ACCESS_TOKEN}
    res = requests.get(url=BASE_URL+ INVALID_FILEPATH_STORAGE_TRANSCRIPTION_ENDPOINT, headers=headers_get_transcriptions_api)
    print(res)
    assert res.status_code == 400

def  test_get_audio_file_transcription_api_filePath_key_missing():
    headers_get_transcriptions_api = {'Authorization': ACCESS_TOKEN}
    res = requests.get(url=BASE_URL +'/storage/files/' + '/transcriptions', headers=headers_get_transcriptions_api)
    print(res)
    assert res.status_code == 400

def  test_get_audio_file_transcription_api_filePath_blank():
    headers_get_transcriptions_api = {'Authorization': ACCESS_TOKEN}
    res = requests.get(url=BASE_URL + INVALID_FILEPATH_STORAGE_TRANSCRIPTION_ENDPOINT_BLANK, headers=headers_get_transcriptions_api)
    print(res)
    assert res.status_code == 400

def test_get_audio_file_transcription_api_filePath_with_no_audio_file():
    NO_AUDIO_FILE_PATH_ENCODED_1 = helper.urlEncoder(VALID_FILE_PATH_MISSING_FILE)
    status, data = API_Calls.get_audio_file_transcription(BASE_URL, NO_AUDIO_FILE_PATH_ENCODED_1,ACCESS_TOKEN)
    print(status, data)
    assert status == 404


def  test_get_audio_file_transcription_api_filePath_does_not_have_transcriptions():
    headers_get_transcriptions_api = {'Authorization': ACCESS_TOKEN}
    res = requests.get(url=BASE_URL +'/storage/files/' +TRANSCRIPTION_NOT_FOUND + '/transcriptions', headers=headers_get_transcriptions_api)
    print(res)
    assert res.status_code == 404


def  test_get_audio_file_transcription_api_filePath_donot_have_permission_to_download():
    headers_get_transcriptions_api = {'Authorization': ACCESS_TOKEN}
    res = requests.get(url=BASE_URL +'/storage/files/' +NO_ACCESS_DOWNLOAD_FILE + '/transcriptions', headers=headers_get_transcriptions_api)
    print(res)
    assert res.status_code == 403


def test_get_audio_file_transcription_api_access_token_missing():
    headers_get_transcriptions_api = {'Authorization': ''}
    res = requests.get(url=BASE_URL +'/storage/files/'+ FILE_PATH_ENCODED + '/transcriptions', headers=headers_get_transcriptions_api)
    print(res)
    assert res.status_code == 401


def test_get_audio_file_transcription_api_extra_content_type_header_is_added():
    headers_get_transcriptions_api = {'Authorization': ACCESS_TOKEN, 'Content-Type': CONTENT_TYPE_URL_ENCODED}
    res = requests.get(url=BASE_URL +'/storage/files/'+ FILE_PATH_ENCODED + '/transcriptions' , headers=headers_get_transcriptions_api)
    print(res)
    assert res.status_code == 415

def test_get_audio_file_transcription_api_post_request(input_url2,get_token):
    headers_get_transcriptions_api = {'Authorization': get_token}
    res = requests.post(url=input_url2 +'/storage/files/'+ FILE_PATH_ENCODED + '/transcriptions',headers=headers_get_transcriptions_api)
    print(res)
    assert res.status_code == 403


def test_get_audio_file_transcription_api_put_request(input_url2,get_token):
    headers_get_transcriptions_api = {'Authorization': get_token}
    res = requests.put(url=input_url2 +'/storage/files/'+ FILE_PATH_ENCODED + '/transcriptions',headers=headers_get_transcriptions_api)
    print(res)
    assert res.status_code == 403

def test_get_audio_file_transcription_api_delete_request(input_url2,get_token):
    headers_get_transcriptions_api = {'Authorization': get_token}
    res = requests.delete(url=input_url2 +'/storage/files/'+ FILE_PATH_ENCODED + '/transcriptions',headers=headers_get_transcriptions_api)
    print(res)
    assert res.status_code == 403


### New transcription API negative cases ###

#platform/v1/storage/files/transcriptions

def test_get_transcriptions_with_single_file_path_invalid_url_encoded():
    headers = {'Authorization': ACCESS_TOKEN}
    parameters = {'filePath': FILE_PATH_ENCODED_SAVED2}
    res = requests.get(url=BASE_URL + '/storage/files/' + 'transcriptions', headers=headers, params=parameters)
    print(res)
    assert res.status_code == 404


def test_get_transcriptions_with_two_file_path_one_is_valid_one_is_invalid():
    headers = {'Authorization': ACCESS_TOKEN}
    parameters = {'filePath': FILE_PATH_VALID_INVALID}
    res = requests.get(url=BASE_URL + '/storage/files/' + 'transcriptions', headers=headers, params=parameters)
    print(res)
    assert res.status_code == 404


def test_get_transcriptions_with_two_file_path_one_has_transcription_present_another_one_has_transcription_not_found():
    headers = {'Authorization': ACCESS_TOKEN}
    parameters = {'filePath': FILE_PATHS_ONE_FILE_TRANSCRIPTION_PRESENT}
    res = requests.get(url=BASE_URL + '/storage/files/' + 'transcriptions', headers=headers, params=parameters)
    print(res)
    assert res.status_code == 404

def test_get_transcriptions_with_single_file_without_encoding_url():
    headers = {'Authorization': ACCESS_TOKEN}
    parameters = {'filePath': FILE_PATH_WITHOUT_ENCODING}
    res = requests.get(url=BASE_URL + '/storage/files/' + 'transcriptions', headers=headers, params=parameters)
    print(res)
    assert res.status_code == 404

def test_get_transcriptions_with_single_file_with_passing_file_path_as_integer():
    headers = {'Authorization': ACCESS_TOKEN}
    parameters = {'filePath': FILE_PATH_AS_INTEGER}
    res = requests.get(url=BASE_URL + '/storage/files/' + 'transcriptions', headers=headers, params=parameters)
    print(res)
    assert res.status_code == 400


def test_get_transcriptions_with_single_file_with_passing_file_path_as_string():
    headers = {'Authorization': ACCESS_TOKEN}
    parameters = {'filePath': FILE_PATH_AS_STRING}
    res = requests.get(url=BASE_URL + '/storage/files/' + 'transcriptions', headers=headers, params=parameters)
    print(res)
    assert res.status_code == 400


def test_get_transcriptions_with_single_file_with_passing_file_path_as_blank():
    headers = {'Authorization': ACCESS_TOKEN}
    parameters = {'filePath': FILE_PATH_BLANK}
    res = requests.get(url=BASE_URL + '/storage/files/' + 'transcriptions', headers=headers, params=parameters)
    print(res)
    assert res.status_code == 400


#
comma_separated_params = []
for file_path1 in MAX_FILE_PATH_CHECK:
    #encoded_file_path = encode_file_path(file_path)
    comma_separated_params.append(file_path1)
all_file_paths = ','.join(comma_separated_params)
params = {'filePath' : all_file_paths}
#print(file_paths)

# def test_get_transcriptions_with_more_than_forty_file_paths():
#     headers = {'Authorization': ACCESS_TOKEN}
#     parameters = {'filePath': all_file_paths}
#     res = requests.get(url=BASE_URL + '/storage/files/' + 'transcriptions', headers=headers, params=parameters)
#     assert res.status_code == 400
#Working manually

# def test_get_transcriptions_with_no_file_path_as_parameter():
#     headers = {'Authorization': ACCESS_TOKEN}
#     #parameters = {'filePath': FILE_PATH_BLANK}
#     res = requests.get(url=BASE_URL + '/storage/files/' + 'transcriptions')
#     print(res)
#     assert res.status_code == 400

def test_get_transcriptions_with_single_file_with_no_transcription_present():
    headers = {'Authorization': ACCESS_TOKEN}
    parameters = {'filePath': TRANSCRIPTION_NOT_FOUND}
    res = requests.get(url=BASE_URL + '/storage/files/' + 'transcriptions', headers=headers, params=parameters)
    print(res)
    assert res.status_code == 404


def test_speech_text_url_expiration_case():
    #headers = {'Authorization': ACCESS_TOKEN}
   # parameters = {'filePath': TRANSCRIPTION_NOT_FOUND}
    res = requests.get(url=speechtexturlexpire)
    print(res)
    assert res.status_code == 403

def test_get_transcriptions_with_file_path_with_no_audio_file_present():
    headers = {'Authorization': ACCESS_TOKEN, 'Content-Type': CONTENT_TYPE_APPLICATION_JSON}
    parameters = {'filePath': FILE_PATH_MISSING_AUDIO_FILE}
    res = requests.get(url=BASE_URL + '/storage/files/' + 'transcriptions', headers=headers, params=parameters)
    print(res)
    assert res.status_code == 404



def test_get_transcriptions_api_invalid_end_point():
    headers_get_transcriptions_api = {'Authorization': ACCESS_TOKEN}
    res = requests.get(url=BASE_URL +'/storage/files/'+'transcriptions' + '/XYZ', headers=headers_get_transcriptions_api)
    print(res)
    assert res.status_code == 403


def test_get_transcriptions_api_header_missing():
    res = requests.get(url=BASE_URL + '/storage/files/' + 'transcriptions')
    print(res)
    assert res.status_code == 401

def test_get_transcriptions_api_invalid_access_token():
    status, data = API_Calls.get_transcriptions(BASE_URL,INCORRECT_ACCESS_TOKEN)
    print(status, data)
    assert status == 401


def test_get_transcriptions_api_filePath_associated_with_other_party():
    headers = {'Authorization': ACCESS_TOKEN}
    parameters = {'filePath': NO_ACCESS_DOWNLOAD_FILE}
    res = requests.get(url=BASE_URL + '/storage/files/' +'transcriptions', headers=headers, params=parameters)
    print(res)
    assert res.status_code == 404


def test_get_transcriptions_api_access_token_missing():
    headers_get_transcriptions_api = {'Authorization': ''}
    res = requests.get(url=BASE_URL +'/storage/files/'+'transcriptions', headers=headers_get_transcriptions_api)
    print(res)
    assert res.status_code == 401


def test_get_transcriptions_api_content_type_header_is_modified():
    headers_get_transcriptions_api = {'Authorization': ACCESS_TOKEN, 'Content-Type': CONTENT_TYPE_URL_ENCODED}
    parameters = {'filePath': FILE_PATH_ENCODED_SAVED1}
    res = requests.get(url=BASE_URL +'/storage/files/'+ 'transcriptions' , headers=headers_get_transcriptions_api,params=parameters)
    print(res)
    assert res.status_code == 415


    #need to check


def test_get_transcriptions_api_content_type_is_not_provided():
    headers_get_transcriptions_api = {'Authorization': ACCESS_TOKEN}
    parameters = {'filePath': FILE_PATH_ENCODED_SAVED1}
    res = requests.get(url=BASE_URL +'/storage/files/'+ 'transcriptions' , headers=headers_get_transcriptions_api,params=parameters)
    print(res)
    assert res.status_code == 200



def test_get_transcriptions_api_post_request(input_url2,get_token):
    headers = {'Authorization': ACCESS_TOKEN}
    parameters = {'filePath': FILE_PATH_ENCODED_SAVED1}
    res = requests.post(url=BASE_URL +'/storage/files/'+'transcriptions',headers=headers,params=parameters)
    print(res)
    assert res.status_code == 403

def test_get_transcriptions_api_put_request(input_url2,get_token):
    headers = {'Authorization': ACCESS_TOKEN}
    parameters = {'filePath': FILE_PATH_ENCODED_SAVED1}
    res = requests.put(url=BASE_URL +'/storage/files/'+ 'transcriptions',headers=headers,params=parameters)
    print(res)
    assert res.status_code == 403

def test_get_transcriptions_api_delete_request(input_url2,get_token):
    headers = {'Authorization': ACCESS_TOKEN}
    parameters = {'filePath': FILE_PATH_ENCODED_SAVED1}
    res = requests.delete(url=BASE_URL +'/storage/files/'+'transcriptions',headers=headers,params=parameters)
    print(res)
    assert res.status_code == 403


