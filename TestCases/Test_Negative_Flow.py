import json
import pytest
import requests
from TestCases import API_Calls
from Variables.variable import *
from TestCases.Support import helper

# ---------------- Get the Base64 --------------------------------#

base64secrets = helper.get_base64secrets(CLIENT_ID_Shruti, CLIENT_SECRET_Shruti)

BASE_TOKEN = 'Basic ' + base64secrets

# ----------- Get the ACCESS TOKEN ----------------------------#

status_code, json_data = API_Calls.token_api(BASE_URL, VALID_TOKEN_DATA, BASE_TOKEN, CONTENT_TYPE_URL_ENCODED)
ACCESS_TOKEN = json_data['access_token']

# ---------------- Get the Base64 testclient --------------------------------#

base64secrets = helper.get_base64secrets(CLIENT_ID_Shruti_test, CLIENT_SECRET_Shruti_test)
print(base64secrets)

BASE_TOKEN_TEST = 'Basic ' + base64secrets


# ----------- Get the ACCESS TOKEN for missing party client credentials ----------------------------#

status_code, json_data = API_Calls.token_api(BASE_URL, VALID_TOKEN_DATA, BASE_TOKEN_TEST, CONTENT_TYPE_URL_ENCODED)
ACCESS_TOKEN_TEST = json_data['access_token']

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

#AUDIO_FILE_PATH = 'C:\\Users\\GS-1329\\Downloads\\File_1_6sec.wav'

AUDIO_FILE_PATH = 'C:\\Users\\GS-1431\\Downloads\\ahh_SK.wav'
#AUDIO_FILE_PATH = 'C:\\Users\\GS-1329\\Downloads\\1__7FC800CA-456C-4CA2-A568-DE6A96E54705_7251_9067.wav'

status_code = API_Calls.upload_sample_file(STORAGE_SIGNED_URL, AUDIO_FILE_PATH)

# --------------------------------- GET ALL MEASURES- ------------------------------------------------------------#
status, response_json = API_Calls.measures_api(BASE_URL, ACCESS_TOKEN)
MEASURE_ID = response_json['measures'][0]['id']

# ------------------------------GET THE QUESTIONNAIRE ID----------------------------------------#

MEASURE_NAME = 'respiratory-symptoms-risk'

status, response_json = API_Calls.get_questionnaire_ID_required_for_measure(BASE_URL, MEASURE_NAME, ACCESS_TOKEN)
print(status, response_json)
QUESTIONNAIRE_ID = response_json['questionnaire']['id']
QUESTIONNAIRE_LANGUAGES = response_json['questionnaire']['languages'][0]

# -------------------------------GET THE QUESTIONNAIRE -------------------------------------------------

status, response_json = API_Calls.get_questionnaire_required_for_measure(BASE_URL, QUESTIONNAIRE_ID,
                                                                         QUESTIONNAIRE_LANGUAGES, ACCESS_TOKEN)
QUES_ID = response_json['id']
LANGUAGE = response_json['language']

# ------------------------------SUBMIT THE QUESTIONNAIRE RESPONSE------------------------------------------

QUESTIONNAIRE_BODY = {

    "questionnaire": {
         "id": QUES_ID,
        "language": LANGUAGE,
        "userIdentifier":SUB_IDENTIFIER,
        "respondedAt": "1994-11-05T13:15:30Z",
        "questionResponses": [
            {
                "optionIndex": 1
            },
                        {
                "optionIndex": 1
            },
                        {
                "optionIndex": 1
            },
                        {
                "optionIndex": 1
            },
            {
                "optionIndexes": [1,2]
            },
            {
                "optionIndex": 1
            }
        ]
    }
}

#Sachin's questionnaire request
# QUESTIONNAIRE_BODY = {
#     "questionnaire": {
#         "id": QUES_ID,
#         "language": LANGUAGE,
#         "userIdentifier": SUB_IDENTIFIER,
#         "respondedAt": "1994-11-05T13:15:30Z",
#         "questionResponses": [
#             {
#                 "optionIndex": 1
#             },
#             {
#                 "optionIndexes": [
#                     0,
#                     1
#                 ]
#             },
#             {
#                 "response": 3
#             },
#             {
#                 "response": "104F"
#             }
#         ]
#     }
# }

status, response_json = API_Calls.submit_questionnaire_response(BASE_URL, QUESTIONNAIRE_BODY, ACCESS_TOKEN)
QUESTIONNAIRE_RESPONSE_ID = response_json['id']

# ---------------------------- GET THE SCORE --------------------------------#

VALID_SCORE_DATA = {
    "userIdentifier": SUB_IDENTIFIER,
    "filePath": FILE_PATH,
    "questionnaireResponseId": QUESTIONNAIRE_RESPONSE_ID,
    "measureName": MEASURE_NAME
}

status_code, response_json = API_Calls.score_api(BASE_URL, VALID_SCORE_DATA, ACCESS_TOKEN,
                                                 CONTENT_TYPE_APPLICATION_JSON)


def generate_questionnaire_raw_data(q_data):
    q_data['questionnaire']['id'] = QUES_ID
    q_data['questionnaire']['language'] = LANGUAGE
    q_data['questionnaire']['userIdentifier'] = SUB_IDENTIFIER
    return q_data


# # ----------------------------------------------------------------------------------------------------------------#
# # -------------------------------------------- TEST CASES --------------------------------------------------------#
TOKEN_DATA = {
    'grant_type': 'client_credentials'
}


def test_token_api_invalid_end_point():
    status, data = API_Calls.token_api(INVALID_BASE_URL, VALID_TOKEN_DATA, BASE_TOKEN, CONTENT_TYPE_URL_ENCODED)
    assert status == 403
    print(status, data)



def test_token_api_invalid_end_point1():
     headers1 = {'Authorization': BASE_TOKEN, 'Content-Type': CONTENT_TYPE_APPLICATION_JSON}
     #INVALID_END_POINT = '/XYZ'
     res = requests.post(url=INVALID_BASE_URL, data=json.dumps(VALID_SCORE_DATA), headers=headers1)
     print(res)
     assert res.status_code == 403


def test_token_api_invalid_base_token():
    INVALID_BASE_TOKEN = 'Invalid_String'
    status, data = API_Calls.token_api(BASE_URL, VALID_TOKEN_DATA, INVALID_BASE_TOKEN,
                                       CONTENT_TYPE_URL_ENCODED)
    print(status, data)
    assert status == 400


# 'BASE 64 USER DOES NOT HAVE SCOPES DEFINED' #
def test_token_api_unauthorized_user():
    INVALID_SCOPES_BASE_TOKEN = 'BASE 64 USER DOES NOT HAVE SCOPES DEFINED'
    status, data = API_Calls.token_api(BASE_URL, VALID_TOKEN_DATA, INVALID_SCOPES_BASE_TOKEN,
                                       CONTENT_TYPE_URL_ENCODED)
    print(status, data)
    assert status == 400


def test_token_api_authentication_header_missing():
    headers = {'Content-Type': CONTENT_TYPE_URL_ENCODED}
    r = requests.post(BASE_URL + TOKEN_END_POINT, data=VALID_TOKEN_DATA, headers=headers)
    print(r)
    assert r.status_code == 400


def test_token_authentication_header_value_missing():
    headers = {'Content-Type': ''}
    r = requests.post(BASE_URL + TOKEN_END_POINT, data=VALID_TOKEN_DATA, headers=headers)
    print(r)
    assert r.status_code == 405


def test_token_api_request_body_grant_type_key_blank():
    D_CP = TOKEN_DATA.copy()
    DATA = helper.update_dictionary(D_CP, grant_type='')
    print (DATA)
    status, data = API_Calls.token_api(BASE_URL, DATA, BASE_TOKEN, CONTENT_TYPE_URL_ENCODED)
    print(status, data)
    assert status == 400


def test_token_api_request_body_grant_type_key_invalid():
    D_CP = TOKEN_DATA.copy()
    DATA = helper.update_dictionary(D_CP, grant_type='XYZ')
    status, data = API_Calls.token_api(BASE_URL, DATA, BASE_TOKEN,
                                       CONTENT_TYPE_URL_ENCODED)
    print(status, data)
    assert status == 400


def test_token_api_request_body_grant_type_key_missing():
    D_CP = TOKEN_DATA.copy()
    DATA = helper.delete_key(D_CP, 'grant_type')
    status, data = API_Calls.token_api(BASE_URL, DATA, BASE_TOKEN,
                                       CONTENT_TYPE_URL_ENCODED)
    print(status, data)
    assert status == 400


def test_token_api_request_body_scope_key_blank():
    D_CP = TOKEN_DATA.copy()
    DATA = helper.update_dictionary(D_CP, scope='')
    status, data = API_Calls.token_api(BASE_URL, DATA, BASE_TOKEN, CONTENT_TYPE_URL_ENCODED)
    print(status, data)
    assert status == 200


def test_token_api_request_body_scope_key_invalid():
    D_CP = TOKEN_DATA.copy()
    DATA = helper.update_dictionary(D_CP, scope='sonde-platform/storage.write/storage.read/storage.list')
    status, data = API_Calls.token_api(BASE_URL, DATA, BASE_TOKEN, CONTENT_TYPE_URL_ENCODED)
    print(status, data)
    assert status == 400


def test_token_api_request_body_scope_key_missing():
    D_CP = TOKEN_DATA.copy()
    DATA = helper.delete_key(D_CP, 'scope')
    status, data = API_Calls.token_api(BASE_URL, DATA, BASE_TOKEN, CONTENT_TYPE_URL_ENCODED)
    print(status, data)
    assert status == 200


def test_token_api_request_extra_key_added():
    D_CP = TOKEN_DATA.copy()
    DATA = helper.update_dictionary(D_CP, test='test')
    status, data = API_Calls.token_api(BASE_URL, DATA, BASE_TOKEN, CONTENT_TYPE_URL_ENCODED)
    print(status, data)
    assert status == 200


def test_token_api_contentType_header_value_invalid():
    headers1 = {'Authorization': BASE_TOKEN, 'Content-Type': CONTENT_TYPE_APPLICATION_JSON}
    r = requests.post(BASE_URL + TOKEN_END_POINT, data=TOKEN_DATA, headers=headers1)
    print(r)
    assert r.status_code == 405


def test_token_api_with_put_request():
    headers1 = {'Authorization': BASE_TOKEN, 'Content-Type': CONTENT_TYPE_URL_ENCODED}
    r = requests.put(BASE_URL + TOKEN_END_POINT, data=TOKEN_DATA, headers=headers1)
    print(r)
    assert r.status_code == 405


def test_token_api_with_get_request():
    headers1 = {'Authorization': BASE_TOKEN, 'Content-Type': CONTENT_TYPE_URL_ENCODED}
    r = requests.get(BASE_URL + TOKEN_END_POINT, data=TOKEN_DATA, headers=headers1)
    print(r)
    assert r.status_code == 403


def test_token_api_with_delete_request():
    headers1 = {'Authorization': BASE_TOKEN, 'Content-Type': CONTENT_TYPE_URL_ENCODED}
    r = requests.delete(BASE_URL + TOKEN_END_POINT, data=TOKEN_DATA, headers=headers1)
    print(r)
    assert r.status_code == 405


# # --------------------- SUBJECT API TEST CASES ---------- #
# # ---------------------------------------------------#
#Sachin's subject data
# SUBJECT_DATA = {
#     "gender": "MALE",
#     "yearOfBirth": "1985",
#     "language": "ENGLISH",
#     "device": {
#         "type": "MOBILE",
#         "manufacturer": "Vivo"
#     },
#     "diseases": [
#         {
#             "name": "Nasality"
#         },
#         {
#             "name": "Hypertension"
#         },
#         {
#             "name": "CHF"
#         }
#     ]
# }


SUBJECT_DATA ={
  "gender": "female",
  "yearOfBirth": "1985",
  "language" : "ENGLISH",
   "device": {
    "type": "MOBILE",
    "manufacturer": "VIVO"
  },
  "diseases": [
    {"name":"test"}
  ]
}


def test_subject_api_invalid_end_point():
    INVALID_END_POINT = '/xyz'
    headers_subject = {'Authorization': ACCESS_TOKEN, 'Content-Type': CONTENT_TYPE_APPLICATION_JSON}
    res = requests.post(url=BASE_URL + INVALID_END_POINT, data=json.dumps(VALID_SUBJECT_DATA), headers=headers_subject)
    print(res)
    assert res.status_code == 403



def test_subject_api_incorrect_access_token():
    INCORRECT_BASE_TOKEN = 'xyz'
    status, data = API_Calls.subject_api(BASE_URL, VALID_SUBJECT_DATA, INCORRECT_BASE_TOKEN,
                                         CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 401

def test_subject_api_access_token_with_bearer_in_small_case():
    ACCESS_TOKEN_BEARER1 = 'bearer ' + ACCESS_TOKEN
    print(ACCESS_TOKEN_BEARER1)
    status, data = API_Calls.subject_api(BASE_URL, VALID_SUBJECT_DATA, ACCESS_TOKEN_BEARER1,
                                         CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 401


def test_subject_api_expired_access_token():
    status, data = API_Calls.subject_api(BASE_URL, VALID_SUBJECT_DATA, EXPIRED_ACCESS_TOKEN,
                                         CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 401
    # ACCESS DENIED


def test_subject_api_missing_access_token():
    headers_subject = {'Content-Type': CONTENT_TYPE_APPLICATION_JSON}
    res = requests.post(url=BASE_URL + SUBJECT_END_POINT, data=json.dumps(VALID_SUBJECT_DATA), headers=headers_subject)
    print(res)
    assert res.status_code == 401


def test_subject_api_blank_auth_key():
    headers_subject = {'Authorization': '', 'Content-Type': CONTENT_TYPE_APPLICATION_JSON}
    res = requests.post(url=BASE_URL + SUBJECT_END_POINT, data=json.dumps(VALID_SUBJECT_DATA), headers=headers_subject)
    print(res)
    assert res.status_code == 401


def test_subject_api_request_body_device_key_missing():
    D_CP = SUBJECT_DATA.copy()
    DATA = helper.delete_key(D_CP, 'device')
    status, data = API_Calls.subject_api(BASE_URL, DATA, ACCESS_TOKEN,
                                         CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 201


def test_subject_api_request_body_device_key_blank():
    D_CP = SUBJECT_DATA.copy()
    DATA = helper.update_dictionary(D_CP, device='')
    status, data = API_Calls.subject_api(BASE_URL, DATA, ACCESS_TOKEN,
                                         CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 400


def test_subject_api_request_body_diseases_key_missing():
    D_CP = SUBJECT_DATA.copy()
    DATA = helper.delete_key(D_CP, 'diseases')
    status, data = API_Calls.subject_api(BASE_URL, DATA, ACCESS_TOKEN,
                                         CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 201


def test_subject_api_request_body_diseases_key_blank():
    D_CP = SUBJECT_DATA.copy()
    DATA = helper.update_dictionary(D_CP, diseases=[])
    print(DATA)
    status, data = API_Calls.subject_api(BASE_URL, DATA, ACCESS_TOKEN,
                                         CONTENT_TYPE_APPLICATION_JSON)
    print(data)
    print(status, data)
    assert status == 201


def test_subject_api_request_body_gender_key_blank():
    D_CP = SUBJECT_DATA.copy()
    DATA = helper.update_dictionary(D_CP, gender='')
    status, data = API_Calls.subject_api(BASE_URL, DATA, ACCESS_TOKEN,
                                         CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 400
    # status = 400


def test_subject_api_request_body_gender_key_invalid():
    D_CP = SUBJECT_DATA.copy()
    DATA = helper.update_dictionary(D_CP, gender='')
    status, response = API_Calls.subject_api(BASE_URL, DATA, ACCESS_TOKEN,
                                             CONTENT_TYPE_APPLICATION_JSON)
    print(status, response)
    assert status == 400
    # status = 400



def test_subject_api_request_body_gender_key_missing():
    D_CP = SUBJECT_DATA.copy()
    DATA = helper.delete_key(D_CP, 'gender')
    status, data = API_Calls.subject_api(BASE_URL, DATA, ACCESS_TOKEN,
                                         CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 400
    # status = 400


def test_subject_api_request_body_gender_key_incorrect_data_type():
    D_CP = SUBJECT_DATA.copy()
    DATA = helper.update_dictionary(D_CP, gender=123)
    status, data = API_Calls.subject_api(BASE_URL, DATA, ACCESS_TOKEN,
                                         CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 400


def test_subject_api_request_body_yearOfBirth_key_blank():
    D_CP = SUBJECT_DATA.copy()
    DATA = helper.update_dictionary(D_CP, yearOfBirth='')
    status, data = API_Calls.subject_api(BASE_URL, DATA, ACCESS_TOKEN,
                                         CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 400
    # status = 400


def test_subject_api_request_body_yearOfBirth_key_invalid():
    D_CP = SUBJECT_DATA.copy()
    DATA = helper.update_dictionary(D_CP, yearOfBirth=19000)
    status, data = API_Calls.subject_api(BASE_URL, DATA, ACCESS_TOKEN,
                                         CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 400
    # status = 400


def test_subject_api_request_body_yearOfBirth_key_missing():
    D_CP = SUBJECT_DATA.copy()
    DATA = helper.delete_key(D_CP, 'yearOfBirth')
    status, data = API_Calls.subject_api(BASE_URL, DATA, ACCESS_TOKEN,
                                         CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 400
    # status = 400


def test_subject_api_request_body_yearOfBirth_key_incorrect_data_type():
    D_CP = SUBJECT_DATA.copy()
    DATA = helper.update_dictionary(D_CP, yearOfBirth='xyz')
    status, data = API_Calls.subject_api(BASE_URL, DATA, ACCESS_TOKEN,
                                         CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 400


def test_subject_api_request_body_language_key_blank():
    D_CP = SUBJECT_DATA.copy()
    DATA = helper.update_dictionary(D_CP, language='')
    status, data = API_Calls.subject_api(BASE_URL, DATA, ACCESS_TOKEN,
                                         CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 400
    # status = 400


def test_subject_api_request_body_language_key_invalid():
    D_CP = SUBJECT_DATA.copy()
    DATA = helper.update_dictionary(D_CP, language='xyz')
    status, data = API_Calls.subject_api(BASE_URL, DATA, ACCESS_TOKEN,
                                         CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 201
    # status = 400


def test_subject_api_request_body_language_key_missing():
    D_CP = SUBJECT_DATA.copy()
    DATA = helper.delete_key(D_CP, 'language')
    status, data = API_Calls.subject_api(BASE_URL, DATA, ACCESS_TOKEN,
                                         CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 201


def test_subject_api_request_body_language_key_incorrect_data_type():
    D_CP = SUBJECT_DATA.copy()
    DATA = helper.update_dictionary(D_CP, language=123)
    status, data = API_Calls.subject_api(BASE_URL, DATA, ACCESS_TOKEN,
                                         CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 400


def test_subject_api_request_extra_key_added():
    D_CP = SUBJECT_DATA.copy()
    DATA = helper.update_dictionary(D_CP, test='XYZ')
    status, data = API_Calls.subject_api(BASE_URL, DATA, ACCESS_TOKEN,
                                         CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 400


def test_subject_api_with_put_request():
    headers_storage = {'Authorization': ACCESS_TOKEN, 'Content-Type': 'Application/json'}
    res = requests.put(BASE_URL + '/storage/files', data=json.dumps(VALID_SUBJECT_DATA), headers=headers_storage)
    print(res)
    assert res.status_code == 403


def test_subject_api_with_get_request():
    headers = {'Authorization': ACCESS_TOKEN, 'Content-Type': 'Application/json'}
    res = requests.get(BASE_URL + '/storage/files', data=json.dumps(VALID_SUBJECT_DATA), headers=headers)
    print(res)
    assert res.status_code == 403


def test_subject_api_with_delete_request():
    headers = {'Authorization': ACCESS_TOKEN, 'Content-Type': 'Application/json'}
    res = requests.delete(BASE_URL + '/storage/files', data=json.dumps(VALID_SUBJECT_DATA), headers=headers)
    print(res)
    assert res.status_code == 403


REQUIRED_SUBJECT_DATA = {
    "gender": "MALE",
    "yearOfBirth": "1985",
}


def test_subject_api_with_multiple_variable_missing():
    D_CP = REQUIRED_SUBJECT_DATA.copy()
    for key in range(0, 3):
        DATA = helper.get_random_pairs(D_CP)
        status, data = API_Calls.subject_api(BASE_URL, DATA, ACCESS_TOKEN,
                                             CONTENT_TYPE_APPLICATION_JSON)
        print(status, data)
        assert status == 400

### --------unknown user API support -------------####

def test_subject_v1_api_with_unknown_gender_inlowercase():
    D_CP = VALID_SUBJECT_DATA_V2.copy()
    DATA = helper.update_dictionary(D_CP, gender="unknown")
    print(DATA)
    status, data = API_Calls.subject_api(BASE_URL, DATA, ACCESS_TOKEN,
                                         CONTENT_TYPE_APPLICATION_JSON)
    assert status == 400
    print(status, data)


def test_subject_v1_api_with_unknown_incaps_gender():
    D_CP = VALID_SUBJECT_DATA_V2.copy()
    DATA = helper.update_dictionary(D_CP, gender="UNKNOWN")
    print(DATA)
    status, data = API_Calls.subject_api(BASE_URL, DATA, ACCESS_TOKEN,
                                         CONTENT_TYPE_APPLICATION_JSON)
    assert status == 400
    print(status, data)

def test_subject_v1_api_with_unknown_in_uppercase_yearOfBirth():
    D_CP = VALID_SUBJECT_DATA_V2.copy()
    DATA = helper.update_dictionary(D_CP, yearOfBirth="UNKNOWN")
    print(DATA)
    status, data = API_Calls.subject_api(BASE_URL, DATA, ACCESS_TOKEN,
                                         CONTENT_TYPE_APPLICATION_JSON)
    assert status == 400
    print(status, data)


def test_subject_v1_api_with_unknown_inlowercase_yearOfBirth():
    D_CP = VALID_SUBJECT_DATA_V2.copy()
    DATA = helper.update_dictionary(D_CP, yearOfBirth="unknown")
    print(DATA)
    status, data = API_Calls.subject_api(BASE_URL, DATA, ACCESS_TOKEN,
                                         CONTENT_TYPE_APPLICATION_JSON)
    assert status == 400
    print(status, data)


def test_subject_v1_api_with_unknown_device_in_uppercase():
    status, data = API_Calls.subject_api(BASE_URL, VALID_SUBJECT_DATA_DEVICE_UNKNOWN, ACCESS_TOKEN, CONTENT_TYPE_APPLICATION_JSON)
    assert status == 400
    print(status, data)


def test_subject_v1_api_unknown_device_in_lowercase():
    status, data = API_Calls.subject_api(BASE_URL, SUBJECT_DATA_1, ACCESS_TOKEN, CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 400


def test_subject_v1_api_with_unknown_device_yob_gender_in_caps():
    status, data = API_Calls.subject_api(BASE_URL, VALID_SUBJECT_DATA_ALL_M_UNKNOWN, ACCESS_TOKEN, CONTENT_TYPE_APPLICATION_JSON)
    assert status == 400
    print(status, data)



def test_subject_v1_api_unknown_in_lowercase_device_yob_gender():
    status, data = API_Calls.subject_api(BASE_URL, VALID_SUBJECT_DATA_ALL_M_UNKNOWN_IN_SMALL, ACCESS_TOKEN, CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 400


#
# # # ------------------------- Subject Details Put API ----------------------------------- #
# #
# #
UPDATE_SUBJECT_DATA = {
    "type": "MOBILE",
    "manufacturer": "VIVO"
}


def test_subject_details_update_api_invalid_end_point():
    INVALID_END_POINT = '/xyz'
    headers_subject = {'Authorization': ACCESS_TOKEN, 'Content-Type': CONTENT_TYPE_APPLICATION_JSON}
    res = requests.post(url=BASE_URL + INVALID_END_POINT, data=json.dumps(VALID_SUBJECT_DATA), headers=headers_subject)
    print(res)
    assert res.status_code == 403


def test_subject_details_update_api_incorrect_access_token():
    INCORRECT_BASE_TOKEN = 'xyz'
    status, data = API_Calls.update_subject_details(BASE_URL, SUB_IDENTIFIER, UPDATE_SUBJECT_DATA, INCORRECT_BASE_TOKEN)
    print(status, data)
    assert status == 401


def test_subject_details_update_api_expired_access_token():
    status, data = API_Calls.update_subject_details(BASE_URL, SUB_IDENTIFIER, UPDATE_SUBJECT_DATA, EXPIRED_ACCESS_TOKEN)
    print(status, data)
    assert status == 401

def test_subject_details_update_api_with_access_token_bearer_in_small_case():
    ACCESS_TOKEN_BEARER1 = 'bearer ' + ACCESS_TOKEN
    print(ACCESS_TOKEN_BEARER1)
    status, data = API_Calls.update_subject_details(BASE_URL, SUB_IDENTIFIER, UPDATE_SUBJECT_DATA,
                                                        ACCESS_TOKEN_BEARER1)
    print(status, data)
    assert status == 401

    # ACCESS DENIED


def test_subject_details_update_api_missing_access_token():
    headers_subject_update = {'Authorization': '', 'Content-Type': CONTENT_TYPE_APPLICATION_JSON}
    res = requests.put(url=BASE_URL + '/users/' + SUB_IDENTIFIER + '/device', data=json.dumps(UPDATE_SUBJECT_DATA),
                       headers=headers_subject_update)
    print(res)
    assert res.status_code == 401


def test_subject_details_update_api_blank_auth_key():
    headers_subject_update = {'Content-Type': CONTENT_TYPE_APPLICATION_JSON}
    res = requests.put(url=BASE_URL + '/users/' + SUB_IDENTIFIER + '/device', data=json.dumps(UPDATE_SUBJECT_DATA),
                       headers=headers_subject_update)
    print(res)
    assert res.status_code == 401


def test_subject_details_update_api_incorrect_userIdentifier():
    INCORRECT_SUB_IDENTIFIER = '12a1234s'
    status, data = API_Calls.update_subject_details(BASE_URL, INCORRECT_SUB_IDENTIFIER, UPDATE_SUBJECT_DATA,
                                                    ACCESS_TOKEN)
    print(status, data)
    assert status == 404


def test_subject_details_update_api_incorrect_device_type():
    D_CP = UPDATE_SUBJECT_DATA.copy()
    DATA = helper.update_dictionary(D_CP, type='XYZ')
    status, data = API_Calls.update_subject_details(BASE_URL, SUB_IDENTIFIER, DATA,
                                                    ACCESS_TOKEN)
    print(status, data)
    assert status == 400


def test_subject_details_update_api_device_type_not_in_list():
    D_CP = UPDATE_SUBJECT_DATA.copy()
    DATA = helper.update_dictionary(D_CP, type='Tablet')
    status, data = API_Calls.update_subject_details(BASE_URL, SUB_IDENTIFIER, DATA,
                                                    ACCESS_TOKEN)
    print(status, data)
    assert status == 400


def test_subject_details_update_api_missing_device_type():
    D_CP = UPDATE_SUBJECT_DATA.copy()
    DATA = helper.delete_key(D_CP, 'type')
    status, data = API_Calls.update_subject_details(BASE_URL, SUB_IDENTIFIER, DATA,
                                                    ACCESS_TOKEN)
    print(status, data)
    assert status == 400


def test_subject_details_update_api_invalid_manufacturer():
    D_CP = UPDATE_SUBJECT_DATA.copy()
    DATA = helper.update_dictionary(D_CP, type=1234)
    status, data = API_Calls.update_subject_details(BASE_URL, SUB_IDENTIFIER, DATA,
                                                    ACCESS_TOKEN)
    print(status, data)
    assert status == 400


def test_subject_details_update_api_missing_manufacturer():
    D_CP = UPDATE_SUBJECT_DATA.copy()
    DATA = helper.delete_key(D_CP, 'manufacturer')
    status, data = API_Calls.update_subject_details(BASE_URL, SUB_IDENTIFIER, DATA,
                                                    ACCESS_TOKEN)
    print(status, data)
    assert status == 400


def test_subject_details_update_api_with_multiple_variable_missing():
    D_CP = UPDATE_SUBJECT_DATA.copy()
    for key in range(0, 3):
        DATA = helper.get_random_pairs(D_CP)
        status, data = API_Calls.update_subject_details(BASE_URL, SUB_IDENTIFIER, DATA,
                                                        ACCESS_TOKEN)
        print(status, data)
        assert status == 400


#
# # ------------------------------------------------ MEASURE -------------------------#

def test_measure_api_invalid_end_point():
    headers_measure = {'Authorization': ACCESS_TOKEN}
    res = requests.get(url=BASE_URL + '/XYZ', headers=headers_measure)
    print(res)
    assert res.status_code == 403


def test_measure_api_invalid_access_token():
    status, data = API_Calls.measures_api(BASE_URL, INVALID_ACCESS_TOKEN)
    print(status, data)
    assert status == 401

def test_measure_api_access_token_with_bearer_in_small_case():
    ACCESS_TOKEN_BEARER1 = 'bearer ' + ACCESS_TOKEN
    print(ACCESS_TOKEN_BEARER1)
    status, data = API_Calls.measures_api(BASE_URL, ACCESS_TOKEN_BEARER1)
    print(status, data)
    assert status == 401



def test_measure_id_api_invalid_end_point():
    status, data = API_Calls.measure_id_api(BASE_URL, INVALID_MEASURE_ID_END_POINT, ACCESS_TOKEN)
    print(status, data)
    assert status == 404


def test_measure_id_header_missing():
    r = requests.get(BASE_URL + '/measures/' + str(MEASURE_ID))
    print(r)
    assert r.status_code == 401


def test_measure_id_api_invalid_access_token():
    status, data = API_Calls.measure_id_api(BASE_URL, MEASURE_ID, INVALID_ACCESS_TOKEN)
    print(status, data)
    assert status == 401


#
# # ================================ STORAGE API TEST CASES==================================================#
STORAGE_DATA = {
    "fileType": "wav",
    "countryCode": "US",
    "userIdentifier": SUB_IDENTIFIER
}


#

def test_storage_api_invalid_endpoint():
    INVALID_END_POINT = 'xyz'
    headers_storage = {'Authorization': ACCESS_TOKEN, 'Content-Type': CONTENT_TYPE_APPLICATION_JSON}
    res = requests.post(BASE_URL + INVALID_END_POINT, data=json.dumps(VALID_STORAGE_DATA),
                        headers=headers_storage)
    print(res)
    assert res.status_code == 403


def test_storage_api_incorrect_access_token():
    INCORRECT_ACCESS_TOKEN = 'xyz'
    status, data = API_Calls.storage_api(BASE_URL, STORAGE_DATA, INCORRECT_ACCESS_TOKEN,
                                         CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 401
    # ACCESS DENIED
    # status code == 403

def test_storage_api_access_token_with_bearer_in_small_case():
    ACCESS_TOKEN_BEARER1 = 'bearer ' + ACCESS_TOKEN
    print(ACCESS_TOKEN_BEARER1)
    status, data = API_Calls.storage_api(BASE_URL, STORAGE_DATA, ACCESS_TOKEN_BEARER1,
                                             CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 401



def test_storage_api_expired_access_token():
    status, data = API_Calls.storage_api(BASE_URL, STORAGE_DATA, EXPIRED_ACCESS_TOKEN,
                                         CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 401
    # ACCESS DENIED


def test_storage_api_missing_access_token():
    headers = {'Content-Type': CONTENT_TYPE_APPLICATION_JSON}
    res = requests.post(url=BASE_URL + STORAGE_END_POINT, data=json.dumps(STORAGE_DATA), headers=headers)
    print(res)
    assert res.status_code == 401


def test_storage_api_blank_auth_key():
    headers = {'Authorization': '', 'Content-Type': CONTENT_TYPE_APPLICATION_JSON}
    res = requests.post(url=BASE_URL + STORAGE_END_POINT, data=json.dumps(STORAGE_DATA), headers=headers)
    print(res)
    assert res.status_code == 401


# @pytest.mark.storage_api
def test_storage_api_request_extra_key_added():
    D_CP = STORAGE_DATA.copy()
    DATA = helper.update_dictionary(D_CP, test='test')
    status, data = API_Calls.storage_api(BASE_URL, DATA, BASE_TOKEN,
                                         CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 401


def test_storage_api_Content_type_header_missing():
    headers1 = {'Authorization': BASE_TOKEN}
    r = requests.post(BASE_URL + '/storage/files', data=json.dumps(STORAGE_DATA), headers=headers1)
    print(r)
    assert r.status_code == 401


def test_storage_api_contentType_header_value_missing():
    headers = {'Authorization': BASE_TOKEN, 'content-type': ''}
    r = requests.post(BASE_URL + '/storage/files', data=json.dumps(STORAGE_DATA), headers=headers)
    print(r)
    assert r.status_code == 401


def test_storage_api_request_body_countryCode_key_blank():
    D_CP = STORAGE_DATA.copy()
    DATA = helper.update_dictionary(D_CP, countryCode='')
    status, data = API_Calls.storage_api(BASE_URL, DATA, ACCESS_TOKEN,
                                         CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 400


# @pytest.mark.storage_api
def test_storage_api_request_body_countryCode_invalid():
    D_CP = STORAGE_DATA.copy()
    DATA = helper.update_dictionary(D_CP, countryCode='xyz')
    status, data = API_Calls.storage_api(BASE_URL, DATA, ACCESS_TOKEN,
                                         CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 422


def test_storage_api_request_body_countryCode_key_missing():
    D_CP = STORAGE_DATA.copy()
    DATA = helper.delete_key(D_CP, 'countryCode')
    status, data = API_Calls.storage_api(BASE_URL, DATA, ACCESS_TOKEN,
                                         CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 400


def test_storage_api_request_body_countryCode_not_supported():
    D_CP = STORAGE_DATA.copy()
    DATA = helper.update_dictionary(D_CP, countryCode='UAE')
    status, data = API_Calls.storage_api(BASE_URL, DATA, ACCESS_TOKEN,
                                         CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 422


# @pytest.mark.storage_api
def test_storage_api_request_body_countryCode_not_registered():
    D_CP = STORAGE_DATA.copy()
    DATA = helper.update_dictionary(D_CP, countryCode='DE')
    status, data = API_Calls.storage_api(BASE_URL, DATA, ACCESS_TOKEN_TEST,
                                         CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 403


# @pytest.mark.storage_api
def test_storage_api_request_body_subject_identifier_key_blank():
    D_CP = STORAGE_DATA.copy()
    DATA = helper.update_dictionary(D_CP, userIdentifier='')
    status, data = API_Calls.storage_api(BASE_URL, DATA, ACCESS_TOKEN,
                                         CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 400


def test_storage_api_request_body_subject_identifier_key_invalid():
    D_CP = STORAGE_DATA.copy()
    DATA = helper.update_dictionary(D_CP, userIdentifier='xyz')
    status, data = API_Calls.storage_api(BASE_URL, DATA, ACCESS_TOKEN,
                                         CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 400


def test_storage_api_request_body_subject_identifier_key_missing():
    D_CP = STORAGE_DATA.copy()
    DATA = helper.delete_key(D_CP, 'userIdentifier')
    status, data = API_Calls.storage_api(BASE_URL, DATA, ACCESS_TOKEN,
                                         CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 400


def test_storage_api_request_body_file_type_key_blank():
    D_CP = STORAGE_DATA.copy()
    DATA = helper.update_dictionary(D_CP, fileType='')
    status, data = API_Calls.storage_api(BASE_URL, DATA, ACCESS_TOKEN,
                                         CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 400


def test_storage_api_request_body_file_type_key_invalid():
    D_CP = STORAGE_DATA.copy()
    DATA = helper.update_dictionary(D_CP, fileType='XYZ')
    status, data = API_Calls.storage_api(BASE_URL, DATA, ACCESS_TOKEN,
                                         CONTENT_TYPE_URL_ENCODED)
    print(status, data)
    assert status == 415


def test_storage_api_request_body_file_type_key_missing():
    D_CP = STORAGE_DATA.copy()
    DATA = helper.delete_key(D_CP, 'fileType')
    status, data = API_Calls.storage_api(BASE_URL, DATA, ACCESS_TOKEN,
                                         CONTENT_TYPE_URL_ENCODED)
    print(status, data)
    assert status == 415


def test_storage_api_request_body_file_type_key_unsupported():
    D_CP = STORAGE_DATA.copy()
    DATA = helper.update_dictionary(D_CP, fileType='txt')
    status, data = API_Calls.storage_api(BASE_URL, DATA, ACCESS_TOKEN,
                                         CONTENT_TYPE_URL_ENCODED)
    print(status, data)
    assert status == 415


def test_storage_api_incorrect_file_type():
    D_CP = STORAGE_DATA.copy()
    DATA = helper.update_dictionary(D_CP, fileType='txt')
    status, data = API_Calls.storage_api(BASE_URL, DATA, ACCESS_TOKEN,
                                         CONTENT_TYPE_URL_ENCODED)
    print(status, data)
    assert status == 415


def test_storage_api_with_put_request():
    headers_storage = {'Authorization': ACCESS_TOKEN, 'Content-Type': CONTENT_TYPE_APPLICATION_JSON}
    res = requests.put(BASE_URL + '/storage/files', data=json.dumps(STORAGE_DATA), headers=headers_storage)
    print(res)
    assert res.status_code == 403


def test_storage_api_with_get_request():
    headers_storage = {'Authorization': ACCESS_TOKEN, 'Content-Type': CONTENT_TYPE_APPLICATION_JSON}
    res = requests.get(BASE_URL + '/storage/files', data=json.dumps(STORAGE_DATA), headers=headers_storage)
    print(res)
    assert res.status_code == 403


def test_storage_api_with_multiple_variable_missing():
    D_CP = STORAGE_DATA.copy()
    for key in range(0, 5):
        DATA = helper.get_random_pairs(D_CP)
        status, data = API_Calls.storage_api(BASE_URL, DATA, ACCESS_TOKEN,
                                             CONTENT_TYPE_APPLICATION_JSON)
        print(status, data)
        assert status == 400


# # ==================================== GET QUESIONNAIRE ID===============================================================================================
#

def test_questionnaire_id_for_measure_authentication_header_missing():
    headers_get = {'Authorization': ''}
    res_get = requests.get(url=BASE_URL + '/measures/name/' + MEASURE_NAME, headers=headers_get)
    print(res_get)
    assert res_get.status_code == 401


def test_questionnaire_id_for_measure_incorrect_access_token():
    status, data = API_Calls.get_questionnaire_ID_required_for_measure(BASE_URL, MEASURE_NAME, INVALID_ACCESS_TOKEN)
    print(status, data)
    assert status == 401


def test_questionnaire_id_for_measure_access_token_with_bearer_in_small_case():
    ACCESS_TOKEN_BEARER1 = 'bearer ' + ACCESS_TOKEN
    print(ACCESS_TOKEN_BEARER1)
    status, data = API_Calls.get_questionnaire_ID_required_for_measure(BASE_URL, MEASURE_NAME, ACCESS_TOKEN_BEARER1)
    print(status, data)
    assert status == 401


def test_questionnaire_id_for_incorrect_measure_name():
    INCORRECT_MEASURE_NAME = 'XYZ'
    status, data = API_Calls.get_questionnaire_ID_required_for_measure(BASE_URL, INCORRECT_MEASURE_NAME,
                                                                       ACCESS_TOKEN)
    print(status, data)
    assert status == 404


# --------------------------------------------------------------------------------------------
header_get_questionnaire = {'Authorization': ACCESS_TOKEN}
parameters = {'language': QUESTIONNAIRE_LANGUAGES}


def test_get_questionnaire_with_authentication_header_missing():
    headers = {'Authorization': ''}
    res_get = requests.get(url=BASE_URL + '/questionnaires/' + QUESTIONNAIRE_ID, headers=headers, params=parameters)
    print(res_get)
    assert res_get.status_code == 401

def test_get_questionnaire_with_access_token_in_small_case():
    ACCESS_TOKEN_BEARER1 = 'bearer ' + ACCESS_TOKEN
    print(ACCESS_TOKEN_BEARER1)
    headers = {'Authorization': ACCESS_TOKEN_BEARER1}
    res_get = requests.get(url=BASE_URL + '/questionnaires/' + QUESTIONNAIRE_ID, headers=headers, params=parameters)
    print(res_get)
    assert res_get.status_code == 401


def test_get_questionnaire_with_language_parameter_missing():
    res = requests.get(url=BASE_URL + '/questionnaires/' + QUESTIONNAIRE_ID,
                       headers=header_get_questionnaire)
    print(res)
    assert res.status_code == 400


def test_get_questionnaire_with_incorrect_language_parameter():
    param = helper.update_dictionary(parameters, language='hindi')
    res = requests.get(url=BASE_URL + '/questionnaires/' + QUESTIONNAIRE_ID, params=param,
                       headers=header_get_questionnaire)
    print(res)
    assert res.status_code == 404


def test_get_questionnaire_with_incorrect_questionnaire_id():
    INCORRECT_QUESTIONNAIRE_ID = 'XYZ'
    res = requests.get(url=BASE_URL + '/questionnaires/' + INCORRECT_QUESTIONNAIRE_ID,
                       headers=header_get_questionnaire)
    print(res)
    assert res.status_code == 400


#
# # # -----------------------------------------------------------------------------------------------------

header_submit_questionnaire = {'Authorization': ACCESS_TOKEN, 'Content-Type': CONTENT_TYPE_APPLICATION_JSON}

QUESTIONNAIRE_BODY = {
    "questionnaire": {
        "id": QUES_ID,
        "language": LANGUAGE,
        "userIdentifier": SUB_IDENTIFIER,
        "respondedAt": "1994-11-05T13:15:30Z",
        "questionResponses": [
            {
                "optionIndex": 1
            },
            {
                "optionIndexes": [
                    0,
                    2
                ]
            },
            {
                "isSkipped": True
            },
            {
                "response": "36C"
            }
        ]
    }
}


def test_submit_questionnaire_response_with_authentication_header_missing():
    header = {'Content-Type': CONTENT_TYPE_APPLICATION_JSON}
    response = requests.post(url=BASE_URL + '/questionnaire-responses', data=json.dumps(QUESTIONNAIRE_BODY),
                             headers=header)
    print(response)
    assert response.status_code == 401


def test_submit_questionnaire_response_with_incorrect_access_token():
    header = {'Authorization': 'XYZ', 'Content-Type': CONTENT_TYPE_APPLICATION_JSON}
    response = requests.post(url=BASE_URL + '/questionnaire-responses', data=json.dumps(QUESTIONNAIRE_BODY),
                             headers=header)
    print(response)
    assert response.status_code == 401

def test_submit_questionnaire_response_with_access_token_with_bearer_in_small_case():
    ACCESS_TOKEN_BEARER1 = 'bearer ' + ACCESS_TOKEN
    print(ACCESS_TOKEN_BEARER1)
    header = {'Authorization': ACCESS_TOKEN_BEARER1, 'Content-Type': CONTENT_TYPE_APPLICATION_JSON}
    response = requests.post(url=BASE_URL + '/questionnaire-responses', data=json.dumps(QUESTIONNAIRE_BODY),
                                 headers=header)
    print(response)
    assert response.status_code == 401


def test_submit_questionnaire_response_with_incorrect_id():
    D_CP = QUESTIONNAIRE_BODY['questionnaire'].copy()
    D = helper.update_dictionary(D_CP, id=123)
    DATA = {'questionnaire': D}
    status, data = API_Calls.submit_questionnaire_response(BASE_URL, DATA, ACCESS_TOKEN)
    print(status, data)
    assert status == 400


def test_submit_questionnaire_response_with_incorrect_language_key():
    D_CP = QUESTIONNAIRE_BODY['questionnaire'].copy()
    D = helper.update_dictionary(D_CP, language='Tamil')
    DATA = {'questionnaire': D}
    status, data = API_Calls.submit_questionnaire_response(BASE_URL, DATA, ACCESS_TOKEN)
    print(status, data)
    assert status == 404


def test_submit_questionnaire_response_with_incorrect_userIdentifier():
    D_CP = QUESTIONNAIRE_BODY['questionnaire'].copy()
    D = helper.update_dictionary(D_CP, userIdentifier="XYZ")
    DATA = {'questionnaire': D}
    status, data = API_Calls.submit_questionnaire_response(BASE_URL, DATA, ACCESS_TOKEN)
    print(status, data)
    assert status == 400


def test_submit_questionnaire_response_with_incorrect_questionResponses():
    D_CP = QUESTIONNAIRE_BODY['questionnaire'].copy()
    D = helper.update_dictionary(D_CP, questionResponses={})
    DATA = {'questionnaire': D}
    status, data = API_Calls.submit_questionnaire_response(BASE_URL, DATA, ACCESS_TOKEN)
    print(status, data)
    assert status == 400


def test_submit_questionnaire_response_with_multiple_variable_missing():
    D_CP = QUESTIONNAIRE_BODY['questionnaire'].copy()
    n = helper.factorial(len(D_CP))
    for key in range(n):
        D = helper.get_random_pairs(D_CP)
        DATA = {'questionnaire': D}
        status, data = API_Calls.submit_questionnaire_response(BASE_URL, DATA, ACCESS_TOKEN)
        print(status, data)
        assert status == 400


#
# ##################################################################################

def test_submit_questionnaire_response_with_id_missing():
    D_CP = QUESTIONNAIRE_BODY['questionnaire'].copy()
    D = helper.delete_key(D_CP, 'id')
    DATA = {'questionnaire': D}
    status, data = API_Calls.submit_questionnaire_response(BASE_URL, DATA, ACCESS_TOKEN)
    print(status, data)
    assert status == 400


def test_submit_questionnaire_response_with_language_missing():
    D_CP = QUESTIONNAIRE_BODY['questionnaire'].copy()
    D = helper.delete_key(D_CP, 'language')
    DATA = {'questionnaire': D}
    status, data = API_Calls.submit_questionnaire_response(BASE_URL, DATA, ACCESS_TOKEN)
    print(status, data)
    assert status == 400


def test_submit_questionnaire_response_with_userIdentifier_missing():
    D_CP = QUESTIONNAIRE_BODY['questionnaire'].copy()
    D = helper.delete_key(D_CP, 'userIdentifier')
    DATA = {'questionnaire': D}
    status, data = API_Calls.submit_questionnaire_response(BASE_URL, DATA, ACCESS_TOKEN)
    print(status, data)
    assert status == 400


def test_submit_questionnaire_response_with_questionResponses_missing():
    D_CP = QUESTIONNAIRE_BODY['questionnaire'].copy()
    D = helper.delete_key(D_CP, 'questionResponses')
    DATA = {'questionnaire': D}
    status, data = API_Calls.submit_questionnaire_response(BASE_URL, DATA, ACCESS_TOKEN)
    print(status, data)
    assert status == 400


def test_submit_questionnaire_response_with_extra_field_added():
    D_CP = QUESTIONNAIRE_BODY.copy()
    DATA = helper.update_dictionary(D_CP, test='test')
    status, data = API_Calls.submit_questionnaire_response(BASE_URL, DATA, ACCESS_TOKEN)
    print(status, data)
    assert status == 400


def test_submit_questionnaire_response_with_option_index_missing():
    raw_data = generate_questionnaire_raw_data(MISSING_REQUIRED_FIELDS)
    status, data = API_Calls.submit_questionnaire_response(BASE_URL, raw_data, ACCESS_TOKEN)
    print(status, data)
    assert status == 422


def test_submit_questionnaire_response_with_extra_field_added_to_questionResponses():
    raw_data = generate_questionnaire_raw_data(EXTRA_FIELD_ADDED)
    status, data = API_Calls.submit_questionnaire_response(BASE_URL, raw_data, ACCESS_TOKEN)
    print(status, data)
    assert status == 422


def test_submit_questionnaire_response_with_incorrect_skip_value():
    raw_data = generate_questionnaire_raw_data(SKIPPED_OPPOSITE)
    status, data = API_Calls.submit_questionnaire_response(BASE_URL, raw_data, ACCESS_TOKEN)
    print(status, data)
    assert status == 422


def test_submit_questionnaire_response_with_list_type_value_instead_of_dictionary():
    raw_data = generate_questionnaire_raw_data(LIST_INSTEAD_OF_DICT)
    status, data = API_Calls.submit_questionnaire_response(BASE_URL, raw_data, ACCESS_TOKEN)
    print(status, data)
    assert status == 400


def test_submit_questionnaire_response_with_extra_value_added_to_option_index():
    raw_data = generate_questionnaire_raw_data(EXTRA_VALUE_OPTION_INDEX)
    status, data = API_Calls.submit_questionnaire_response(BASE_URL, raw_data, ACCESS_TOKEN)
    print(status, data)
    assert status == 422


def test_submit_questionnaire_response_with_jumbled_sequences_of_keys():
    raw_data = generate_questionnaire_raw_data(JUMBLED_SEQUENCE)
    status, data = API_Calls.submit_questionnaire_response(BASE_URL, raw_data, ACCESS_TOKEN)
    print(status, data)
    assert status == 422


def test_submit_questionnaire_response_with_other_temperature_units():
    raw_data = generate_questionnaire_raw_data(OTHER_TEMPERATURE_UNIT)
    status, data = API_Calls.submit_questionnaire_response(BASE_URL, raw_data, ACCESS_TOKEN)
    print(status, data)
    assert status == 422


def test_submit_questionnaire_response_with_incorrect_data_type_of_text_field():
    raw_data = generate_questionnaire_raw_data(STRING_INSTEAD_OF_INT)
    status, data = API_Calls.submit_questionnaire_response(BASE_URL, raw_data, ACCESS_TOKEN)
    print(status, data)
    assert status == 422


# ----------------------------------------------------------------------------------------------------------

headers_scores = {'Authorization': ACCESS_TOKEN, 'Content-Type': CONTENT_TYPE_APPLICATION_JSON}


VALID_SCORE_DATA = {
    "userIdentifier": SUB_IDENTIFIER,
    "filePath": FILE_PATH,
    "questionnaireResponseId": QUESTIONNAIRE_RESPONSE_ID,
    "measureName": MEASURE_NAME
}

VALID_SCORE_DATA_WQ = {
    "filePath": FILE_PATH,
    "measureName": MEASURE_NAME_WQ
}




def test_score_api_invalid_end_point():
    INVALID_END_POINT = 'XYZ'
    res = requests.post(url=BASE_URL + INVALID_END_POINT, data=json.dumps(VALID_SCORE_DATA), headers=headers_scores)
    print(res)
    assert res.status_code == 403


def test_score_api_incorrect_access_token():
    INCORRECT_ACCESS_TOKEN = 'xyz'
    status, data = API_Calls.score_api(BASE_URL, VALID_SCORE_DATA, INCORRECT_ACCESS_TOKEN,
                                       CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 401
    # ACCESS DENIED
    # status code == 403


def test_score_api_expired_access_token():
    status, data = API_Calls.score_api(BASE_URL, VALID_SCORE_DATA, EXPIRED_ACCESS_TOKEN,
                                       CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 401
    # ACCESS DENIED

def test_score_api_with_bearer_in_small_case():
    ACCESS_TOKEN_BEARER1 = 'bearer ' + ACCESS_TOKEN
    print(ACCESS_TOKEN_BEARER1)
    status, data = API_Calls.score_api(BASE_URL, VALID_SCORE_DATA, ACCESS_TOKEN_BEARER1,
                                           CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 401
    ACCESS_TOKEN_BEARER1 = 'bearer ' + ACCESS_TOKEN
    print(ACCESS_TOKEN_BEARER1)


def test_score_api_missing_access_token():
    headers = {'Content-Type': CONTENT_TYPE_APPLICATION_JSON}
    res = requests.post(url=BASE_URL + SCORE_END_POINT, data=json.dumps(VALID_SCORE_DATA), headers=headers)
    print(res)
    assert res.status_code == 401


def test_score_api_blank_auth_key():
    headers = {'Authorization': '', 'Content-Type': CONTENT_TYPE_APPLICATION_JSON}
    res = requests.post(url=BASE_URL + SCORE_END_POINT, data=json.dumps(VALID_SCORE_DATA), headers=headers)
    print(res)
    assert res.status_code == 401


def test_score_api_request_body_subjectIdentifier_key_blank():
    D_CP = VALID_SCORE_DATA.copy()
    DATA = helper.update_dictionary(D_CP, userIdentifier='')
    status, data = API_Calls.score_api(BASE_URL, DATA, ACCESS_TOKEN,
                                       CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 400


def test_score_api_request_body_subjectIdentifier_key_invalid():
    D_CP = VALID_SCORE_DATA.copy()
    DATA = helper.update_dictionary(D_CP, userIdentifier='ar123')
    status, data = API_Calls.score_api(BASE_URL, DATA, ACCESS_TOKEN,
                                       CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 404


def test_score_api_request_body_subjectIdentifier_key_invalid_data_type():
    D_CP = VALID_SCORE_DATA.copy()
    DATA = helper.update_dictionary(D_CP, userIdentifier='Text')
    status, data = API_Calls.score_api(BASE_URL, DATA, ACCESS_TOKEN,
                                       CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 404


# @pytest.mark.score_api
def test_score_api_request_body_fileLocation_key_blank():
    D_CP = VALID_SCORE_DATA.copy()
    DATA = helper.update_dictionary(D_CP, filePath='')
    status, data = API_Calls.score_api(BASE_URL, DATA, ACCESS_TOKEN,
                                       CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 400


# @pytest.mark.score_api
def test_score_api_request_body_fileLocation_key_invalid():
    D_CP = VALID_SCORE_DATA.copy()
    DATA = helper.update_dictionary(D_CP, filePath='XYZ')
    status, data = API_Calls.score_api(BASE_URL, DATA, ACCESS_TOKEN,
                                       CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 404


# @pytest.mark.score_api
def test_score_api_request_body_fileLocation_key_missing():
    D_CP = VALID_SCORE_DATA.copy()
    DATA = helper.delete_key(D_CP, 'filePath')
    status, data = API_Calls.score_api(BASE_URL, DATA, ACCESS_TOKEN,
                                       CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 400


def test_score_api_request_body_fileLocation_with_no_audio_file():
    D_CP = VALID_SCORE_DATA.copy()
    DATA = helper.update_dictionary(D_CP, filePath=NO_AUDIO_FILE_ON_GIVEN_FILE_PATH)
    status, data = API_Calls.score_api(BASE_URL, DATA, ACCESS_TOKEN,
                                       CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 404


def test_score_api_request_body_fileLocation_with_incorrect_file_present():
    D_CP = VALID_SCORE_DATA.copy()
    DATA = helper.update_dictionary(D_CP, filePath=FILE_PATH_WITH_INVALID_FILE)
    status, data = API_Calls.score_api(BASE_URL, DATA, ACCESS_TOKEN,
                                       CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 422


# @pytest.mark.score_api
def test_score_api_request_body_measureName_key_blank():
    D_CP = VALID_SCORE_DATA.copy()
    DATA = helper.update_dictionary(D_CP, measureName='')
    status, data = API_Calls.score_api(BASE_URL, DATA, ACCESS_TOKEN,
                                       CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 400


# @pytest.mark.score_api
def test_score_api_request_body_measureName_key_invalid():
    D_CP = VALID_SCORE_DATA.copy()
    DATA = helper.update_dictionary(D_CP, measureName='XYZ')
    status, data = API_Calls.score_api(BASE_URL, DATA, ACCESS_TOKEN,
                                       CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 404


# @pytest.mark.score_api
def test_score_api_request_body_measureName_key_missing():
    D_CP = VALID_SCORE_DATA.copy()
    DATA = helper.delete_key(D_CP, 'measureName')
    status, data = API_Calls.score_api(BASE_URL, DATA, ACCESS_TOKEN,
                                       CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 400


# @pytest.mark.score_api
def test_score_api_request_body_questionnaire_response_id_key_blank():
    D_CP = VALID_SCORE_DATA.copy()
    DATA = helper.update_dictionary(D_CP, questionnaireResponseId='')
    status, data = API_Calls.score_api(BASE_URL, DATA, ACCESS_TOKEN,
                                       CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 400


# @pytest.mark.score_api
def test_score_api_request_body_questionnaire_response_id_key_invalid():
    D_CP = VALID_SCORE_DATA.copy()
    DATA = helper.update_dictionary(D_CP, questionnaireResponseId='XYZ')
    status, data = API_Calls.score_api(BASE_URL, DATA, ACCESS_TOKEN,
                                       CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 404


def test_score_api_request_extra_key_added():
    D_CP = VALID_SCORE_DATA.copy()
    DATA = helper.update_dictionary(D_CP, test='XYZ')
    status, data = API_Calls.score_api(BASE_URL, DATA, ACCESS_TOKEN,
                                       CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 400


# @pytest.mark.score_api
def test_score_api_content_type_header_missing():
    header1 = {'Authorization': ACCESS_TOKEN}
    r = requests.post(BASE_URL + SCORE_END_POINT, data=VALID_SCORE_DATA, headers=header1)
    assert r.status_code == 415


# @pytest.mark.score_api
def test_score_api_contentType_header_value_invalid():
    status, data = API_Calls.score_api(BASE_URL, VALID_SCORE_DATA, ACCESS_TOKEN, CONTENT_TYPE_URL_ENCODED)
    print(status, data)
    assert status == 415



def test_score_api_with_multiple_variable_missing():
    D_CP = VALID_SCORE_DATA_WQ.copy()
    for key in range(0, 4):
        DATA = helper.get_random_pairs(D_CP)
        status, data = API_Calls.score_api(BASE_URL, DATA, ACCESS_TOKEN,
                                           CONTENT_TYPE_APPLICATION_JSON)
        print(status, data)
        assert status == 400






