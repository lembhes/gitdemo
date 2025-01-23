import json
import pytest
from TestCases import API_Calls
from TestCases.Support import assertion
from Variables.variableprod import *
from TestCases.Support import helper
import time



# ---------------- Get the Base64 --------------------------------#

base64secrets = helper.get_base64secrets(CLIENT_ID_Shruti, CLIENT_SECRET_Shruti)
print(base64secrets)

BASE_TOKEN = 'Basic ' + base64secrets


# ----------- Get the ACCESS TOKEN ----------------------------#

status_code, json_data = API_Calls.token_api(BASE_URL, VALID_TOKEN_DATA, BASE_TOKEN, CONTENT_TYPE_URL_ENCODED)
ACCESS_TOKEN = json_data['access_token']
#ACCESS_TOKEN_BEARER = 'Bearer ' + ACCESS_TOKEN
print(ACCESS_TOKEN)

# ---------------- Get the Base64  for without questionnaire client credentials --------------------------------#
#
base64secretswq = helper.get_base64secrets(CLIENT_ID_Shruti, CLIENT_SECRET_Shruti)
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
FILE_PATH= response_json['filePath']

status_code, response_json = API_Calls.storage_api(BASE_URL, VALID_STORAGE_DATA, ACCESS_TOKEN,
                                                   CONTENT_TYPE_APPLICATION_JSON)

STORAGE_SIGNED_URL1 = response_json['signedURL']
FILE_PATH_30SEC= response_json['filePath']

FILE_PATH_ENCODED1 = helper.urlEncoder(FILE_PATH_30SEC)
print(FILE_PATH_ENCODED1)
FILE_PATH_ENCODEDSAVED ='s3%3A%2F%2Fprod-sondeplatform-us-subject-metadata%2F488fd2d6-a492-4cef-a41e-491c12252593%2Fvoice-samples%2Fb890c382-3959-4add-ae4c-20ef4f34e12e.wav'

# ____________________UPLOAD THE AUDIO SAMPLE  ____________________________________________#


#AUDIO_FILE_PATH = 'C:\\Users\\GS-1329\\Downloads\\File_1_6sec.wav'


AUDIO_FILE_PATH = 'C:\\Users\\GS-1431\\Downloads\\ahh_SK.wav'
AUDIO_FILE_PATH1 = 'C:\\Users\\GS-1431\\Downloads\\shrutiD_audio_30sec.wav'
#AUDIO_FILE_PATH = 'C:\\Users\\GS-1329\\Downloads\\1__7FC800CA-456C-4CA2-A568-DE6A96E54705_7251_9067.wav'

status_code = API_Calls.upload_sample_file(STORAGE_SIGNED_URL, AUDIO_FILE_PATH)
status_code = API_Calls.upload_sample_file(STORAGE_SIGNED_URL1, AUDIO_FILE_PATH1)

# # --------------------------------- GET ALL MEASURES- ------------------------------------------------------------#
status, response_json = API_Calls.measures_api(BASE_URL, ACCESS_TOKEN)
MEASURE_ID = response_json['measures'][0]['id']
# #
# # ------------------------------GET THE QUESTIONNAIRE ID BY USING MEASURE ----------------------------------------#
#
MEASURE_NAME = 'respiratory-symptoms-risk'
MEASURE_NAME_MF = 'mental-fitness'

status, response_json = API_Calls.get_questionnaire_ID_required_for_measure(BASE_URL, MEASURE_NAME_MF, ACCESS_TOKEN)

QUESTIONNAIRE_ID = response_json['questionnaire']['id']
QUESTIONNAIRE_LANGUAGES = response_json['questionnaire']['languages'][0]
#
# # -------------------------------GET THE QUESTIONNAIRE -------------------------------------------------

status, response_json = API_Calls.get_questionnaire_required_for_measure(BASE_URL, QUESTIONNAIRE_ID,
                                                                         QUESTIONNAIRE_LANGUAGES, ACCESS_TOKEN)
QUES_ID = response_json['id']
LANGUAGE = response_json['language']


# #Shruti questionnaire response
QUESTIONNAIRE_BODY = {
    "questionnaire": {
         "id": QUES_ID,
        "language": "en",
        "userIdentifier":SUB_IDENTIFIER,
        "respondedAt": "1994-11-05T13:15:30Z",
        "questionResponses": [
            {
                "optionIndex": 1
            },

                        {
                "optionIndexes": [1]
            }

        ]
    }
}
#
#
# QUESTIONNAIRE_BODY_SKIP_ENABLED = {
#     "questionnaire": {
#          "id": QUES_ID,
#         "language": LANGUAGE,
#         "userIdentifier":SUB_IDENTIFIER,
#         "respondedAt": "1994-11-05T13:15:30Z",
#         "questionResponses": [
#             {
#                 "optionIndex": 1
#             },
#
#                         {
#                 "optionIndex": 1
#             },
#                         {
#                 "optionIndex": 1
#             },
#                         {
#                 "optionIndex": 1
#             },
#             {
#                 "optionIndexes": [1,2]
#             },
#             {
#                  "isSkipped": True
#              }
#
#         ]
#     }
# }

QUESTIONNAIRE_BODY_SKIP_ENABLED = {
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
                "isSkipped": True
            }]
    }}

status, response_json = API_Calls.submit_questionnaire_response(BASE_URL, QUESTIONNAIRE_BODY, ACCESS_TOKEN)
print(status, response_json)

QUESTIONNAIRE_RESPONSE_ID = response_json['id']

# ---------------------------- GET THE SCORE --------------------------------#

VALID_SCORE_DATA = {
    "userIdentifier": SUB_IDENTIFIER,
    "filePath": FILE_PATH,
    "measureName": MEASURE_NAME
}


VALID_SCORE_DATA_WITH_QS = {
    "userIdentifier": SUB_IDENTIFIER,
    "filePath": FILE_PATH_30SEC,
    "measureName": MEASURE_NAME_MF,
    "questionnaireResponseId": "qrs_514e16101e5d"
}



ASYNC_SCORE_API_DATA ={
    "infer": [
        {
            "type": "Acoustic",
            "version": "v1"
        }
    ],
    "filePath": FILE_PATH_30SEC,
    "measureName": "mental-fitness"
}
ASYNC_SCORE_API_DATA_V2 ={
    "infer": [
        {
            "type": "Acoustic",
            "version": "v2"
        }
    ],
    "filePath": FILE_PATH_30SEC,
    "measureName": "mental-fitness"
}

ASYNC_SCORE_API_DATA_V3 ={
    "infer": [
        {
            "type": "Acoustic",
            "version": "v3"
        }
    ],
    "filePath": FILE_PATH_30SEC,
    "measureName": "mental-fitness"
}


#---------- post score API ----------#

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
    ACCESS_TOKEN = json_data['ACCESS_TOKEN']
    return  ACCESS_TOKEN


@pytest.fixture
def input_data():
   input = ASYNC_SCORE_API_DATA
   return input

@pytest.fixture
def get_header():
   content_type = CONTENT_TYPE_APPLICATION_JSON
   return content_type


ASYNC_TRANSCRIPTION_API_DATA ={
    "filePath": FILE_PATH_30SEC
}
@pytest.fixture()
def get_job_id():
    status, transcriptions_json_data = API_Calls.post_async_transcriptions_api(ASYNC_URL, ASYNC_TRANSCRIPTION_API_DATA,
                                                                               ACCESS_TOKEN,
                                                                               CONTENT_TYPE_APPLICATION_JSON)
    print(status, transcriptions_json_data)
    ASYNC_JOB_ID=transcriptions_json_data['jobId']
    return  ASYNC_JOB_ID
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

def test_subject_v2_api():
    status, data = API_Calls.subject_api(BASE_URL2, VALID_SUBJECT_DATA_V2, ACCESS_TOKEN, CONTENT_TYPE_APPLICATION_JSON)
    assert status == 201
    print(status, data)
    assertion.assert_valid_schema(data, 'subject_v2.json')

def test_subject_v2_api_with_unknown_gender_inlowercase():
    D_CP = VALID_SUBJECT_DATA_V2.copy()
    DATA = helper.update_dictionary(D_CP, gender="unknown")
    print(DATA)
    status, data = API_Calls.subject_api(BASE_URL2, DATA, ACCESS_TOKEN,
                                         CONTENT_TYPE_APPLICATION_JSON)
    assert status == 201
    print(status, data)
    assertion.assert_valid_schema(data, 'subject_v2.json')

def test_subject_v2_api_with_unknown_incaps_gender():
    D_CP = VALID_SUBJECT_DATA_V2.copy()
    DATA = helper.update_dictionary(D_CP, gender="UNKNOWN")
    print(DATA)
    status, data = API_Calls.subject_api(BASE_URL2, DATA, ACCESS_TOKEN,
                                         CONTENT_TYPE_APPLICATION_JSON)
    assert status == 201
    print(status, data)
    assertion.assert_valid_schema(data, 'subject_v2.json')

def test_subject_v2_api_with_unknown_in_uppercase_yearOfBirth():
    D_CP = VALID_SUBJECT_DATA_V2.copy()
    DATA = helper.update_dictionary(D_CP, yearOfBirth="UNKNOWN")
    print(DATA)
    status, data = API_Calls.subject_api(BASE_URL2, DATA, ACCESS_TOKEN,
                                         CONTENT_TYPE_APPLICATION_JSON)
    assert status == 201
    print(status, data)
    assertion.assert_valid_schema(data, 'subject_v2.json')

def test_subject_v2_api_with_unknown_inlowercase_yearOfBirth():
    D_CP = VALID_SUBJECT_DATA_V2.copy()
    DATA = helper.update_dictionary(D_CP, yearOfBirth="unknown")
    print(DATA)
    status, data = API_Calls.subject_api(BASE_URL2, DATA, ACCESS_TOKEN,
                                         CONTENT_TYPE_APPLICATION_JSON)
    assert status == 201
    print(status, data)
    assertion.assert_valid_schema(data, 'subject_v2.json')

def test_subject_v2_api_with_unknown_device_in_uppercase():
    status, data = API_Calls.subject_api(BASE_URL2, VALID_SUBJECT_DATA_DEVICE_UNKNOWN, ACCESS_TOKEN, CONTENT_TYPE_APPLICATION_JSON)
    assert status == 201
    print(status, data)
    assertion.assert_valid_schema(data, 'subject_v2_unknown_schema.json')

def test_subject_v2_api_unknown_device_in_lowercase():
    status, data = API_Calls.subject_api(BASE_URL2, SUBJECT_DATA_1, ACCESS_TOKEN, CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 201
    assertion.assert_valid_schema(data, 'subject_v2_unknown_schema.json')

def test_subject_v2_api_with_unknown_device_yob_gender_in_caps():
    status, data = API_Calls.subject_api(BASE_URL2, VALID_SUBJECT_DATA_ALL_M_UNKNOWN, ACCESS_TOKEN, CONTENT_TYPE_APPLICATION_JSON)
    assert status == 201
    print(status, data)
    assertion.assert_valid_schema(data, 'subject_v2_unknown_schema.json')


def test_subject_v2_api_unknown_in_lowercase_device_yob_gender():
    status, data = API_Calls.subject_api(BASE_URL2, VALID_SUBJECT_DATA_ALL_M_UNKNOWN_IN_SMALL, ACCESS_TOKEN, CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 201
    assertion.assert_valid_schema(data, 'subject_v2_unknown_schema.json')

def test_update_subject_data_api():
    status, data = API_Calls.update_subject_details(BASE_URL, SUB_IDENTIFIER, UPDATE_SUBJECT_DATA, ACCESS_TOKEN)
    print(status, data)
    assert status == 200


def test_storage_api():
    status, data = API_Calls.storage_api(BASE_URL, VALID_STORAGE_DATA, ACCESS_TOKEN, CONTENT_TYPE_APPLICATION_JSON)
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


def test_get_measures_api():
    status, data = API_Calls.measures_api(BASE_URL, ACCESS_TOKEN)
    print(status, data)
    assert status == 200
    assertion.assert_valid_schema(data, 'measure_schema.json')


def test_get_measure_by_id():
    status, data = API_Calls.measure_id_api(BASE_URL, MEASURE_ID, ACCESS_TOKEN)
    print(status, data)
    assert status == 200
    assertion.assert_valid_schema(data, 'get_questionnaire_id.json')

#
def test_get_questionnaire_ID_required_for_measure():
    status, data = API_Calls.get_questionnaire_ID_required_for_measure(BASE_URL, MEASURE_NAME_MF, ACCESS_TOKEN)
    print(status, data)
    assert status == 200
    assertion.assert_valid_schema(data, 'get_questionnaire_id.json')
#
#
def test_get_questionnaire_api():
    status, data = API_Calls.get_questionnaire_required_for_measure(BASE_URL, QUESTIONNAIRE_ID,
                                                                    QUESTIONNAIRE_LANGUAGES, ACCESS_TOKEN)
    print(status, data)
    assert status == 200
    assertion.assert_valid_schema(data, 'get_questionnaire.json')


def test_upload_questionnaire_response_api():
    status, data = API_Calls.submit_questionnaire_response(BASE_URL, QUESTIONNAIRE_BODY, ACCESS_TOKEN)
    print(status, data)
    assert status == 201
    assertion.assert_valid_schema(data, 'questionnaire_response.json')


def test_upload_questionnaire_response_api_with_skip_option():
    status, data = API_Calls.submit_questionnaire_response(BASE_URL, QUESTIONNAIRE_BODY_SKIP_ENABLED, ACCESS_TOKEN)
    print(status, data)
    assert status == 201
    assertion.assert_valid_schema(data, 'questionnaire_response.json')


def test_score_api():
    status, score_json_data = API_Calls.score_api(BASE_URL, VALID_SCORE_DATA, ACCESS_TOKEN,
                                                  CONTENT_TYPE_APPLICATION_JSON)
    print(status, score_json_data)
    assert status == 200
    assertion.assert_valid_schema(score_json_data, 'score_schema.json')


def test_score_api_with_questionnaire():
    status, score_json_data = API_Calls.score_api(BASE_URL, VALID_SCORE_DATA_WITH_QS, ACCESS_TOKEN,
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


# def test_score_api_questionnaire_response_id_optional():
#     #D_CP = VALID_SCORE_DATA.copy()
#     #DATA = helper.delete_key(D_CP, 'questionnaireResponseId')
#     status, data = API_Calls.score_api(BASE_URL,VALID_SCORE_DATA_WITHOUT_QUESTIONNAIRE, ACCESS_TOKEN_WQ,CONTENT_TYPE_APPLICATION_JSON)
#     print(status, data)
#     assert status == 200
#     assertion.assert_valid_schema(data, 'score_schema.json')

def test_get_inference_scores_api_duration():
    status, score_json_data = API_Calls.get_inference_scores_api_duration(BASE_URL,ACCESS_TOKEN)
    print(status, score_json_data)
    assert status == 200


def test_get_inference_scores_api_userIdentifier():
    status, score_json_data = API_Calls.get_inference_scores_api_userIdentifier(BASE_URL, ACCESS_TOKEN,SUB_IDENTIFIER)
    print(status, score_json_data)
    assert status == 200
    #assertion.assert_valid_schema(score_json_data, 'score_schema.json')


@pytest.mark.transcription
######## Voice feature score cases ########

def test_async_score_v1_api():
    status, score_json_data = API_Calls.post_async_score_api(ASYNC_URL, ASYNC_SCORE_API_DATA ,ACCESS_TOKEN, CONTENT_TYPE_APPLICATION_JSON)
    print(status, score_json_data)
    assert status == 202
    assertion.assert_valid_schema(score_json_data, 'score_3.0_api.json')

@pytest.mark.transcription
def test_async_score_v2_api():
    status, score_json_data = API_Calls.post_async_score_api(ASYNC_URL, ASYNC_SCORE_API_DATA_V2, ACCESS_TOKEN, CONTENT_TYPE_APPLICATION_JSON)
    print(status, score_json_data)
    assert status == 202
    assertion.assert_valid_schema(score_json_data, 'score_3.0_api.json')

def test_async_score_v3_api():
    status, score_json_data = API_Calls.post_async_score_api(ASYNC_URL, ASYNC_SCORE_API_DATA_V3, ACCESS_TOKEN, CONTENT_TYPE_APPLICATION_JSON)
    print(status, score_json_data)
    assert status == 202
    assertion.assert_valid_schema(score_json_data, 'score_3.0_api.json')

@pytest.mark.transcription
def test_get_async_score_v1_api():
    status, get_score_json =  API_Calls.get_async_score_api(ASYNC_URL,ACCESS_TOKEN,JOB_ID)
    print(JOB_ID)
    print (status,get_score_json)
    assert status == 200
    assertion.assert_valid_schema(get_score_json, 'score_3.0_reponse.json')

@pytest.mark.transcription
def test_get_async_score_v2_api_with_ACCESS_TOKEN():
    status, get_score_json =  API_Calls.get_async_score_api(ASYNC_URL,ACCESS_TOKEN,JOB_ID)
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

@pytest.mark.transcription
def test_get_voice_feature_by_measure_api():
    status, get_voice_feature_json = API_Calls.get_voice_feature_by_measure_api(BASE_URL,ACCESS_TOKEN)
    print (status,get_voice_feature_json)
    assert status == 200
    assertion.assert_valid_schema(get_voice_feature_json, 'get_voice_feature_by_measure.json')

@pytest.mark.transcription
#py.test -m API_VIE   --html="C:\Users\gs-1431\Desktop\Sonde Health System\Mental fitness app 1.2\API Automation reports\test.html"
######## Transcription API ########

def test_post_async_transcriptions_api():
    status, transcriptions_json_data = API_Calls.post_async_transcriptions_api(ASYNC_URL, ASYNC_TRANSCRIPTION_API_DATA,ACCESS_TOKEN,  CONTENT_TYPE_APPLICATION_JSON)
    print(status, transcriptions_json_data)
    assert status == 202
    assertion.assert_valid_schema(transcriptions_json_data, 'post_transcription.json')


time.sleep(10)

@pytest.mark.transcription
def test_post_async_transcriptions_api_secondtime():
    status, transcriptions_json_data = API_Calls.post_async_transcriptions_api(ASYNC_URL, ASYNC_TRANSCRIPTION_API_DATA, ACCESS_TOKEN,                                                                    CONTENT_TYPE_APPLICATION_JSON)
    print(status, transcriptions_json_data)
    assert status == 200
    assertion.assert_valid_schema(transcriptions_json_data, 'post_transcription.json')


time.sleep(20)

@pytest.mark.transcription
def test_get_async_transcription_api():
    status, get_score_json =  API_Calls.get_async_transcription_api(ASYNC_URL,ACCESS_TOKEN,str(get_job_id))
    print(status, get_score_json)
    assert status_code == 200
    assertion.assert_valid_schema(get_score_json, 'get_transcription.json')

time.sleep(20)

def test_get_async_transcription_api_with_ACCESS_TOKEN():
    status, get_score_json =  API_Calls.get_async_transcription_api(ASYNC_URL,ACCESS_TOKEN,str(get_job_id))
    print(status, get_score_json)
    assert status_code == 200
    assertion.assert_valid_schema(get_score_json, 'get_transcription.json')

time.sleep(20)

@pytest.mark.transcription
def test_get_audio_file_transcription():
    status, response = API_Calls.get_audio_file_transcription(BASE_URL, FILE_PATH_ENCODEDSAVED, ACCESS_TOKEN)
    #print(API_Calls.get_audio_file_transcription(BASE_URL, FILE_PATH_ENCODED_SAVED, ACCESS_TOKEN))
    print(FILE_PATH_ENCODEDSAVED)
    print(status, response)
    assert status == 200
    assertion.assert_valid_schema(response, 'get_file_transcription.json')

def test_get_audio_file_transcription_with_ACCESS_TOKEN():
    status, response = API_Calls.get_audio_file_transcription(BASE_URL, FILE_PATH_ENCODEDSAVED, ACCESS_TOKEN)
    #print(API_Calls.get_audio_file_transcription(BASE_URL, FILE_PATH_ENCODED_SAVED, ACCESS_TOKEN))
    print(FILE_PATH_ENCODEDSAVED)
    print(status, response)
    assert status == 200
    assertion.assert_valid_schema(response, 'get_file_transcription.json')

@pytest.mark.transcription
######## Two Sample Scoring API ########
def test_E2E_reliable_score_US_location():

    # #login with token
    # status_code, json_data = API_Calls.token_api(BASE_URL, VALID_TOKEN_DATA, BASE_TOKEN, CONTENT_TYPE_URL_ENCODED)
    # print("token api result:",status_code)
    # #assert status_code == 200
    # ACCESS_TOKEN = json_data['ACCESS_TOKEN']

    #create subject
    status, subject_json = API_Calls.subject_api(BASE_URL, VALID_SUBJECT_DATA, ACCESS_TOKEN,CONTENT_TYPE_APPLICATION_JSON)
    print("subject api result:",status, subject_json )
    SUB_IDENTIFIER1 = subject_json['userIdentifier']

    VALID_STORAGE_DATA1 = {
        "fileType": "wav",
        "countryCode": "US",
        "userIdentifier": SUB_IDENTIFIER1
    }
    #storage api
    status_code, response_json = API_Calls.storage_api(BASE_URL, VALID_STORAGE_DATA1, ACCESS_TOKEN,CONTENT_TYPE_APPLICATION_JSON)
    STORAGE_SIGNED_URL1 = response_json['signedURL']
    print("1st audio storage api result:", status_code, response_json)
    FILE_PATH1 = response_json['filePath']

    #first file upload
    status_code = API_Calls.upload_sample_file(STORAGE_SIGNED_URL1, TC1_FILE_PATH1)
    print("First audio file upload:", status_code)

    INFERENCE_PARAMETER_DATA = {
        "measure": {
            "name": "respiratory-symptoms-risk",
            "variant": "v2"
        },
        "filePath": FILE_PATH1
    }
    #POST inference paramteres
    status_code, response_json = API_Calls.post_inference_parameters_api(BASE_URL2, INFERENCE_PARAMETER_DATA, ACCESS_TOKEN,CONTENT_TYPE_APPLICATION_JSON)
    print("POST inference parameters API result",status_code, response_json)
    INFERENCE_PARAMETER_ID = response_json['id']
    print(INFERENCE_PARAMETER_ID)

    #storage api for 2nd audio file
    status_code, response_json = API_Calls.storage_api(BASE_URL, VALID_STORAGE_DATA1, ACCESS_TOKEN,CONTENT_TYPE_APPLICATION_JSON)
    print("2nd audio storage api result:", status_code, response_json)
    STORAGE_SIGNED_URL2 = response_json['signedURL']
    FILE_PATH2 = response_json['filePath']

    INFERENCE_PARAMETER_DATA2 = {

        "filePath": FILE_PATH2
    }

    # second file upload
    status_code = API_Calls.upload_sample_file(STORAGE_SIGNED_URL2, TC1_FILE_PATH2)
    print("Second audio file upload: ",status_code)

    # PUT inference paramteres
    status_code, response_json = API_Calls.put_inference_parameters_api(BASE_URL2,ACCESS_TOKEN,INFERENCE_PARAMETER_ID,INFERENCE_PARAMETER_DATA2, CONTENT_TYPE_APPLICATION_JSON)

    print("PUT inference parameters API result:",status_code,response_json)

    #POST inference scores API
    time.sleep(10)
    SCORE_V2_DATA = {
        "inferenceParameterId": INFERENCE_PARAMETER_ID
    }
    status_code, response_json = API_Calls.post_inference_scorev2_api(BASE_URL2,SCORE_V2_DATA,ACCESS_TOKEN,CONTENT_TYPE_APPLICATION_JSON)
    print("POST inference score v2 API result:", status_code, response_json)
    SCOREID = response_json['id']

    #GET inference scores API
    status_code, response_json = API_Calls.get_inference_scorev2_api(BASE_URL2, SCOREID, ACCESS_TOKEN,CONTENT_TYPE_APPLICATION_JSON)
    assert  status_code == 200
    print("GET inference score v2 API result:", status_code, response_json)



@pytest.mark.transcription
def test_E2E_unreliable_score_condition():

    #login with token
    # status_code, json_data = API_Calls.token_api(BASE_URL, VALID_TOKEN_DATA, BASE_TOKEN, CONTENT_TYPE_URL_ENCODED)
    # print("token api result:",status_code)
    # #assert status_code == 200
    # ACCESS_TOKEN = json_data['ACCESS_TOKEN']

    #create subject
    status, subject_json = API_Calls.subject_api(BASE_URL, VALID_SUBJECT_DATA, ACCESS_TOKEN,CONTENT_TYPE_APPLICATION_JSON)
    print("subject api result:",status, subject_json )
    SUB_IDENTIFIER1 = subject_json['userIdentifier']

    VALID_STORAGE_DATA1 = {
        "fileType": "wav",
        "countryCode": "US",
        "userIdentifier": SUB_IDENTIFIER1
    }
    #storage api
    status_code, response_json = API_Calls.storage_api(BASE_URL, VALID_STORAGE_DATA1, ACCESS_TOKEN,CONTENT_TYPE_APPLICATION_JSON)
    STORAGE_SIGNED_URL1 = response_json['signedURL']
    print("1st audio storage api result:", status_code, response_json)
    FILE_PATH1 = response_json['filePath']

    #first file upload
    status_code = API_Calls.upload_sample_file(STORAGE_SIGNED_URL1, TC3_FILE_PATH1)
    print("First audio file upload:", status_code)

    INFERENCE_PARAMETER_DATA = {
        "measure": {
            "name": "respiratory-symptoms-risk",
            "variant": "v2"
        },
        "filePath": FILE_PATH1
    }
    #POST inference paramteres
    status_code, response_json = API_Calls.post_inference_parameters_api(BASE_URL2, INFERENCE_PARAMETER_DATA, ACCESS_TOKEN,CONTENT_TYPE_APPLICATION_JSON)
    print("POST inference parameters API result",status_code, response_json)
    INFERENCE_PARAMETER_ID = response_json['id']
    print(INFERENCE_PARAMETER_ID)

    #storage api for 2nd audio file
    status_code, response_json = API_Calls.storage_api(BASE_URL, VALID_STORAGE_DATA1, ACCESS_TOKEN,CONTENT_TYPE_APPLICATION_JSON)
    print("2nd audio storage api result:", status_code, response_json)
    STORAGE_SIGNED_URL2 = response_json['signedURL']
    FILE_PATH2 = response_json['filePath']

    INFERENCE_PARAMETER_DATA2 = {

        "filePath": FILE_PATH2
    }

    # second file upload
    status_code = API_Calls.upload_sample_file(STORAGE_SIGNED_URL2, TC3_FILE_PATH2)
    print("Second audio file upload: ",status_code)

    # PUT inference paramteres
    status_code, response_json = API_Calls.put_inference_parameters_api(BASE_URL2,ACCESS_TOKEN,INFERENCE_PARAMETER_ID,INFERENCE_PARAMETER_DATA2, CONTENT_TYPE_APPLICATION_JSON)

    print("PUT inference parameters API result:",status_code,response_json)

    #POST inference scores API
    time.sleep(10)
    SCORE_V2_DATA = {
        "inferenceParameterId": INFERENCE_PARAMETER_ID
    }
    status_code, response_json = API_Calls.post_inference_scorev2_api(BASE_URL2,SCORE_V2_DATA,ACCESS_TOKEN,CONTENT_TYPE_APPLICATION_JSON)
    print("POST inference score v2 API result:", status_code, response_json)
    SCOREID = response_json['id']
    time.sleep(10)
    #GET inference scores API
    status_code, response_json = API_Calls.get_inference_scorev2_api(BASE_URL2, SCOREID, ACCESS_TOKEN,CONTENT_TYPE_APPLICATION_JSON)
    assert status_code == 422
    print("GET inference score v2 API result:", status_code, response_json)

#
# def test_E2E_create_questionnaire_use_case_flow():
#
#     #login with token
#     status_code, json_data = API_Calls.token_api(BASE_URL, VALID_TOKEN_DATA, BASE_TOKEN, CONTENT_TYPE_URL_ENCODED)
#     print("token api result:",status_code)
#     #assert status_code == 200
#     ACCESS_TOKEN = json_data['ACCESS_TOKEN']
#
#     #create subject
#     status, subject_json = API_Calls.subject_api(BASE_URL, VALID_SUBJECT_DATA, ACCESS_TOKEN,CONTENT_TYPE_APPLICATION_JSON)
#     print("subject api result:",status, subject_json )
#     SUB_IDENTIFIER1 = subject_json['userIdentifier']
#
#     D_CP = CREATE_QUESTIONNAIRE_DATA_E2E.copy()
#     ques_title = helper.random_title()
#     time.sleep(3)
#     DATA = helper.update_dictionary(D_CP, title=ques_title)
#
#     status,createq_json = API_Calls.post_create_questionnaire_api(BASE_URL,DATA,ACCESS_TOKEN,CONTENT_TYPE_APPLICATION_JSON)
#     print("create questionnaire api result:", status, createq_json)
#     Q_ID=createq_json['id']
#     Q_LANGUAGE=createq_json['language']
#
#     time.sleep(5)
#
#     status,getq_json=API_Calls.get_questionnaire_required_for_measure(BASE_URL,Q_ID,Q_LANGUAGE,ACCESS_TOKEN)
#     print("get questionnaire api result:", status, getq_json)
#
#     time.sleep(5)
#     SUBMIT_QUES_RESPONSE_DATA = {
#     "questionnaire": {
#          "id": Q_ID,
#         "language": Q_LANGUAGE,
#         "userIdentifier":SUB_IDENTIFIER1,
#         "respondedAt": "1994-11-05T13:15:30Z",
#         "questionResponses": [
#             {
#                 "optionIndex": 1
#             },
#
#             {
#                 "optionIndexes": [1]
#             },
#             {
#                 "response": 4
#             },
#             {
#                 "isSkipped": True
#             }
#
#         ]
#     }
# }
#
#     status, submit_q_response_json = API_Calls.submit_questionnaire_response(BASE_URL,SUBMIT_QUES_RESPONSE_DATA, ACCESS_TOKEN )
#     print("get questionnaire api result:", status, submit_q_response_json)
#     assert status == 201
#
#
