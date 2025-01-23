import json
import pytest
import requests
import time
from TestCases import API_Calls
from TestCases.Support import assertion
from Variables.variable import *
from TestCases.Support import helper

NewVar=""

#------Base64------#

base64secrets = helper.get_base64secrets(CLIENT_ID_Shruti, CLIENT_SECRET_Shruti)
BASE_TOKEN = 'Basic ' + base64secrets
print(base64secrets)

#------Token-------#
status_code, json_data = API_Calls.token_api(BASE_URL, VALID_TOKEN_DATA, BASE_TOKEN, CONTENT_TYPE_URL_ENCODED)
ACCESS_TOKEN = json_data['access_token']
print(ACCESS_TOKEN)

#------User--------#

status_code,json_data=API_Calls.subject_api(BASE_URL,VALID_SUBJECT_DATA,ACCESS_TOKEN,CONTENT_TYPE_APPLICATION_JSON)
SUB_IDENTIFIER=json_data['userIdentifier']
print(SUB_IDENTIFIER)

#-----Storage1------#

VALID_STORAGE_DATA = {
   "fileType": "wav",
   "countryCode": "US",
   "userIdentifier": SUB_IDENTIFIER
}

status_code, response_json = API_Calls.storage_api(BASE_URL, VALID_STORAGE_DATA, ACCESS_TOKEN,
                                                  CONTENT_TYPE_APPLICATION_JSON)

STORAGE_SIGNED_URL1 = response_json['signedURL']
FILE_PATH1 = response_json['filePath']
FILE_PATH_ENCODED1 = helper.urlEncoder(FILE_PATH1)

#--------Upload File1 -------#

TC1_FILE_PATH1 = 'C:\\Users\\gs-1431\\Downloads\\Two_sample_scoring_api\\Reliable_score\\first.wav'
status_code = API_Calls.upload_sample_file(STORAGE_SIGNED_URL1, TC1_FILE_PATH1)


#------Storage2------#

status_code, response_json = API_Calls.storage_api(BASE_URL, VALID_STORAGE_DATA, ACCESS_TOKEN,
                                                  CONTENT_TYPE_APPLICATION_JSON)

STORAGE_SIGNED_URL2 = response_json['signedURL']
FILE_PATH2 = response_json['filePath']
FILE_PATH_ENCODED2 = helper.urlEncoder(FILE_PATH2)

#--------Upload File2 -------#
TC1_FILE_PATH2 = 'C:\\Users\\gs-1431\\Downloads\\Two_sample_scoring_api\\Reliable_score\\second.wav'
#AUDIO_FILE_PATH2 = 'C:/Users/GS-1329/Downloads/Audio samples Two sample scoring/second.wav'
status_code = API_Calls.upload_sample_file(STORAGE_SIGNED_URL2, TC1_FILE_PATH2)

#-----Storage 3 but file is same as File 1------#

VALID_STORAGE_DATA = {
   "fileType": "wav",
   "countryCode": "US",
   "userIdentifier": SUB_IDENTIFIER
}

status_code, response_json = API_Calls.storage_api(BASE_URL, VALID_STORAGE_DATA, ACCESS_TOKEN,
                                                  CONTENT_TYPE_APPLICATION_JSON)

STORAGE_SIGNED_URL3 = response_json['signedURL']
FILE_PATH3 = response_json['filePath']
FILE_PATH_ENCODED3 = helper.urlEncoder(FILE_PATH3)

#--------Upload File1 -------#

status_code = API_Calls.upload_sample_file(STORAGE_SIGNED_URL3, TC1_FILE_PATH1) # Same file 1 is uploaded at url 3

#----- Create Inference parameter API  ------#

POST_INFERENCE_PARAMETER_DATA={
 "measure": {
   "name": "respiratory-symptoms-risk",
   "variant": "v2"
 },
 "filePath":FILE_PATH1
}

PUT_INFERENCE_PARAMETER_DATA={
 "filePath":FILE_PATH2
}

INFERENCE_PARAMETER_ID =''
SCORE_ID=''

def test_post_inference_parameter_api_inprogress():
   print(FILE_PATH1)
   global INFERENCE_PARAMETER_ID
   status_code, response_json = API_Calls.post_inference_parameters_api(BASE_URLV2, POST_INFERENCE_PARAMETER_DATA, ACCESS_TOKEN,
                                                                            CONTENT_TYPE_APPLICATION_JSON)
   assert status_code == 202
   INFERENCE_PARAMETER_ID = response_json['id']
   assertion.assert_valid_schema(response_json, 'v2_post_inference_parameter.json')


def test_post_inference_parameter_api_inprogress_access_token_with_bearer():
    ACCESS_TOKEN_BEARER = 'Bearer ' + ACCESS_TOKEN
    print(ACCESS_TOKEN_BEARER)
    print(FILE_PATH1)
    global INFERENCE_PARAMETER_ID
    status_code, response_json = API_Calls.post_inference_parameters_api(BASE_URLV2, POST_INFERENCE_PARAMETER_DATA, ACCESS_TOKEN_BEARER,
                                                                            CONTENT_TYPE_APPLICATION_JSON)
    assert status_code == 202
    INFERENCE_PARAMETER_ID = response_json['id']
    assertion.assert_valid_schema(response_json, 'v2_post_inference_parameter.json')

time.sleep(10)
'''
def test_post_inference_parameter_api_created():
   status_code, response_json = API_Calls.post_inference_parameters_api(BASE_URLV2, POST_INFERENCE_PARAMETER_DATA, ACCESS_TOKEN,
                                                                            CONTENT_TYPE_APPLICATION_JSON)
   assert status_code == 201
'''

def test_post_inference_parameter_api_incorrect_accesstoken():
   INCORRECT_ACCESS_TOKEN = 'xyz'
   status_code, response_json = API_Calls.post_inference_parameters_api(BASE_URLV2, POST_INFERENCE_PARAMETER_DATA, INCORRECT_ACCESS_TOKEN,
                                                                            CONTENT_TYPE_APPLICATION_JSON)
   assert status_code == 401

def test_post_inference_parameter_api_incorrect_accesstoken_with_bearer_in_small_case():
    ACCESS_TOKEN_BEARER1 = 'bearer ' + ACCESS_TOKEN
    print(ACCESS_TOKEN_BEARER1)
    status_code, response_json = API_Calls.post_inference_parameters_api(BASE_URLV2, POST_INFERENCE_PARAMETER_DATA,
                                                                            ACCESS_TOKEN_BEARER1,
                                                                            CONTENT_TYPE_APPLICATION_JSON)
    assert status_code == 401


def test_post_inference_parameter_api_expired_accesstoken():
   status_code, response_json = API_Calls.post_inference_parameters_api(BASE_URLV2, POST_INFERENCE_PARAMETER_DATA, EXPIRED_ACCESS_TOKEN,
                                                                            CONTENT_TYPE_APPLICATION_JSON)
   assert status_code == 401

def test_post_inference_parameter_api_missing_accesstoken():
   headers = {'Content-Type': CONTENT_TYPE_APPLICATION_JSON}
   res = requests.post(url=BASE_URLV2 + INFERENCE_PARAMETER_ENDPOINT, data=json.dumps(POST_INFERENCE_PARAMETER_DATA),headers=headers)
   assert res.status_code == 401

def test_post_inference_parameter_api_blank_accesstoken():
   headers = {'Authorization': '', 'Content-Type': CONTENT_TYPE_APPLICATION_JSON}
   res = requests.post(url=BASE_URLV2 + INFERENCE_PARAMETER_ENDPOINT, data=json.dumps(POST_INFERENCE_PARAMETER_DATA),headers=headers)
   assert res.status_code == 401

def test_post_inference_parameter_api_no_request_body():
   D_CP = POST_INFERENCE_PARAMETER_DATA.copy()
   DATA1 = helper.delete_key(D_CP, 'filePath')
   DATA = helper.delete_key(DATA1, 'measure')
   status_code, response_json = API_Calls.post_inference_parameters_api(BASE_URLV2, DATA, ACCESS_TOKEN,
                                                                            CONTENT_TYPE_APPLICATION_JSON)
   assert status_code == 400

def test_post_inference_parameter_api_invalid_endpoint():
   INVALID_INFERENCE_PARAMETER_ENDPOINT = '/inference/inferenceparameters123'
   headers = {'Authorization': ACCESS_TOKEN, 'Content-Type': CONTENT_TYPE_APPLICATION_JSON}
   res = requests.post(url=BASE_URLV2 + INVALID_INFERENCE_PARAMETER_ENDPOINT, data=json.dumps(POST_INFERENCE_PARAMETER_DATA),headers=headers)
   assert res.status_code == 403

def test_post_inference_parameter_api_requestbody_measure_key_missing():
   D_CP = POST_INFERENCE_PARAMETER_DATA.copy()
   DATA = helper.delete_key(D_CP, 'measure')
   status_code, response_json = API_Calls.post_inference_parameters_api(BASE_URLV2, DATA, ACCESS_TOKEN,
                                                                            CONTENT_TYPE_APPLICATION_JSON)
   assert status_code == 400

def test_post_inference_parameter_api_requestbody_measure_key_blank():
   D_CP = POST_INFERENCE_PARAMETER_DATA.copy()
   DATA = helper.update_dictionary(D_CP, measure=' ')
   status_code, response_json = API_Calls.post_inference_parameters_api(BASE_URLV2, DATA, ACCESS_TOKEN,
                                                                            CONTENT_TYPE_APPLICATION_JSON)
   assert status_code == 400

def test_post_inference_parameter_api_requestbody_measure_keyname_blank():
   DATA1 = {
       "  ": {
           "name": "respiratory-symptoms-risk",
           "variant": "v2"
       },
       "filePath": FILE_PATH1
   }
   status_code, response_json = API_Calls.post_inference_parameters_api(BASE_URLV2, DATA1, ACCESS_TOKEN,
                                                                            CONTENT_TYPE_APPLICATION_JSON)
   assert status_code == 400

def test_post_inference_parameter_api_requestbody_measure_keyname_invalid():
   DATA1 = {
       "measure1234": {
           "name": "respiratory-symptoms-risk",
           "variant": "v2"
       },
       "filePath": FILE_PATH1
   }
   status_code, response_json = API_Calls.post_inference_parameters_api(BASE_URLV2, DATA1, ACCESS_TOKEN,
                                                                            CONTENT_TYPE_APPLICATION_JSON)
   assert status_code == 400

def test_post_inference_parameter_api_requestbody_measure_name_keyvalue_missing():
   DATA1 = {
       "measure": {
           "variant": "v2"
       },
       "filePath": FILE_PATH1
   }
   status_code, response_json = API_Calls.post_inference_parameters_api(BASE_URLV2, DATA1, ACCESS_TOKEN,
                                                                            CONTENT_TYPE_APPLICATION_JSON)
   assert status_code == 400

def test_post_inference_parameter_api_measure_name_keyvalue_invalid():
   DATA1 = {
       "measure": {
           "name": "respiratory-symptoms-risk1234",
           "variant": "v2"
       },
       "filePath": FILE_PATH1
   }
   status_code, response_json = API_Calls.post_inference_parameters_api(BASE_URLV2, DATA1, ACCESS_TOKEN,
                                                                            CONTENT_TYPE_APPLICATION_JSON)
   assert status_code == 404

def test_post_inference_parameter_api_measure_name_keyvalue_blank():
   DATA1 = {
       "measure": {
           "name": "  ",
           "variant": "v2"
       },
       "filePath": FILE_PATH1
   }
   status_code, response_json = API_Calls.post_inference_parameters_api(BASE_URLV2, DATA1, ACCESS_TOKEN,
                                                                            CONTENT_TYPE_APPLICATION_JSON)
   assert status_code == 404

def test_post_inference_parameter_api_requestbody_measure_variant_key_missing():
   DATA1 = {
       "measure": {
           "name": "respiratory-symptoms-risk"
       },
       "filePath": FILE_PATH1
   }
   status_code, response_json = API_Calls.post_inference_parameters_api(BASE_URLV2, DATA1, ACCESS_TOKEN,
                                                                        CONTENT_TYPE_APPLICATION_JSON)
   assert status_code == 400

def test_post_inference_parameter_api_measure_variant_keyvalue_invalid():
   DATA1 = {
       "measure": {
           "name": "respiratory-symptoms-risk",
           "variant": "1234"
       },
       "filePath": FILE_PATH1
   }
   status_code, response_json = API_Calls.post_inference_parameters_api(BASE_URLV2, DATA1, ACCESS_TOKEN,
                                                                        CONTENT_TYPE_APPLICATION_JSON)
   assert status_code == 400

def test_post_inference_parameter_api_measure_variant_keyvalue_invalid1():
   DATA1 = {
       "measure": {
           "name": "respiratory-symptoms-risk",
           "variant": "v1234"
       },
       "filePath": FILE_PATH1
   }
   status_code, response_json = API_Calls.post_inference_parameters_api(BASE_URLV2, DATA1, ACCESS_TOKEN,
                                                                        CONTENT_TYPE_APPLICATION_JSON)
   assert status_code == 404

def test_post_inference_parameter_api_measure_variant_keyvalue_blank():
   DATA1 = {
       "measure": {
           "name": "respiratory-symptoms-risk",
           "variant": " "
       },
       "filePath": FILE_PATH1
   }
   status_code, response_json = API_Calls.post_inference_parameters_api(BASE_URLV2, DATA1, ACCESS_TOKEN,
                                                                        CONTENT_TYPE_APPLICATION_JSON)
   assert status_code == 400

def test_post_inference_parameter_api_measure_name_and_variant_keyname_invalid():
   DATA1 = {
       "measure": {
           "name123": "respiratory-symptoms-risk",
           "variant123": "v2"
       },
       "filePath": FILE_PATH1
   }
   status_code, response_json = API_Calls.post_inference_parameters_api(BASE_URLV2, DATA1, ACCESS_TOKEN,
                                                                        CONTENT_TYPE_APPLICATION_JSON)
   assert status_code == 400

def test_post_inference_parameter_api_measure_name_and_variant_keyname_blank():
   DATA1 = {
       "measure": {
           " ": "respiratory-symptoms-risk",
           " ": "v2"
       },
       "filePath": FILE_PATH1
   }
   status_code, response_json = API_Calls.post_inference_parameters_api(BASE_URLV2, DATA1, ACCESS_TOKEN,
                                                                        CONTENT_TYPE_APPLICATION_JSON)
   assert status_code == 400

def test_post_inference_parameter_api_measure_name_and_variant_keyvalue_invalid():
   DATA1 = {
       "measure": {
           "name": "respiratory-symptoms-risk1234",
           "variant": "v21234"
       },
       "filePath": FILE_PATH1
   }
   status_code, response_json = API_Calls.post_inference_parameters_api(BASE_URLV2, DATA1, ACCESS_TOKEN,
                                                                        CONTENT_TYPE_APPLICATION_JSON)
   assert status_code == 404

def test_post_inference_parameter_api_measure_name_and_variant_keyvalue_blank():
   DATA1 = {
       "measure": {
           "name": " ",
           "variant": " "
       },
       "filePath": FILE_PATH1
   }
   status_code, response_json = API_Calls.post_inference_parameters_api(BASE_URLV2, DATA1, ACCESS_TOKEN,
                                                                        CONTENT_TYPE_APPLICATION_JSON)
   assert status_code == 400

def test_post_inference_parameter_api_requestbody_filePath_key_missing():
   D_CP = POST_INFERENCE_PARAMETER_DATA.copy()
   DATA = helper.delete_key(D_CP, 'filePath')
   status_code, response_json = API_Calls.post_inference_parameters_api(BASE_URLV2, DATA, ACCESS_TOKEN,
                                                                            CONTENT_TYPE_APPLICATION_JSON)
   assert status_code == 400

def test_post_inference_parameter_api_requestbody_filePath_keyname_blank():
   DATA1 = {
       "measure": {
           "name": "respiratory-symptoms-risk",
           "variant": "v2"
       },
       " ": FILE_PATH1,
   }
   status_code, response_json = API_Calls.post_inference_parameters_api(BASE_URLV2, DATA1, ACCESS_TOKEN,
                                                                        CONTENT_TYPE_APPLICATION_JSON)
   assert status_code == 400


def test_post_inference_parameter_api_requestbody_filePath_keyvalue_blank():
   D_CP = POST_INFERENCE_PARAMETER_DATA.copy()
   DATA = helper.update_dictionary(D_CP, filePath=' ')
   status_code, response_json = API_Calls.post_inference_parameters_api(BASE_URLV2, DATA, ACCESS_TOKEN,
                                                                            CONTENT_TYPE_APPLICATION_JSON)
   assert status_code == 404

def test_post_inference_parameter_api_requestbody_filePath_keyvalue_invalid():
   D_CP = POST_INFERENCE_PARAMETER_DATA.copy()
   DATA = helper.update_dictionary(D_CP, filePath='1234')
   status_code, response_json = API_Calls.post_inference_parameters_api(BASE_URLV2, DATA, ACCESS_TOKEN,
                                                                            CONTENT_TYPE_APPLICATION_JSON)
   assert status_code == 404 #File not found

def test_post_inference_parameter_api_requestbody_filePath_keyvalue_audio_file_with_silence():
   D_CP = POST_INFERENCE_PARAMETER_DATA.copy()
   DATA = helper.update_dictionary(D_CP, filePath=AUDIO_FILE_WITH_SILENCE)
   status_code, response_json = API_Calls.post_inference_parameters_api(BASE_URLV2, DATA, ACCESS_TOKEN,
                                                                            CONTENT_TYPE_APPLICATION_JSON)
   assert status_code == 404 # or 422  NEED TO CHECK THIS received ELICITATION_CHECK_FAILED

def test_post_inference_parameter_api_requestbody_filePath_keyvalue_no_audio_file_present_at_location():
    # login with token
    status_code, json_data = API_Calls.token_api(BASE_URL, VALID_TOKEN_DATA, BASE_TOKEN, CONTENT_TYPE_URL_ENCODED)
    print("token api result:", status_code)
    # assert status_code == 200
    ACCESS_TOKEN = json_data['access_token']

    # create subject
    status, subject_json = API_Calls.subject_api(BASE_URL, VALID_SUBJECT_DATA, ACCESS_TOKEN,
                                                 CONTENT_TYPE_APPLICATION_JSON)
    print("subject api result:", status, subject_json)
    SUB_IDENTIFIER1 = subject_json['userIdentifier']

    VALID_STORAGE_DATA1 = {
        "fileType": "wav",
        "countryCode": "US",
        "userIdentifier": SUB_IDENTIFIER1
    }
    # storage api
    status_code, response_json = API_Calls.storage_api(BASE_URL, VALID_STORAGE_DATA1, ACCESS_TOKEN,
                                                       CONTENT_TYPE_APPLICATION_JSON)
    STORAGE_SIGNED_URL1 = response_json['signedURL']
    print("1st audio storage api result:", status_code, response_json)
    FILE_PATH1 = response_json['filePath']

    # first file upload
    status_code = API_Calls.upload_sample_file(STORAGE_SIGNED_URL1, TC1_FILE_PATH1)
    print("First audio file upload:", status_code)

    INFERENCE_PARAMETER_DATA = {
        "measure": {
            "name": "respiratory-symptoms-risk",
            "variant": "v2"
        },
        "filePath": FILE_PATH1
    }
    # POST inference paramteres
    status_code, response_json = API_Calls.post_inference_parameters_api(BASE_URLV2, INFERENCE_PARAMETER_DATA,
                                                                         ACCESS_TOKEN, CONTENT_TYPE_APPLICATION_JSON)
    print("POST inference parameters API result", status_code, response_json)
    INFERENCE_PARAMETER_ID = response_json['id']
    print(INFERENCE_PARAMETER_ID)

    # storage api for 2nd audio file
    status_code, response_json = API_Calls.storage_api(BASE_URL, VALID_STORAGE_DATA1, ACCESS_TOKEN,
                                                       CONTENT_TYPE_APPLICATION_JSON)
    print("2nd audio storage api result:", status_code, response_json)
    STORAGE_SIGNED_URL2 = response_json['signedURL']
    FILE_PATH2 = response_json['filePath']

    INFERENCE_PARAMETER_DATA2 = {

        "filePath": FILE_PATH2
    }

    # second file upload
    #status_code = API_Calls.upload_sample_file(STORAGE_SIGNED_URL2, TC1_FILE_PATH2)
    #print("Second audio file upload: ", status_code)

    # PUT inference paramteres
    status_code, response_json = API_Calls.put_inference_parameters_api(BASE_URLV2, ACCESS_TOKEN,
                                                                        INFERENCE_PARAMETER_ID,
                                                                        INFERENCE_PARAMETER_DATA2,
                                                                        CONTENT_TYPE_APPLICATION_JSON)

    print("PUT inference parameters API result:", status_code, response_json)
    assert status_code == 404


def test_post_inference_parameter_api_requestbody_filePath_keyvalue_elicitation_failed():
   D_CP = POST_INFERENCE_PARAMETER_DATA.copy()
   DATA = helper.update_dictionary(D_CP, filePath=TC8_FILE_PATH1)
   status_code, response_json = API_Calls.post_inference_parameters_api(BASE_URLV2, DATA, ACCESS_TOKEN,
                                                                            CONTENT_TYPE_APPLICATION_JSON)
   assert status_code == 422  #   NEED TO CHECK THIS

def test_post_inference_parameter_api_requestbody_filePath_keyvalue_invalid_file_duration():
   D_CP = POST_INFERENCE_PARAMETER_DATA.copy()
   DATA = helper.update_dictionary(D_CP, filePath=TC9_FILE_PATH1)
   status_code, response_json = API_Calls.post_inference_parameters_api(BASE_URLV2, DATA, ACCESS_TOKEN,
                                                                            CONTENT_TYPE_APPLICATION_JSON)
   assert status_code == 422

def test_post_inference_parameter_api_requestbody_filePath_keyvalue_invalid_type():
   D_CP = POST_INFERENCE_PARAMETER_DATA.copy()
   DATA = helper.update_dictionary(D_CP, filePath=TC5_FILE_PATH1)
   status_code, response_json = API_Calls.post_inference_parameters_api(BASE_URLV2, DATA, ACCESS_TOKEN,
                                                                            CONTENT_TYPE_APPLICATION_JSON)
   assert status_code == 422

########################
# def test_post_inference_parameter_api_requestbody_filePath_keyvalue_file_specification_invalid():
########################

def test_post_inference_parameter_api_requestbody_extra_key_added():
   DATA1 = {
       "measure": {
           "name": " ",
           "variant": " "
       },
       "filePath": FILE_PATH1,
       "Test":"1234"
   }
   status_code, response_json = API_Calls.post_inference_parameters_api(BASE_URLV2, DATA1, ACCESS_TOKEN,
                                                                        CONTENT_TYPE_APPLICATION_JSON)
   assert status_code == 400

def test_post_inference_parameter_api_content_type_missing():
   headers = {'Authorization': ACCESS_TOKEN}
   res = requests.post(url=BASE_URLV2 + INFERENCE_PARAMETER_ENDPOINT, data=json.dumps(POST_INFERENCE_PARAMETER_DATA),
                       headers=headers)
   assert status_code == 415  # NEED TO CHECK

def test_post_inference_parameter_api_content_type_invalid():
   headers = {'Authorization': ACCESS_TOKEN, 'Content-Type': CONTENT_TYPE_URL_ENCODED}
   res = requests.post(url=BASE_URLV2 + INFERENCE_PARAMETER_ENDPOINT, data=json.dumps(POST_INFERENCE_PARAMETER_DATA),
                       headers=headers)
   assert res.status_code == 415 # NEED TO CHECK

def test_post_inference_parameter_api_content_type_blank():
   headers = {'Authorization': ACCESS_TOKEN, 'Content-Type': ' '}
   res = requests.post(url=BASE_URLV2 + INFERENCE_PARAMETER_ENDPOINT, data=json.dumps(POST_INFERENCE_PARAMETER_DATA),
                       headers=headers)
   assert res.status_code == 415 # NEED TO CHECK


# ------- score api before second file upload to test parameter_not_constructed yet ------#

def create_inference_payload():
   return {
       "inferenceParameterId": INFERENCE_PARAMETER_ID
   }

POST_INFERENCE_DATA = {
   "inferenceParameterId": INFERENCE_PARAMETER_ID
}



def test_POST_inference_scorev2_api_inference_parameter_not_constructed():
   status_code, response_json = API_Calls.post_inference_scorev2_api(BASE_URLV2, create_inference_payload(), ACCESS_TOKEN, CONTENT_TYPE_APPLICATION_JSON)
   assert status_code == 422

def test_POST_inference_scorev2_api_inference_parameter_not_constructed_with_access_token_bearer():
    ACCESS_TOKEN_BEARER = 'Bearer ' + ACCESS_TOKEN
    print(ACCESS_TOKEN_BEARER)
    status_code, response_json = API_Calls.post_inference_scorev2_api(BASE_URLV2, create_inference_payload(), ACCESS_TOKEN_BEARER, CONTENT_TYPE_APPLICATION_JSON)
    assert status_code == 422

#----- Update Inference parameter ------#

# def put_inference_parameters_api(BASE_URLV2, ACCESS_TOKEN,INFERENCE_PARAMETER_ID,DATA, CONTENT_TYPE_APPLICATION_JSON):
#    headers_inference_parameters= {'Authorization': ACCESS_TOKEN, 'Content-Type': CONTENT_TYPE_APPLICATION_JSON}
#    res = requests.put(url=BASE_URLV2 + INFERENCE_PARAMETER_PUTENDPOINT + INFERENCE_PARAMETER_ID,data=json.dumps(DATA),  headers=headers_inference_parameters)
# #    return res.status_code, res.json()
# def test_post_inference_parameter_api_inprogress():
#    print(FILE_PATH1)
#    global INFERENCE_PARAMETER_ID
#    status_code, response_json = API_Calls.post_inference_parameters_api(BASE_URLV2, POST_INFERENCE_PARAMETER_DATA, ACCESS_TOKEN,
#                                                                             CONTENT_TYPE_APPLICATION_JSON)
#    assert status_code == 202
#    INFERENCE_PARAMETER_ID = response_json['id']
#    assertion.assert_valid_schema(response_json, 'v2_post_inference_parameter.json')



def test_put_inference_parameter_api():
   status_code, response_json = API_Calls.put_inference_parameters_api(BASE_URLV2, ACCESS_TOKEN,INFERENCE_PARAMETER_ID,PUT_INFERENCE_PARAMETER_DATA,                                                                            CONTENT_TYPE_APPLICATION_JSON)
   assert status_code == 201
   assertion.assert_valid_schema(response_json, 'v2_post_inference_parameter.json')


def test_put_inference_parameter_api_access_token_with_bearer():
    ACCESS_TOKEN_BEARER = 'Bearer ' + ACCESS_TOKEN
    print(ACCESS_TOKEN_BEARER)
    status_code, response_json = API_Calls.put_inference_parameters_api(BASE_URLV2, ACCESS_TOKEN_BEARER,INFERENCE_PARAMETER_ID,PUT_INFERENCE_PARAMETER_DATA,                                                                            CONTENT_TYPE_APPLICATION_JSON)
    assert status_code == 201
    assertion.assert_valid_schema(response_json, 'v2_post_inference_parameter.json')


def test_put_inference_parameter_api_incorrect_accesstoken():
   INCORRECT_ACCESS_TOKEN = 'xyz'
   print(INFERENCE_PARAMETER_ID)
   status_code, response_json = API_Calls.put_inference_parameters_api(BASE_URLV2,INCORRECT_ACCESS_TOKEN,INFERENCE_PARAMETER_ID,PUT_INFERENCE_PARAMETER_DATA,CONTENT_TYPE_APPLICATION_JSON)

   assert status_code == 401

def test_put_inference_parameter_api_expired_accesstoken():
   status_code, response_json = API_Calls.put_inference_parameters_api(BASE_URLV2, EXPIRED_ACCESS_TOKEN,INFERENCE_PARAMETER_ID,PUT_INFERENCE_PARAMETER_DATA,CONTENT_TYPE_APPLICATION_JSON)
   assert status_code == 401

def test_put_inference_parameter_api_accesstoken_with_bearer_in_small_case():
    ACCESS_TOKEN_BEARER1 = 'bearer ' + ACCESS_TOKEN
    print(ACCESS_TOKEN_BEARER1)
    status_code, response_json = API_Calls.put_inference_parameters_api(BASE_URLV2, ACCESS_TOKEN_BEARER1,INFERENCE_PARAMETER_ID,PUT_INFERENCE_PARAMETER_DATA,CONTENT_TYPE_APPLICATION_JSON)
    assert status_code == 401

def test_put_inference_parameter_api_missing_accesstoken():
   headers = {'Content-Type': CONTENT_TYPE_APPLICATION_JSON}
   res = requests.put(BASE_URLV2 + INFERENCE_PARAMETER_PUTENDPOINT + INFERENCE_PARAMETER_ID,data=json.dumps(PUT_INFERENCE_PARAMETER_DATA),  headers=headers)
   assert res.status_code == 401

def test_put_inference_parameter_api_blank_accesstoken():
   headers = {'Authorization': '', 'Content-Type': CONTENT_TYPE_APPLICATION_JSON}
   res = requests.put(BASE_URLV2 + INFERENCE_PARAMETER_PUTENDPOINT + INFERENCE_PARAMETER_ID,data=json.dumps(PUT_INFERENCE_PARAMETER_DATA),  headers=headers)
   assert res.status_code == 401

def test_put_inference_parameter_api_no_request_body():
    status_code, json_data = API_Calls.token_api(BASE_URL, VALID_TOKEN_DATA, BASE_TOKEN, CONTENT_TYPE_URL_ENCODED)
    print("token api result:", status_code)
    # assert status_code == 200
    ACCESS_TOKEN = json_data['access_token']

    # create subject
    status, subject_json = API_Calls.subject_api(BASE_URL, VALID_SUBJECT_DATA, ACCESS_TOKEN,
                                                 CONTENT_TYPE_APPLICATION_JSON)
    print("subject api result:", status, subject_json)
    SUB_IDENTIFIER1 = subject_json['userIdentifier']

    VALID_STORAGE_DATA1 = {
        "fileType": "wav",
        "countryCode": "US",
        "userIdentifier": SUB_IDENTIFIER1
    }
    # storage api
    status_code, response_json = API_Calls.storage_api(BASE_URL, VALID_STORAGE_DATA1, ACCESS_TOKEN,
                                                       CONTENT_TYPE_APPLICATION_JSON)
    STORAGE_SIGNED_URL1 = response_json['signedURL']
    print("1st audio storage api result:", status_code, response_json)
    FILE_PATH1 = response_json['filePath']

    # first file upload
    status_code = API_Calls.upload_sample_file(STORAGE_SIGNED_URL1, TC1_FILE_PATH1)
    print("First audio file upload:", status_code)

    INFERENCE_PARAMETER_DATA = {
        "measure": {
            "name": "respiratory-symptoms-risk",
            "variant": "v2"
        },
        "filePath": FILE_PATH1
    }
    # POST inference paramteres
    status_code, response_json = API_Calls.post_inference_parameters_api(BASE_URLV2, INFERENCE_PARAMETER_DATA,
                                                                         ACCESS_TOKEN, CONTENT_TYPE_APPLICATION_JSON)
    print("POST inference parameters API result", status_code, response_json)
    INFERENCE_PARAMETER_ID = response_json['id']
    print(INFERENCE_PARAMETER_ID)

    # storage api for 2nd audio file
    status_code, response_json = API_Calls.storage_api(BASE_URL, VALID_STORAGE_DATA1, ACCESS_TOKEN,
                                                       CONTENT_TYPE_APPLICATION_JSON)
    print("2nd audio storage api result:", status_code, response_json)
    STORAGE_SIGNED_URL2 = response_json['signedURL']
    FILE_PATH2 = response_json['filePath']

    INFERENCE_PARAMETER_DATA2 = {


    }

    # second file upload
    status_code = API_Calls.upload_sample_file(STORAGE_SIGNED_URL2, TC1_FILE_PATH2)
    print("Second audio file upload: ", status_code)

    # PUT inference paramteres
    status_code, response_json = API_Calls.put_inference_parameters_api(BASE_URLV2, ACCESS_TOKEN,
                                                                        INFERENCE_PARAMETER_ID,
                                                                        INFERENCE_PARAMETER_DATA2,
                                                                        CONTENT_TYPE_APPLICATION_JSON)

    print("PUT inference parameters API result:", status_code, response_json)
    assert status_code == 400

def test_put_inference_parameter_api_invalid_endpoint():
   INVALID_INFERENCE_PARAMETER_ENDPOINT = '/inference/inference-parameters123/'
   headers = {'Authorization': ACCESS_TOKEN, 'Content-Type': CONTENT_TYPE_APPLICATION_JSON}
   res = requests.put(BASE_URLV2 + INVALID_INFERENCE_PARAMETER_ENDPOINT + INFERENCE_PARAMETER_ID,
                      data=json.dumps(PUT_INFERENCE_PARAMETER_DATA), headers=headers)
   assert res.status_code == 403

def test_put_inference_parameter_api_requestbody_filePath_key_missing():
    status_code, json_data = API_Calls.token_api(BASE_URL, VALID_TOKEN_DATA, BASE_TOKEN, CONTENT_TYPE_URL_ENCODED)
    print("token api result:", status_code)
    # assert status_code == 200
    ACCESS_TOKEN = json_data['access_token']

    # create subject
    status, subject_json = API_Calls.subject_api(BASE_URL, VALID_SUBJECT_DATA, ACCESS_TOKEN,
                                                 CONTENT_TYPE_APPLICATION_JSON)
    print("subject api result:", status, subject_json)
    SUB_IDENTIFIER1 = subject_json['userIdentifier']

    VALID_STORAGE_DATA1 = {
        "fileType": "wav",
        "countryCode": "US",
        "userIdentifier": SUB_IDENTIFIER1
    }
    # storage api
    status_code, response_json = API_Calls.storage_api(BASE_URL, VALID_STORAGE_DATA1, ACCESS_TOKEN,
                                                       CONTENT_TYPE_APPLICATION_JSON)
    STORAGE_SIGNED_URL1 = response_json['signedURL']
    print("1st audio storage api result:", status_code, response_json)
    FILE_PATH1 = response_json['filePath']

    # first file upload
    status_code = API_Calls.upload_sample_file(STORAGE_SIGNED_URL1, TC1_FILE_PATH1)
    print("First audio file upload:", status_code)

    INFERENCE_PARAMETER_DATA = {
        "measure": {
            "name": "respiratory-symptoms-risk",
            "variant": "v2"
        },
        "filePath": FILE_PATH1
    }
    # POST inference paramteres
    status_code, response_json = API_Calls.post_inference_parameters_api(BASE_URLV2, INFERENCE_PARAMETER_DATA,
                                                                         ACCESS_TOKEN, CONTENT_TYPE_APPLICATION_JSON)
    print("POST inference parameters API result", status_code, response_json)
    INFERENCE_PARAMETER_ID = response_json['id']
    print(INFERENCE_PARAMETER_ID)

    # storage api for 2nd audio file
    status_code, response_json = API_Calls.storage_api(BASE_URL, VALID_STORAGE_DATA1, ACCESS_TOKEN,
                                                       CONTENT_TYPE_APPLICATION_JSON)
    print("2nd audio storage api result:", status_code, response_json)
    STORAGE_SIGNED_URL2 = response_json['signedURL']
    FILE_PATH2 = response_json['filePath']

    INFERENCE_PARAMETER_DATA2 = {
        #"filePath": FILE_PATH2
    }

    # second file upload
    status_code = API_Calls.upload_sample_file(STORAGE_SIGNED_URL2, TC1_FILE_PATH2)
    print("Second audio file upload: ", status_code)

    # PUT inference paramteres
    status_code, response_json = API_Calls.put_inference_parameters_api(BASE_URLV2, ACCESS_TOKEN,
                                                                        INFERENCE_PARAMETER_ID,
                                                                        INFERENCE_PARAMETER_DATA2,
                                                                        CONTENT_TYPE_APPLICATION_JSON)

    print("PUT inference parameters API result:", status_code, response_json)
    assert status_code == 400


def test_put_inference_parameter_api_requestbody_filePath_keyname_blank():
    status_code, json_data = API_Calls.token_api(BASE_URL, VALID_TOKEN_DATA, BASE_TOKEN, CONTENT_TYPE_URL_ENCODED)
    print("token api result:", status_code)
    # assert status_code == 200
    ACCESS_TOKEN = json_data['access_token']

    # create subject
    status, subject_json = API_Calls.subject_api(BASE_URL, VALID_SUBJECT_DATA, ACCESS_TOKEN,
                                                 CONTENT_TYPE_APPLICATION_JSON)
    print("subject api result:", status, subject_json)
    SUB_IDENTIFIER1 = subject_json['userIdentifier']

    VALID_STORAGE_DATA1 = {
        "fileType": "wav",
        "countryCode": "US",
        "userIdentifier": SUB_IDENTIFIER1
    }
    # storage api
    status_code, response_json = API_Calls.storage_api(BASE_URL, VALID_STORAGE_DATA1, ACCESS_TOKEN,
                                                       CONTENT_TYPE_APPLICATION_JSON)
    STORAGE_SIGNED_URL1 = response_json['signedURL']
    print("1st audio storage api result:", status_code, response_json)
    FILE_PATH1 = response_json['filePath']

    # first file upload
    status_code = API_Calls.upload_sample_file(STORAGE_SIGNED_URL1, TC1_FILE_PATH1)
    print("First audio file upload:", status_code)

    INFERENCE_PARAMETER_DATA = {
        "measure": {
            "name": "respiratory-symptoms-risk",
            "variant": "v2"
        },
        "filePath": FILE_PATH1
    }
    # POST inference paramteres
    status_code, response_json = API_Calls.post_inference_parameters_api(BASE_URLV2, INFERENCE_PARAMETER_DATA,
                                                                         ACCESS_TOKEN, CONTENT_TYPE_APPLICATION_JSON)
    print("POST inference parameters API result", status_code, response_json)
    INFERENCE_PARAMETER_ID = response_json['id']
    print(INFERENCE_PARAMETER_ID)

    # storage api for 2nd audio file
    status_code, response_json = API_Calls.storage_api(BASE_URL, VALID_STORAGE_DATA1, ACCESS_TOKEN,
                                                       CONTENT_TYPE_APPLICATION_JSON)
    print("2nd audio storage api result:", status_code, response_json)
    STORAGE_SIGNED_URL2 = response_json['signedURL']
    FILE_PATH2 = response_json['filePath']

    INFERENCE_PARAMETER_DATA2 = {
        "": FILE_PATH2
    }

    # second file upload
    status_code = API_Calls.upload_sample_file(STORAGE_SIGNED_URL2, TC1_FILE_PATH2)
    print("Second audio file upload: ", status_code)

    # PUT inference paramteres
    status_code, response_json = API_Calls.put_inference_parameters_api(BASE_URLV2, ACCESS_TOKEN,
                                                                        INFERENCE_PARAMETER_ID,
                                                                        INFERENCE_PARAMETER_DATA2,
                                                                        CONTENT_TYPE_APPLICATION_JSON)

    print("PUT inference parameters API result:", status_code, response_json)
    assert status_code == 400


def test_put_inference_parameter_api_requestbody_filePath_keyvalue_blank():
    status_code, json_data = API_Calls.token_api(BASE_URL, VALID_TOKEN_DATA, BASE_TOKEN, CONTENT_TYPE_URL_ENCODED)
    print("token api result:", status_code)
    # assert status_code == 200
    ACCESS_TOKEN = json_data['access_token']

    # create subject
    status, subject_json = API_Calls.subject_api(BASE_URL, VALID_SUBJECT_DATA, ACCESS_TOKEN,
                                                 CONTENT_TYPE_APPLICATION_JSON)
    print("subject api result:", status, subject_json)
    SUB_IDENTIFIER1 = subject_json['userIdentifier']

    VALID_STORAGE_DATA1 = {
        "fileType": "wav",
        "countryCode": "US",
        "userIdentifier": SUB_IDENTIFIER1
    }
    # storage api
    status_code, response_json = API_Calls.storage_api(BASE_URL, VALID_STORAGE_DATA1, ACCESS_TOKEN,
                                                       CONTENT_TYPE_APPLICATION_JSON)
    STORAGE_SIGNED_URL1 = response_json['signedURL']
    print("1st audio storage api result:", status_code, response_json)
    FILE_PATH1 = response_json['filePath']

    # first file upload
    status_code = API_Calls.upload_sample_file(STORAGE_SIGNED_URL1, TC1_FILE_PATH1)
    print("First audio file upload:", status_code)

    INFERENCE_PARAMETER_DATA = {
        "measure": {
            "name": "respiratory-symptoms-risk",
            "variant": "v2"
        },
        "filePath": FILE_PATH1
    }
    # POST inference paramteres
    status_code, response_json = API_Calls.post_inference_parameters_api(BASE_URLV2, INFERENCE_PARAMETER_DATA,
                                                                         ACCESS_TOKEN, CONTENT_TYPE_APPLICATION_JSON)
    print("POST inference parameters API result", status_code, response_json)
    INFERENCE_PARAMETER_ID = response_json['id']
    print(INFERENCE_PARAMETER_ID)

    # storage api for 2nd audio file
    status_code, response_json = API_Calls.storage_api(BASE_URL, VALID_STORAGE_DATA1, ACCESS_TOKEN,
                                                       CONTENT_TYPE_APPLICATION_JSON)
    print("2nd audio storage api result:", status_code, response_json)
    STORAGE_SIGNED_URL2 = response_json['signedURL']
    FILE_PATH2 = response_json['filePath']

    INFERENCE_PARAMETER_DATA2 = {
        "filePath": ''       ''
    }

    # second file upload
    status_code = API_Calls.upload_sample_file(STORAGE_SIGNED_URL2, TC1_FILE_PATH2)
    print("Second audio file upload: ", status_code)

    # PUT inference paramteres
    status_code, response_json = API_Calls.put_inference_parameters_api(BASE_URLV2, ACCESS_TOKEN,
                                                                        INFERENCE_PARAMETER_ID,
                                                                        INFERENCE_PARAMETER_DATA2,
                                                                        CONTENT_TYPE_APPLICATION_JSON)

    print("PUT inference parameters API result:", status_code, response_json)
    assert status_code == 400


def test_put_inference_parameter_api_requestbody_filePath_keyvalue_invalid():
    status_code, json_data = API_Calls.token_api(BASE_URL, VALID_TOKEN_DATA, BASE_TOKEN, CONTENT_TYPE_URL_ENCODED)
    print("token api result:", status_code)
    # assert status_code == 200
    ACCESS_TOKEN = json_data['access_token']

    # create subject
    status, subject_json = API_Calls.subject_api(BASE_URL, VALID_SUBJECT_DATA, ACCESS_TOKEN,
                                                 CONTENT_TYPE_APPLICATION_JSON)
    print("subject api result:", status, subject_json)
    SUB_IDENTIFIER1 = subject_json['userIdentifier']

    VALID_STORAGE_DATA1 = {
        "fileType": "wav",
        "countryCode": "US",
        "userIdentifier": SUB_IDENTIFIER1
    }
    # storage api
    status_code, response_json = API_Calls.storage_api(BASE_URL, VALID_STORAGE_DATA1, ACCESS_TOKEN,
                                                       CONTENT_TYPE_APPLICATION_JSON)
    STORAGE_SIGNED_URL1 = response_json['signedURL']
    print("1st audio storage api result:", status_code, response_json)
    FILE_PATH1 = response_json['filePath']

    # first file upload
    status_code = API_Calls.upload_sample_file(STORAGE_SIGNED_URL1, TC1_FILE_PATH1)
    print("First audio file upload:", status_code)

    INFERENCE_PARAMETER_DATA = {
        "measure": {
            "name": "respiratory-symptoms-risk",
            "variant": "v2"
        },
        "filePath": FILE_PATH1
    }
    # POST inference paramteres
    status_code, response_json = API_Calls.post_inference_parameters_api(BASE_URLV2, INFERENCE_PARAMETER_DATA,
                                                                         ACCESS_TOKEN, CONTENT_TYPE_APPLICATION_JSON)
    print("POST inference parameters API result", status_code, response_json)
    INFERENCE_PARAMETER_ID = response_json['id']
    print(INFERENCE_PARAMETER_ID)

    # storage api for 2nd audio file
    status_code, response_json = API_Calls.storage_api(BASE_URL, VALID_STORAGE_DATA1, ACCESS_TOKEN,
                                                       CONTENT_TYPE_APPLICATION_JSON)
    print("2nd audio storage api result:", status_code, response_json)
    STORAGE_SIGNED_URL2 = response_json['signedURL']
    FILE_PATH2 = response_json['filePath']

    INFERENCE_PARAMETER_DATA2 = {
        "filePath": "abcdef"
    }

    # second file upload
    status_code = API_Calls.upload_sample_file(STORAGE_SIGNED_URL2, TC1_FILE_PATH2)
    print("Second audio file upload: ", status_code)

    # PUT inference paramteres
    status_code, response_json = API_Calls.put_inference_parameters_api(BASE_URLV2, ACCESS_TOKEN,
                                                                        INFERENCE_PARAMETER_ID,
                                                                        INFERENCE_PARAMETER_DATA2,
                                                                        CONTENT_TYPE_APPLICATION_JSON)

    print("PUT inference parameters API result:", status_code, response_json)
    assert status_code == 404


def test_put_inference_parameter_api_requestbody_filePath_keyvalue_audio_file_with_silence():
   D_CP = PUT_INFERENCE_PARAMETER_DATA.copy()
   DATA = helper.update_dictionary(D_CP, filePath=AUDIO_FILE_WITH_SILENCE)
   status_code, response_json = API_Calls.put_inference_parameters_api(BASE_URLV2, ACCESS_TOKEN,INFERENCE_PARAMETER_ID,DATA, CONTENT_TYPE_APPLICATION_JSON)
   assert status_code == 422

def test_put_inference_parameter_api_requestbody_filePath_keyvalue_no_audio_file_present_at_location():
    # login with token
    status_code, json_data = API_Calls.token_api(BASE_URL, VALID_TOKEN_DATA, BASE_TOKEN, CONTENT_TYPE_URL_ENCODED)
    print("token api result:", status_code)
    # assert status_code == 200
    ACCESS_TOKEN = json_data['access_token']

    # create subject
    status, subject_json = API_Calls.subject_api(BASE_URL, VALID_SUBJECT_DATA, ACCESS_TOKEN,
                                                 CONTENT_TYPE_APPLICATION_JSON)
    print("subject api result:", status, subject_json)
    SUB_IDENTIFIER1 = subject_json['userIdentifier']

    VALID_STORAGE_DATA1 = {
        "fileType": "wav",
        "countryCode": "US",
        "userIdentifier": SUB_IDENTIFIER1
    }
    # storage api
    status_code, response_json = API_Calls.storage_api(BASE_URL, VALID_STORAGE_DATA1, ACCESS_TOKEN,
                                                       CONTENT_TYPE_APPLICATION_JSON)
    STORAGE_SIGNED_URL1 = response_json['signedURL']
    print("1st audio storage api result:", status_code, response_json)
    FILE_PATH1 = response_json['filePath']

    # first file upload
    status_code = API_Calls.upload_sample_file(STORAGE_SIGNED_URL1, TC1_FILE_PATH1)
    print("First audio file upload:", status_code)

    INFERENCE_PARAMETER_DATA = {
        "measure": {
            "name": "respiratory-symptoms-risk",
            "variant": "v2"
        },
        "filePath": FILE_PATH1
    }
    # POST inference paramteres
    status_code, response_json = API_Calls.post_inference_parameters_api(BASE_URLV2, INFERENCE_PARAMETER_DATA,
                                                                         ACCESS_TOKEN, CONTENT_TYPE_APPLICATION_JSON)
    print("POST inference parameters API result", status_code, response_json)
    INFERENCE_PARAMETER_ID = response_json['id']
    print(INFERENCE_PARAMETER_ID)

    # storage api for 2nd audio file
    status_code, response_json = API_Calls.storage_api(BASE_URL, VALID_STORAGE_DATA1, ACCESS_TOKEN,
                                                       CONTENT_TYPE_APPLICATION_JSON)
    print("2nd audio storage api result:", status_code, response_json)
    STORAGE_SIGNED_URL2 = response_json['signedURL']
    FILE_PATH2 = response_json['filePath']

    INFERENCE_PARAMETER_DATA2 = {

        "filePath": FILE_PATH2
    }

    # second file upload
   # status_code = API_Calls.upload_sample_file(STORAGE_SIGNED_URL2, TC1_FILE_PATH2)
    # print("Second audio file upload: ", status_code)

    # PUT inference paramteres
    status_code, response_json = API_Calls.put_inference_parameters_api(BASE_URLV2, ACCESS_TOKEN,
                                                                        INFERENCE_PARAMETER_ID,
                                                                        INFERENCE_PARAMETER_DATA2,
                                                                        CONTENT_TYPE_APPLICATION_JSON)

    print("PUT inference parameters API result:", status_code, response_json)
    assert status_code == 404

def test_put_inference_parameter_api_requestbody_filePath_keyvalue_elicitation_failed():
   D_CP = PUT_INFERENCE_PARAMETER_DATA.copy()
   DATA = helper.update_dictionary(D_CP, filePath=ELECITATION_FILED_FILE)
   status_code, response_json = API_Calls.put_inference_parameters_api(BASE_URLV2, ACCESS_TOKEN,INFERENCE_PARAMETER_ID,DATA, CONTENT_TYPE_APPLICATION_JSON)
   assert status_code == 422

def test_put_inference_parameter_api_requestbody_filePath_keyvalue_invalid_file_duration():
   D_CP = PUT_INFERENCE_PARAMETER_DATA.copy()
   DATA = helper.update_dictionary(D_CP, filePath=TC9_FILE_PATH1)
   status_code, response_json = API_Calls.put_inference_parameters_api(BASE_URLV2, ACCESS_TOKEN,INFERENCE_PARAMETER_ID,DATA, CONTENT_TYPE_APPLICATION_JSON)
   assert status_code == 422

def test_put_inference_parameter_api_requestbody_filePath_keyvalue_invalid_type():
   D_CP = PUT_INFERENCE_PARAMETER_DATA.copy()
   DATA = helper.update_dictionary(D_CP, filePath=TC5_FILE_PATH1)
   status_code, response_json = API_Calls.put_inference_parameters_api(BASE_URLV2, ACCESS_TOKEN,INFERENCE_PARAMETER_ID,DATA, CONTENT_TYPE_APPLICATION_JSON)
   assert status_code == 422  #or 400

########################
# def test_put_inference_parameter_api_requestbody_filePath_keyvalue_file_specification_invalid():
########################

def test_put_inference_parameter_api_requestbody_extra_key_added():
    # login with token
    status_code, json_data = API_Calls.token_api(BASE_URL, VALID_TOKEN_DATA, BASE_TOKEN, CONTENT_TYPE_URL_ENCODED)
    print("token api result:", status_code)
    # assert status_code == 200
    ACCESS_TOKEN = json_data['access_token']

    # create subject
    status, subject_json = API_Calls.subject_api(BASE_URL, VALID_SUBJECT_DATA, ACCESS_TOKEN,
                                                 CONTENT_TYPE_APPLICATION_JSON)
    print("subject api result:", status, subject_json)
    SUB_IDENTIFIER1 = subject_json['userIdentifier']

    VALID_STORAGE_DATA1 = {
        "fileType": "wav",
        "countryCode": "US",
        "userIdentifier": SUB_IDENTIFIER1
    }
    # storage api
    status_code, response_json = API_Calls.storage_api(BASE_URL, VALID_STORAGE_DATA1, ACCESS_TOKEN,
                                                       CONTENT_TYPE_APPLICATION_JSON)
    STORAGE_SIGNED_URL1 = response_json['signedURL']
    print("1st audio storage api result:", status_code, response_json)
    FILE_PATH1 = response_json['filePath']

    # first file upload
    status_code = API_Calls.upload_sample_file(STORAGE_SIGNED_URL1, TC1_FILE_PATH1)
    print("First audio file upload:", status_code)

    INFERENCE_PARAMETER_DATA = {
        "measure": {
            "name": "respiratory-symptoms-risk",
            "variant": "v2"
        },
        "filePath": FILE_PATH1
    }
    # POST inference paramteres
    status_code, response_json = API_Calls.post_inference_parameters_api(BASE_URLV2, INFERENCE_PARAMETER_DATA,
                                                                         ACCESS_TOKEN, CONTENT_TYPE_APPLICATION_JSON)
    print("POST inference parameters API result", status_code, response_json)
    INFERENCE_PARAMETER_ID = response_json['id']
    print(INFERENCE_PARAMETER_ID)

    # storage api for 2nd audio file
    status_code, response_json = API_Calls.storage_api(BASE_URL, VALID_STORAGE_DATA1, ACCESS_TOKEN,
                                                       CONTENT_TYPE_APPLICATION_JSON)
    print("2nd audio storage api result:", status_code, response_json)
    STORAGE_SIGNED_URL2 = response_json['signedURL']
    FILE_PATH2 = response_json['filePath']

    INFERENCE_PARAMETER_DATA2 = {

        "filePath": FILE_PATH2,
        "abc" :"xyz"

    }

    # second file upload
    status_code = API_Calls.upload_sample_file(STORAGE_SIGNED_URL2, TC1_FILE_PATH2)
    print("Second audio file upload: ", status_code)

    # PUT inference paramteres
    status_code, response_json = API_Calls.put_inference_parameters_api(BASE_URLV2, ACCESS_TOKEN,
                                                                        INFERENCE_PARAMETER_ID,
                                                                        INFERENCE_PARAMETER_DATA2,
                                                                        CONTENT_TYPE_APPLICATION_JSON)

    print("PUT inference parameters API result:", status_code, response_json)
    assert status_code == 400

def test_put_inference_parameter_api_content_type_missing():

    status_code, json_data = API_Calls.token_api(BASE_URL, VALID_TOKEN_DATA, BASE_TOKEN, CONTENT_TYPE_URL_ENCODED)
    print("token api result:", status_code)
    # assert status_code == 200
    ACCESS_TOKEN = json_data['access_token']

    # create subject
    status, subject_json = API_Calls.subject_api(BASE_URL, VALID_SUBJECT_DATA, ACCESS_TOKEN,
                                                 CONTENT_TYPE_APPLICATION_JSON)
    print("subject api result:", status, subject_json)
    SUB_IDENTIFIER1 = subject_json['userIdentifier']

    VALID_STORAGE_DATA1 = {
        "fileType": "wav",
        "countryCode": "US",
        "userIdentifier": SUB_IDENTIFIER1
    }
    # storage api
    status_code, response_json = API_Calls.storage_api(BASE_URL, VALID_STORAGE_DATA1, ACCESS_TOKEN,
                                                       CONTENT_TYPE_APPLICATION_JSON)
    STORAGE_SIGNED_URL1 = response_json['signedURL']
    print("1st audio storage api result:", status_code, response_json)
    FILE_PATH1 = response_json['filePath']

    # first file upload
    status_code = API_Calls.upload_sample_file(STORAGE_SIGNED_URL1, TC1_FILE_PATH1)
    print("First audio file upload:", status_code)

    INFERENCE_PARAMETER_DATA = {
        "measure": {
            "name": "respiratory-symptoms-risk",
            "variant": "v2"
        },
        "filePath": FILE_PATH1
    }
    # POST inference paramteres
    status_code, response_json = API_Calls.post_inference_parameters_api(BASE_URLV2, INFERENCE_PARAMETER_DATA,
                                                                         ACCESS_TOKEN, CONTENT_TYPE_APPLICATION_JSON)
    print("POST inference parameters API result", status_code, response_json)
    INFERENCE_PARAMETER_ID = response_json['id']
    print(INFERENCE_PARAMETER_ID)

    # storage api for 2nd audio file
    status_code, response_json = API_Calls.storage_api(BASE_URL, VALID_STORAGE_DATA1, ACCESS_TOKEN,
                                                       CONTENT_TYPE_APPLICATION_JSON)
    print("2nd audio storage api result:", status_code, response_json)
    STORAGE_SIGNED_URL2 = response_json['signedURL']
    FILE_PATH2 = response_json['filePath']

    INFERENCE_PARAMETER_DATA2 = {

        "filePath": FILE_PATH2


    }

    # second file upload
    status_code = API_Calls.upload_sample_file(STORAGE_SIGNED_URL2, TC1_FILE_PATH2)
    print("Second audio file upload: ", status_code)

    # PUT inference paramteres

    headers = {'Authorization': ACCESS_TOKEN}
    status_code = requests.put(url=BASE_URLV2 + INFERENCE_PARAMETER_ENDPOINT+ '/' +INFERENCE_PARAMETER_ID, data=json.dumps(POST_INFERENCE_PARAMETER_DATA),
                       headers=headers)
    assert status_code == 415


def test_put_inference_parameter_api_content_type_invalid():
   headers = {'Authorization': ACCESS_TOKEN, 'Content-Type': CONTENT_TYPE_URL_ENCODED}
   res = requests.put(BASE_URLV2 + INFERENCE_PARAMETER_PUTENDPOINT + INFERENCE_PARAMETER_ID,data=json.dumps(PUT_INFERENCE_PARAMETER_DATA), headers=headers)
   assert res.status_code == 415

def test_put_inference_parameter_api_content_type_blank():
   headers = {'Authorization': ACCESS_TOKEN, 'Content-Type': ' '}
   res = requests.put(BASE_URLV2 + INFERENCE_PARAMETER_PUTENDPOINT + INFERENCE_PARAMETER_ID,data=json.dumps(PUT_INFERENCE_PARAMETER_DATA), headers=headers)
   assert res.status_code == 415

   # INFERENCE_PARAMETER_ALREADY_CONSTRUCTED
def test_put_inference_parameters_api_inference_prameter_already_constructed():
    # login with token
    status_code, json_data = API_Calls.token_api(BASE_URL, VALID_TOKEN_DATA, BASE_TOKEN, CONTENT_TYPE_URL_ENCODED)
    print("token api result:", status_code)
    # assert status_code == 200
    ACCESS_TOKEN = json_data['access_token']

    # create subject
    status, subject_json = API_Calls.subject_api(BASE_URL, VALID_SUBJECT_DATA, ACCESS_TOKEN,
                                                 CONTENT_TYPE_APPLICATION_JSON)
    print("subject api result:", status, subject_json)
    SUB_IDENTIFIER1 = subject_json['userIdentifier']

    VALID_STORAGE_DATA1 = {
        "fileType": "wav",
        "countryCode": "US",
        "userIdentifier": SUB_IDENTIFIER1
    }
    # storage api
    status_code, response_json = API_Calls.storage_api(BASE_URL, VALID_STORAGE_DATA1, ACCESS_TOKEN,
                                                       CONTENT_TYPE_APPLICATION_JSON)
    STORAGE_SIGNED_URL1 = response_json['signedURL']
    print("1st audio storage api result:", status_code, response_json)
    FILE_PATH1 = response_json['filePath']

    # first file upload
    status_code = API_Calls.upload_sample_file(STORAGE_SIGNED_URL1, TC1_FILE_PATH1)
    print("First audio file upload:", status_code)

    INFERENCE_PARAMETER_DATA = {
        "measure": {
            "name": "respiratory-symptoms-risk",
            "variant": "v2"
        },
        "filePath": FILE_PATH1
    }
    # POST inference paramteres
    status_code, response_json = API_Calls.post_inference_parameters_api(BASE_URLV2, INFERENCE_PARAMETER_DATA,
                                                                         ACCESS_TOKEN, CONTENT_TYPE_APPLICATION_JSON)
    print("POST inference parameters API result", status_code, response_json)
    INFERENCE_PARAMETER_ID = response_json['id']
    print(INFERENCE_PARAMETER_ID)

    # storage api for 2nd audio file
    status_code, response_json = API_Calls.storage_api(BASE_URL, VALID_STORAGE_DATA1, ACCESS_TOKEN,
                                                       CONTENT_TYPE_APPLICATION_JSON)
    print("2nd audio storage api result:", status_code, response_json)
    STORAGE_SIGNED_URL2 = response_json['signedURL']
    FILE_PATH2 = response_json['filePath']

    INFERENCE_PARAMETER_DATA2 = {

        "filePath": FILE_PATH2
    }

    # second file upload
    status_code = API_Calls.upload_sample_file(STORAGE_SIGNED_URL2, TC1_FILE_PATH2)
    print("Second audio file upload: ", status_code)

    # PUT inference paramteres
    status_code, response_json = API_Calls.put_inference_parameters_api(BASE_URLV2, ACCESS_TOKEN,
                                                                        INFERENCE_PARAMETER_ALREADY_CONSTRUCTED2,
                                                                        INFERENCE_PARAMETER_DATA2,
                                                                        CONTENT_TYPE_APPLICATION_JSON)

    print("PUT inference parameters API result:", status_code, response_json)

    assert  status_code == 422

# INDIFFERENT_AUDIO_FILE_ERROR
def test_put_inference_parameters_api_same_audio_file():
   D_CP = PUT_INFERENCE_PARAMETER_DATA.copy()
   DATA = helper.update_dictionary(D_CP, filePath=FILE_PATH3)
   status_code, response_json = API_Calls.put_inference_parameters_api(BASE_URLV2, ACCESS_TOKEN,INFERENCE_PARAMETER_ID,DATA,CONTENT_TYPE_APPLICATION_JSON)
   assert status_code == 422

   # DIFFERENT_USER_FOR_AUDIO_FILES
def test_put_inference_parameters_api_different_user_audio_file():
   D_CP = PUT_INFERENCE_PARAMETER_DATA.copy()
   DATA = helper.update_dictionary(D_CP, filePath=FILE_BELONGS_TO_OTHER_USER)
   status_code, response_json = API_Calls.put_inference_parameters_api(BASE_URLV2, ACCESS_TOKEN,INFERENCE_PARAMETER_ID,DATA,CONTENT_TYPE_APPLICATION_JSON)
   assert status_code == 422

   # DIFFERENT_COUNTRY_FOR_AUDIO_FILES
def test_put_inference_parameters_api_different_country_audio_file():
   D_CP = PUT_INFERENCE_PARAMETER_DATA.copy()
   DATA = helper.update_dictionary(D_CP, filePath=FILE_BELONGS_TO_DIFFERENT_COUNTRY)
   status_code, response_json = API_Calls.put_inference_parameters_api(BASE_URLV2, ACCESS_TOKEN,INFERENCE_PARAMETER_ID,DATA,CONTENT_TYPE_APPLICATION_JSON)
   assert status_code == 422

   # INFERENCE_PARAMETER_NOT_FOUND
def test_put_inference_parameters_api_inference_parameter_not_found():

    # login with token
    status_code, json_data = API_Calls.token_api(BASE_URL, VALID_TOKEN_DATA, BASE_TOKEN, CONTENT_TYPE_URL_ENCODED)
    print("token api result:", status_code)
    # assert status_code == 200
    ACCESS_TOKEN = json_data['access_token']

    # create subject
    status, subject_json = API_Calls.subject_api(BASE_URL, VALID_SUBJECT_DATA, ACCESS_TOKEN,
                                                 CONTENT_TYPE_APPLICATION_JSON)
    print("subject api result:", status, subject_json)
    SUB_IDENTIFIER1 = subject_json['userIdentifier']

    VALID_STORAGE_DATA1 = {
        "fileType": "wav",
        "countryCode": "US",
        "userIdentifier": SUB_IDENTIFIER1
    }
    # storage api
    status_code, response_json = API_Calls.storage_api(BASE_URL, VALID_STORAGE_DATA1, ACCESS_TOKEN,
                                                       CONTENT_TYPE_APPLICATION_JSON)
    STORAGE_SIGNED_URL1 = response_json['signedURL']
    print("1st audio storage api result:", status_code, response_json)
    FILE_PATH1 = response_json['filePath']

    # first file upload
    status_code = API_Calls.upload_sample_file(STORAGE_SIGNED_URL1, TC1_FILE_PATH1)
    print("First audio file upload:", status_code)

    INFERENCE_PARAMETER_DATA = {
        "measure": {
            "name": "respiratory-symptoms-risk",
            "variant": "v2"
        },
        "filePath": FILE_PATH1
    }
    # POST inference paramteres
    status_code, response_json = API_Calls.post_inference_parameters_api(BASE_URLV2, INFERENCE_PARAMETER_DATA,
                                                                         ACCESS_TOKEN, CONTENT_TYPE_APPLICATION_JSON)
    print("POST inference parameters API result", status_code, response_json)
    INFERENCE_PARAMETER_ID = response_json['id']
    print(INFERENCE_PARAMETER_ID)

    # storage api for 2nd audio file
    status_code, response_json = API_Calls.storage_api(BASE_URL, VALID_STORAGE_DATA1, ACCESS_TOKEN,
                                                       CONTENT_TYPE_APPLICATION_JSON)
    print("2nd audio storage api result:", status_code, response_json)
    STORAGE_SIGNED_URL2 = response_json['signedURL']
    FILE_PATH2 = response_json['filePath']

    INFERENCE_PARAMETER_DATA2 = {

        "filePath": FILE_PATH2
    }

    # second file upload
    status_code = API_Calls.upload_sample_file(STORAGE_SIGNED_URL2, TC1_FILE_PATH2)
    print("Second audio file upload: ", status_code)

    # PUT inference paramteres

    headers = {'Authorization': ACCESS_TOKEN, 'Content-Type': CONTENT_TYPE_URL_ENCODED}
    res = requests.put(url=BASE_URLV2 + INFERENCE_PARAMETER_ENDPOINT +'/'+ INFERENCE_PARAMETER_NOT_FOUND, data=json.dumps(POST_INFERENCE_PARAMETER_DATA),
                        headers=headers)

    #status_code, response_json = API_Calls.put_inference_parameters_api(BASE_URLV2, ACCESS_TOKEN,INFERENCE_PARAMETER_NOT_FOUND,INFERENCE_PARAMETER_DATA2,CONTENT_TYPE_APPLICATION_JSON)

    print("PUT inference parameters API result:", status_code, response_json)
    assert status_code == 422

def test_put_inference_parameters_api_inference_parameter_blank():
   INFERENCE_PARAMETER_BLANK=" "
   status_code, response_json = API_Calls.put_inference_parameters_api(BASE_URLV2, ACCESS_TOKEN,INFERENCE_PARAMETER_BLANK,PUT_INFERENCE_PARAMETER_DATA,CONTENT_TYPE_APPLICATION_JSON)
   assert status_code == 400

def test_put_inference_parameters_api_no_inference_parameter():
   headers = {'Authorization': ACCESS_TOKEN, 'Content-Type': CONTENT_TYPE_APPLICATION_JSON}
   res = requests.put(BASE_URLV2 + INFERENCE_PARAMETER_PUTENDPOINT,data=json.dumps(PUT_INFERENCE_PARAMETER_DATA),  headers=headers)
   assert res.status_code == 403

'''
def test_put_inference_parameters_api_inprogress():
   status_code, response_json = API_Calls.put_inference_parameters_api(BASE_URLV2, ACCESS_TOKEN,INFERENCE_PARAMETER_ID,PUT_INFERENCE_PARAMETER_DATA, CONTENT_TYPE_APPLICATION_JSON)
   assert status_code == 202
   assertion.assert_valid_schema(response_json, 'get_inference_parameter.json')
'''
time.sleep(10)
def test_put_inference_parameters_api_created():
    # login with token
    status_code, json_data = API_Calls.token_api(BASE_URL, VALID_TOKEN_DATA, BASE_TOKEN, CONTENT_TYPE_URL_ENCODED)
    print("token api result:", status_code)
    # assert status_code == 200
    ACCESS_TOKEN = json_data['access_token']

    # create subject
    status, subject_json = API_Calls.subject_api(BASE_URL, VALID_SUBJECT_DATA, ACCESS_TOKEN,
                                                 CONTENT_TYPE_APPLICATION_JSON)
    print("subject api result:", status, subject_json)
    SUB_IDENTIFIER1 = subject_json['userIdentifier']

    VALID_STORAGE_DATA1 = {
        "fileType": "wav",
        "countryCode": "US",
        "userIdentifier": SUB_IDENTIFIER1
    }
    # storage api
    status_code, response_json = API_Calls.storage_api(BASE_URL, VALID_STORAGE_DATA1, ACCESS_TOKEN,
                                                       CONTENT_TYPE_APPLICATION_JSON)
    STORAGE_SIGNED_URL1 = response_json['signedURL']
    print("1st audio storage api result:", status_code, response_json)
    FILE_PATH1 = response_json['filePath']

    # first file upload
    status_code = API_Calls.upload_sample_file(STORAGE_SIGNED_URL1, TC1_FILE_PATH1)
    print("First audio file upload:", status_code)

    INFERENCE_PARAMETER_DATA = {
        "measure": {
            "name": "respiratory-symptoms-risk",
            "variant": "v2"
        },
        "filePath": FILE_PATH1
    }
    # POST inference paramteres
    status_code, response_json = API_Calls.post_inference_parameters_api(BASE_URLV2, INFERENCE_PARAMETER_DATA,
                                                                         ACCESS_TOKEN, CONTENT_TYPE_APPLICATION_JSON)
    print("POST inference parameters API result", status_code, response_json)
    INFERENCE_PARAMETER_ID = response_json['id']
    print(INFERENCE_PARAMETER_ID)

    # storage api for 2nd audio file
    status_code, response_json = API_Calls.storage_api(BASE_URL, VALID_STORAGE_DATA1, ACCESS_TOKEN,
                                                       CONTENT_TYPE_APPLICATION_JSON)
    print("2nd audio storage api result:", status_code, response_json)
    STORAGE_SIGNED_URL2 = response_json['signedURL']
    FILE_PATH2 = response_json['filePath']

    INFERENCE_PARAMETER_DATA2 = {

        "filePath": FILE_PATH2
    }

    # second file upload
    status_code = API_Calls.upload_sample_file(STORAGE_SIGNED_URL2, TC1_FILE_PATH2)
    print("Second audio file upload: ", status_code)

    # PUT inference paramteres
    status_code, response_json = API_Calls.put_inference_parameters_api(BASE_URLV2, ACCESS_TOKEN,
                                                                        INFERENCE_PARAMETER_ID,
                                                                        INFERENCE_PARAMETER_DATA2,
                                                                        CONTENT_TYPE_APPLICATION_JSON)

    print("PUT inference parameters API result:", status_code, response_json)

    assert status_code == 201


#-------------------- POST INFERENCE----------------------#


def test_post_inference_scorev2_api_incorrect_accesstoken():
   INCORRECT_ACCESS_TOKEN = 'xyz'
   status_code, response_json = API_Calls.post_inference_scorev2_api(BASE_URLV2, create_inference_payload(), INCORRECT_ACCESS_TOKEN, CONTENT_TYPE_APPLICATION_JSON)
   assert status_code == 401


def test_post_inference_scorev2_api_with_accesstoken_bearer_in_small_case():
    ACCESS_TOKEN_BEARER1 = 'bearer ' + ACCESS_TOKEN
    print(ACCESS_TOKEN_BEARER1)
    status_code, response_json = API_Calls.post_inference_scorev2_api(BASE_URLV2, create_inference_payload(), ACCESS_TOKEN_BEARER1, CONTENT_TYPE_APPLICATION_JSON)
    assert status_code == 401


def test_post_inference_scorev2_api_expired_accesstoken():
   status_code, response_json = API_Calls.post_inference_scorev2_api(BASE_URLV2, create_inference_payload(), EXPIRED_ACCESS_TOKEN, CONTENT_TYPE_APPLICATION_JSON)
   assert status_code == 401

def test_post_inference_scorev2_api_missing_accesstoken():
   headers = {'Content-Type': CONTENT_TYPE_APPLICATION_JSON}
   res = requests.post(url=BASE_URLV2 + INFERENCE_ENDPOINT, data=json.dumps(create_inference_payload()), headers=headers)
   assert res.status_code == 401

def test_post_inference_scorev2_api_blank_accesstoken():
   headers = {'Authorization': '', 'Content-Type': CONTENT_TYPE_APPLICATION_JSON}
   res = requests.post(url=BASE_URLV2 + INFERENCE_ENDPOINT, data=json.dumps(create_inference_payload()), headers=headers)
   assert res.status_code == 401

def test_post_inference_scorev2_api_no_request_body():
   D_CP = PUT_INFERENCE_PARAMETER_DATA.copy()
   DATA = helper.delete_key(D_CP, 'inferenceParameterId')
   status_code, response_json = API_Calls.post_inference_scorev2_api(BASE_URLV2, DATA, ACCESS_TOKEN, CONTENT_TYPE_APPLICATION_JSON)
   assert status_code == 400

def test_post_inference_scorev2_invalid_endpoint():
   INVALID_INFERENCE_SCORE_ENDPOINT = '/inference/scores123'
   headers = {'Authorization': ACCESS_TOKEN, 'Content-Type': CONTENT_TYPE_APPLICATION_JSON}
   res = requests.post(url=BASE_URLV2 + INVALID_INFERENCE_SCORE_ENDPOINT, data=json.dumps(create_inference_payload()), headers=headers)
   assert res.status_code == 403

def test_post_inference_scorev2_api_requestbody_extra_key_added():
   POST_INFERENCE_DATA1 = {
       "inferenceParameterId": INFERENCE_PARAMETER_ID,
       "test":"123"
   }
   status_code, response_json = API_Calls.post_inference_scorev2_api(BASE_URLV2, POST_INFERENCE_DATA1, ACCESS_TOKEN, CONTENT_TYPE_APPLICATION_JSON)
   assert status_code == 400

def test_post_inference_scorev2_api_content_type_missing():
   headers = {'Authorization': ACCESS_TOKEN}
   res = requests.post(url=BASE_URLV2 + INFERENCE_ENDPOINT, data=json.dumps(create_inference_payload()), headers=headers)
   assert res.status_code == 400

def test_post_inference_scorev2_api_content_type_invalid():
   headers = {'Authorization': ACCESS_TOKEN, 'Content-Type': CONTENT_TYPE_URL_ENCODED}
   res = requests.post(url=BASE_URLV2 + INFERENCE_ENDPOINT, data=json.dumps(create_inference_payload()), headers=headers)
   assert res.status_code == 415

def test_post_inference_scorev2_api_content_type_blank():
   headers = {'Authorization': ACCESS_TOKEN, 'Content-Type': ""}
   res = requests.post(url=BASE_URLV2 + INFERENCE_ENDPOINT, data=json.dumps(create_inference_payload()), headers=headers)
   assert res.status_code == 415

def test_post_inference_scorev2_api_inference_parameter_not_found():
   D_CP = POST_INFERENCE_DATA.copy()
   DATA = helper.update_dictionary(D_CP, inferenceParameterId="1234")
   status_code, response_json = API_Calls.post_inference_scorev2_api(BASE_URLV2, DATA, ACCESS_TOKEN, CONTENT_TYPE_APPLICATION_JSON)
   assert status_code == 404

def test_post_inference_scorev2_api_inference_parameter_blank():
   D_CP = POST_INFERENCE_DATA.copy()
   DATA = helper.update_dictionary(D_CP, inferenceParameterId="")
   status_code, response_json = API_Calls.post_inference_scorev2_api(BASE_URLV2, DATA, ACCESS_TOKEN, CONTENT_TYPE_APPLICATION_JSON)
   assert status_code == 400

def test_POST_inference_scorev2_api_inprogress():
   print(INFERENCE_PARAMETER_ID)
   POST_INFERENCE_DATA
   global SCORE_ID
   status_code, response_json = API_Calls.post_inference_scorev2_api(BASE_URLV2, create_inference_payload(), ACCESS_TOKEN, CONTENT_TYPE_APPLICATION_JSON)
   assert status_code == 202
   assertion.assert_valid_schema(response_json, 'v2_post_inference_score.json')
   SCORE_ID=response_json['id']

# def test_POST_inference_scorev2_api_inprogress_with_access_token_bearer():
#     ACCESS_TOKEN_BEARER = 'Bearer ' + ACCESS_TOKEN
#     print(ACCESS_TOKEN_BEARER)
#     print(INFERENCE_PARAMETER_ID)
#     POST_INFERENCE_DATA
#     global SCORE_ID
#     status_code, response_json = API_Calls.post_inference_scorev2_api(BASE_URLV2, create_inference_payload(), ACCESS_TOKEN_BEARER, CONTENT_TYPE_APPLICATION_JSON)
#     assert status_code == 202
#     assertion.assert_valid_schema(response_json, 'v2_post_inference_score.json')
#     SCORE_ID=response_json['id']



time.sleep(10)
def test_POST_inference_scorev2_api_measure_score_already_present1():
    status_code, json_data = API_Calls.token_api(BASE_URL, VALID_TOKEN_DATA, BASE_TOKEN, CONTENT_TYPE_URL_ENCODED)
    print("token api result:", status_code)
    # assert status_code == 200
    ACCESS_TOKEN = json_data['access_token']

    # create subject
    status, subject_json = API_Calls.subject_api(BASE_URL, VALID_SUBJECT_DATA, ACCESS_TOKEN,
                                                 CONTENT_TYPE_APPLICATION_JSON)
    print("subject api result:", status, subject_json)
    SUB_IDENTIFIER1 = subject_json['userIdentifier']

    VALID_STORAGE_DATA1 = {
        "fileType": "wav",
        "countryCode": "US",
        "userIdentifier": SUB_IDENTIFIER1
    }
    # storage api
    status_code, response_json = API_Calls.storage_api(BASE_URL, VALID_STORAGE_DATA1, ACCESS_TOKEN,
                                                       CONTENT_TYPE_APPLICATION_JSON)
    STORAGE_SIGNED_URL1 = response_json['signedURL']
    print("1st audio storage api result:", status_code, response_json)
    FILE_PATH1 = response_json['filePath']

    # first file upload
    status_code = API_Calls.upload_sample_file(STORAGE_SIGNED_URL1, TC1_FILE_PATH1)
    print("First audio file upload:", status_code)

    INFERENCE_PARAMETER_DATA = {
        "measure": {
            "name": "respiratory-symptoms-risk",
            "variant": "v2"
        },
        "filePath": FILE_PATH1
    }
    # POST inference paramteres
    status_code, response_json = API_Calls.post_inference_parameters_api(BASE_URLV2, INFERENCE_PARAMETER_DATA,
                                                                         ACCESS_TOKEN, CONTENT_TYPE_APPLICATION_JSON)
    print("POST inference parameters API result", status_code, response_json)
    INFERENCE_PARAMETER_ID = response_json['id']
    print(INFERENCE_PARAMETER_ID)


    # storage api for 2nd audio file
    status_code, response_json = API_Calls.storage_api(BASE_URL, VALID_STORAGE_DATA1, ACCESS_TOKEN,
                                                       CONTENT_TYPE_APPLICATION_JSON)
    print("2nd audio storage api result:", status_code, response_json)
    STORAGE_SIGNED_URL2 = response_json['signedURL']
    FILE_PATH2 = response_json['filePath']

    INFERENCE_PARAMETER_DATA2 = {

        "filePath": FILE_PATH2
    }

    # second file upload
    status_code = API_Calls.upload_sample_file(STORAGE_SIGNED_URL2, TC1_FILE_PATH2)
    print("Second audio file upload: ", status_code)

    # PUT inference paramteres
    status_code, response_json = API_Calls.put_inference_parameters_api(BASE_URLV2, ACCESS_TOKEN,
                                                                        INFERENCE_PARAMETER_ID,
                                                                        INFERENCE_PARAMETER_DATA2,
                                                                        CONTENT_TYPE_APPLICATION_JSON)

    print("PUT inference parameters API result:", status_code, response_json)

    # POST inference scores API
    time.sleep(10)
    SCORE_V2_DATA = {
        "inferenceParameterId": INFERENCE_PARAMETER_ID
    }
    status_code, response_json = API_Calls.post_inference_scorev2_api(BASE_URLV2, SCORE_V2_DATA, ACCESS_TOKEN,
                                                                      CONTENT_TYPE_APPLICATION_JSON)
    print("POST inference score v2 API result:", status_code, response_json)
    SCOREID = response_json['id']


    time.sleep(15)
    SCORE_V2_DATA = {
        "inferenceParameterId": INFERENCE_PARAMETER_ID
    }
    status_code, response_json = API_Calls.post_inference_scorev2_api(BASE_URLV2, SCORE_V2_DATA, ACCESS_TOKEN,
                                                                      CONTENT_TYPE_APPLICATION_JSON)
    assert  status_code == 422


# ----- GET SCORE-----

def test_get_inference_scorev2_api_incorrect_accesstoken():
   INCORRECT_ACCESS_TOKEN = 'xyz'
   status_code, response_json = API_Calls.get_inference_scorev2_api(BASE_URLV2, SCORE_ID, INCORRECT_ACCESS_TOKEN, CONTENT_TYPE_APPLICATION_JSON)
   assert status_code == 401

def test_get_inference_scorev2_api_expired_accesstoken():
   status_code, response_json = API_Calls.get_inference_scorev2_api(BASE_URLV2, SCORE_ID, EXPIRED_ACCESS_TOKEN, CONTENT_TYPE_APPLICATION_JSON)
   assert status_code == 401

def test_get_inference_scorev2_api_accesstoken_with_bearer_in_small_case():
    ACCESS_TOKEN_BEARER1 = 'bearer ' + ACCESS_TOKEN
    print(ACCESS_TOKEN_BEARER1)
    status_code, response_json = API_Calls.get_inference_scorev2_api(BASE_URLV2, SCORE_ID, ACCESS_TOKEN_BEARER1, CONTENT_TYPE_APPLICATION_JSON)
    assert status_code == 401

def test_get_inference_scorev2_api_missing_accesstoken():
   headers = {'Content-Type': CONTENT_TYPE_APPLICATION_JSON}
   res = requests.get(url=BASE_URLV2 + INFERENCE_ENDPOINT + '/' +SCORE_ID, headers=headers)
   assert res.status_code == 401

def test_get_inference_scorev2_api_blank_accesstoken():
   headers = {'Authorization': '', 'Content-Type': CONTENT_TYPE_APPLICATION_JSON}
   res = requests.get(url=BASE_URLV2 + INFERENCE_ENDPOINT + '/' +SCORE_ID, headers=headers)
   assert res.status_code == 401

def test_get_inference_scorev2_invalid_endpoint():
   INVALID_INFERENCE_SCORE_ENDPOINT = '/inference/scores123'
   headers = {'Authorization': ACCESS_TOKEN, 'Content-Type': CONTENT_TYPE_APPLICATION_JSON}
   res = requests.get(url=BASE_URLV2 + INVALID_INFERENCE_SCORE_ENDPOINT + '/' +SCORE_ID, headers=headers)
   assert res.status_code == 403

def test_get_inference_scorev2_invalid_scoreId():
   INVALID_SCORE_ID="1234"
   status_code, response_json = API_Calls.get_inference_scorev2_api(BASE_URLV2, INVALID_SCORE_ID, ACCESS_TOKEN, CONTENT_TYPE_APPLICATION_JSON)
   assert status_code == 404

def test_get_inference_scorev2_blank_scoreId():
   BLANK_SCORE_ID=" "
   status_code, response_json = API_Calls.get_inference_scorev2_api(BASE_URLV2, BLANK_SCORE_ID, ACCESS_TOKEN, CONTENT_TYPE_APPLICATION_JSON)
   assert status_code == 404

def test_get_inference_scorev2_api_no_scoreId():
   headers = {'Authorization': ACCESS_TOKEN, 'Content-Type': CONTENT_TYPE_APPLICATION_JSON}
   res = requests.get(url=BASE_URLV2 + INFERENCE_ENDPOINT, headers=headers)
   assert res.status_code == 403





