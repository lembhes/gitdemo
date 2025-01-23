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

#AUDIO_FILE_PATH1 = 'C:\\Users\\gs-1431\\Desktop\\test\\first.wav'

#status_code = API_Calls.upload_sample_file(STORAGE_SIGNED_URL1,AUDIO_FILE_PATH1)

AUDIO_FILE_PATH1 = 'C:\\Users\\gs-1431\\Downloads\\ahh.wav'

#AUDIO_FILE_PATH = 'C:\\Users\\GS-1329\\Downloads\\1__7FC800CA-456C-4CA2-A568-DE6A96E54705_7251_9067.wav'

status_code = API_Calls.upload_sample_file(STORAGE_SIGNED_URL1, AUDIO_FILE_PATH1)



#------Storage2------#

status_code, response_json = API_Calls.storage_api(BASE_URL, VALID_STORAGE_DATA, ACCESS_TOKEN,
                                                   CONTENT_TYPE_APPLICATION_JSON)

STORAGE_SIGNED_URL2 = response_json['signedURL']
FILE_PATH2 = response_json['filePath']
FILE_PATH_ENCODED2 = helper.urlEncoder(FILE_PATH2)

#--------Upload File2 -------#

AUDIO_FILE_PATH2 = 'C:\\Users\\gs-1431\\Downloads\\ahhtwo.wav'

status_code = API_Calls.upload_sample_file(STORAGE_SIGNED_URL2,AUDIO_FILE_PATH2)

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

status_code = API_Calls.upload_sample_file(STORAGE_SIGNED_URL3, AUDIO_FILE_PATH1) # Same file 1 is uploaded at url 3

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

def create_inference_payload():
   return {
       "inferenceParameterId": INFERENCE_PARAMETER_ID
   }
INFERENCE_PARAMETER_ID = ''

def test_post_inference_parameter_api_inprogress():
    status_code, response_json = API_Calls.post_inference_parameters_api(BASE_URLV2, POST_INFERENCE_PARAMETER_DATA, ACCESS_TOKEN,CONTENT_TYPE_APPLICATION_JSON)
    assert status_code == 202
    assertion.assert_valid_schema(response_json, 'post_inference_parameter.json')
    INFERENCE_PARAMETER_ID = response_json['id']

time.sleep(10)

def test_post_inference_parameter_api_created():
    global INFERENCE_PARAMETER_ID
    status_code, response_json = API_Calls.post_inference_parameters_api(BASE_URLV2, POST_INFERENCE_PARAMETER_DATA, ACCESS_TOKEN,
                                                                             CONTENT_TYPE_APPLICATION_JSON)
    assert status_code == 201
    assertion.assert_valid_schema(response_json, 'post_inference_parameter.json')
    INFERENCE_PARAMETER_ID = response_json['id']

def test_post_inference_parameter_api_incorrect_accesstoken():
    INCORRECT_ACCESS_TOKEN = 'xyz'
    status_code, response_json = API_Calls.post_inference_parameters_api(BASE_URLV2, POST_INFERENCE_PARAMETER_DATA, INCORRECT_ACCESS_TOKEN,
                                                                             CONTENT_TYPE_APPLICATION_JSON)
    assert status_code == 401

def test_post_inference_parameter_api_expired_accesstoken():
    status_code, response_json = API_Calls.post_inference_parameters_api(BASE_URLV2, POST_INFERENCE_PARAMETER_DATA, EXPIRED_ACCESS_TOKEN,
                                                                             CONTENT_TYPE_APPLICATION_JSON)
    assert status_code == 401

def test_post_inference_parameter_api_missing_accesstoken():
    headers = {'Content-Type': CONTENT_TYPE_APPLICATION_JSON}
    res = requests.post(url=BASE_URLV2 + INFERENCE_PARAMETER_ENDPOINT, data=json.dumps(POST_INFERENCE_PARAMETER_DATA),
                        headers=headers)
    assert res.status_code == 401

def test_post_inference_parameter_api_blank_accesstoken():
    headers = {'Authorization': '', 'Content-Type': CONTENT_TYPE_APPLICATION_JSON}
    res = requests.post(url=BASE_URLV2 + INFERENCE_PARAMETER_ENDPOINT, data=json.dumps(POST_INFERENCE_PARAMETER_DATA),
                        headers=headers)
    assert res.status_code == 401

def test_post_inference_parameter_api_no_request_body():
    D_CP = POST_INFERENCE_PARAMETER_DATA.copy()
    DATA1 = helper.delete_key(D_CP, 'filePath')
    DATA = helper.delete_key(D_CP, 'measure')
    status_code, response_json = API_Calls.post_inference_parameters_api(BASE_URLV2, DATA, ACCESS_TOKEN,
                                                                             CONTENT_TYPE_APPLICATION_JSON)
    assert status_code == 400

def test_post_inference_parameter_api_invalid_endpoint():
    INVALID_INFERENCE_PARAMETER_ENDPOINT = '/inference/inferenceparameters123'
    headers = {'Authorization': ACCESS_TOKEN, 'Content-Type': CONTENT_TYPE_APPLICATION_JSON}
    res = requests.post(url=BASE_URLV2 + INVALID_INFERENCE_PARAMETER_ENDPOINT, data=json.dumps(POST_INFERENCE_PARAMETER_DATA),
                        headers=headers)
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
    assert status_code == 400

def test_post_inference_parameter_api_measure_name_and_variant_keyvalue_blank():
    DATA1 = {
        "measure": {
            "name": "",
            "variant": ""
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
    assert status_code == 400

def test_post_inference_parameter_api_requestbody_filePath_keyvalue_invalid():
    D_CP = POST_INFERENCE_PARAMETER_DATA.copy()
    DATA = helper.update_dictionary(D_CP, filePath='1234')
    status_code, response_json = API_Calls.post_inference_parameters_api(BASE_URLV2, DATA, ACCESS_TOKEN,
                                                                             CONTENT_TYPE_APPLICATION_JSON)
    assert status_code == 404   #or 400

def test_post_inference_parameter_api_requestbody_filePath_keyvalue_audio_file_with_silence():
    status_code, response_json = API_Calls.storage_api(BASE_URL, VALID_STORAGE_DATA, ACCESS_TOKEN,
                                                       CONTENT_TYPE_APPLICATION_JSON)
    STORAGE_SIGNED_URL1 = response_json['signedURL']
    FILE_PATH_NEW = response_json['filePath']
    AUDIO_FILE_PATH1 = 'C:/Users/GS-1329/Downloads/Silence.wav'
    status_code = API_Calls.upload_sample_file(STORAGE_SIGNED_URL1, AUDIO_FILE_PATH1)

    D_CP = POST_INFERENCE_PARAMETER_DATA.copy()
    DATA = helper.update_dictionary(D_CP, filePath=FILE_PATH_NEW)
    status_code, response_json = API_Calls.post_inference_parameters_api(BASE_URLV2, DATA, ACCESS_TOKEN,
                                                                             CONTENT_TYPE_APPLICATION_JSON)
 
    assert status_code == 422 # or 422  NEED TO CHECK THIS received ELICITATION_CHECK_FAILED
 
    assert status_code == 404 # or 422
 

def test_post_inference_parameter_api_requestbody_filePath_keyvalue_no_audio_file_present_at_loction():
    status_code, response_json = API_Calls.storage_api(BASE_URL, VALID_STORAGE_DATA, ACCESS_TOKEN,
                                                       CONTENT_TYPE_APPLICATION_JSON)
    FILE_PATH_NEW = response_json['filePath']
    D_CP = POST_INFERENCE_PARAMETER_DATA.copy()
 
   # DATA = helper.update_dictionary(D_CP, filePath=FILE_PATH_NEW)
 
    DATA = helper.update_dictionary(D_CP, filePath=FILE_PATH_MISSING_TS)
 
    status_code, response_json = API_Calls.post_inference_parameters_api(BASE_URLV2, DATA, ACCESS_TOKEN,
                                                                             CONTENT_TYPE_APPLICATION_JSON)
    assert status_code == 404

def test_post_inference_parameter_api_requestbody_filePath_keyvalue_elicitation_failed():
    status_code, response_json = API_Calls.storage_api(BASE_URL, VALID_STORAGE_DATA, ACCESS_TOKEN,
                                                       CONTENT_TYPE_APPLICATION_JSON)
    STORAGE_SIGNED_URL1 = response_json['signedURL']
    FILE_PATH_NEW = response_json['filePath']
    AUDIO_FILE_PATH1 = 'C:/Users/GS-1329/Downloads/Audio samples Two sample scoring/1st elck failed 2nd elck passed/ELCK_FAILED.wav'
    status_code = API_Calls.upload_sample_file(STORAGE_SIGNED_URL1, AUDIO_FILE_PATH1)

    D_CP = POST_INFERENCE_PARAMETER_DATA.copy()
 
    #DATA = helper.update_dictionary(D_CP, filePath=FILE_PATH_NEW)
 
    DATA = helper.update_dictionary(D_CP, filePath=TC8_FILE_PATH1)
 
    status_code, response_json = API_Calls.post_inference_parameters_api(BASE_URLV2, DATA, ACCESS_TOKEN,
                                                                             CONTENT_TYPE_APPLICATION_JSON)
    assert status_code == 422

def test_post_inference_parameter_api_requestbody_filePath_keyvalue_invalid_file_duration():
    status_code, response_json = API_Calls.storage_api(BASE_URL, VALID_STORAGE_DATA, ACCESS_TOKEN,
                                                       CONTENT_TYPE_APPLICATION_JSON)
    STORAGE_SIGNED_URL1 = response_json['signedURL']
    FILE_PATH_NEW = response_json['filePath']
    AUDIO_FILE_PATH1 = 'C:/Users/GS-1329/Downloads/Audio samples Two sample scoring/13 sec Ahh/1a890745-1332-40e2-b8ad-ab1110710a68_0e67afee-11cb-497d-86ae-f206923366ff_8419_10529.wav'
    status_code = API_Calls.upload_sample_file(STORAGE_SIGNED_URL1, AUDIO_FILE_PATH1)

    D_CP = POST_INFERENCE_PARAMETER_DATA.copy()
 
    DATA = helper.update_dictionary(D_CP, filePath=FILE_PATH_NEW)
 
    DATA = helper.update_dictionary(D_CP, filePath=INVALID_FILE_DURATION_8SEC)
 
    status_code, response_json = API_Calls.post_inference_parameters_api(BASE_URLV2, DATA, ACCESS_TOKEN,
                                                                             CONTENT_TYPE_APPLICATION_JSON)
    assert status_code == 422

def test_post_inference_parameter_api_requestbody_filePath_keyvalue_invalid_type():
    status_code, response_json = API_Calls.storage_api(BASE_URL, VALID_STORAGE_DATA, ACCESS_TOKEN,
                                                       CONTENT_TYPE_APPLICATION_JSON)
    STORAGE_SIGNED_URL1 = response_json['signedURL']
    FILE_PATH_NEW = response_json['filePath']
    AUDIO_FILE_PATH1 = 'C:/Users/GS-1329/Downloads/RPReplay_Final1626673127.MP4'
    status_code = API_Calls.upload_sample_file(STORAGE_SIGNED_URL1, AUDIO_FILE_PATH1)

    D_CP = POST_INFERENCE_PARAMETER_DATA.copy()
 
    DATA = helper.update_dictionary(D_CP, filePath=FILE_PATH_NEW)
 
    DATA = helper.update_dictionary(D_CP, filePath=TC5_FILE_PATH1)
 
    status_code, response_json = API_Calls.post_inference_parameters_api(BASE_URLV2, DATA, ACCESS_TOKEN,
                                                                             CONTENT_TYPE_APPLICATION_JSON)
    assert status_code == 422  #or 400

########################
# def test_post_inference_parameter_api_requestbody_filePath_keyvalue_file_specification_invalid():
########################

def test_post_inference_parameter_api_requestbody_extra_key_added():
    DATA1 = {
        "measure": {
            "name": "respiratory-symptoms-risk",
            "variant": "v2"
        },
        "filePath": FILE_PATH1,
        "Test":"1234"
    }
    status_code, response_json = API_Calls.post_inference_parameters_api(BASE_URLV2, DATA1, ACCESS_TOKEN,
                                                                         CONTENT_TYPE_APPLICATION_JSON)
    assert status_code == 400

def test_post_inference_parameter_api_content_type_missing():
    headers = {'Authorization': ACCESS_TOKEN}
    status_code, response_json = requests.post(url=BASE_URLV2 + INFERENCE_PARAMETER_ENDPOINT, data=json.dumps(POST_INFERENCE_PARAMETER_DATA),
                        headers=headers)
 
    assert status_code == 400

 

def test_post_inference_parameter_api_content_type_invalid():
    headers = {'Authorization': ACCESS_TOKEN, 'Content-Type': CONTENT_TYPE_URL_ENCODED}
    status_code, response_json = requests.post(url=BASE_URLV2 + INFERENCE_PARAMETER_ENDPOINT, data=json.dumps(POST_INFERENCE_PARAMETER_DATA),
                        headers=headers)
    assert status_code == 415

def test_post_inference_parameter_api_content_type_blank():
 
    headers = {'Authorization': ACCESS_TOKEN, 'Content-Type':""}
    res = requests.post(url=BASE_URLV2 + INFERENCE_PARAMETER_ENDPOINT, data=json.dumps(POST_INFERENCE_PARAMETER_DATA),
    headers=headers)
    assert status_code == 415

#----- Update Inference parameter ------#

def test_put_inference_parameter_api_inprogress():
    status_code, response_json = API_Calls.put_inference_parameters_api(BASE_URLV2, POST_INFERENCE_PARAMETER_DATA, ACCESS_TOKEN,CONTENT_TYPE_APPLICATION_JSON)
    assert status_code == 202
    assertion.assert_valid_schema(response_json, 'v2_put_inference_parameter.json')

def test_put_inference_parameter_api_incorrect_accesstoken():
    INCORRECT_ACCESS_TOKEN = 'xyz'
    status_code, response_json = API_Calls.put_inference_parameters_api(BASE_URLV2, INCORRECT_ACCESS_TOKEN,INFERENCE_PARAMETER_ID,PUT_INFERENCE_PARAMETER_DATA,CONTENT_TYPE_APPLICATION_JSON)

    assert status_code == 401

def test_put_inference_parameter_api_expired_accesstoken():
    status_code, response_json = API_Calls.put_inference_parameters_api(BASE_URLV2, EXPIRED_ACCESS_TOKEN,INFERENCE_PARAMETER_ID,PUT_INFERENCE_PARAMETER_DATA,CONTENT_TYPE_APPLICATION_JSON)
    assert status_code == 401

def test_put_inference_parameter_api_missing_accesstoken():
    headers = {'Content-Type': CONTENT_TYPE_APPLICATION_JSON}
    res = requests.put(BASE_URLV2 + INFERENCE_PARAMETER_ENDPOINT + INFERENCE_PARAMETER_ID,data=json.dumps(PUT_INFERENCE_PARAMETER_DATA),  headers=headers)
    assert res.status_code == 401

def test_put_inference_parameter_api_blank_accesstoken():
    headers = {'Authorization': '', 'Content-Type': CONTENT_TYPE_APPLICATION_JSON}
    res = requests.put(BASE_URLV2 + INFERENCE_PARAMETER_ENDPOINT + INFERENCE_PARAMETER_ID,data=json.dumps(PUT_INFERENCE_PARAMETER_DATA),  headers=headers)
    assert res.status_code == 401

def test_put_inference_parameter_api_no_request_body():
    D_CP = PUT_INFERENCE_PARAMETER_DATA.copy()
    DATA = helper.delete_key(D_CP, 'filePath')
    status_code, response_json = API_Calls.put_inference_parameters_api(BASE_URLV2, ACCESS_TOKEN,INFERENCE_PARAMETER_ID,DATA, CONTENT_TYPE_APPLICATION_JSON)
    assert status_code == 400

def test_put_inference_parameter_api_invalid_endpoint():
    INVALID_INFERENCE_PARAMETER_ENDPOINT = '/inference/inference-parameters123'
    headers = {'Authorization': ACCESS_TOKEN, 'Content-Type': CONTENT_TYPE_APPLICATION_JSON}
    res = requests.put(BASE_URLV2 + INVALID_INFERENCE_PARAMETER_ENDPOINT + INFERENCE_PARAMETER_ID,
                       data=json.dumps(PUT_INFERENCE_PARAMETER_DATA), headers=headers)
    assert res.status_code == 403

def test_put_inference_parameter_api_requestbody_filePath_key_missing():
    D_CP = PUT_INFERENCE_PARAMETER_DATA.copy()
    DATA = helper.delete_key(D_CP, 'filePath')
    status_code, response_json = API_Calls.put_inference_parameters_api(BASE_URLV2, ACCESS_TOKEN,INFERENCE_PARAMETER_ID,DATA, CONTENT_TYPE_APPLICATION_JSON)
    assert status_code == 400

def test_put_inference_parameter_api_requestbody_filePath_keyname_blank():
    DATA= {
        " ": FILE_PATH2,
    }
    status_code, response_json = API_Calls.put_inference_parameters_api(BASE_URLV2, ACCESS_TOKEN,INFERENCE_PARAMETER_ID,DATA, CONTENT_TYPE_APPLICATION_JSON)
    assert status_code == 400

def test_put_inference_parameter_api_requestbody_filePath_keyvalue_blank():
    D_CP = PUT_INFERENCE_PARAMETER_DATA.copy()
    DATA = helper.update_dictionary(D_CP, filePath=' ')
    status_code, response_json = API_Calls.put_inference_parameters_api(BASE_URLV2, ACCESS_TOKEN,INFERENCE_PARAMETER_ID,DATA, CONTENT_TYPE_APPLICATION_JSON)
    assert status_code == 400

def test_put_inference_parameter_api_requestbody_filePath_keyvalue_invalid():
    D_CP = PUT_INFERENCE_PARAMETER_DATA.copy()
    DATA = helper.update_dictionary(D_CP, filePath='1234')
    status_code, response_json = API_Calls.put_inference_parameters_api(BASE_URLV2, ACCESS_TOKEN,INFERENCE_PARAMETER_ID,DATA, CONTENT_TYPE_APPLICATION_JSON)
    assert status_code == 422   #or 400

def test_put_inference_parameter_api_requestbody_filePath_keyvalue_audio_file_with_silence():
    status_code, response_json = API_Calls.storage_api(BASE_URL, VALID_STORAGE_DATA, ACCESS_TOKEN,
                                                       CONTENT_TYPE_APPLICATION_JSON)
    STORAGE_SIGNED_URL1 = response_json['signedURL']
    FILE_PATH_NEW = response_json['filePath']
    AUDIO_FILE_PATH1 = 'C:/Users/GS-1329/Downloads/Silence.wav'

    status_code = API_Calls.upload_sample_file(STORAGE_SIGNED_URL1, AUDIO_FILE_PATH1)
    D_CP = PUT_INFERENCE_PARAMETER_DATA.copy()
    DATA = helper.update_dictionary(D_CP, filePath=FILE_PATH_NEW)
    status_code, response_json = API_Calls.put_inference_parameters_api(BASE_URLV2, ACCESS_TOKEN,INFERENCE_PARAMETER_ID,DATA, CONTENT_TYPE_APPLICATION_JSON)
    assert status_code == 422

def test_put_inference_parameter_api_requestbody_filePath_keyvalue_no_audio_file_present_at_loction():
    status_code, response_json = API_Calls.storage_api(BASE_URL, VALID_STORAGE_DATA, ACCESS_TOKEN,
                                                       CONTENT_TYPE_APPLICATION_JSON)
    FILE_PATH_NEW = response_json['filePath']
    D_CP = PUT_INFERENCE_PARAMETER_DATA.copy()
    DATA = helper.update_dictionary(D_CP, filePath=FILE_PATH_NEW)
    status_code, response_json = API_Calls.put_inference_parameters_api(BASE_URLV2, ACCESS_TOKEN,INFERENCE_PARAMETER_ID,DATA, CONTENT_TYPE_APPLICATION_JSON)
    assert status_code == 422

def test_put_inference_parameter_api_requestbody_filePath_keyvalue_elicitation_failed():
    status_code, response_json = API_Calls.storage_api(BASE_URL, VALID_STORAGE_DATA, ACCESS_TOKEN,
                                                       CONTENT_TYPE_APPLICATION_JSON)
    STORAGE_SIGNED_URL1 = response_json['signedURL']
    FILE_PATH_NEW = response_json['filePath']
    AUDIO_FILE_PATH1 = 'C:/Users/GS-1329/Downloads/Audio samples Two sample scoring/1st elck failed 2nd elck passed/ELCK_FAILED.wav'
    status_code = API_Calls.upload_sample_file(STORAGE_SIGNED_URL1, AUDIO_FILE_PATH1)
    D_CP = PUT_INFERENCE_PARAMETER_DATA.copy()
    DATA = helper.update_dictionary(D_CP, filePath=FILE_PATH_NEW)
    status_code, response_json = API_Calls.put_inference_parameters_api(BASE_URLV2, ACCESS_TOKEN,INFERENCE_PARAMETER_ID,DATA, CONTENT_TYPE_APPLICATION_JSON)
    assert status_code == 422

def test_put_inference_parameter_api_requestbody_filePath_keyvalue_invalid_file_duration():
    status_code, response_json = API_Calls.storage_api(BASE_URL, VALID_STORAGE_DATA, ACCESS_TOKEN,
                                                       CONTENT_TYPE_APPLICATION_JSON)
    STORAGE_SIGNED_URL1 = response_json['signedURL']
    FILE_PATH_NEW = response_json['filePath']
    AUDIO_FILE_PATH1 = 'C:/Users/GS-1329/Downloads/Audio samples Two sample scoring/13 sec Ahh/1a890745-1332-40e2-b8ad-ab1110710a68_0e67afee-11cb-497d-86ae-f206923366ff_8419_10529.wav'
    status_code = API_Calls.upload_sample_file(STORAGE_SIGNED_URL1, AUDIO_FILE_PATH1)

    D_CP = PUT_INFERENCE_PARAMETER_DATA.copy()
    DATA = helper.update_dictionary(D_CP, filePath=FILE_PATH_NEW)
    status_code, response_json = API_Calls.put_inference_parameters_api(BASE_URLV2, ACCESS_TOKEN,INFERENCE_PARAMETER_ID,DATA, CONTENT_TYPE_APPLICATION_JSON)
    assert status_code == 422

def test_put_inference_parameter_api_requestbody_filePath_keyvalue_invalid_type():
    status_code, response_json = API_Calls.storage_api(BASE_URL, VALID_STORAGE_DATA, ACCESS_TOKEN,
                                                       CONTENT_TYPE_APPLICATION_JSON)
    STORAGE_SIGNED_URL1 = response_json['signedURL']
    FILE_PATH_NEW = response_json['filePath']
    AUDIO_FILE_PATH1 = 'C:/Users/GS-1329/Downloads/RPReplay_Final1626673127.MP4'
    status_code = API_Calls.upload_sample_file(STORAGE_SIGNED_URL1, AUDIO_FILE_PATH1)

    D_CP = PUT_INFERENCE_PARAMETER_DATA.copy()
    DATA = helper.update_dictionary(D_CP, filePath=FILE_PATH_NEW)
    status_code, response_json = API_Calls.put_inference_parameters_api(BASE_URLV2, ACCESS_TOKEN,INFERENCE_PARAMETER_ID,DATA, CONTENT_TYPE_APPLICATION_JSON)
    assert status_code == 422  #or 400

########################
# def test_put_inference_parameter_api_requestbody_filePath_keyvalue_file_specification_invalid():
########################

def test_put_inference_parameter_api_requestbody_extra_key_added():
    DATA = {
        "measure": {
            "name": " ",
            "variant": " "
        },
        "filePath": FILE_PATH2
    }
    status_code, response_json = API_Calls.put_inference_parameters_api(BASE_URLV2, ACCESS_TOKEN,INFERENCE_PARAMETER_ID,DATA, CONTENT_TYPE_APPLICATION_JSON)
    assert status_code == 400

def test_put_inference_parameter_api_content_type_missing():
    headers = {'Authorization': ACCESS_TOKEN}
    res = requests.put(BASE_URLV2 + INFERENCE_PARAMETER_ENDPOINT + INFERENCE_PARAMETER_ID,data=json.dumps(PUT_INFERENCE_PARAMETER_DATA), headers=headers)
    assert res.status_code == 400


def test_put_inference_parameter_api_content_type_invalid():
    headers = {'Authorization': ACCESS_TOKEN, 'Content-Type': CONTENT_TYPE_URL_ENCODED}
 
    res = requests.put(BASE_URLV2 + INFERENCE_PARAMETER_PUTENDPOINT + INFERENCE_PARAMETER_ID,data=json.dumps(PUT_INFERENCE_PARAMETER_DATA), headers=headers)
    assert res.status_code == 415



def test_put_inference_parameter_api_content_type_blank():
    headers = {'Authorization': ACCESS_TOKEN, 'Content-Type': ' '}
    res = requests.put(BASE_URLV2 + INFERENCE_PARAMETER_ENDPOINT + INFERENCE_PARAMETER_ID,data=json.dumps(PUT_INFERENCE_PARAMETER_DATA), headers=headers)
    assert res.status_code == 400


    # INFERENCE_PARAMETER_ALREADY_CONSTRUCTED
def test_put_inference_parameters_api_inference_prameter_already_constructed():
    status_code, response_json = API_Calls.put_inference_parameters_api(BASE_URLV2, ACCESS_TOKEN,INFERENCE_PARAMETER_ALREADY_CONSTRUCTED,PUT_INFERENCE_PARAMETER_DATA,CONTENT_TYPE_APPLICATION_JSON)
    assert status_code == 422

    # INDIFFERENT_AUDIO_FILE_ERROR
def test_put_inference_parameters_api_same_audio_file():
    D_CP = PUT_INFERENCE_PARAMETER_DATA.copy()
    DATA = helper.update_dictionary(D_CP, filePath=FILE_PATH3)
    status_code, response_json = API_Calls.put_inference_parameters_api(BASE_URLV2, ACCESS_TOKEN,INFERENCE_PARAMETER_ID,DATA,CONTENT_TYPE_APPLICATION_JSON)
    assert status_code == 422

    # DIFFERENT_USER_FOR_AUDIO_FILES
def test_put_inference_parameters_api_different_user_audio_file():
    status_code, json_data = API_Calls.subject_api(BASE_URL, VALID_SUBJECT_DATA, ACCESS_TOKEN,
                                                   CONTENT_TYPE_APPLICATION_JSON)
    SUB_IDENTIFIER1 = json_data['userIdentifier']
    print(SUB_IDENTIFIER)
    VALID_STORAGE_DATA1 = {
        "fileType": "wav",
        "countryCode": "US",
        "userIdentifier": SUB_IDENTIFIER1
    }

    status_code, response_json = API_Calls.storage_api(BASE_URL, VALID_STORAGE_DATA1, ACCESS_TOKEN,
                                                       CONTENT_TYPE_APPLICATION_JSON)

    STORAGE_SIGNED_URL1 = response_json['signedURL']
    FILE_PATH_NEW = response_json['filePath']
    AUDIO_FILE_PATH1 = 'C:/Users/GS-1329/Downloads/Audio samples Two sample scoring/second.wav'
    status_code = API_Calls.upload_sample_file(STORAGE_SIGNED_URL1, AUDIO_FILE_PATH1)

    D_CP = PUT_INFERENCE_PARAMETER_DATA.copy()
    DATA = helper.update_dictionary(D_CP, filePath=FILE_PATH_NEW)
    status_code, response_json = API_Calls.put_inference_parameters_api(BASE_URLV2, ACCESS_TOKEN,INFERENCE_PARAMETER_ID,DATA,CONTENT_TYPE_APPLICATION_JSON)
    assert status_code == 422

    # DIFFERENT_COUNTRY_FOR_AUDIO_FILES
def test_put_inference_parameters_api_different_country_audio_file():
    VALID_STORAGE_DATA1 = {
        "fileType": "wav",
        "countryCode": "IN",
        "userIdentifier": SUB_IDENTIFIER
    }

    status_code, response_json = API_Calls.storage_api(BASE_URL, VALID_STORAGE_DATA1, ACCESS_TOKEN,
                                                       CONTENT_TYPE_APPLICATION_JSON)

    STORAGE_SIGNED_URL1 = response_json['signedURL']
    FILE_PATH_NEW = response_json['filePath']
    AUDIO_FILE_PATH1 = 'C:/Users/GS-1329/Downloads/Audio samples Two sample scoring/second.wav'
    status_code = API_Calls.upload_sample_file(STORAGE_SIGNED_URL1, AUDIO_FILE_PATH1)
    D_CP = PUT_INFERENCE_PARAMETER_DATA.copy()
    DATA = helper.update_dictionary(D_CP, filePath=FILE_PATH_NEW)
    status_code, response_json = API_Calls.put_inference_parameters_api(BASE_URLV2, ACCESS_TOKEN,INFERENCE_PARAMETER_ID,DATA,CONTENT_TYPE_APPLICATION_JSON)
    assert status_code == 422

    # INFERENCE_PARAMETER_NOT_FOUND
def test_put_inference_parameters_api_inference_parameter_not_found():
    D_CP = PUT_INFERENCE_PARAMETER_DATA.copy()
    INFERENCE_PARAMETER_INVALID="inp_325f89c12"
    status_code, response_json = API_Calls.put_inference_parameters_api(BASE_URLV2, ACCESS_TOKEN,INFERENCE_PARAMETER_INVALID,D_CP,CONTENT_TYPE_APPLICATION_JSON)
    assert status_code == 404

def test_put_inference_parameters_api_inference_parameter_blank():
    D_CP = PUT_INFERENCE_PARAMETER_DATA.copy()
    INFERENCE_PARAMETER_BLANK=" "
    status_code, response_json = API_Calls.put_inference_parameters_api(BASE_URLV2, ACCESS_TOKEN,INFERENCE_PARAMETER_BLANK,D_CP,CONTENT_TYPE_APPLICATION_JSON)
    assert status_code == 400

def test_put_inference_parameters_api_no_inference_parameter():
    D_CP = PUT_INFERENCE_PARAMETER_DATA.copy()
    headers = {'Authorization': ACCESS_TOKEN, 'Content-Type': CONTENT_TYPE_APPLICATION_JSON}
 
    res = requests.put(BASE_URLV2 + INFERENCE_PARAMETER_PUTENDPOINT,data=json.dumps(D_CP),  headers=headers)
    assert res.status_code == 403

    res = requests.put(BASE_URLV2 + INFERENCE_PARAMETER_ENDPOINT,data=json.dumps(PUT_INFERENCE_PARAMETER_DATA),  headers=headers)
    assert res.status_code == 404
 

def test_put_inference_parameters_api_inprogress():
    status_code, response_json = API_Calls.put_inference_parameters_api(BASE_URLV2, ACCESS_TOKEN,INFERENCE_PARAMETER_ID,PUT_INFERENCE_PARAMETER_DATA, CONTENT_TYPE_APPLICATION_JSON)
    assert status_code == 202
    assertion.assert_valid_schema(response_json, 'get_inference_parameter.json')

POST_INFERENCE_DATA = {
        "inferenceParameterId": INFERENCE_PARAMETER_ID
    }

def test_POST_inference_scorev2_api_inference_parameter_not_constructed():
    status_code, response_json = API_Calls.post_inference_scorev2_api(BASE_URLV2, POST_INFERENCE_DATA, ACCESS_TOKEN, CONTENT_TYPE_APPLICATION_JSON)
    assert status_code == 422

time.sleep(10)
def test_put_inference_parameters_api_created():
    status_code, response_json = API_Calls.put_inference_parameters_api(BASE_URLV2, ACCESS_TOKEN,INFERENCE_PARAMETER_ID,PUT_INFERENCE_PARAMETER_DATA, CONTENT_TYPE_APPLICATION_JSON)
    assert status_code == 201
 
    assertion.assert_valid_schema(response_json, 'v2_put_inference_parameter.json')

    assertion.assert_valid_schema(response_json, 'get_inference_parameter.json')
 

#-------------------- POST INFERENCE----------------------#


def test_post_inference_scorev2_api_incorrect_accesstoken():
    INCORRECT_ACCESS_TOKEN = 'xyz'
    status_code, response_json = API_Calls.post_inference_scorev2_api(BASE_URLV2, POST_INFERENCE_DATA, INCORRECT_ACCESS_TOKEN, CONTENT_TYPE_APPLICATION_JSON)
    assert status_code == 401

def test_post_inference_scorev2_api_expired_accesstoken():
    status_code, response_json = API_Calls.post_inference_scorev2_api(BASE_URLV2, POST_INFERENCE_DATA, EXPIRED_ACCESS_TOKEN, CONTENT_TYPE_APPLICATION_JSON)
    assert status_code == 401

def test_post_inference_scorev2_api_missing_accesstoken():
    headers = {'Content-Type': CONTENT_TYPE_APPLICATION_JSON}
    res = requests.POST(url=BASE_URLV2 + INFERENCE_ENDPOINT, data=json.dumps(POST_INFERENCE_DATA), headers=headers)
    assert res.status_code == 401

def test_post_inference_scorev2_api_blank_accesstoken():
    headers = {'Authorization': '', 'Content-Type': CONTENT_TYPE_APPLICATION_JSON}
    res = requests.POST(url=BASE_URLV2 + INFERENCE_ENDPOINT, data=json.dumps(POST_INFERENCE_DATA), headers=headers)
    assert res.status_code == 401

def test_post_inference_scorev2_api_no_request_body():
    D_CP = PUT_INFERENCE_PARAMETER_DATA.copy()
    DATA = helper.delete_key(D_CP, 'inferenceParameterId')
    status_code, response_json = API_Calls.post_inference_scorev2_api(BASE_URLV2, DATA, ACCESS_TOKEN, CONTENT_TYPE_APPLICATION_JSON)
    assert status_code == 400

def test_post_inference_scorev2_invalid_endpoint():
    INVALID_INFERENCE_SCORE_ENDPOINT = '/inference/scores123'
    headers = {'Authorization': ACCESS_TOKEN, 'Content-Type': CONTENT_TYPE_APPLICATION_JSON}
    res = requests.POST(url=BASE_URLV2 + INVALID_INFERENCE_SCORE_ENDPOINT, data=json.dumps(POST_INFERENCE_DATA), headers=headers)
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
    res = requests.POST(url=BASE_URLV2 + INFERENCE_ENDPOINT, data=json.dumps(POST_INFERENCE_DATA), headers=headers)
    assert res.status_code == 400

def test_post_inference_scorev2_api_content_type_invalid():
    headers = {'Authorization': ACCESS_TOKEN, 'Content-Type': CONTENT_TYPE_URL_ENCODED}
    res = requests.POST(url=BASE_URLV2 + INFERENCE_ENDPOINT, data=json.dumps(POST_INFERENCE_DATA), headers=headers)
    assert res.status_code == 400

def test_post_inference_scorev2_api_content_type_blank():
 
    headers = {'Authorization': ACCESS_TOKEN, 'Content-Type': ""}
    res = requests.post(url=BASE_URLV2 + INFERENCE_ENDPOINT, data=json.dumps(create_inference_payload()), headers=headers)
    assert res.status_code == 415
 
    headers = {'Authorization': ACCESS_TOKEN, 'Content-Type': ' '}
    res = requests.POST(url=BASE_URLV2 + INFERENCE_ENDPOINT, data=json.dumps(POST_INFERENCE_DATA), headers=headers)
    assert res.status_code == 400
 

def test_post_inference_scorev2_api_inference_parameter_not_found():
    D_CP = POST_INFERENCE_DATA.copy()
    DATA = helper.update_dictionary(D_CP, inferenceParameterId="1234")
    status_code, response_json = API_Calls.post_inference_scorev2_api(BASE_URLV2, DATA, ACCESS_TOKEN, CONTENT_TYPE_APPLICATION_JSON)
    assert status_code == 404

def test_post_inference_scorev2_api_inference_parameter_blank():
    D_CP = POST_INFERENCE_DATA.copy()
    DATA = helper.update_dictionary(D_CP, inferenceParameterId="")
    status_code, response_json = API_Calls.post_inference_scorev2_api(BASE_URLV2, DATA, ACCESS_TOKEN, CONTENT_TYPE_APPLICATION_JSON)
    assert status_code == 404

def test_POST_inference_scorev2_api_inprogress():
    status_code, response_json = API_Calls.post_inference_scorev2_api(BASE_URLV2, POST_INFERENCE_DATA, ACCESS_TOKEN, CONTENT_TYPE_APPLICATION_JSON)
    assert status_code == 202
    assertion.assert_valid_schema(response_json, 'post_inference_scorev2.json')

time.sleep(10)
 
def test_POST_inference_scorev2_api_measure_score_already_present1():
    status_code, response_json = API_Calls.post_inference_scorev2_api(BASE_URLV2, create_inference_payload(), ACCESS_TOKEN, CONTENT_TYPE_APPLICATION_JSON)
    assert status_code == 422
 
def test_POST_inference_scorev2_api_generated():
    global SCORE_ID
    status_code, response_json = API_Calls.post_inference_scorev2_api(BASE_URLV2, POST_INFERENCE_DATA, ACCESS_TOKEN, CONTENT_TYPE_APPLICATION_JSON)
    assert status_code == 202
    assertion.assert_valid_schema(response_json, 'post_inference_scorev2.json')
    SCORE_ID=response_json['id']
 

# ----- GET SCORE-----

def test_get_inference_scorev2_api_incorrect_accesstoken():
    status_code, response_json = API_Calls.get_inference_scorev2_api(BASE_URLV2, SCORE_ID, ACCESS_TOKEN, CONTENT_TYPE_APPLICATION_JSON)
    assert status_code == 200

def test_get_inference_scorev2_api_incorrect_accesstoken():
    INCORRECT_ACCESS_TOKEN = 'xyz'
    status_code, response_json = API_Calls.get_inference_scorev2_api(BASE_URLV2, SCORE_ID, INCORRECT_ACCESS_TOKEN, CONTENT_TYPE_APPLICATION_JSON)
    assert status_code == 401

def test_get_inference_scorev2_api_expired_accesstoken():
    status_code, response_json = API_Calls.get_inference_scorev2_api(BASE_URLV2, SCORE_ID, EXPIRED_ACCESS_TOKEN, CONTENT_TYPE_APPLICATION_JSON)
    assert status_code == 401

def test_get_inference_scorev2_api_missing_accesstoken():
    headers = {'Content-Type': CONTENT_TYPE_APPLICATION_JSON}
    res = requests.GET(url=BASE_URLV2 + INFERENCE_ENDPOINT + '/' +SCORE_ID, headers=headers)
    assert res.status_code == 401

def test_get_inference_scorev2_api_blank_accesstoken():
    headers = {'Authorization': '', 'Content-Type': CONTENT_TYPE_APPLICATION_JSON}
    res = requests.GET(url=BASE_URLV2 + INFERENCE_ENDPOINT + '/' +SCORE_ID, headers=headers)
    assert res.status_code == 401

def test_get_inference_scorev2_invalid_endpoint():
    INVALID_INFERENCE_SCORE_ENDPOINT = '/inference/scores123'
    headers = {'Authorization': ACCESS_TOKEN, 'Content-Type': CONTENT_TYPE_APPLICATION_JSON}
    res = requests.GET(url=BASE_URLV2 + INVALID_INFERENCE_SCORE_ENDPOINT + '/' +SCORE_ID, headers=headers)
    assert res.status_code == 403

def test_get_inference_scorev2_invalid_scoreId():
    INVALID_SCORE_ID="1234"
    status_code, response_json = API_Calls.get_inference_scorev2_api(BASE_URLV2, INVALID_SCORE_ID, INCORRECT_ACCESS_TOKEN, CONTENT_TYPE_APPLICATION_JSON)
    assert status_code == 404

def test_get_inference_scorev2_blank_scoreId():
    BLANK_SCORE_ID=" "
    status_code, response_json = API_Calls.get_inference_scorev2_api(BASE_URLV2, BLANK_SCORE_ID, INCORRECT_ACCESS_TOKEN, CONTENT_TYPE_APPLICATION_JSON)
    assert status_code == 404

def test_get_inference_scorev2_api_no_scoreId():
    headers = {'Authorization': ACCESS_TOKEN, 'Content-Type': CONTENT_TYPE_APPLICATION_JSON}
 
    res = requests.get(url=BASE_URLV2 + INFERENCE_ENDPOINT, headers=headers)
    assert res.status_code == 403
 
    res = requests.GET(url=BASE_URLV2 + INFERENCE_ENDPOINT, headers=headers)
    assert res.status_code == 404
 




