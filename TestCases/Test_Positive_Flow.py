import json
import pytest
from TestCases import API_Calls
from TestCases.Support import assertion
from Variables.variable import *
from TestCases.Support import helper
import time



# ---------------- Get the Base64 --------------------------------#

base64secrets = helper.get_base64secrets(CLIENT_ID_Shruti, CLIENT_SECRET_Shruti)
print(base64secrets)

BASE_TOKEN = 'Basic ' + base64secrets


# ----------- Get the ACCESS TOKEN ----------------------------#

status_code, json_data = API_Calls.token_api(BASE_URL, VALID_TOKEN_DATA, BASE_TOKEN, CONTENT_TYPE_URL_ENCODED)
ACCESS_TOKEN = json_data['access_token']

# ---------------- Get the Base64  for without questionnaire client credentials --------------------------------#
#
base64secretswq = helper.get_base64secrets(CLIENT_ID_WQ, CLIENT_SECRET_WQ)
print(base64secretswq)

BASE_TOKEN_WQ = 'Basic ' + base64secrets
#
# # ----------- Get the ACCESS TOKEN for without questionnaire client credentials  ----------------------------#
#
status_code, json_data = API_Calls.token_api(BASE_URL, VALID_TOKEN_DATA, BASE_TOKEN_WQ, CONTENT_TYPE_URL_ENCODED)
ACCESS_TOKEN_WQ = json_data['access_token']

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


VALID_STORAGE_DATA_IN = {
    "fileType": "wav",
    "countryCode": "IN",
    "userIdentifier": SUB_IDENTIFIER
}


status_code, response_json = API_Calls.storage_api(BASE_URL, VALID_STORAGE_DATA_IN, ACCESS_TOKEN,
                                                   CONTENT_TYPE_APPLICATION_JSON)

STORAGE_SIGNED_URL_IN = response_json['signedURL']
FILE_PATH_IN = response_json['filePath']


VALID_STORAGE_DATA_DE = {
    "fileType": "wav",
    "countryCode": "DE",
    "userIdentifier": SUB_IDENTIFIER
}



status_code, response_json = API_Calls.storage_api(BASE_URL, VALID_STORAGE_DATA_DE, ACCESS_TOKEN,
                                                   CONTENT_TYPE_APPLICATION_JSON)

STORAGE_SIGNED_URL_DE = response_json['signedURL']
FILE_PATH_DE = response_json['filePath']



# ____________________UPLOAD THE AUDIO SAMPLE  ____________________________________________#


#AUDIO_FILE_PATH = 'C:\\Users\\GS-1329\\Downloads\\File_1_6sec.wav'


AUDIO_FILE_PATH = 'C:\\Users\\GS-1431\\Downloads\\ahh_SK.wav'
#AUDIO_FILE_PATH = 'C:\\Users\\GS-1329\\Downloads\\1__7FC800CA-456C-4CA2-A568-DE6A96E54705_7251_9067.wav'

status_code = API_Calls.upload_sample_file(STORAGE_SIGNED_URL, AUDIO_FILE_PATH)
status_code = API_Calls.upload_sample_file(STORAGE_SIGNED_URL_IN, AUDIO_FILE_PATH)
status_code = API_Calls.upload_sample_file(STORAGE_SIGNED_URL_DE, AUDIO_FILE_PATH)
# --------------------------------- GET ALL MEASURES- ------------------------------------------------------------#
status, response_json = API_Calls.measures_api(BASE_URL, ACCESS_TOKEN)
MEASURE_ID = response_json['measures'][0]['id']

# ------------------------------GET THE QUESTIONNAIRE ID BY USING MEASURE ----------------------------------------#

MEASURE_NAME = 'respiratory-symptoms-risk'

status, response_json = API_Calls.get_questionnaire_ID_required_for_measure(BASE_URL, MEASURE_NAME, ACCESS_TOKEN)

QUESTIONNAIRE_ID = response_json['questionnaire']['id']
QUESTIONNAIRE_LANGUAGES = response_json['questionnaire']['languages'][0]

# -------------------------------GET THE QUESTIONNAIRE -------------------------------------------------

status, response_json = API_Calls.get_questionnaire_required_for_measure(BASE_URL, QUESTIONNAIRE_ID,
                                                                         QUESTIONNAIRE_LANGUAGES, ACCESS_TOKEN)
QUES_ID = response_json['id']
LANGUAGE = response_json['language']

# ------------------------------SUBMIT THE QUESTIONNAIRE RESPONSE------------------------------------------
#Sachin's questionnaire response
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


#Shruti questionnaire response
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


QUESTIONNAIRE_BODY_SKIP_ENABLED = {
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
                 "isSkipped": True
             }

        ]
    }
}

# QUESTIONNAIRE_BODY_SKIP_ENABLED = {
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
#                 "isSkipped": True
#             },
#             {
#                 "response": "104F"
#             }
#         ]
#     }
# }

status, response_json = API_Calls.submit_questionnaire_response(BASE_URL, QUESTIONNAIRE_BODY, ACCESS_TOKEN)
print(status, response_json)

QUESTIONNAIRE_RESPONSE_ID = response_json['id']

# ---------------------------- GET THE SCORE --------------------------------#

VALID_SCORE_DATA = {
    "userIdentifier": SUB_IDENTIFIER,
    "filePath": FILE_PATH,
    "questionnaireResponseId": QUESTIONNAIRE_RESPONSE_ID,
    "measureName": MEASURE_NAME
}


VALID_SCORE_DATA_IN = {
    "userIdentifier": SUB_IDENTIFIER,
    "filePath": FILE_PATH_IN,
    "questionnaireResponseId": QUESTIONNAIRE_RESPONSE_ID,
    "measureName": MEASURE_NAME
}


VALID_SCORE_DATA_DE = {
    "userIdentifier": SUB_IDENTIFIER,
    "filePath": FILE_PATH_DE,
    "questionnaireResponseId": QUESTIONNAIRE_RESPONSE_ID,
    "measureName": MEASURE_NAME
}


#-------------------------------------------------------------------------------------------------------------------
#------------------------------------------- Test Cases --------------------------------------------------------- #


def test_token_api():
    status, data = API_Calls.token_api(BASE_URL, VALID_TOKEN_DATA, BASE_TOKEN, CONTENT_TYPE_URL_ENCODED)
    assert status == 200
    print(status, data)
    assertion.assert_valid_schema(data, 'token_schema.json')


def test_subject_api():
    status, data = API_Calls.subject_api(BASE_URL, VALID_SUBJECT_DATA, ACCESS_TOKEN, CONTENT_TYPE_APPLICATION_JSON)
    assert status == 201
    print(status, data)
    assertion.assert_valid_schema(data, 'subject_schema.json')


def test_subject_api_access_token_with_bearer():
    ACCESS_TOKEN_BEARER = 'Bearer ' + ACCESS_TOKEN
    print (ACCESS_TOKEN_BEARER)
    status, data = API_Calls.subject_api(BASE_URL, VALID_SUBJECT_DATA, ACCESS_TOKEN_BEARER, CONTENT_TYPE_APPLICATION_JSON)
    assert status == 201
    print(status, data)
    assertion.assert_valid_schema(data, 'subject_schema.json')

def test_subject_v2_api():
    status, data = API_Calls.subject_api(BASE_URL_V2, VALID_SUBJECT_DATA_V2, ACCESS_TOKEN, CONTENT_TYPE_APPLICATION_JSON)
    assert status == 201
    print(status, data)
    assertion.assert_valid_schema(data, 'subject_v2.json')


def test_subject_v2_api_access_token_with_bearer():
    ACCESS_TOKEN_BEARER = 'Bearer ' + ACCESS_TOKEN
    print(ACCESS_TOKEN_BEARER)
    status, data = API_Calls.subject_api(BASE_URL_V2, VALID_SUBJECT_DATA_V2, ACCESS_TOKEN, CONTENT_TYPE_APPLICATION_JSON)
    assert status == 201
    print(status, data)
    assertion.assert_valid_schema(data, 'subject_v2.json')



def test_subject_v2_api_with_unknown_gender_inlowercase():
    D_CP = VALID_SUBJECT_DATA_V2.copy()
    DATA = helper.update_dictionary(D_CP, gender="unknown")
    print(DATA)
    status, data = API_Calls.subject_api(BASE_URL_V2, DATA, ACCESS_TOKEN,
                                         CONTENT_TYPE_APPLICATION_JSON)
    assert status == 201
    print(status, data)
    assertion.assert_valid_schema(data, 'subject_v2.json')

def test_subject_v2_api_with_unknown_incaps_gender():
    D_CP = VALID_SUBJECT_DATA_V2.copy()
    DATA = helper.update_dictionary(D_CP, gender="UNKNOWN")
    print(DATA)
    status, data = API_Calls.subject_api(BASE_URL_V2, DATA, ACCESS_TOKEN,
                                         CONTENT_TYPE_APPLICATION_JSON)
    assert status == 201
    print(status, data)
    assertion.assert_valid_schema(data, 'subject_v2.json')

def test_subject_v2_api_with_unknown_in_uppercase_yearOfBirth():
    D_CP = VALID_SUBJECT_DATA_V2.copy()
    DATA = helper.update_dictionary(D_CP, yearOfBirth="UNKNOWN")
    print(DATA)
    status, data = API_Calls.subject_api(BASE_URL_V2, DATA, ACCESS_TOKEN,
                                         CONTENT_TYPE_APPLICATION_JSON)
    assert status == 201
    print(status, data)
    assertion.assert_valid_schema(data, 'subject_v2.json')

def test_subject_v2_api_with_unknown_inlowercase_yearOfBirth():
    D_CP = VALID_SUBJECT_DATA_V2.copy()
    DATA = helper.update_dictionary(D_CP, yearOfBirth="unknown")
    print(DATA)
    status, data = API_Calls.subject_api(BASE_URL_V2, DATA, ACCESS_TOKEN,
                                         CONTENT_TYPE_APPLICATION_JSON)
    assert status == 201
    print(status, data)
    assertion.assert_valid_schema(data, 'subject_v2.json')

def test_subject_v2_api_with_unknown_device_in_uppercase():
    status, data = API_Calls.subject_api(BASE_URL_V2, VALID_SUBJECT_DATA_DEVICE_UNKNOWN, ACCESS_TOKEN, CONTENT_TYPE_APPLICATION_JSON)
    assert status == 201
    print(status, data)
    assertion.assert_valid_schema(data, 'subject_v2_unknown_schema.json')

def test_subject_v2_api_unknown_device_in_lowercase():
    status, data = API_Calls.subject_api(BASE_URL_V2, SUBJECT_DATA_1, ACCESS_TOKEN, CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 201
    assertion.assert_valid_schema(data, 'subject_v2_unknown_schema.json')

def test_subject_v2_api_with_unknown_device_yob_gender_in_caps():
    status, data = API_Calls.subject_api(BASE_URL_V2, VALID_SUBJECT_DATA_ALL_M_UNKNOWN, ACCESS_TOKEN, CONTENT_TYPE_APPLICATION_JSON)
    assert status == 201
    print(status, data)
    assertion.assert_valid_schema(data, 'subject_v2_unknown_schema.json')


def test_subject_v2_api_unknown_in_lowercase_device_yob_gender():
    status, data = API_Calls.subject_api(BASE_URL_V2, VALID_SUBJECT_DATA_ALL_M_UNKNOWN_IN_SMALL, ACCESS_TOKEN, CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 201
    assertion.assert_valid_schema(data, 'subject_v2_unknown_schema.json')

def test_update_subject_data_api():
    status, data = API_Calls.update_subject_details(BASE_URL, SUB_IDENTIFIER, UPDATE_SUBJECT_DATA, ACCESS_TOKEN)
    print(status, data)
    assert status == 200

def test_update_subject_data_api_with_access_token_bearer():
    ACCESS_TOKEN_BEARER = 'Bearer ' + ACCESS_TOKEN
    print(ACCESS_TOKEN_BEARER)
    status, data = API_Calls.update_subject_details(BASE_URL, SUB_IDENTIFIER, UPDATE_SUBJECT_DATA, ACCESS_TOKEN_BEARER)
    print(status, data)
    assert status == 200



def test_storage_api():
    status, data = API_Calls.storage_api(BASE_URL, VALID_STORAGE_DATA, ACCESS_TOKEN, CONTENT_TYPE_APPLICATION_JSON)
    assert status == 201
    print(status, data)
    assertion.assert_valid_schema(data, 'storage_schema.json')

def test_storage_api_with_access_token_bearer():
    ACCESS_TOKEN_BEARER = 'Bearer ' + ACCESS_TOKEN
    print(ACCESS_TOKEN_BEARER)
    status, data = API_Calls.storage_api(BASE_URL, VALID_STORAGE_DATA, ACCESS_TOKEN_BEARER, CONTENT_TYPE_APPLICATION_JSON)
    assert status == 201
    print(status, data)
    assertion.assert_valid_schema(data, 'storage_schema.json')


def test_audio_file_upload():
    status_code = API_Calls.upload_sample_file(STORAGE_SIGNED_URL, AUDIO_FILE_PATH)
    print(status_code)
    assert status_code == 200


def test_get_audio_file():
    FILE_PATH_ENCODED = helper.urlEncoder(FILE_PATH)
    status, response = API_Calls.get_audio_file(BASE_URL, FILE_PATH_ENCODED, ACCESS_TOKEN)
    print(status, response)
    assert status == 200
    assertion.assert_valid_schema(response, 'get_audio_file.json')

def test_get_audio_file_with_access_token_bearer():
    ACCESS_TOKEN_BEARER = 'Bearer ' + ACCESS_TOKEN
    print(ACCESS_TOKEN_BEARER)
    FILE_PATH_ENCODED = helper.urlEncoder(FILE_PATH)
    status, response = API_Calls.get_audio_file(BASE_URL, FILE_PATH_ENCODED, ACCESS_TOKEN_BEARER)
    print(status, response)
    assert status == 200
    assertion.assert_valid_schema(response, 'get_audio_file.json')


def test_get_measures_api():
    status, data = API_Calls.measures_api(BASE_URL, ACCESS_TOKEN)
    print(status, data)
    assert status == 200
    assertion.assert_valid_schema(data, 'measure_schema.json')


def test_get_measures_api_with_access_token_bearer():
    ACCESS_TOKEN_BEARER = 'Bearer ' + ACCESS_TOKEN
    print(ACCESS_TOKEN_BEARER)
    status, data = API_Calls.measures_api(BASE_URL, ACCESS_TOKEN_BEARER)
    print(status, data)
    assert status == 200
    assertion.assert_valid_schema(data, 'measure_schema.json')


def test_get_measure_by_id():
    status, data = API_Calls.measure_id_api(BASE_URL, MEASURE_ID, ACCESS_TOKEN)
    print(status, data)
    assert status == 200
    assertion.assert_valid_schema(data, 'get_questionnaire_id.json')


def test_get_measure_by_id_with_access_token_bearer():
    ACCESS_TOKEN_BEARER = 'Bearer ' + ACCESS_TOKEN
    print(ACCESS_TOKEN_BEARER)
    status, data = API_Calls.measure_id_api(BASE_URL, MEASURE_ID, ACCESS_TOKEN_BEARER)
    print(status, data)
    assert status == 200
    assertion.assert_valid_schema(data, 'get_questionnaire_id.json')


def test_get_questionnaire_ID_required_for_measure():
    status, data = API_Calls.get_questionnaire_ID_required_for_measure(BASE_URL, MEASURE_NAME, ACCESS_TOKEN)
    print(status, data)
    assert status == 200
    assertion.assert_valid_schema(data, 'get_questionnaire_id.json')

def test_get_questionnaire_ID_required_for_measure_with_access_token_bearer():
    ACCESS_TOKEN_BEARER = 'Bearer ' + ACCESS_TOKEN
    print(ACCESS_TOKEN_BEARER)
    status, data = API_Calls.get_questionnaire_ID_required_for_measure(BASE_URL, MEASURE_NAME, ACCESS_TOKEN_BEARER)
    print(status, data)
    assert status == 200
    assertion.assert_valid_schema(data, 'get_questionnaire_id.json')


def test_get_questionnaire_api():
    status, data = API_Calls.get_questionnaire_required_for_measure(BASE_URL, QUESTIONNAIRE_ID,
                                                                    QUESTIONNAIRE_LANGUAGES, ACCESS_TOKEN)
    print(status, data)
    assert status == 200
    assertion.assert_valid_schema(data, 'get_questionnaire.json')

def test_get_questionnaire_api_with_access_token_bearer():
    ACCESS_TOKEN_BEARER = 'Bearer ' + ACCESS_TOKEN
    print(ACCESS_TOKEN_BEARER)
    status, data = API_Calls.get_questionnaire_required_for_measure(BASE_URL, QUESTIONNAIRE_ID,
                                                                    QUESTIONNAIRE_LANGUAGES, ACCESS_TOKEN_BEARER)
    print(status, data)
    assert status == 200
    assertion.assert_valid_schema(data, 'get_questionnaire.json')


def test_upload_questionnaire_response_api():
    status, data = API_Calls.submit_questionnaire_response(BASE_URL, QUESTIONNAIRE_BODY, ACCESS_TOKEN)
    print(status, data)
    assert status == 201
    assertion.assert_valid_schema(data, 'questionnaire_response.json')


def test_upload_questionnaire_response_api_with_access_token_bearer():
    ACCESS_TOKEN_BEARER = 'Bearer ' + ACCESS_TOKEN
    print(ACCESS_TOKEN_BEARER)
    status, data = API_Calls.submit_questionnaire_response(BASE_URL, QUESTIONNAIRE_BODY, ACCESS_TOKEN_BEARER)
    print(status, data)
    assert status == 201
    assertion.assert_valid_schema(data, 'questionnaire_response.json')


def test_upload_questionnaire_response_api_with_skip_option():
    status, data = API_Calls.submit_questionnaire_response(BASE_URL, QUESTIONNAIRE_BODY_SKIP_ENABLED, ACCESS_TOKEN)
    print(status, data)
    assert status == 201
    assertion.assert_valid_schema(data, 'questionnaire_response.json')


def test_upload_questionnaire_response_api_with_skip_option_with_access_token_bearer():
    ACCESS_TOKEN_BEARER = 'Bearer ' + ACCESS_TOKEN
    print(ACCESS_TOKEN_BEARER)
    status, data = API_Calls.submit_questionnaire_response(BASE_URL, QUESTIONNAIRE_BODY_SKIP_ENABLED, ACCESS_TOKEN_BEARER)
    print(status, data)
    assert status == 201
    assertion.assert_valid_schema(data, 'questionnaire_response.json')


def test_score_api_in():
    status, score_json_data = API_Calls.score_api(BASE_URL, VALID_SCORE_DATA_IN, ACCESS_TOKEN,
                                                  CONTENT_TYPE_APPLICATION_JSON)
    print(status, score_json_data)
    assert status == 200
    assertion.assert_valid_schema(score_json_data, 'score_schema.json')

def test_score_api_in_with_access_token_bearer():
    ACCESS_TOKEN_BEARER = 'Bearer ' + ACCESS_TOKEN
    print(ACCESS_TOKEN_BEARER)
    status, score_json_data = API_Calls.score_api(BASE_URL, VALID_SCORE_DATA_IN, ACCESS_TOKEN_BEARER,
                                                  CONTENT_TYPE_APPLICATION_JSON)
    print(status, score_json_data)
    assert status == 200
    assertion.assert_valid_schema(score_json_data, 'score_schema.json')

def test_score_api_us():
    status, score_json_data = API_Calls.score_api(BASE_URL, VALID_SCORE_DATA, ACCESS_TOKEN,
                                                  CONTENT_TYPE_APPLICATION_JSON)
    print(status, score_json_data)
    assert status == 200
    assertion.assert_valid_schema(score_json_data, 'score_schema.json')



def test_score_api_de():
    status, score_json_data = API_Calls.score_api(BASE_URL, VALID_SCORE_DATA_DE, ACCESS_TOKEN,
                                                  CONTENT_TYPE_APPLICATION_JSON)
    print(status, score_json_data)
    assert status == 200
    assertion.assert_valid_schema(score_json_data, 'score_schema.json')



def test_score_api_subjectIdentifier_optional():
    D_CP = VALID_SCORE_DATA.copy()
    DATA = helper.delete_key(D_CP, 'userIdentifier')
    status, data = API_Calls.score_api(BASE_URL, DATA, ACCESS_TOKEN,
                                       CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 200
    assertion.assert_valid_schema(data, 'score_schema.json')


def test_score_api_questionnaire_response_id_optional():
    #D_CP = VALID_SCORE_DATA.copy()
    #DATA = helper.delete_key(D_CP, 'questionnaireResponseId')
    status, data = API_Calls.score_api(BASE_URL,VALID_SCORE_DATA_WITHOUT_QUESTIONNAIRE, ACCESS_TOKEN_WQ,CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 200
    assertion.assert_valid_schema(data, 'score_schema.json')

def test_get_inference_scores_api_duration():
    status, score_json_data = API_Calls.get_inference_scores_api_duration(BASE_URL,ACCESS_TOKEN)
    print(status, score_json_data)
    assert status == 200


def test_get_inference_scores_api_duration_with_access_token_bearer():
    ACCESS_TOKEN_BEARER = 'Bearer ' + ACCESS_TOKEN
    print(ACCESS_TOKEN_BEARER)
    status, score_json_data = API_Calls.get_inference_scores_api_duration(BASE_URL,ACCESS_TOKEN_BEARER)
    print(status, score_json_data)
    assert status == 200

def test_get_inference_scores_api_userIdentifier():
    status, score_json_data = API_Calls.get_inference_scores_api_userIdentifier(BASE_URL, ACCESS_TOKEN,SUB_IDENTIFIER)
    print(status, score_json_data)
    assert status == 200
    #assertion.assert_valid_schema(score_json_data, 'score_schema.json')

def test_get_inference_scores_api_userIdentifier_with_access_token_bearer():
    ACCESS_TOKEN_BEARER = 'Bearer ' + ACCESS_TOKEN
    print(ACCESS_TOKEN_BEARER)
    status, score_json_data = API_Calls.get_inference_scores_api_userIdentifier(BASE_URL, ACCESS_TOKEN_BEARER,SUB_IDENTIFIER)
    print(status, score_json_data)
    assert status == 200

def test_E2E_use_case_flow_create_ques_api():

    #login with token
    status_code, json_data = API_Calls.token_api(BASE_URL, VALID_TOKEN_DATA, BASE_TOKEN, CONTENT_TYPE_URL_ENCODED)
    print("token api result:",status_code)
    #assert status_code == 200
    ACCESS_TOKEN = json_data['access_token']

    #create subject
    status, subject_json = API_Calls.subject_api(BASE_URL, VALID_SUBJECT_DATA, ACCESS_TOKEN,CONTENT_TYPE_APPLICATION_JSON)
    print("subject api result:",status, subject_json )
    SUB_IDENTIFIER1 = subject_json['userIdentifier']

    D_CP = CREATE_QUESTIONNAIRE_DATA_E2E.copy()
    ques_title = helper.random_title()
    time.sleep(3)
    DATA = helper.update_dictionary(D_CP, title=ques_title)
    status,createq_json = API_Calls.post_create_questionnaire_api(BASE_URL,CREATE_QUESTIONNAIRE_DATA_E2E,ACCESS_TOKEN,CONTENT_TYPE_APPLICATION_JSON)
    print("create questionnaire api result:", status, createq_json)
    Q_ID=createq_json['id']
    Q_LANGUAGE=createq_json['language']

    time.sleep(10)

    status,getq_json=API_Calls.get_questionnaire_required_for_measure(BASE_URL,Q_ID,Q_LANGUAGE,ACCESS_TOKEN)
    print("get questionnaire api result:", status, getq_json)

    time.sleep(5)
    SUBMIT_QUES_RESPONSE_DATA = {
    "questionnaire": {
         "id": Q_ID,
        "language": Q_LANGUAGE,
        "userIdentifier":SUB_IDENTIFIER1,
        "respondedAt": "1994-11-05T13:15:30Z",
        "questionResponses": [
            {
                "optionIndex": 1
            },

            {
                "optionIndexes": [1]
            },
            {
                "response": 4
            },
            {
                "isSkipped": True
            }

        ]
    }
}

    status, submit_q_response_json = API_Calls.submit_questionnaire_response(BASE_URL,SUBMIT_QUES_RESPONSE_DATA, ACCESS_TOKEN )
    print("submit questionnaire API result:", status, submit_q_response_json)
    assert status == 201

