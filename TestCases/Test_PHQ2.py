import json
import random
import pytest
import requests
import time
from TestCases import API_Calls
from TestCases.Support import assertion
from Variables.variable import *
from TestCases.Support import helper

#------Base64------#

base64secrets = helper.get_base64secrets(CLIENT_ID_Shruti, CLIENT_SECRET_Shruti)
BASE_TOKEN = 'Basic ' + base64secrets
#print(base64secrets)

#------Token-------#

status_code, json_data = API_Calls.token_api(BASE_URL, VALID_TOKEN_DATA, BASE_TOKEN, CONTENT_TYPE_URL_ENCODED)
ACCESS_TOKEN = json_data['access_token']
#print(ACCESS_TOKEN)

#------User--------#

status_code,json_data=API_Calls.subject_api(BASE_URL,VALID_SUBJECT_DATA,ACCESS_TOKEN,CONTENT_TYPE_APPLICATION_JSON)
SUB_IDENTIFIER=json_data['userIdentifier']
#print(SUB_IDENTIFIER)

#------Questionnaire detials ----------#

QUESTIONNAIRE_ID ="qnr-5f44ecbe4"
QUESTIONNAIRE_LANGUAGES ="en"
QUESTIONNAIRE_RESPONSE_ID=""
INFERENCE_PARAMETER_ID=""
SCORE_ID=""

#--------- GET Questionniare with measure name (mental fitness) ----------#

def test_get_questionnaire_by_measure_get_request():
    #global QUESTIONNAIRE_ID
    #global QUESTIONNAIRE_LANGUAGES
    headers = {'Authorization': ACCESS_TOKEN}
    res = requests.get(url=BASE_URL + GET_QUESTIONNAIRE_BY_MEASURENAME_ENDPOINT.format(measureName=MEASURE_NAME),headers=headers)
    #QUESTIONNAIRE_ID = res['questionnaire']['id']
    #QUESTIONNAIRE_LANGUAGES = res['questionnaire']['languages'][0]
    #print(res)
    #print(status)
    assertion.assert_valid_schema(res.json(), 'get_details_by_measure_name.json')
    assert res.status_code == 200

def test_get_questionnaire_by_measure_get_request_access_token_with_bearer():
    ACCESS_TOKEN_BEARER = 'Bearer ' + ACCESS_TOKEN
    print(ACCESS_TOKEN_BEARER)
    headers = {'Authorization': ACCESS_TOKEN_BEARER}
    res = requests.get(url=BASE_URL + GET_QUESTIONNAIRE_BY_MEASURENAME_ENDPOINT.format(measureName=MEASURE_NAME),headers=headers)
    #QUESTIONNAIRE_ID = res['questionnaire']['id']
    #QUESTIONNAIRE_LANGUAGES = res['questionnaire']['languages'][0]
    #print(res)
    #print(status)
    assertion.assert_valid_schema(res.json(), 'get_details_by_measure_name.json')
    assert res.status_code == 200


def test_get_questionnaire_by_measure_post_request():
    headers = {'Authorization': ACCESS_TOKEN}
    res = requests.post(url=BASE_URL + GET_QUESTIONNAIRE_BY_MEASURENAME_ENDPOINT.format(measureName=MEASURE_NAME),headers=headers)
    assert res.status_code == 403

def test_get_questionnaire_by_measure_put_request():
    headers = {'Authorization': ACCESS_TOKEN}
    res = requests.put(url=BASE_URL + GET_QUESTIONNAIRE_BY_MEASURENAME_ENDPOINT.format(measureName=MEASURE_NAME),headers=headers)
    assert res.status_code == 403

def test_get_questionnaire_by_measure_delete_request():
    headers = {'Authorization': ACCESS_TOKEN}
    res = requests.delete(url=BASE_URL + GET_QUESTIONNAIRE_BY_MEASURENAME_ENDPOINT.format(measureName=MEASURE_NAME),headers=headers)
    assert res.status_code == 403

def test_get_questionnaire_by_measure_invalid_end_point():
    headers = {'Authorization': ACCESS_TOKEN}
    res = requests.get(url=BASE_URL + GET_QUESTIONNAIRE_BY_MEASURENAME_INVALID_ENDPOINT.format(measureName=MEASURE_NAME),headers=headers)
    assert res.status_code == 403

def test_get_questionnaire_by_measure_api_header_missing():
    res = requests.get(url=BASE_URL + GET_QUESTIONNAIRE_BY_MEASURENAME_ENDPOINT.format(measureName=MEASURE_NAME))
    assert res.status_code == 401

def test_get_questionnaire_by_measure_api_invalid_access_token():
    headers = {'Authorization': INVALID_ACCESS_TOKEN}
    res = requests.get(url=BASE_URL + GET_QUESTIONNAIRE_BY_MEASURENAME_ENDPOINT.format(measureName=MEASURE_NAME),headers=headers)
    assert res.status_code == 401

def test_get_questionnaire_by_measure_api_access_token_with_bearer_small_case():
    ACCESS_TOKEN_BEARER1 = 'bearer ' + ACCESS_TOKEN
    print(ACCESS_TOKEN_BEARER1)
    headers = {'Authorization': ACCESS_TOKEN_BEARER1}
    res = requests.get(url=BASE_URL + GET_QUESTIONNAIRE_BY_MEASURENAME_ENDPOINT.format(measureName=MEASURE_NAME),headers=headers)
    assert res.status_code == 401

def test_get_questionnaire_by_measure_api_access_token_missing():
    headers = {'Authorization': ''}
    res = requests.get(url=BASE_URL + GET_QUESTIONNAIRE_BY_MEASURENAME_ENDPOINT.format(measureName=MEASURE_NAME),headers=headers)
    assert res.status_code == 401

def test_get_questionnaire_by_measure_api_extra_content_type_header_is_added():
    headers = {'Authorization': ACCESS_TOKEN, 'Content-Type': CONTENT_TYPE_URL_ENCODED}
    res = requests.get(url=BASE_URL + GET_QUESTIONNAIRE_BY_MEASURENAME_ENDPOINT.format(measureName=MEASURE_NAME),headers=headers)
    assert res.status_code == 415

def test_get_questionnaire_by_measure_api_invalid_measure_name():
    headers = {'Authorization': ACCESS_TOKEN}
    res = requests.get(url=BASE_URL + GET_QUESTIONNAIRE_BY_MEASURENAME_INVALID_MEASURENAME.format(invalidMeasureName=INVALID_MEASURE_NAME),headers=headers)
    assert res.status_code == 404
'''
def test_get_questionnaire_by_measure_api_no_access_to_measure():
    headers_get_voice_feature_by_measure_api = {'Authorization': ACCESS_TOKEN}
    res = requests.get(url=BASE_URL + '/measures/name/'+FEATURE_BY_MEASURE_NAME_NO_ACCESS +'/voice-features', headers=headers_get_voice_feature_by_measure_api)
    print(res)
    assert res.status_code == 403
'''
def test_get_questionnaire_by_measure_api_measure_name_is_blank():
    headers = {'Authorization': ACCESS_TOKEN}
    res = requests.get(url=BASE_URL + GET_QUESTIONNAIRE_BY_MEASURENAME_BLANK.format(blankMeasureName=BLANK_MEASURE_NAME),headers=headers)
    assert res.status_code == 404

def test_get_questionnaire_by_measure_api_measure_name_is_missing():
    headers = {'Authorization': ACCESS_TOKEN}
    res = requests.get(url=BASE_URL + GET_QUESTIONNAIRE_BY_MEASURENAME_MISSING,headers=headers)
    assert res.status_code == 404

def test_get_questionnaire_by_measure_api_measure_name_is_integer():
    headers = {'Authorization': ACCESS_TOKEN}
    res = requests.get(url=BASE_URL + GET_QUESTIONNAIRE_BY_MEASURENAME_INTEGER.format(integerMeasureName=INTEGER_MEASURE_NAME),headers=headers)
    assert res.status_code == 404

def test_get_questionnaire_by_measure_api_invalid_variant():
    headers = {'Authorization': ACCESS_TOKEN}
    res = requests.get(url=BASE_URL + GET_QUESTIONNAIRE_BY_MEASURENAME_INVALID_VARIANT,headers=headers)
    assert res.status_code == 404

def test_get_questionnaire_by_measure_api_varient_is_blank():
    headers = {'Authorization': ACCESS_TOKEN}
    url = BASE_URL + GET_QUESTIONNAIRE_BY_MEASURENAME_VARIANT_BLANK.format(measureName=MEASURE_NAME, blankVariant=BLANK_VARIANT)
    #print(url)
    res = requests.get(url,headers=headers)

    assert res.status_code == 400

def test_get_questionnaire_by_measure_api_varient_is_missing():
    headers = {'Authorization': ACCESS_TOKEN}
    res = requests.get(url=BASE_URL + GET_QUESTIONNAIRE_BY_VARIENT_MISSING.format(measureName=MEASURE_NAME),headers=headers)
    assert res.status_code == 200

def test_get_questionnaire_by_measure_api_varient_is_integer():
    headers = {'Authorization': ACCESS_TOKEN}
    res = requests.get(url=BASE_URL + GET_QUESTIONNAIRE_BY_VARIENT_INTEGER,headers=headers)
    assert res.status_code == 404


#----- Party didn't have access to v2 varient



#--------------------POST Questionnaire Response -------------------------#

header_submit_questionnaire = {'Authorization': ACCESS_TOKEN, 'Content-Type': CONTENT_TYPE_APPLICATION_JSON}
INDEX1=random.randrange(0, 3)
INDEX2=random.randrange(0, 3)
QUESTIONNAIRE_BODY = {
    "questionnaire": {
        "id": QUESTIONNAIRE_ID,
        "language": QUESTIONNAIRE_LANGUAGES,
        "userIdentifier": SUB_IDENTIFIER,
        "respondedAt": "1994-11-05T13:15:30Z",
        "questionResponses": [
            {
                "optionIndex": random.randrange(0, 3)
            },
            {
                "optionIndex": random.randrange(0, 3)
            }
        ]
    }
}
def test_upload_questionnaire_response_api():
    global QUESTIONNAIRE_RESPONSE_ID
    status, data = API_Calls.submit_questionnaire_response(BASE_URL, QUESTIONNAIRE_BODY, ACCESS_TOKEN)
    QUESTIONNAIRE_RESPONSE_ID=data['id']
    assertion.assert_valid_schema(data, 'Post_Questionnaire_Response.json')
    assert status == 201
    POST_INFERENCE_PARAMETER_DATA["parameter"]["questionnaireResponse"]["id"] = QUESTIONNAIRE_RESPONSE_ID

def test_upload_questionnaire_response_api_with_bearer_access_token():
    ACCESS_TOKEN_BEARER = 'Bearer ' + ACCESS_TOKEN
    print(ACCESS_TOKEN_BEARER)
    global QUESTIONNAIRE_RESPONSE_ID
    status, data = API_Calls.submit_questionnaire_response(BASE_URL, QUESTIONNAIRE_BODY, ACCESS_TOKEN_BEARER)
    QUESTIONNAIRE_RESPONSE_ID = data['id']
    assertion.assert_valid_schema(data, 'Post_Questionnaire_Response.json')
    assert status == 201
    POST_INFERENCE_PARAMETER_DATA["parameter"]["questionnaireResponse"]["id"] = QUESTIONNAIRE_RESPONSE_ID


def test_submit_questionnaire_response_with_authentication_header_missing():
    header = {'Content-Type': CONTENT_TYPE_APPLICATION_JSON}
    response = requests.post(url=BASE_URL + '/questionnaire-responses', data=json.dumps(QUESTIONNAIRE_BODY),
                             headers=header)
    #print(response)
    assert response.status_code == 401


def test_submit_questionnaire_response_with_incorrect_access_token():
    header = {'Authorization': 'XYZ', 'Content-Type': CONTENT_TYPE_APPLICATION_JSON}
    response = requests.post(url=BASE_URL + '/questionnaire-responses', data=json.dumps(QUESTIONNAIRE_BODY),
                             headers=header)
    #print(response)
    assert response.status_code == 401

def test_submit_questionnaire_response_with_incorrect_number_of_responses():
    QUESTIONNAIRE_BODY1 = {
        "questionnaire": {
            "id": QUESTIONNAIRE_ID,
            "language": QUESTIONNAIRE_LANGUAGES,
            "userIdentifier": SUB_IDENTIFIER,
            "respondedAt": "1994-11-05T13:15:30Z",
            "questionResponses": [
                {
                    "optionIndex": 1
                }
            ]
        }
    }
    status, data = API_Calls.submit_questionnaire_response(BASE_URL, QUESTIONNAIRE_BODY1, ACCESS_TOKEN)
    assert status == 422

def test_submit_questionnaire_response_with_incorrect_number_of_responses1():
    QUESTIONNAIRE_BODY1 = {
        "questionnaire": {
            "id": QUESTIONNAIRE_ID,
            "language": QUESTIONNAIRE_LANGUAGES,
            "userIdentifier": SUB_IDENTIFIER,
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
                }
            ]
        }
    }
    status, data = API_Calls.submit_questionnaire_response(BASE_URL, QUESTIONNAIRE_BODY1, ACCESS_TOKEN)
    assert status == 422

def test_submit_questionnaire_response_with_incorrect_number_of_responses_optionIndex():
    QUESTIONNAIRE_BODY1 = {
        "questionnaire": {
            "id": QUESTIONNAIRE_ID,
            "language": QUESTIONNAIRE_LANGUAGES,
            "userIdentifier": SUB_IDENTIFIER,
            "respondedAt": "1994-11-05T13:15:30Z",
            "questionResponses": [
                {
                    "optionIndex": 1
                },
                {
                    "optionIndex": 5
                }
            ]
        }
    }
    status, data = API_Calls.submit_questionnaire_response(BASE_URL, QUESTIONNAIRE_BODY1, ACCESS_TOKEN)
    assert status == 422

def test_submit_questionnaire_response_with_incorrect_number_of_responses_type():
    QUESTIONNAIRE_BODY1 = {
        "questionnaire": {
            "id": QUESTIONNAIRE_ID,
            "language": QUESTIONNAIRE_LANGUAGES,
            "userIdentifier": SUB_IDENTIFIER,
            "respondedAt": "1994-11-05T13:15:30Z",
            "questionResponses": [
                {
                    "optionIndex": 1
                },
                {
                    "optionIndexes": [1, 2]
                }
            ]
        }
    }
    status, data = API_Calls.submit_questionnaire_response(BASE_URL, QUESTIONNAIRE_BODY1, ACCESS_TOKEN)
    assert status == 422

def test_submit_questionnaire_response_with_isSkipable():
    QUESTIONNAIRE_BODY1 = {
        "questionnaire": {
            "id": QUESTIONNAIRE_ID,
            "language": QUESTIONNAIRE_LANGUAGES,
            "userIdentifier": SUB_IDENTIFIER,
            "respondedAt": "1994-11-05T13:15:30Z",
            "questionResponses": [
                {
                    "optionIndex": 1
                },
                {
                    "isSkipped": "True"
                }
            ]
        }
    }
    status, data = API_Calls.submit_questionnaire_response(BASE_URL, QUESTIONNAIRE_BODY1, ACCESS_TOKEN)
    assert status == 422

def test_submit_questionnaire_response_with_incorrect_id():
    D_CP = QUESTIONNAIRE_BODY['questionnaire'].copy()
    D = helper.update_dictionary(D_CP, id=123)
    DATA = {'questionnaire': D}
    status, data = API_Calls.submit_questionnaire_response(BASE_URL, DATA, ACCESS_TOKEN)
    #print(status, data)
    assert status == 400


def test_submit_questionnaire_response_with_incorrect_language_key():
    D_CP = QUESTIONNAIRE_BODY['questionnaire'].copy()
    D = helper.update_dictionary(D_CP, language='Tamil')
    DATA = {'questionnaire': D}
    status, data = API_Calls.submit_questionnaire_response(BASE_URL, DATA, ACCESS_TOKEN)
    #print(status, data)
    assert status == 404


def test_submit_questionnaire_response_with_incorrect_userIdentifier():
    D_CP = QUESTIONNAIRE_BODY['questionnaire'].copy()
    D = helper.update_dictionary(D_CP, userIdentifier="XYZ")
    DATA = {'questionnaire': D}
    status, data = API_Calls.submit_questionnaire_response(BASE_URL, DATA, ACCESS_TOKEN)
    #print(status, data)
    assert status == 400


def test_submit_questionnaire_response_with_incorrect_questionResponses():
    D_CP = QUESTIONNAIRE_BODY['questionnaire'].copy()
    D = helper.update_dictionary(D_CP, questionResponses={})
    DATA = {'questionnaire': D}
    status, data = API_Calls.submit_questionnaire_response(BASE_URL, DATA, ACCESS_TOKEN)
    #print(status, data)
    assert status == 400


def test_submit_questionnaire_response_with_multiple_variable_missing():
    D_CP = QUESTIONNAIRE_BODY['questionnaire'].copy()
    n = helper.factorial(len(D_CP))
    for key in range(n):
        D = helper.get_random_pairs(D_CP)
        DATA = {'questionnaire': D}
        status, data = API_Calls.submit_questionnaire_response(BASE_URL, DATA, ACCESS_TOKEN)
        #print(status, data)
        assert status == 400

#-------------------------------Create Inference Parameter--------------------------#

POST_INFERENCE_PARAMETER_DATA={
  "infer": "QuestionnaireScore",
  "parameter": {
    "measure": {
      "name": MEASURE_NAME,
      "variant": "v2"
    },
    "questionnaireResponse": {
      "id": QUESTIONNAIRE_RESPONSE_ID
    }
  }
}


def test_post_questionnaire_inference_parameter_api_inprogress():
    global INFERENCE_PARAMETER_ID
    print("hi"+QUESTIONNAIRE_RESPONSE_ID)
    status_code, response_json = API_Calls.post_inference_parameters_api(BASE_URLV2, POST_INFERENCE_PARAMETER_DATA, ACCESS_TOKEN,
                                                                             CONTENT_TYPE_APPLICATION_JSON)
    assertion.assert_valid_schema(response_json, 'v2_post_inference_parameter.json')
    assert status_code == 201
    INFERENCE_PARAMETER_ID = response_json['id']
    INFERENCE_PARAMETER_DATA["inferenceParameterId"]= INFERENCE_PARAMETER_ID

def test_post_questionnaire_inference_parameter_api_inprogress_with_bearer_access_token():
    ACCESS_TOKEN_BEARER = 'Bearer ' + ACCESS_TOKEN
    print(ACCESS_TOKEN_BEARER)
    global INFERENCE_PARAMETER_ID
    print("hi" + QUESTIONNAIRE_RESPONSE_ID)
    status_code, response_json = API_Calls.post_inference_parameters_api(BASE_URLV2, POST_INFERENCE_PARAMETER_DATA,
                                                                             ACCESS_TOKEN_BEARER,
                                                                             CONTENT_TYPE_APPLICATION_JSON)
    assertion.assert_valid_schema(response_json, 'v2_post_inference_parameter.json')
    assert status_code == 201
    INFERENCE_PARAMETER_ID = response_json['id']
    INFERENCE_PARAMETER_DATA["inferenceParameterId"] = INFERENCE_PARAMETER_ID



def test_post_questionnaire_inference_parameter_api_incorrect_accesstoken():
    INCORRECT_ACCESS_TOKEN = 'xyz'
    status_code, response_json = API_Calls.post_inference_parameters_api(BASE_URLV2, POST_INFERENCE_PARAMETER_DATA, INCORRECT_ACCESS_TOKEN,
                                                                             CONTENT_TYPE_APPLICATION_JSON)
    assert status_code == 401

def test_post_questionnaire_inference_parameter_api_expired_accesstoken():
    status_code, response_json = API_Calls.post_inference_parameters_api(BASE_URLV2, POST_INFERENCE_PARAMETER_DATA, EXPIRED_ACCESS_TOKEN,
                                                                             CONTENT_TYPE_APPLICATION_JSON)
    assert status_code == 401

def test_post_questionnaire_inference_parameter_api_access_token_with_bearer_in_small_case():
    ACCESS_TOKEN_BEARER1 = 'bearer ' + ACCESS_TOKEN
    print(ACCESS_TOKEN_BEARER1)
    status_code, response_json = API_Calls.post_inference_parameters_api(BASE_URLV2, POST_INFERENCE_PARAMETER_DATA,
                                                                             ACCESS_TOKEN_BEARER1,
                                                                             CONTENT_TYPE_APPLICATION_JSON)
    assert status_code == 401


def test_post_questionnaire_inference_parameter_api_missing_accesstoken():
    headers = {'Content-Type': CONTENT_TYPE_APPLICATION_JSON}
    res = requests.post(url=BASE_URLV2 + INFERENCE_PARAMETER_ENDPOINT, data=json.dumps(POST_INFERENCE_PARAMETER_DATA),
                        headers=headers)
    assert res.status_code == 401

def test_post_questionnaire_inference_parameter_api_blank_accesstoken():
    headers = {'Authorization': '', 'Content-Type': CONTENT_TYPE_APPLICATION_JSON}
    res = requests.post(url=BASE_URLV2 + INFERENCE_PARAMETER_ENDPOINT, data=json.dumps(POST_INFERENCE_PARAMETER_DATA),
                        headers=headers)
    assert res.status_code == 401

def test_post_questionnaire_inference_parameter_api_no_request_body():
    D_CP = POST_INFERENCE_PARAMETER_DATA.copy()
    DATA1 = helper.delete_key(D_CP, 'infer')
    DATA = helper.delete_key(DATA1, 'parameter')
    status_code, response_json = API_Calls.post_inference_parameters_api(BASE_URLV2, DATA, ACCESS_TOKEN,
                                                                             CONTENT_TYPE_APPLICATION_JSON)
    assert status_code == 400

def test_post_questionnaire_inference_parameter_api_invalid_endpoint():
    INVALID_INFERENCE_PARAMETER_ENDPOINT = '/inference/inferenceparameters123'
    headers = {'Authorization': ACCESS_TOKEN, 'Content-Type': CONTENT_TYPE_APPLICATION_JSON}
    res = requests.post(url=BASE_URLV2 + INVALID_INFERENCE_PARAMETER_ENDPOINT, data=json.dumps(POST_INFERENCE_PARAMETER_DATA),
                        headers=headers)
    assert res.status_code == 403

def test_post_questionnaire_inference_parameter_api_requestbody_infer_key_missing():

    DATA1 = {
        "parameter": {
            "measure": {
                "name": MEASURE_NAME,
                "variant": "v2"
         },
    "questionnaireResponse": {
    "id": QUESTIONNAIRE_RESPONSE_ID
    }
  }
    }

    status_code, response_json = API_Calls.post_inference_parameters_api(BASE_URLV2, DATA1, ACCESS_TOKEN,CONTENT_TYPE_APPLICATION_JSON)
    assert status_code == 400
    
def test_post_questionnaire_inference_parameter_api_requestbody_infer_keyname_missing():

    DATA1 = {
       " ": "QuestionnaireScore",
        "parameter": {
            "measure": {
                "name": MEASURE_NAME,
                "variant": "v2"
         },
    "questionnaireResponse": {
    "id": QUESTIONNAIRE_RESPONSE_ID
    }
  }
    }

    status_code, response_json = API_Calls.post_inference_parameters_api(BASE_URLV2, DATA1, ACCESS_TOKEN,CONTENT_TYPE_APPLICATION_JSON)
    assert status_code == 400
    
def test_post_questionnaire_inference_parameter_api_requestbody_infer_keyname_invalid():

    DATA1 = {
       "1234": "QuestionnaireScore",
        "parameter": {
            "measure": {
                "name": MEASURE_NAME,
                "variant": "v2"
         },
    "questionnaireResponse": {
    "id": QUESTIONNAIRE_RESPONSE_ID
    }
  }
    }

    status_code, response_json = API_Calls.post_inference_parameters_api(BASE_URLV2, DATA1, ACCESS_TOKEN,CONTENT_TYPE_APPLICATION_JSON)
    assert status_code == 400
    
def test_post_questionnaire_inference_parameter_api_requestbody_infer_keyvalue_missing():

    DATA1 = {
       "infer": " ",
        "parameter": {
            "measure": {
                "name": MEASURE_NAME,
                "variant": "v2"
         },
    "questionnaireResponse": {
    "id": QUESTIONNAIRE_RESPONSE_ID
    }
  }
    }

    status_code, response_json = API_Calls.post_inference_parameters_api(BASE_URLV2, DATA1, ACCESS_TOKEN,CONTENT_TYPE_APPLICATION_JSON)
    assert status_code == 404
    
def test_post_questionnaire_inference_parameter_api_requestbody_infer_keyvalue_invalid():

    DATA1 = {
       "infer": "1234",
        "parameter": {
            "measure": {
                "name": MEASURE_NAME,
                "variant": "v2"
         },
    "questionnaireResponse": {
    "id": QUESTIONNAIRE_RESPONSE_ID
    }
  }
    }

    status_code, response_json = API_Calls.post_inference_parameters_api(BASE_URLV2, DATA1, ACCESS_TOKEN,CONTENT_TYPE_APPLICATION_JSON)
    assert status_code == 404

def test_post_questionnaire_inference_parameter_api_requestbody_measure_key_missing():

    DATA1 = {
        "infer": "QuestionnaireScore",
        "parameter": {
            "questionnaireResponse": {
                "id": QUESTIONNAIRE_RESPONSE_ID
            }
        }
    }

    status_code, response_json = API_Calls.post_inference_parameters_api(BASE_URLV2, DATA1, ACCESS_TOKEN,
                                                                             CONTENT_TYPE_APPLICATION_JSON)
    assert status_code == 400

def test_post_questionnaire_inference_parameter_api_requestbody_measure_key_blank():
    D_CP = POST_INFERENCE_PARAMETER_DATA.copy()
    DATA = helper.update_dictionary(D_CP, parameter=' ')
    status_code, response_json = API_Calls.post_inference_parameters_api(BASE_URLV2, DATA, ACCESS_TOKEN,
                                                                             CONTENT_TYPE_APPLICATION_JSON)
    assert status_code == 400

def test_post_questionnaire_inference_parameter_api_requestbody_measure_keyname_blank():
    DATA1 = {
        "infer": "QuestionnaireScore",
        "parameter": {
            "measure": {
                " ": MEASURE_NAME,
                "variant": "v2"
            },
            "questionnaireResponse": {
                "id": QUESTIONNAIRE_RESPONSE_ID
            }
        }
    }
    status_code, response_json = API_Calls.post_inference_parameters_api(BASE_URLV2, DATA1, ACCESS_TOKEN,
                                                                             CONTENT_TYPE_APPLICATION_JSON)
    assert status_code == 400

def test_post_questionnaire_inference_parameter_api_requestbody_measure_keyname_invalid():
    DATA1 = {
        "infer": "QuestionnaireScore",
        "parameter": {
             "measure1234": {
             "name": MEASURE_NAME,
             "variant": "v2"
    },
        "questionnaireResponse": {
            "id": QUESTIONNAIRE_RESPONSE_ID
    }
  }
    }
    status_code, response_json = API_Calls.post_inference_parameters_api(BASE_URLV2, DATA1, ACCESS_TOKEN,
                                                                             CONTENT_TYPE_APPLICATION_JSON)
    assert status_code == 400

def test_post_questionnaire_inference_parameter_api_requestbody_measure_name_keyvalue_missing():
    DATA1 = {
        "infer": "QuestionnaireScore",
        "parameter": {
            "measure": {
                "name": " ",
                "variant": "v2"
            },
            "questionnaireResponse": {
                "id": QUESTIONNAIRE_RESPONSE_ID
            }
        }
    }
    status_code, response_json = API_Calls.post_inference_parameters_api(BASE_URLV2, DATA1, ACCESS_TOKEN,
                                                                             CONTENT_TYPE_APPLICATION_JSON)
    assert status_code == 404

def test_post_questionnaire_inference_parameter_api_measure_name_keyvalue_invalid():
    DATA1 = {
        "infer": "QuestionnaireScore",
        "parameter": {
             "measure": {
             "name": "12345",
             "variant": "v2"
    },
        "questionnaireResponse": {
            "id": QUESTIONNAIRE_RESPONSE_ID
    }
    }
    }
    status_code, response_json = API_Calls.post_inference_parameters_api(BASE_URLV2, DATA1, ACCESS_TOKEN,
                                                                             CONTENT_TYPE_APPLICATION_JSON)
    assert status_code == 404

def test_post_questionnaire_inference_parameter_api_requestbody_measure_variant_key_missing():
    DATA1 = {
        "infer": "QuestionnaireScore",
        "parameter": {
            "measure": {
                "name": MEASURE_NAME,
            },
            "questionnaireResponse": {
                "id": QUESTIONNAIRE_RESPONSE_ID
            }
        }
    }
    status_code, response_json = API_Calls.post_inference_parameters_api(BASE_URLV2, DATA1, ACCESS_TOKEN,
                                                                         CONTENT_TYPE_APPLICATION_JSON)
    assert status_code == 400

def test_post_questionnaire_inference_parameter_api_measure_variant_keyvalue_invalid():
    DATA1 = {
        "infer": "QuestionnaireScore",
        "parameter": {
             "measure": {
             "name": MEASURE_NAME,
             "variant": "1234"
    },
        "questionnaireResponse": {
            "id": QUESTIONNAIRE_RESPONSE_ID
    }
    }
    }
    status_code, response_json = API_Calls.post_inference_parameters_api(BASE_URLV2, DATA1, ACCESS_TOKEN,
                                                                         CONTENT_TYPE_APPLICATION_JSON)
    assert status_code == 400

def test_post_questionnaire_inference_parameter_api_measure_variant_keyvalue_invalid1():
    DATA1 = {
        "infer": "QuestionnaireScore",
        "parameter": {
            "measure": {
                "name": MEASURE_NAME,
                "variant": "v1234"
            },
            "questionnaireResponse": {
                "id": QUESTIONNAIRE_RESPONSE_ID
            }
        }
    }
    status_code, response_json = API_Calls.post_inference_parameters_api(BASE_URLV2, DATA1, ACCESS_TOKEN,
                                                                         CONTENT_TYPE_APPLICATION_JSON)
    assert status_code == 404

def test_post_questionnaire_inference_parameter_api_measure_variant_keyvalue_blank():
    DATA1 = {
        "infer": "QuestionnaireScore",
        "parameter": {
            "measure": {
                "name": MEASURE_NAME,
                "variant": " "
            },
            "questionnaireResponse": {
                "id": QUESTIONNAIRE_RESPONSE_ID
            }
        }
    }
    status_code, response_json = API_Calls.post_inference_parameters_api(BASE_URLV2, DATA1, ACCESS_TOKEN,
                                                                         CONTENT_TYPE_APPLICATION_JSON)
    assert status_code == 400

def test_post_questionnaire_inference_parameter_api_measure_name_and_variant_keyname_invalid():
    DATA1 = {
        "infer": "QuestionnaireScore",
        "parameter": {
            "measure": {
                "name123": MEASURE_NAME,
                "variant12345": "v2"
            },
            "questionnaireResponse": {
                "id": QUESTIONNAIRE_RESPONSE_ID
            }
        }
    }
    status_code, response_json = API_Calls.post_inference_parameters_api(BASE_URLV2, DATA1, ACCESS_TOKEN,
                                                                         CONTENT_TYPE_APPLICATION_JSON)
    assert status_code == 400

def test_post_questionnaire_inference_parameter_api_measure_name_and_variant_keyname_blank():
    DATA1 = {
        "infer": "QuestionnaireScore",
        "parameter": {
            "measure": {
                " ": MEASURE_NAME,
                " ": "v2"
            },
            "questionnaireResponse": {
                "id": QUESTIONNAIRE_RESPONSE_ID
            }
        }
    }
    status_code, response_json = API_Calls.post_inference_parameters_api(BASE_URLV2, DATA1, ACCESS_TOKEN,
                                                                         CONTENT_TYPE_APPLICATION_JSON)
    assert status_code == 400

def test_post_questionnaire_inference_parameter_api_measure_name_and_variant_keyvalue_invalid():
    DATA1 = {
            "infer": "QuestionnaireScore",
        "parameter": {
            "measure": {
                "name": "123",
                "variant": "v2123"
            },
            "questionnaireResponse": {
                "id": QUESTIONNAIRE_RESPONSE_ID
            }
        }
    }
    status_code, response_json = API_Calls.post_inference_parameters_api(BASE_URLV2, DATA1, ACCESS_TOKEN,
                                                                         CONTENT_TYPE_APPLICATION_JSON)
    assert status_code == 404

def test_post_questionnaire_inference_parameter_api_measure_name_and_variant_keyvalue_blank():
    DATA1 = {
        "infer": "QuestionnaireScore",
        "parameter": {
            "measure": {
                "name": " ",
                "variant": " "
            },
            "questionnaireResponse": {
                "id": QUESTIONNAIRE_RESPONSE_ID
            }
        }
    }
    status_code, response_json = API_Calls.post_inference_parameters_api(BASE_URLV2, DATA1, ACCESS_TOKEN,
                                                                         CONTENT_TYPE_APPLICATION_JSON)
    assert status_code == 400

def test_post_questionnaire_inference_parameter_api_requestbody_questionnaireResponse_key_missing():
    DATA1 = {
        "infer": "QuestionnaireScore",
        "parameter": {
            "measure": {
                "name": MEASURE_NAME,
                "variant": "v2"
            }
        }
    }

    status_code, response_json = API_Calls.post_inference_parameters_api(BASE_URLV2, DATA1, ACCESS_TOKEN,
                                                                             CONTENT_TYPE_APPLICATION_JSON)
    assert status_code == 400

def test_post_questionnaire_inference_parameter_api_requestbody_questionnaireResponse_keyname_blank():
    DATA1 = {
        "infer": "QuestionnaireScore",
        "parameter": {
            "measure": {
                "name": MEASURE_NAME,
                "variant": "v2"
            },
            " ": {
                "id": QUESTIONNAIRE_RESPONSE_ID
            }
        }
    }
    status_code, response_json = API_Calls.post_inference_parameters_api(BASE_URLV2, DATA1, ACCESS_TOKEN,
                                                                         CONTENT_TYPE_APPLICATION_JSON)
    assert status_code == 400

def test_post_questionnaire_inference_parameter_api_requestbody_questionnaireResponse_id_keyname_blank():
        DATA1 = {
            "infer": "QuestionnaireScore",
            "parameter": {
                "measure": {
                    "name": MEASURE_NAME,
                    "variant": "v2"
                },
                "questionnaireResponse": {
                    " ": QUESTIONNAIRE_RESPONSE_ID
                }
            }
        }
        status_code, response_json = API_Calls.post_inference_parameters_api(BASE_URLV2, DATA1, ACCESS_TOKEN,
                                                                             CONTENT_TYPE_APPLICATION_JSON)
        assert status_code == 400


def test_post_questionnaire_inference_parameter_api_requestbody_questionnaireResponse_id_keyvalue_blank():
    DATA1 = {
        "infer": "QuestionnaireScore",
        "parameter": {
            "measure": {
                "name": MEASURE_NAME,
                "variant": "v2"
            },
            "questionnaireResponse": {
                "id": " "
            }
        }
    }
    status_code, response_json = API_Calls.post_inference_parameters_api(BASE_URLV2, DATA1, ACCESS_TOKEN,
                                                                         CONTENT_TYPE_APPLICATION_JSON)

    assert status_code == 404


def test_post_questionnaire_inference_parameter_api_requestbody_questionnaireResponse_keyname_invalid():
    DATA1 = {
        "infer": "QuestionnaireScore",
        "parameter": {
            "measure": {
                "name": MEASURE_NAME,
                "variant": "v2"
            },
            "zcdfd": {
                "id": QUESTIONNAIRE_RESPONSE_ID
            }
        }
    }
    status_code, response_json = API_Calls.post_inference_parameters_api(BASE_URLV2, DATA1, ACCESS_TOKEN,
                                                                         CONTENT_TYPE_APPLICATION_JSON)
    assert status_code == 400


def test_post_questionnaire_inference_parameter_api_requestbody_questionnaireResponse_id_keyname_invalid():
    DATA1 = {
        "infer": "QuestionnaireScore",
        "parameter": {
            "measure": {
                "name": MEASURE_NAME,
                "variant": "v2"
            },
            "questionnaireResponse": {
                "id12345": QUESTIONNAIRE_RESPONSE_ID
            }
        }
    }
    status_code, response_json = API_Calls.post_inference_parameters_api(BASE_URLV2, DATA1, ACCESS_TOKEN,
                                                                         CONTENT_TYPE_APPLICATION_JSON)
    assert status_code == 400

# ----- 422 : INVALID_QUESTIONNAIRE_RESPONSE
def test_post_questionnaire_inference_scorev2_api_INVALID_QUESTIONNAIRE_RESPONSE():
    DATA1 = {
        "infer": "QuestionnaireScore",
        "parameter": {
            "measure": {
                "name": MEASURE_NAME,
                "variant": "v2"
            },
            "questionnaireResponse": {
                "id": "qrs_36409cdb7f77"
            }
        }
    }
    status_code, response_json = API_Calls.post_inference_parameters_api(BASE_URLV2, DATA1, ACCESS_TOKEN,
                                                                         CONTENT_TYPE_APPLICATION_JSON)
    assert status_code == 422

# ------ 422 :  QUESTIONNAIRE_SCORE_NOT_SUPPORTED
def test_post_questionnaire_inference_scorev2_api_QUESTIONNAIRE_SCORE_NOT_SUPPORTED():
    DATA1 = {
        "infer": "QuestionnaireScore",
        "parameter": {
            "measure": {
                "name": "respiratory-symptoms-risk",
                "variant": "v1"
            },
            "questionnaireResponse": {
                "id": "qrs_940a643f5c9f"
            }
        }
    }
    status_code, response_json = API_Calls.post_inference_parameters_api(BASE_URLV2, DATA1, ACCESS_TOKEN,
                                                                         CONTENT_TYPE_APPLICATION_JSON)
    assert status_code == 422

# -----  422 : QUESTIONNAIRE_NOT_SUPPORTED
def test_post_questionnaire_inference_scorev2_api_QUESTIONNAIRE_NOT_SUPPORTED():
    DATA1 = {
        "infer": "QuestionnaireScore",
        "parameter": {
            "measure": {
                "name": "respiratory-symptoms-risk",
                "variant": "v2"
            },
            "questionnaireResponse": {
                "id": "qrs_940a643f5c9f"
            }
        }
    }
    status_code, response_json = API_Calls.post_inference_parameters_api(BASE_URLV2, DATA1, ACCESS_TOKEN,
                                                                         CONTENT_TYPE_APPLICATION_JSON)
    assert status_code == 422

def test_post_questionnaire_inference_parameter_api_requestbody_questionnaireResponse_id_keyvalue_invalid():
    DATA1 = {
        "infer": "QuestionnaireScore",
        "parameter": {
            "measure": {
                "name": MEASURE_NAME,
                "variant": "v2"
            },
            "questionnaireResponse": {
                "id": "abcd"
            }
        }
    }
    status_code, response_json = API_Calls.post_inference_parameters_api(BASE_URLV2, DATA1, ACCESS_TOKEN,
                                                                         CONTENT_TYPE_APPLICATION_JSON)
    assert status_code == 404

#--------------------------Generate Inference Score -------------------------#

INFERENCE_PARAMETER_DATA={
    "inferenceParameterId": INFERENCE_PARAMETER_ID
}

def test_post_questionnaire_inference_scorev2_api_incorrect_accesstoken():
    INCORRECT_ACCESS_TOKEN = 'xyz'
    status_code, response_json = API_Calls.post_inference_scorev2_api(BASE_URLV2, INFERENCE_PARAMETER_DATA, INCORRECT_ACCESS_TOKEN, CONTENT_TYPE_APPLICATION_JSON)
    assert status_code == 401

def test_post_questionnaire_inference_scorev2_api_expired_accesstoken():
    status_code, response_json = API_Calls.post_inference_scorev2_api(BASE_URLV2, INFERENCE_PARAMETER_DATA, EXPIRED_ACCESS_TOKEN, CONTENT_TYPE_APPLICATION_JSON)
    assert status_code == 401

def test_post_questionnaire_inference_scorev2_api_access_token_with_bearer_in_small_case():
    ACCESS_TOKEN_BEARER1 = 'bearer ' + ACCESS_TOKEN
    print(ACCESS_TOKEN_BEARER1)
    status_code, response_json = API_Calls.post_inference_scorev2_api(BASE_URLV2, INFERENCE_PARAMETER_DATA,
                                                                          ACCESS_TOKEN_BEARER1,
                                                                          CONTENT_TYPE_APPLICATION_JSON)
    assert status_code == 401


def test_post_questionnaire_inference_scorev2_api_missing_accesstoken():
    headers = {'Content-Type': CONTENT_TYPE_APPLICATION_JSON}
    res = requests.post(url=BASE_URLV2 + INFERENCE_ENDPOINT, data=json.dumps(INFERENCE_PARAMETER_DATA), headers=headers)
    assert res.status_code == 401

def test_post_questionnaire_inference_scorev2_api_blank_accesstoken():
    headers = {'Authorization': '', 'Content-Type': CONTENT_TYPE_APPLICATION_JSON}
    res = requests.post(url=BASE_URLV2 + INFERENCE_ENDPOINT, data=json.dumps(INFERENCE_PARAMETER_DATA), headers=headers)
    assert res.status_code == 401

def test_post_questionnaire_inference_scorev2_api_no_request_body():
    D_CP = INFERENCE_PARAMETER_DATA.copy()
    DATA = helper.delete_key(D_CP, 'inferenceParameterId')
    status_code, response_json = API_Calls.post_inference_scorev2_api(BASE_URLV2, DATA, ACCESS_TOKEN, CONTENT_TYPE_APPLICATION_JSON)
    assert status_code == 400

def test_post_questionnaire_inference_scorev2_invalid_endpoint():
    INVALID_INFERENCE_SCORE_ENDPOINT = '/inference/scores123'
    headers = {'Authorization': ACCESS_TOKEN, 'Content-Type': CONTENT_TYPE_APPLICATION_JSON}
    res = requests.post(url=BASE_URLV2 + INVALID_INFERENCE_SCORE_ENDPOINT, data=json.dumps(INFERENCE_PARAMETER_DATA), headers=headers)
    assert res.status_code == 403

def test_post_questionnaire_inference_scorev2_api_requestbody_extra_key_added():
    POST_INFERENCE_DATA1 = {
        "inferenceParameterId": INFERENCE_PARAMETER_ID,
        "test":"123"
    }
    status_code, response_json = API_Calls.post_inference_scorev2_api(BASE_URLV2, POST_INFERENCE_DATA1, ACCESS_TOKEN, CONTENT_TYPE_APPLICATION_JSON)
    assert status_code == 400

def test_post_questionnaire_inference_scorev2_api_content_type_missing():
    headers = {'Authorization': ACCESS_TOKEN}
    res = requests.post(url=BASE_URLV2 + INFERENCE_ENDPOINT, data=json.dumps(INFERENCE_PARAMETER_DATA), headers=headers)
    assert res.status_code == 400

def test_post_questionnaire_inference_scorev2_api_content_type_invalid():
    headers = {'Authorization': ACCESS_TOKEN, 'Content-Type': CONTENT_TYPE_URL_ENCODED}
    res = requests.post(url=BASE_URLV2 + INFERENCE_ENDPOINT, data=json.dumps(INFERENCE_PARAMETER_DATA), headers=headers)
    assert res.status_code == 415

def test_post_questionnaire_inference_scorev2_api_content_type_blank():
    headers = {'Authorization': ACCESS_TOKEN, 'Content-Type': ""}
    res = requests.post(url=BASE_URLV2 + INFERENCE_ENDPOINT, data=json.dumps(INFERENCE_PARAMETER_DATA), headers=headers)
    assert res.status_code == 415

def test_post_questionnaire_inference_scorev2_api_inference_parameter_not_found():
    D_CP = INFERENCE_PARAMETER_DATA.copy()
    DATA = helper.update_dictionary(D_CP, inferenceParameterId="1234")
    status_code, response_json = API_Calls.post_inference_scorev2_api(BASE_URLV2, DATA, ACCESS_TOKEN, CONTENT_TYPE_APPLICATION_JSON)
    assert status_code == 404

def test_post_questionnaire_inference_scorev2_api_inference_parameter_blank():
    D_CP = INFERENCE_PARAMETER_DATA.copy()
    DATA = helper.update_dictionary(D_CP, inferenceParameterId="")
    status_code, response_json = API_Calls.post_inference_scorev2_api(BASE_URLV2, DATA, ACCESS_TOKEN, CONTENT_TYPE_APPLICATION_JSON)
    assert status_code == 400

def test_POST_questionnaire_inference_scorev2_api_inprogress():
    global SCORE_ID
    status_code, response_json = API_Calls.post_inference_scorev2_api(BASE_URLV2, INFERENCE_PARAMETER_DATA, ACCESS_TOKEN, CONTENT_TYPE_APPLICATION_JSON)
    assert status_code == 202
    assertion.assert_valid_schema(response_json, 'v2_post_inference_score.json')
    SCORE_ID=response_json['id']


time.sleep(10)
def test_POST_questionnaire_inference_scorev2_api_measure_score_already_present1():
    status_code, response_json = API_Calls.post_inference_scorev2_api(BASE_URLV2, INFERENCE_PARAMETER_DATA, ACCESS_TOKEN, CONTENT_TYPE_APPLICATION_JSON)
    assert status_code == 422

# ----------------------------- Get Score ------------------------#

def test_get_questionnaire_inference_scorev2_api():
    status_code, response_json = API_Calls.get_inference_scorev2_api(BASE_URLV2, SCORE_ID, ACCESS_TOKEN,
                                                                         CONTENT_TYPE_APPLICATION_JSON)
    assert status_code == 200
    assertion.assert_valid_schema(response_json, 'get_inference_score.json')


def test_get_questionnaire_inference_scorev2_api_access_token_with_bearer():
    ACCESS_TOKEN_BEARER = 'Bearer ' + ACCESS_TOKEN
    print(ACCESS_TOKEN_BEARER)
    status_code, response_json = API_Calls.get_inference_scorev2_api(BASE_URLV2, SCORE_ID, ACCESS_TOKEN_BEARER,
                                                                         CONTENT_TYPE_APPLICATION_JSON)
    assert status_code == 200
    assertion.assert_valid_schema(response_json, 'get_inference_score.json')


def test_get_questionnaire_inference_scorev2_api_incorrect_accesstoken():
    INCORRECT_ACCESS_TOKEN = 'xyz'
    status_code, response_json = API_Calls.get_inference_scorev2_api(BASE_URLV2, SCORE_ID, INCORRECT_ACCESS_TOKEN, CONTENT_TYPE_APPLICATION_JSON)
    assert status_code == 401

def test_get_questionnaire_inference_scorev2_api_expired_accesstoken():
    status_code, response_json = API_Calls.get_inference_scorev2_api(BASE_URLV2, SCORE_ID, EXPIRED_ACCESS_TOKEN, CONTENT_TYPE_APPLICATION_JSON)
    assert status_code == 401


def test_get_questionnaire_inference_scorev2_api_accesstoken_with_small_case():
    ACCESS_TOKEN_BEARER1 = 'bearer ' + ACCESS_TOKEN
    print(ACCESS_TOKEN_BEARER1)
    status_code, response_json = API_Calls.get_inference_scorev2_api(BASE_URLV2, SCORE_ID, ACCESS_TOKEN_BEARER1, CONTENT_TYPE_APPLICATION_JSON)
    assert status_code == 401


def test_get_questionnaire_inference_scorev2_api_missing_accesstoken():
    headers = {'Content-Type': CONTENT_TYPE_APPLICATION_JSON}
    res = requests.get(url=BASE_URLV2 + INFERENCE_ENDPOINT + '/' +SCORE_ID, headers=headers)
    assert res.status_code == 401

def test_get_questionnaire_inference_scorev2_api_blank_accesstoken():
    headers = {'Authorization': '', 'Content-Type': CONTENT_TYPE_APPLICATION_JSON}
    res = requests.get(url=BASE_URLV2 + INFERENCE_ENDPOINT + '/' +SCORE_ID, headers=headers)
    assert res.status_code == 401

def test_get_questionnaire_inference_scorev2_invalid_endpoint():
    INVALID_INFERENCE_SCORE_ENDPOINT = '/inference/scores123'
    headers = {'Authorization': ACCESS_TOKEN, 'Content-Type': CONTENT_TYPE_APPLICATION_JSON}
    res = requests.get(url=BASE_URLV2 + INVALID_INFERENCE_SCORE_ENDPOINT + '/' +SCORE_ID, headers=headers)
    assert res.status_code == 403

def test_get_questionnaire_inference_scorev2_invalid_scoreId():
    INVALID_SCORE_ID="1234"
    status_code, response_json = API_Calls.get_inference_scorev2_api(BASE_URLV2, INVALID_SCORE_ID, ACCESS_TOKEN, CONTENT_TYPE_APPLICATION_JSON)
    assert status_code == 404

def test_get_questionnaire_inference_scorev2_blank_scoreId():
    BLANK_SCORE_ID=" "
    status_code, response_json = API_Calls.get_inference_scorev2_api(BASE_URLV2, BLANK_SCORE_ID, ACCESS_TOKEN, CONTENT_TYPE_APPLICATION_JSON)
    assert status_code == 404

def test_get_questionnaire_inference_scorev2_api_no_scoreId():
    headers = {'Authorization': ACCESS_TOKEN, 'Content-Type': CONTENT_TYPE_APPLICATION_JSON}
    res = requests.get(url=BASE_URLV2 + INFERENCE_ENDPOINT, headers=headers)
    assert res.status_code == 403