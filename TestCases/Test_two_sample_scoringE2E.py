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


base64secrets = helper.get_base64secrets(CLIENT_ID_WQ, CLIENT_SECRET_WQ)
BASE_TOKEN_WQ = 'Basic ' + base64secrets
print(base64secrets)

# ---------------- Get the Base64 testclient --------------------------------#

base64secrets = helper.get_base64secrets(CLIENT_ID_Shruti_test, CLIENT_SECRET_Shruti_test)
print(base64secrets)

BASE_TOKEN_TEST = 'Basic ' + base64secrets


# ----------- Get the ACCESS TOKEN for missing party client credentials ----------------------------#

status_code, json_data = API_Calls.token_api(BASE_URL, VALID_TOKEN_DATA, BASE_TOKEN_TEST, CONTENT_TYPE_URL_ENCODED)
ACCESS_TOKEN_TEST = json_data['access_token']

# ---------------- Get the Base64 No access --------------------------------#

base64secrets = helper.get_base64secrets(CLIENT_ID_NOACCESS_TRANSCRIPTION, CLIENT_SECRET_NOACCESS_TRANSCRIPTION)
BASE_TOKEN_NO_ACCESS = 'Basic ' + base64secrets
print(base64secrets)

## ---------------- Get the Base64  for 19oct1@yopmail.com user --------------------------------#

base64secrets = helper.get_base64secrets(CLIENT_ID_28jul1, CLIENT_SECRET_28jul1)
print(base64secrets)

BASE_TOKEN_28JUL1= 'Basic ' + base64secrets


# ----------- Get the ACCESS TOKEN ----------------------------#

status_code, json_data = API_Calls.token_api(BASE_URL, VALID_TOKEN_DATA, BASE_TOKEN, CONTENT_TYPE_URL_ENCODED)
ACCESS_TOKEN = json_data['access_token']
print(ACCESS_TOKEN)


status_code, json_data = API_Calls.token_api(BASE_URL, VALID_TOKEN_DATA, BASE_TOKEN_WQ, CONTENT_TYPE_URL_ENCODED)
ACCESS_TOKEN_WQ = json_data['access_token']
print(ACCESS_TOKEN)
# ----------- Get the ACCESS TOKEN no Access ----------------------------#

status_code, json_data = API_Calls.token_api(BASE_URL, VALID_TOKEN_DATA, BASE_TOKEN, CONTENT_TYPE_URL_ENCODED)
ACCESS_TOKEN_NOACCESS_FOR_TRANSCRIPTION = json_data['access_token']
print(ACCESS_TOKEN_NOACCESS_FOR_TRANSCRIPTION)

status_code, json_data = API_Calls.token_api(BASE_URL, VALID_TOKEN_DATA, BASE_TOKEN_28JUL1, CONTENT_TYPE_URL_ENCODED)
ACCESS_TOKEN_28JUL1 = json_data['access_token']


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


VALID_STORAGE_DATA_IN = {
    "fileType": "wav",
    "countryCode": "IN",
    "userIdentifier": SUB_IDENTIFIER
}

status_code, response_json = API_Calls.storage_api(BASE_URL, VALID_STORAGE_DATA, ACCESS_TOKEN,
                                                   CONTENT_TYPE_APPLICATION_JSON)

STORAGE_SIGNED_URL = response_json['signedURL']
FILE_PATH = response_json['filePath']
FILE_PATH_ENCODED = helper.urlEncoder(FILE_PATH)
print(FILE_PATH_ENCODED)

MEASURE_OPTIMISM = 'optimism'

# ____________________UPLOAD THE AUDIO SAMPLE  ____________________________________________#


#AUDIO_FILE_PATH = 'C:\\Users\\gs-1431\\Downloads\\shrutiD_audio_30sec.wav'
Shruti_AUDIO_FILE_PATH = 'C:\\Users\\gs-1431\\Downloads\\shrutiD_audio_30sec.wav'
Shruti_AUDIO_FILE_PATH2 = 'C:\\Users\\gs-1431\\Downloads\\ahh_SK.wav'

TC1_FILE_PATH1 = 'C:\\Users\\gs-1431\\Downloads\\Two_sample_scoring_api\\Reliable_score\\first.wav'
TC1_FILE_PATH2 = 'C:\\Users\\gs-1431\\Downloads\\Two_sample_scoring_api\\Reliable_score\\second.wav'

TC3_FILE_PATH1= 'C:\\Users\\gs-1431\\Downloads\\Two_sample_scoring_api\\Unreliable_score\\first.wav'
TC3_FILE_PATH2= 'C:\\Users\\gs-1431\\Downloads\\Two_sample_scoring_api\\Unreliable_score\\second.wav'

TC4_FILE_PATH1= 'C:\\Users\\gs-1431\\Downloads\\Two_sample_scoring_api\\Reliable_score\\first.wav'

TC5_FILE_PATH1= 'C:\\Users\\gs-1431\\Downloads\\test.txt'
TC8_FILE_PATH1= 'C:\\Users\\gs-1431\\Downloads\\Two_sample_scoring_api\\elck\\elckfailed.wav'
TC9_FILE_PATH1= 'C:\\Users\\gs-1431\\Downloads\\Two_sample_scoring_api\\ahh_8sec_44k.wav'
TC9_FILE_PATH_FS = 'C:\\Users\\gs-1431\\Downloads\\Two_sample_scoring_api\\fs.wav'
TC10_FILE_PATH1 = 'C:\\Users\\gs-1431\\Downloads\\Two_sample_scoring_api\\22k.wav'



status_code = API_Calls.upload_sample_file(STORAGE_SIGNED_URL, Shruti_AUDIO_FILE_PATH2)






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
#Business
# ----------------------TEST CASES Positive ---------------------------------------#


#Scenario: Both audio sample and audio file path are different and valid ahh file and reliable score is available  - both from US location  -get score
def test_E2E_reliable_score_US_location():

    #login with token
    status_code, json_data = API_Calls.token_api(BASE_URL, VALID_TOKEN_DATA, BASE_TOKEN, CONTENT_TYPE_URL_ENCODED)
    print("token api result:",status_code)
    #assert status_code == 200
    ACCESS_TOKEN = json_data['access_token']

    ACCESS_TOKEN_BEARER = 'Bearer ' + ACCESS_TOKEN
    print(ACCESS_TOKEN_BEARER)

    #create subject
    status, subject_json = API_Calls.subject_api(BASE_URL, VALID_SUBJECT_DATA, ACCESS_TOKEN_BEARER,CONTENT_TYPE_APPLICATION_JSON)
    print("subject api result:",status, subject_json )
    SUB_IDENTIFIER1 = subject_json['userIdentifier']

    VALID_STORAGE_DATA1 = {
        "fileType": "wav",
        "countryCode": "US",
        "userIdentifier": SUB_IDENTIFIER1
    }
    #storage api
    status_code, response_json = API_Calls.storage_api(BASE_URL, VALID_STORAGE_DATA1, ACCESS_TOKEN_BEARER,CONTENT_TYPE_APPLICATION_JSON)
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
    status_code, response_json = API_Calls.post_inference_parameters_api(BASE_URLV2, INFERENCE_PARAMETER_DATA, ACCESS_TOKEN_BEARER,CONTENT_TYPE_APPLICATION_JSON)
    print("POST inference parameters API result",status_code, response_json)
    INFERENCE_PARAMETER_ID = response_json['id']
    print(INFERENCE_PARAMETER_ID)

    #storage api for 2nd audio file
    status_code, response_json = API_Calls.storage_api(BASE_URL, VALID_STORAGE_DATA1, ACCESS_TOKEN_BEARER,CONTENT_TYPE_APPLICATION_JSON)
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
    status_code, response_json = API_Calls.put_inference_parameters_api(BASE_URLV2,ACCESS_TOKEN_BEARER,INFERENCE_PARAMETER_ID,INFERENCE_PARAMETER_DATA2, CONTENT_TYPE_APPLICATION_JSON)

    print("PUT inference parameters API result:",status_code,response_json)

    #POST inference scores API
    time.sleep(10)
    SCORE_V2_DATA = {
        "inferenceParameterId": INFERENCE_PARAMETER_ID
    }

    status_code, response_json = API_Calls.post_inference_scorev2_api(BASE_URLV2,SCORE_V2_DATA,ACCESS_TOKEN_BEARER,CONTENT_TYPE_APPLICATION_JSON)
    print("POST inference score v2 API result:", status_code, response_json)
    SCOREID = response_json['id']

    #GET inference scores API
    status_code, response_json = API_Calls.get_inference_scorev2_api(BASE_URLV2, SCOREID, ACCESS_TOKEN_BEARER,CONTENT_TYPE_APPLICATION_JSON)
    assert  status_code == 200
    print("GET inference score v2 API result:", status_code, response_json)



def test_E2E_reliable_score_IN_location():

    #login with token
    status_code, json_data = API_Calls.token_api(BASE_URL, VALID_TOKEN_DATA, BASE_TOKEN, CONTENT_TYPE_URL_ENCODED)
    print("token api result:",status_code)
    #assert status_code == 200
    ACCESS_TOKEN = json_data['access_token']

    #create subject
    status, subject_json = API_Calls.subject_api(BASE_URL, VALID_SUBJECT_DATA, ACCESS_TOKEN,CONTENT_TYPE_APPLICATION_JSON)
    print("subject api result:",status, subject_json )
    SUB_IDENTIFIER1 = subject_json['userIdentifier']

    VALID_STORAGE_DATA1 = {
        "fileType": "wav",
        "countryCode": "IN",
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
    status_code, response_json = API_Calls.post_inference_parameters_api(BASE_URLV2, INFERENCE_PARAMETER_DATA, ACCESS_TOKEN,CONTENT_TYPE_APPLICATION_JSON)
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
    status_code, response_json = API_Calls.put_inference_parameters_api(BASE_URLV2,ACCESS_TOKEN,INFERENCE_PARAMETER_ID,INFERENCE_PARAMETER_DATA2, CONTENT_TYPE_APPLICATION_JSON)

    print("PUT inference parameters API result:",status_code,response_json)

    #POST inference scores API
    time.sleep(10)
    SCORE_V2_DATA = {
        "inferenceParameterId": INFERENCE_PARAMETER_ID
    }
    status_code, response_json = API_Calls.post_inference_scorev2_api(BASE_URLV2,SCORE_V2_DATA,ACCESS_TOKEN,CONTENT_TYPE_APPLICATION_JSON)
    print("POST inference score v2 API result:", status_code, response_json)
    SCOREID = response_json['id']

    #GET inference scores API
    status_code, response_json = API_Calls.get_inference_scorev2_api(BASE_URLV2, SCOREID, ACCESS_TOKEN,CONTENT_TYPE_APPLICATION_JSON)
    assert status_code == 200
    print("GET inference score v2 API result:", status_code, response_json)




def test_E2E_unreliable_score_condition():

    #login with token
    status_code, json_data = API_Calls.token_api(BASE_URL, VALID_TOKEN_DATA, BASE_TOKEN, CONTENT_TYPE_URL_ENCODED)
    print("token api result:",status_code)
    #assert status_code == 200
    ACCESS_TOKEN = json_data['access_token']

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
    status_code, response_json = API_Calls.post_inference_parameters_api(BASE_URLV2, INFERENCE_PARAMETER_DATA, ACCESS_TOKEN,CONTENT_TYPE_APPLICATION_JSON)
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
    status_code, response_json = API_Calls.put_inference_parameters_api(BASE_URLV2,ACCESS_TOKEN,INFERENCE_PARAMETER_ID,INFERENCE_PARAMETER_DATA2, CONTENT_TYPE_APPLICATION_JSON)

    print("PUT inference parameters API result:",status_code,response_json)

    #POST inference scores API
    time.sleep(10)
    SCORE_V2_DATA = {
        "inferenceParameterId": INFERENCE_PARAMETER_ID
    }
    status_code, response_json = API_Calls.post_inference_scorev2_api(BASE_URLV2,SCORE_V2_DATA,ACCESS_TOKEN,CONTENT_TYPE_APPLICATION_JSON)
    print("POST inference score v2 API result:", status_code, response_json)
    SCOREID = response_json['id']
    time.sleep(10)
    #GET inference scores API
    status_code, response_json = API_Calls.get_inference_scorev2_api(BASE_URLV2, SCOREID, ACCESS_TOKEN,CONTENT_TYPE_APPLICATION_JSON)
    assert status_code == 422
    print("GET inference score v2 API result:", status_code, response_json)



def test_E2E_both_audio_files_are_same():

    #login with token
    status_code, json_data = API_Calls.token_api(BASE_URL, VALID_TOKEN_DATA, BASE_TOKEN, CONTENT_TYPE_URL_ENCODED)
    print("token api result:",status_code)
    #assert status_code == 200
    ACCESS_TOKEN = json_data['access_token']

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
    status_code = API_Calls.upload_sample_file(STORAGE_SIGNED_URL1, TC4_FILE_PATH1)
    print("First audio file upload:", status_code)

    INFERENCE_PARAMETER_DATA = {
        "measure": {
            "name": "respiratory-symptoms-risk",
            "variant": "v2"
        },
        "filePath": FILE_PATH1
    }
    #POST inference paramteres
    status_code, response_json = API_Calls.post_inference_parameters_api(BASE_URLV2, INFERENCE_PARAMETER_DATA, ACCESS_TOKEN,CONTENT_TYPE_APPLICATION_JSON)
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
    status_code = API_Calls.upload_sample_file(STORAGE_SIGNED_URL2, TC4_FILE_PATH1)
    print("Second audio file upload: ",status_code)

    # PUT inference paramteres
    status_code, response_json = API_Calls.put_inference_parameters_api(BASE_URLV2,ACCESS_TOKEN,INFERENCE_PARAMETER_ID,INFERENCE_PARAMETER_DATA2, CONTENT_TYPE_APPLICATION_JSON)

    print("PUT inference parameters API result:",status_code,response_json)
    assert status_code == 422



def test_E2E_both_audio_file_path_are_same():

    #login with token
    status_code, json_data = API_Calls.token_api(BASE_URL, VALID_TOKEN_DATA, BASE_TOKEN, CONTENT_TYPE_URL_ENCODED)
    print("token api result:",status_code)
    #assert status_code == 200
    ACCESS_TOKEN = json_data['access_token']

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
    status_code, response_json = API_Calls.post_inference_parameters_api(BASE_URLV2, INFERENCE_PARAMETER_DATA, ACCESS_TOKEN,CONTENT_TYPE_APPLICATION_JSON)
    print("POST inference parameters API result",status_code, response_json)
    INFERENCE_PARAMETER_ID = response_json['id']
    print(INFERENCE_PARAMETER_ID)

    #storage api for 2nd audio file
    status_code, response_json = API_Calls.storage_api(BASE_URL, VALID_STORAGE_DATA1, ACCESS_TOKEN,CONTENT_TYPE_APPLICATION_JSON)
    print("2nd audio storage api result:", status_code, response_json)
    STORAGE_SIGNED_URL2 = response_json['signedURL']
    FILE_PATH2 = response_json['filePath']

    INFERENCE_PARAMETER_DATA2 = {

        "filePath": FILE_PATH1
    }

    # second file upload
    status_code = API_Calls.upload_sample_file(STORAGE_SIGNED_URL1, TC4_FILE_PATH1)
    print("Second audio file upload: ",status_code)

    # PUT inference paramteres
    status_code, response_json = API_Calls.put_inference_parameters_api(BASE_URLV2,ACCESS_TOKEN,INFERENCE_PARAMETER_ID,INFERENCE_PARAMETER_DATA2, CONTENT_TYPE_APPLICATION_JSON)

    print("PUT inference parameters API result:",status_code,response_json)
    assert status_code == 422



def test_E2E_first_audio_file_valid_second_invalid():

    #login with token
    status_code, json_data = API_Calls.token_api(BASE_URL, VALID_TOKEN_DATA, BASE_TOKEN, CONTENT_TYPE_URL_ENCODED)
    print("token api result:",status_code)
    #assert status_code == 200
    ACCESS_TOKEN = json_data['access_token']

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
    status_code, response_json = API_Calls.post_inference_parameters_api(BASE_URLV2, INFERENCE_PARAMETER_DATA, ACCESS_TOKEN,CONTENT_TYPE_APPLICATION_JSON)
    print("POST inference parameters API result",status_code, response_json)
    INFERENCE_PARAMETER_ID = response_json['id']
    print(INFERENCE_PARAMETER_ID)

    #storage api for 2nd audio file
    status_code, response_json = API_Calls.storage_api(BASE_URL, VALID_STORAGE_DATA1, ACCESS_TOKEN,CONTENT_TYPE_APPLICATION_JSON)
    print("2nd audio storage api result:", status_code, response_json)
    STORAGE_SIGNED_URL2 = response_json['signedURL']
    FILE_PATH2 = response_json['filePath']

    INFERENCE_PARAMETER_DATA2 = {

        "filePath": FILE_PATH1
    }

    # second file upload
    status_code = API_Calls.upload_sample_file(STORAGE_SIGNED_URL1, TC5_FILE_PATH1)
    print("Second audio file upload: ",status_code)

    # PUT inference paramteres
    status_code, response_json = API_Calls.put_inference_parameters_api(BASE_URLV2,ACCESS_TOKEN,INFERENCE_PARAMETER_ID,INFERENCE_PARAMETER_DATA2, CONTENT_TYPE_APPLICATION_JSON)

    print("PUT inference parameters API result:",status_code,response_json)
    assert status_code == 422



def test_E2E_first_audio_file_invalid_second_valid():

    #login with token
    status_code, json_data = API_Calls.token_api(BASE_URL, VALID_TOKEN_DATA, BASE_TOKEN, CONTENT_TYPE_URL_ENCODED)
    print("token api result:",status_code)
    #assert status_code == 200
    ACCESS_TOKEN = json_data['access_token']

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
    status_code = API_Calls.upload_sample_file(STORAGE_SIGNED_URL1, TC5_FILE_PATH1)
    print("First audio file upload:", status_code)

    INFERENCE_PARAMETER_DATA = {
        "measure": {
            "name": "respiratory-symptoms-risk",
            "variant": "v2"
        },
        "filePath": FILE_PATH1
    }
    #POST inference paramteres
    status_code, response_json = API_Calls.post_inference_parameters_api(BASE_URLV2, INFERENCE_PARAMETER_DATA, ACCESS_TOKEN,CONTENT_TYPE_APPLICATION_JSON)
    print("POST inference parameters API result",status_code, response_json)
    assert  status_code == 422


def test_E2E_first_audio_file_missing():

    #login with token
    status_code, json_data = API_Calls.token_api(BASE_URL, VALID_TOKEN_DATA, BASE_TOKEN, CONTENT_TYPE_URL_ENCODED)
    print("token api result:",status_code)
    #assert status_code == 200
    ACCESS_TOKEN = json_data['access_token']

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
   # status_code = API_Calls.upload_sample_file(STORAGE_SIGNED_URL1, TC5_FILE_PATH1)
    #print("First audio file upload:", status_code)

    INFERENCE_PARAMETER_DATA = {
        "measure": {
            "name": "respiratory-symptoms-risk",
            "variant": "v2"
        },
        "filePath": FILE_PATH1
    }
    #POST inference paramteres
    status_code, response_json = API_Calls.post_inference_parameters_api(BASE_URLV2, INFERENCE_PARAMETER_DATA, ACCESS_TOKEN,CONTENT_TYPE_APPLICATION_JSON)
    print("POST inference parameters API result",status_code, response_json)
    assert  status_code == 404

def test_E2E_first_audio_elck_passed_and_second_elck_failed():

    #login with token
    status_code, json_data = API_Calls.token_api(BASE_URL, VALID_TOKEN_DATA, BASE_TOKEN, CONTENT_TYPE_URL_ENCODED)
    print("token api result:",status_code)
    #assert status_code == 200
    ACCESS_TOKEN = json_data['access_token']

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
    status_code, response_json = API_Calls.post_inference_parameters_api(BASE_URLV2, INFERENCE_PARAMETER_DATA, ACCESS_TOKEN,CONTENT_TYPE_APPLICATION_JSON)
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
    status_code = API_Calls.upload_sample_file(STORAGE_SIGNED_URL2, TC8_FILE_PATH1)
    print("Second audio file upload: ",status_code)

    # PUT inference paramteres
    status_code, response_json = API_Calls.put_inference_parameters_api(BASE_URLV2,ACCESS_TOKEN,INFERENCE_PARAMETER_ID,INFERENCE_PARAMETER_DATA2, CONTENT_TYPE_APPLICATION_JSON)

    print("PUT inference parameters API result:",status_code,response_json)

    #POST inference scores API
    time.sleep(10)
    SCORE_V2_DATA = {
        "inferenceParameterId": INFERENCE_PARAMETER_ID
    }
    status_code, response_json = API_Calls.post_inference_scorev2_api(BASE_URLV2,SCORE_V2_DATA,ACCESS_TOKEN,CONTENT_TYPE_APPLICATION_JSON)
    print("POST inference score v2 API result:", status_code, response_json)
    SCOREID = '"  "'
    assert status_code == 422

    #GET inference scores API
    status_code, response_json = API_Calls.get_inference_scorev2_api(BASE_URLV2, SCOREID, ACCESS_TOKEN,CONTENT_TYPE_APPLICATION_JSON)
    assert  status_code == 404
    print("GET inference score v2 API result:", status_code, response_json)




def test_E2E_first_audio_elck_failed_and_second_elck_passed():

    #login with token
    status_code, json_data = API_Calls.token_api(BASE_URL, VALID_TOKEN_DATA, BASE_TOKEN, CONTENT_TYPE_URL_ENCODED)
    print("token api result:",status_code)
    #assert status_code == 200
    ACCESS_TOKEN = json_data['access_token']

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
    status_code = API_Calls.upload_sample_file(STORAGE_SIGNED_URL1, TC8_FILE_PATH1)
    print("First audio file upload:", status_code)

    INFERENCE_PARAMETER_DATA = {
        "measure": {
            "name": "respiratory-symptoms-risk",
            "variant": "v2"
        },
        "filePath": FILE_PATH1
    }
    #POST inference paramteres
    status_code, response_json = API_Calls.post_inference_parameters_api(BASE_URLV2, INFERENCE_PARAMETER_DATA, ACCESS_TOKEN,CONTENT_TYPE_APPLICATION_JSON)
    print("POST inference parameters API result",status_code, response_json)
    assert status_code == 422
    INFERENCE_PARAMETER_ID = '"   "'
   # print(INFERENCE_PARAMETER_ID)

    #storage api for 2nd audio file
    status_code, response_json = API_Calls.storage_api(BASE_URL, VALID_STORAGE_DATA1, ACCESS_TOKEN,CONTENT_TYPE_APPLICATION_JSON)
    print("2nd audio storage api result:", status_code, response_json)
    STORAGE_SIGNED_URL2 = response_json['signedURL']
    FILE_PATH2 = response_json['filePath']

    INFERENCE_PARAMETER_DATA2 = {

        "filePath": FILE_PATH2
    }

    # second file upload
    status_code = API_Calls.upload_sample_file(STORAGE_SIGNED_URL2, TC1_FILE_PATH1)
    print("Second audio file upload: ",status_code)

    # PUT inference paramteres
    status_code, response_json = API_Calls.put_inference_parameters_api(BASE_URLV2,ACCESS_TOKEN,INFERENCE_PARAMETER_ID,INFERENCE_PARAMETER_DATA2, CONTENT_TYPE_APPLICATION_JSON)
    assert status_code == 400
    print("PUT inference parameters API result:",status_code,response_json)

    #POST inference scores API
    time.sleep(10)
    SCORE_V2_DATA = {
        "inferenceParameterId": INFERENCE_PARAMETER_ID
    }
    status_code, response_json = API_Calls.post_inference_scorev2_api(BASE_URLV2,SCORE_V2_DATA,ACCESS_TOKEN,CONTENT_TYPE_APPLICATION_JSON)
    print("POST inference score v2 API result:", status_code, response_json)
    assert  status_code == 404
    SCOREID = '"  "'

    #GET inference scores API
    status_code, response_json = API_Calls.get_inference_scorev2_api(BASE_URLV2, SCOREID, ACCESS_TOKEN,CONTENT_TYPE_APPLICATION_JSON)
    assert  status_code == 404
    print("GET inference score v2 API result:", status_code, response_json)




def test_E2E_both_audio_different_user():

    #login with token
    status_code, json_data = API_Calls.token_api(BASE_URL, VALID_TOKEN_DATA, BASE_TOKEN, CONTENT_TYPE_URL_ENCODED)
    print("token api result:",status_code)
    #assert status_code == 200
    ACCESS_TOKEN = json_data['access_token']

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
    status_code, response_json = API_Calls.post_inference_parameters_api(BASE_URLV2, INFERENCE_PARAMETER_DATA, ACCESS_TOKEN,CONTENT_TYPE_APPLICATION_JSON)
    print("POST inference parameters API result",status_code, response_json)
    INFERENCE_PARAMETER_ID = response_json['id']
    print(INFERENCE_PARAMETER_ID)


    status, subject_json = API_Calls.subject_api(BASE_URL, VALID_SUBJECT_DATA, ACCESS_TOKEN,
                                                 CONTENT_TYPE_APPLICATION_JSON)
    print("subject api result:", status, subject_json)
    SUB_IDENTIFIER2 = subject_json['userIdentifier']

    VALID_STORAGE_DATA2 = {
        "fileType": "wav",
        "countryCode": "US",
        "userIdentifier": SUB_IDENTIFIER2
    }

    #storage api for 2nd audio file
    status_code, response_json = API_Calls.storage_api(BASE_URL, VALID_STORAGE_DATA2, ACCESS_TOKEN,CONTENT_TYPE_APPLICATION_JSON)
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
    status_code, response_json = API_Calls.put_inference_parameters_api(BASE_URLV2,ACCESS_TOKEN,INFERENCE_PARAMETER_ID,INFERENCE_PARAMETER_DATA2, CONTENT_TYPE_APPLICATION_JSON)
    assert status_code == 422
    print("PUT inference parameters API result:",status_code,response_json)



def test_E2E_files_with_different_access_token():
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
                                                                             ACCESS_TOKEN,
                                                                             CONTENT_TYPE_APPLICATION_JSON)
        print("POST inference parameters API result", status_code, response_json)

        INFERENCE_PARAMETER_ID = response_json['id']
        print(INFERENCE_PARAMETER_ID)


        # storage api for 2nd audio file
        #create_subject_with_different_aprty
        status, subject_json = API_Calls.subject_api(BASE_URL, VALID_SUBJECT_DATA, ACCESS_TOKEN_WQ,
                                                     CONTENT_TYPE_APPLICATION_JSON)
        print("subject api result:", status, subject_json)
        SUB_IDENTIFIER2 = subject_json['userIdentifier']

        VALID_STORAGE_DATA2 = {
            "fileType": "wav",
            "countryCode": "US",
            "userIdentifier": SUB_IDENTIFIER2
        }

        status_code, response_json = API_Calls.storage_api(BASE_URL, VALID_STORAGE_DATA2, ACCESS_TOKEN_WQ,
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
        assert status_code == 404



def first_audio_six_second_second_audio_seven_sec_both_valid_files():

    #login with token
    status_code, json_data = API_Calls.token_api(BASE_URL, VALID_TOKEN_DATA, BASE_TOKEN, CONTENT_TYPE_URL_ENCODED)
    print("token api result:",status_code)
    #assert status_code == 200
    ACCESS_TOKEN = json_data['access_token']

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
    status_code, response_json = API_Calls.post_inference_parameters_api(BASE_URLV2, INFERENCE_PARAMETER_DATA, ACCESS_TOKEN,CONTENT_TYPE_APPLICATION_JSON)
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
    status_code = API_Calls.upload_sample_file(STORAGE_SIGNED_URL2, TC9_FILE_PATH2)
    print("Second audio file upload: ",status_code)

    # PUT inference paramteres
    status_code, response_json = API_Calls.put_inference_parameters_api(BASE_URLV2,ACCESS_TOKEN,INFERENCE_PARAMETER_ID,INFERENCE_PARAMETER_DATA2, CONTENT_TYPE_APPLICATION_JSON)

    print("PUT inference parameters API result:",status_code,response_json)
    assert  status_code == 422




def test_E2E_both_samples_from_different_uer():

    #login with token
    status_code, json_data = API_Calls.token_api(BASE_URL, VALID_TOKEN_DATA, BASE_TOKEN, CONTENT_TYPE_URL_ENCODED)
    print("token api result:",status_code)
    #assert status_code == 200
    ACCESS_TOKEN = json_data['access_token']

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
    status_code, response_json = API_Calls.post_inference_parameters_api(BASE_URLV2, INFERENCE_PARAMETER_DATA, ACCESS_TOKEN,CONTENT_TYPE_APPLICATION_JSON)
    print("POST inference parameters API result",status_code, response_json)
    INFERENCE_PARAMETER_ID = response_json['id']
    print(INFERENCE_PARAMETER_ID)

    # create subject
    status, subject_json = API_Calls.subject_api(BASE_URL, VALID_SUBJECT_DATA, ACCESS_TOKEN,
                                                 CONTENT_TYPE_APPLICATION_JSON)
    print("subject api result:", status, subject_json)
    SUB_IDENTIFIER2 = subject_json['userIdentifier']

    VALID_STORAGE_DATA2 = {
        "fileType": "wav",
        "countryCode": "US",
        "userIdentifier": SUB_IDENTIFIER2
    }

    #storage api for 2nd audio file
    status_code, response_json = API_Calls.storage_api(BASE_URL, VALID_STORAGE_DATA2, ACCESS_TOKEN,CONTENT_TYPE_APPLICATION_JSON)
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
    status_code, response_json = API_Calls.put_inference_parameters_api(BASE_URLV2,ACCESS_TOKEN,INFERENCE_PARAMETER_ID,INFERENCE_PARAMETER_DATA2, CONTENT_TYPE_APPLICATION_JSON)
    assert  status_code == 422
    print("PUT inference parameters API result:",status_code,response_json)

#
# # def test_file_with_different_access_token():
# #
# #     #login with token
# #     status_code, json_data = API_Calls.token_api(BASE_URL, VALID_TOKEN_DATA, BASE_TOKEN, CONTENT_TYPE_URL_ENCODED)
# #     print("token api result:",status_code)
# #     #assert status_code == 200
# #     ACCESS_TOKEN = json_data['access_token']
# #
# #     #create subject
# #     status, subject_json = API_Calls.subject_api(BASE_URL, VALID_SUBJECT_DATA, ACCESS_TOKEN,CONTENT_TYPE_APPLICATION_JSON)
# #     print("subject api result:",status, subject_json )
# #     SUB_IDENTIFIER1 = subject_json['userIdentifier']
# #
# #     VALID_STORAGE_DATA1 = {
# #         "fileType": "wav",
# #         "countryCode": "US",
# #         "userIdentifier": SUB_IDENTIFIER1
# #     }
# #     #storage api
# #     status_code, response_json = API_Calls.storage_api(BASE_URL, VALID_STORAGE_DATA1, ACCESS_TOKEN,CONTENT_TYPE_APPLICATION_JSON)
# #     STORAGE_SIGNED_URL1 = response_json['signedURL']
# #     print("1st audio storage api result:", status_code, response_json)
# #     FILE_PATH1 = response_json['filePath']
# #
# #     #first file upload
# #     status_code = API_Calls.upload_sample_file(STORAGE_SIGNED_URL1, TC1_FILE_PATH1)
# #     print("First audio file upload:", status_code)
# #
# #     INFERENCE_PARAMETER_DATA = {
# #         "measure": {
# #             "name": "respiratory-symptoms-risk",
# #             "variant": "v2"
# #         },
# #         "filePath": FILE_PATH1
# #     }
# #     #POST inference paramteres
# #     status_code, response_json = API_Calls.post_inference_parameters_api(BASE_URLV2, INFERENCE_PARAMETER_DATA, ACCESS_TOKEN,CONTENT_TYPE_APPLICATION_JSON)
# #     print("POST inference parameters API result",status_code, response_json)
# #     INFERENCE_PARAMETER_ID = response_json['id']
# #     print(INFERENCE_PARAMETER_ID)
# #
# #     status_code, json_data = API_Calls.token_api(BASE_URL, VALID_TOKEN_DATA, BASE_TOKEN_WQ, CONTENT_TYPE_URL_ENCODED)
# #     print("token api result:", status_code)
# #     # assert status_code == 200
# #     ACCESS_TOKEN = json_data['access_token']
# #
# #     # create subject
# #     status, subject_json = API_Calls.subject_api(BASE_URL, VALID_SUBJECT_DATA, ACCESS_TOKEN_WQ,
# #                                                  CONTENT_TYPE_APPLICATION_JSON)
# #     print("subject api result:", status, subject_json)
# #     SUB_IDENTIFIER2 = subject_json['userIdentifier']
# #
# #     VALID_STORAGE_DATA2 = {
# #         "fileType": "wav",
# #         "countryCode": "US",
# #         "userIdentifier": SUB_IDENTIFIER2
# #     }
# #
# #
# #     #storage api for 2nd audio file
# #     status_code, response_json = API_Calls.storage_api(BASE_URL, VALID_STORAGE_DATA2, ACCESS_TOKEN,CONTENT_TYPE_APPLICATION_JSON)
# #     print("2nd audio storage api result:", status_code, response_json)
# #     STORAGE_SIGNED_URL2 = response_json['signedURL']
# #     FILE_PATH2 = response_json['filePath']
# #
# #     INFERENCE_PARAMETER_DATA2 = {
# #
# #         "filePath": FILE_PATH2
# #     }
# #
# #     # second file upload
# #     status_code = API_Calls.upload_sample_file(STORAGE_SIGNED_URL2, TC1_FILE_PATH2)
# #     print("Second audio file upload: ",status_code)
# #
# #     # PUT inference paramteres
# #     status_code, response_json = API_Calls.put_inference_parameters_api(BASE_URLV2,ACCESS_TOKEN,INFERENCE_PARAMETER_ID,INFERENCE_PARAMETER_DATA2, CONTENT_TYPE_APPLICATION_JSON)
# #     assert  status_code == 404
# #     print("PUT inference parameters API result:",status_code,response_json)
# #
# #
#
#
def test_audio_files_beyond_defined_length():

    #login with token
    status_code, json_data = API_Calls.token_api(BASE_URL, VALID_TOKEN_DATA, BASE_TOKEN, CONTENT_TYPE_URL_ENCODED)
    print("token api result:",status_code)
    #assert status_code == 200
    ACCESS_TOKEN = json_data['access_token']

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
    status_code = API_Calls.upload_sample_file(STORAGE_SIGNED_URL1, TC9_FILE_PATH1)
    print("First audio file upload:", status_code)

    INFERENCE_PARAMETER_DATA = {
        "measure": {
            "name": "respiratory-symptoms-risk",
            "variant": "v2"
        },
        "filePath": FILE_PATH1
    }
    #POST inference paramteres
    status_code, response_json = API_Calls.post_inference_parameters_api(BASE_URLV2, INFERENCE_PARAMETER_DATA, ACCESS_TOKEN,CONTENT_TYPE_APPLICATION_JSON)
    assert  status_code == 422
    print("POST inference parameters API result",status_code, response_json)



def test_first_audio_ahh_second_audio_fs():

    #login with token
    status_code, json_data = API_Calls.token_api(BASE_URL, VALID_TOKEN_DATA, BASE_TOKEN, CONTENT_TYPE_URL_ENCODED)
    print("token api result:",status_code)
    #assert status_code == 200
    ACCESS_TOKEN = json_data['access_token']

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
    status_code, response_json = API_Calls.post_inference_parameters_api(BASE_URLV2, INFERENCE_PARAMETER_DATA, ACCESS_TOKEN,CONTENT_TYPE_APPLICATION_JSON)
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
    status_code = API_Calls.upload_sample_file(STORAGE_SIGNED_URL2, TC9_FILE_PATH_FS)
    print("Second audio file upload: ",status_code)

    # PUT inference paramteres
    status_code, response_json = API_Calls.put_inference_parameters_api(BASE_URLV2,ACCESS_TOKEN,INFERENCE_PARAMETER_ID,INFERENCE_PARAMETER_DATA2, CONTENT_TYPE_APPLICATION_JSON)
    assert status_code == 422
    print("PUT inference parameters API result:",status_code,response_json)


def test_first_audio_US_and_second_audio_IN_bucket():
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

    status, subject_json = API_Calls.subject_api(BASE_URL, VALID_SUBJECT_DATA, ACCESS_TOKEN,
                                                 CONTENT_TYPE_APPLICATION_JSON)
    print("subject api result:", status, subject_json)
    SUB_IDENTIFIER2 = subject_json['userIdentifier']
    # storage api for 2nd audio file

    VALID_STORAGE_DATA2 = {
        "fileType": "wav",
        "countryCode": "IN",
        "userIdentifier": SUB_IDENTIFIER2
    }
    status_code, response_json = API_Calls.storage_api(BASE_URL, VALID_STORAGE_DATA2, ACCESS_TOKEN,
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
    assert status_code ==422
    print("PUT inference parameters API result:", status_code, response_json)



def test_first_audio_US_and_second_audio_unsupported_country():
    # login with token
    status_code, json_data = API_Calls.token_api(BASE_URL, VALID_TOKEN_DATA, BASE_TOKEN_28JUL1, CONTENT_TYPE_URL_ENCODED)
    print("token api result:", status_code)
    # assert status_code == 200
    ACCESS_TOKEN_28JUL1 = json_data['access_token']

    # create subject
    status, subject_json = API_Calls.subject_api(BASE_URL, VALID_SUBJECT_DATA, ACCESS_TOKEN_28JUL1,
                                                 CONTENT_TYPE_APPLICATION_JSON)
    print("subject api result:", status, subject_json)
    SUB_IDENTIFIER1 = subject_json['userIdentifier']

    VALID_STORAGE_DATA1 = {
        "fileType": "wav",
        "countryCode": "US",
        "userIdentifier": SUB_IDENTIFIER1
    }
    # storage api
    status_code, response_json = API_Calls.storage_api(BASE_URL, VALID_STORAGE_DATA1, ACCESS_TOKEN_28JUL1,
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
                                                                         ACCESS_TOKEN_28JUL1, CONTENT_TYPE_APPLICATION_JSON)
    print("POST inference parameters API result", status_code, response_json)
    INFERENCE_PARAMETER_ID = response_json['id']
    print(INFERENCE_PARAMETER_ID)

    status, subject_json = API_Calls.subject_api(BASE_URL, VALID_SUBJECT_DATA, ACCESS_TOKEN_28JUL1,
                                                 CONTENT_TYPE_APPLICATION_JSON)
    print("subject api result:", status, subject_json)
    SUB_IDENTIFIER2 = subject_json['userIdentifier']
    # storage api for 2nd audio file

    VALID_STORAGE_DATA2 = {
        "fileType": "wav",
        "countryCode": "DE",
        "userIdentifier": SUB_IDENTIFIER2
    }
    status_code, response_json = API_Calls.storage_api(BASE_URL, VALID_STORAGE_DATA2, ACCESS_TOKEN_28JUL1,
                                                       CONTENT_TYPE_APPLICATION_JSON)
    assert status_code == 403



def test_v2_api_with_single_audio_file():

    #login with token
    status_code, json_data = API_Calls.token_api(BASE_URL, VALID_TOKEN_DATA, BASE_TOKEN, CONTENT_TYPE_URL_ENCODED)
    print("token api result:",status_code)
    #assert status_code == 200
    ACCESS_TOKEN = json_data['access_token']

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
            "name": "mental-fitness",
            "variant": "v2"
        },
        "filePath": FILE_PATH1
    }
    #POST inference paramteres
    status_code, response_json = API_Calls.post_inference_parameters_api(BASE_URLV2, INFERENCE_PARAMETER_DATA, ACCESS_TOKEN,CONTENT_TYPE_APPLICATION_JSON)
    print("POST inference parameters API result",status_code, response_json)
    INFERENCE_PARAMETER_ID = response_json['id']
    print(INFERENCE_PARAMETER_ID)

    SCORE_V2_DATA = {
        "inferenceParameterId": INFERENCE_PARAMETER_ID
    }

    status_code, response_json = API_Calls.post_inference_scorev2_api(BASE_URLV2,SCORE_V2_DATA,ACCESS_TOKEN,CONTENT_TYPE_APPLICATION_JSON)
    print("POST inference score v2 API result:", status_code, response_json)
    SCOREID = response_json['id']

    #GET inference scores API
    status_code, response_json = API_Calls.get_inference_scorev2_api(BASE_URLV2, SCOREID, ACCESS_TOKEN,CONTENT_TYPE_APPLICATION_JSON)
    assert  status_code == 200
    print("GET inference score v2 API result:", status_code, response_json)



def test_E2E_reliable_score_male_user():

    #login with token
    status_code, json_data = API_Calls.token_api(BASE_URL, VALID_TOKEN_DATA, BASE_TOKEN, CONTENT_TYPE_URL_ENCODED)
    print("token api result:",status_code)
    #assert status_code == 200
    ACCESS_TOKEN = json_data['access_token']

    #create subject
    status, subject_json = API_Calls.subject_api(BASE_URL, VALID_SUBJECT_DATA_M, ACCESS_TOKEN,CONTENT_TYPE_APPLICATION_JSON)
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
    status_code, response_json = API_Calls.post_inference_parameters_api(BASE_URLV2, INFERENCE_PARAMETER_DATA, ACCESS_TOKEN,CONTENT_TYPE_APPLICATION_JSON)
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
    status_code, response_json = API_Calls.put_inference_parameters_api(BASE_URLV2,ACCESS_TOKEN,INFERENCE_PARAMETER_ID,INFERENCE_PARAMETER_DATA2, CONTENT_TYPE_APPLICATION_JSON)

    print("PUT inference parameters API result:",status_code,response_json)

    #POST inference scores API
    time.sleep(10)
    SCORE_V2_DATA = {
        "inferenceParameterId": INFERENCE_PARAMETER_ID
    }
    status_code, response_json = API_Calls.post_inference_scorev2_api(BASE_URLV2,SCORE_V2_DATA,ACCESS_TOKEN,CONTENT_TYPE_APPLICATION_JSON)
    print("POST inference score v2 API result:", status_code, response_json)
    SCOREID = response_json['id']

    #GET inference scores API
    status_code, response_json = API_Calls.get_inference_scorev2_api(BASE_URLV2, SCOREID, ACCESS_TOKEN,CONTENT_TYPE_APPLICATION_JSON)
    assert  status_code == 200
    print("GET inference score v2 API result:", status_code, response_json)




def test_E2E_reliable_score_other_gender_user():

    #login with token
    status_code, json_data = API_Calls.token_api(BASE_URL, VALID_TOKEN_DATA, BASE_TOKEN, CONTENT_TYPE_URL_ENCODED)
    print("token api result:",status_code)
    #assert status_code == 200
    ACCESS_TOKEN = json_data['access_token']

    #create subject
    status, subject_json = API_Calls.subject_api(BASE_URL, VALID_SUBJECT_DATA_O, ACCESS_TOKEN,CONTENT_TYPE_APPLICATION_JSON)
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
    status_code, response_json = API_Calls.post_inference_parameters_api(BASE_URLV2, INFERENCE_PARAMETER_DATA, ACCESS_TOKEN,CONTENT_TYPE_APPLICATION_JSON)
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
    status_code, response_json = API_Calls.put_inference_parameters_api(BASE_URLV2,ACCESS_TOKEN,INFERENCE_PARAMETER_ID,INFERENCE_PARAMETER_DATA2, CONTENT_TYPE_APPLICATION_JSON)

    print("PUT inference parameters API result:",status_code,response_json)

    #POST inference scores API
    time.sleep(10)
    SCORE_V2_DATA = {
        "inferenceParameterId": INFERENCE_PARAMETER_ID
    }
    status_code, response_json = API_Calls.post_inference_scorev2_api(BASE_URLV2,SCORE_V2_DATA,ACCESS_TOKEN,CONTENT_TYPE_APPLICATION_JSON)
    print("POST inference score v2 API result:", status_code, response_json)
    SCOREID = response_json['id']

    #GET inference scores API
    status_code, response_json = API_Calls.get_inference_scorev2_api(BASE_URLV2, SCOREID, ACCESS_TOKEN,CONTENT_TYPE_APPLICATION_JSON)
    assert  status_code == 200
    print("GET inference score v2 API result:", status_code, response_json)



def test_E2E_audio_files_with_unsupported_sample_rate():

    #login with token
    status_code, json_data = API_Calls.token_api(BASE_URL, VALID_TOKEN_DATA, BASE_TOKEN, CONTENT_TYPE_URL_ENCODED)
    print("token api result:",status_code)
    #assert status_code == 200
    ACCESS_TOKEN = json_data['access_token']

    #create subject
    status, subject_json = API_Calls.subject_api(BASE_URL, VALID_SUBJECT_DATA_O, ACCESS_TOKEN,CONTENT_TYPE_APPLICATION_JSON)
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
    status_code = API_Calls.upload_sample_file(STORAGE_SIGNED_URL1, TC10_FILE_PATH1)
    print("First audio file upload:", status_code)

    INFERENCE_PARAMETER_DATA = {
        "measure": {
            "name": "respiratory-symptoms-risk",
            "variant": "v2"
        },
        "filePath": FILE_PATH1
    }
    #POST inference paramteres
    status_code, response_json = API_Calls.post_inference_parameters_api(BASE_URLV2, INFERENCE_PARAMETER_DATA, ACCESS_TOKEN,CONTENT_TYPE_APPLICATION_JSON)
    print("POST inference parameters API result",status_code, response_json)
    assert  status_code == 422
