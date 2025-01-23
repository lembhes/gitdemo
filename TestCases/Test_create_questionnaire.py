import json
import pytest
import requests
import time
from TestCases import API_Calls
from TestCases.Support import assertion
from Variables.variable import *
from TestCases.Support import helper



# ---------------- Get the Base64 live client --------------------------------#

base64secrets = helper.get_base64secrets(CLIENT_ID_Shruti, CLIENT_SECRET_Shruti)
print(base64secrets)

BASE_TOKEN = 'Basic ' + base64secrets

# ---------------- Get the Base64 testclient --------------------------------#

base64secrets = helper.get_base64secrets(CLIENT_ID_Shruti_test, CLIENT_SECRET_Shruti_test)
print(base64secrets)

BASE_TOKEN_TEST = 'Basic ' + base64secrets

# ---------------- Get the Base64  for dummy API --------------------------------#

base64secrets = helper.get_base64secrets(CLIENT_ID_PARTYM, CLIENT_SECRET_PARTYM)
print(base64secrets)

BASE_TOKEN_PARTYM = 'Basic ' + base64secrets

# ---------------- Get the Base64  for dummy API --------------------------------#

base64secrets = helper.get_base64secrets(CLIENT_ID_WQ, CLIENT_SECRET_WQ)
print(base64secrets)

BASE_TOKEN_WQ = 'Basic ' + base64secrets


## ---------------- Get the Base64  for 19oct1@yopmail.com user --------------------------------#

base64secrets = helper.get_base64secrets(CLIENT_ID_19OCT1, CLIENT_SECRET_19OCT1)
print(base64secrets)

BASE_TOKEN_19OCT1 = 'Basic ' + base64secrets

# ----------- Get the ACCESS TOKEN ----------------------------#

status_code, json_data = API_Calls.token_api(BASE_URL, VALID_TOKEN_DATA, BASE_TOKEN, CONTENT_TYPE_URL_ENCODED)
ACCESS_TOKEN = json_data['access_token']

# ----------- Get the ACCESS TOKEN for missing party client credentials ----------------------------#

status_code, json_data = API_Calls.token_api(BASE_URL, VALID_TOKEN_DATA, BASE_TOKEN_PARTYM, CONTENT_TYPE_URL_ENCODED)
ACCESS_TOKEN_PARTYM = json_data['access_token']

# ----------- Get the ACCESS TOKEN for missing party client credentials ----------------------------#

status_code, json_data = API_Calls.token_api(BASE_URL, VALID_TOKEN_DATA, BASE_TOKEN_TEST, CONTENT_TYPE_URL_ENCODED)
ACCESS_TOKEN_TEST = json_data['access_token']

# ----------- Get the ACCESS TOKEN for missing party client credentials ----------------------------#

status_code, json_data = API_Calls.token_api(BASE_URL, VALID_TOKEN_DATA, BASE_TOKEN_WQ, CONTENT_TYPE_URL_ENCODED)
ACCESS_TOKEN_WQ = json_data['access_token']

#---Get access token for 19oct1@yopmail.com---#

status_code, json_data = API_Calls.token_api(BASE_URL, VALID_TOKEN_DATA, BASE_TOKEN_19OCT1, CONTENT_TYPE_URL_ENCODED)
ACCESS_TOKEN_19OCT1 = json_data['access_token']
# ---------------- GET SUBJECT IDENTIFIER -------------------------------#
#
# status, subject_json = API_Calls.subject_api(BASE_URL, VALID_SUBJECT_DATA, ACCESS_TOKEN,CONTENT_TYPE_APPLICATION_JSON)
# SUB_IDENTIFIER = subject_json['userIdentifier']

# ----------------------STORAGE API CALL TO GET STORAGE_SIGNED_URL & FILE_PATH ----------------------------#

# VALID_STORAGE_DATA = {
#     "fileType": "wav",
#     "countryCode": "US",
#     "userIdentifier": SUB_IDENTIFIER
# }
#
# status_code, response_json = API_Calls.storage_api(BASE_URL, VALID_STORAGE_DATA, ACCESS_TOKEN,
#                                                    CONTENT_TYPE_APPLICATION_JSON)

# STORAGE_SIGNED_URL = response_json['signedURL']
# FILE_PATH = response_json['filePath']



#---------- post create questionnaire API ----------

status, response_json = API_Calls.post_create_questionnaire_api(BASE_URL,CREATE_QUESTIONNAIRE_DATA, ACCESS_TOKEN,CONTENT_TYPE_APPLICATION_JSON)
print(status, response_json, "trace_score_out")


#
#
# def input_url1():
#    input = ASYNC_URL
#    return input
#
@pytest.fixture
def input_url2():
   input = BASE_URL
   return input
# #
@pytest.fixture()
def get_token():
    status_code, json_data = API_Calls.token_api(BASE_URL, VALID_TOKEN_DATA, BASE_TOKEN, CONTENT_TYPE_URL_ENCODED)
    ACCESS_TOKEN = json_data['access_token']
    return  ACCESS_TOKEN
#
#
# @pytest.fixture
# def input_data():
#    input = CREATE_QUESTIONNAIRE_DATA
#    return input
#
# @pytest.fixture
# def get_header():
#    content_type = CONTENT_TYPE_APPLICATION_JSON
#    return content_type



# ------------------------------------------- Test Cases --------------------------------------------------------- #


# def generate_questionnaire_raw_data(q_data):
#      q_data['questions'][0]['type'] = Q_TYPE
#      q_data['questions'][0]['text'] = Q_TEXT
#      q_data['questions'][0]['isSkippable'] = False
#      q_data['questions'][0]['options'][0]['text'] = OTEXT1
#      q_data['questions'][0]['options'][0]['text'] = OSCORE1
#      return q_data



def test_post_create_questionnaire_api_201():
    D_CP = CREATE_QUESTIONNAIRE_DATA.copy()
    ques_title = helper.random_title()
    time.sleep(3)
    DATA = helper.update_dictionary(D_CP, title=ques_title)
    status, data = API_Calls.post_create_questionnaire_api(BASE_URL, DATA, ACCESS_TOKEN, CONTENT_TYPE_APPLICATION_JSON)
    assert status == 201
    print(status, data)
    assertion.assert_valid_schema(data, 'create_ques.json')


def test_post_create_questionnaire_api_201_access_token_with_bearer():
    ACCESS_TOKEN_BEARER = 'Bearer ' + ACCESS_TOKEN
    print(ACCESS_TOKEN_BEARER)
    D_CP = CREATE_QUESTIONNAIRE_DATA.copy()
    ques_title = helper.random_title()
    time.sleep(3)
    DATA = helper.update_dictionary(D_CP, title=ques_title)
    status, data = API_Calls.post_create_questionnaire_api(BASE_URL, DATA, ACCESS_TOKEN_BEARER, CONTENT_TYPE_APPLICATION_JSON)
    assert status == 201
    print(status, data)
    assertion.assert_valid_schema(data, 'create_ques.json')


time.sleep(10)

def test_post_create_questionnaire_api_200():
   status, data = API_Calls.post_create_questionnaire_api(BASE_URL, CREATE_QUESTIONNAIRE_DATA, ACCESS_TOKEN, CONTENT_TYPE_APPLICATION_JSON)
   assert status == 200
   print(status, data)
   assertion.assert_valid_schema(data, 'create_ques.json')


def test_post_create_questionnaire_api_request_body_language_in_lower_case():
    D_CP = CREATE_QUESTIONNAIRE_DATA.copy()
    ques_title = helper.random_title()
    time.sleep(3)
    DATA = helper.update_dictionary(D_CP, title=ques_title,language ='en')
    #D_CP = CREATE_QUESTIONNAIRE_DATA.copy()
    #DATA = helper.update_dictionary(D_CP,language='en')
    #DATA = {'questions':D}
    status, data = API_Calls.post_create_questionnaire_api(BASE_URL, DATA, ACCESS_TOKEN,CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 201

def test_post_create_questionnaire_api_request_body_language_in_upper_case():
    D_CP = CREATE_QUESTIONNAIRE_DATA.copy()
    ques_title = helper.random_title()
    time.sleep(3)
    DATA = helper.update_dictionary(D_CP, title=ques_title)
    D_CP1 = DATA.copy()
    DATA1 = helper.update_dictionary(D_CP1,language='EN')

    #DATA = {'questions':D}
    status, data = API_Calls.post_create_questionnaire_api(BASE_URL, DATA1, ACCESS_TOKEN,CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 400


def test_post_create_questionnaire_api_request_body_title_which_is_already_present():
    D_CP = CREATE_QUESTIONNAIRE_DATA.copy()
    DATA = helper.update_dictionary(D_CP,title='healthcheckapis_Q2_v4')
    #DATA = {'questions':D}
    status, data = API_Calls.post_create_questionnaire_api(BASE_URL, DATA, ACCESS_TOKEN,CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 200


def test_post_create_questionnaire_api_request_body_title_in_upper_case():
    D_CP = CREATE_QUESTIONNAIRE_DATA.copy()
    DATA = helper.update_dictionary(D_CP,title='HEALTHCHECKAPIS_Q2_V4_1')
    #DATA = {'questions':D}
    status, data = API_Calls.post_create_questionnaire_api(BASE_URL, DATA, ACCESS_TOKEN,CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 200



# def test_post_create_questionnaire_api_request_body_title_in_upper_case():
#     D_CP = CREATE_QUESTIONNAIRE_DATA['questions'].copy()
#     DATA = helper.update_dictionary(D_CP,type='multiple_choice')
#     #DATA = {'questions':D}
#     status, data = API_Calls.post_create_questionnaire_api(BASE_URL, DATA, ACCESS_TOKEN,CONTENT_TYPE_APPLICATION_JSON)
#     print(status, data)
#     assert status == 200
#
#
# def test_post_create_questionnaire_api_request_body_title_in_upper_case():
#     D_CP = CREATE_QUESTIONNAIRE_DATA.copy()
#     DATA = helper.update_dictionary(D_CP,title='HEALTHCHECKapiS_Q2_v4')
#     #DATA = {'questions':D}
#     status, data = API_Calls.post_create_questionnaire_api(BASE_URL, DATA, ACCESS_TOKEN,CONTENT_TYPE_APPLICATION_JSON)
#     print(status, data)
#     assert status == 200



def test_post_create_questionnaire_api_request_body_shuffle_sequence():
    D_CP = CREATE_QUESTIONNAIRE_DATA_SEQUENCE_SHUFFLE.copy()
    ques_title = helper.random_title()
    time.sleep(3)
    DATA = helper.update_dictionary(D_CP, title=ques_title, language='en')
    status, data = API_Calls.post_create_questionnaire_api(BASE_URL, DATA, ACCESS_TOKEN, CONTENT_TYPE_APPLICATION_JSON)
    assert status == 201
    print(status, data)
    assertion.assert_valid_schema(data, 'create_ques.json')


def test_post_create_questionnaire_api_request_same_questionnaire_in_hindi_language():
   status, data = API_Calls.post_create_questionnaire_api(BASE_URL, CREATE_QUESTIONNAIRE_DATA_HINDI_QUES_WITH_SAME_Q_IN_ENGLISH, ACCESS_TOKEN, CONTENT_TYPE_APPLICATION_JSON)
   assert status == 422
   print(status, data)
   #assertion.assert_valid_schema(data, 'create_ques.json')

def test_post_create_questionnaire_api_request_body_question_type_in_lower_case():

    CREATE_QUESTIONNAIRE_DATA1 = {
        "title": "covid_19",
        "language": "en",
        "questions": [
            {
                "type": "multiple_choice",
                "text": "Have you been within 6 feet of a person with a lab confirmed case of COVID-19 or with symptoms of COVID-19 for at least 15 minutes, or had direct contact with their mucus or saliva,in the past 14 days?",
                "isSkippable": False,
                "options": [
                    {
                        "text": "No",
                        "score": 0
                    },
                    {
                        "text": "Yes",
                        "score": 1
                    }
                ]
            },
            {
                "type": "MULTIPLE_SELECT",
                "text": "In the last 48 hours, have you had any of the following NEW symptoms? Select all that apply.",
                "isSkippable": False,
                "options": [
                    {
                        "text": "Fever of 100.4° F or above",
                        "score": 3
                    },
                    {
                        "text": "Cough",
                        "score": 2
                    },
                    {
                        "text": "Trouble breathing",
                        "score": 1
                    },
                    {
                        "text": "None of the above",
                        "score": 0
                    }
                ]
            },
            {
                "type": "TEXT_FIELD",
                "text": "How many covid center do you have in your city?",
                "isSkippable": True,
                "inputDataType": "INTEGER"
            },
            {
                "type": "TEXT_FIELD",
                "text": "What is your text temperature?",
                "isSkippable": True,
                "inputDataType": "BODY_TEMPERATURE"
            }
        ]
    }

    D_CP = CREATE_QUESTIONNAIRE_DATA1.copy()
    ques_title = helper.random_title()
    time.sleep(3)
    DATA = helper.update_dictionary(D_CP, title=ques_title)

    status, data = API_Calls.post_create_questionnaire_api(BASE_URL, DATA, ACCESS_TOKEN,CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 400

    # D_CP = QUESTIONNAIRE_BODY['questionnaire'].copy()
    # D = helper.update_dictionary(D_CP, language='Tamil')
    # DATA = {'questionnaire': D}
    # status, data = API_Calls.submit_questionnaire_response(BASE_URL, DATA, ACCESS_TOKEN)
    # print(status, data)
    # assert status == 404


########### --------------- Business Cases -----------------#############


def test_post_create_questionnaire_api_with_single_input_text_question():
    D_CP = CREATE_QUESTIONNAIRE_DATA_INPUT_TEXT1.copy()
    ques_title = helper.random_title()
    time.sleep(3)
    DATA = helper.update_dictionary(D_CP, title=ques_title)
    status, data = API_Calls.post_create_questionnaire_api(BASE_URL, DATA, ACCESS_TOKEN, CONTENT_TYPE_APPLICATION_JSON)
    assert status == 201
    print(status, data)



def test_post_create_questionnaire_api_with_two_input_text_questions():
    D_CP = CREATE_QUESTIONNAIRE_DATA_INPUT_TEXT2.copy()
    ques_title = helper.random_title()
    time.sleep(3)
    DATA = helper.update_dictionary(D_CP, title=ques_title)
    status, data = API_Calls.post_create_questionnaire_api(BASE_URL, DATA, ACCESS_TOKEN, CONTENT_TYPE_APPLICATION_JSON)
    assert status == 201
    print(status, data)


def test_post_create_questionnaire_api_with_single_input_text_question_having_input_datatype_as_float():
    D_CP = CREATE_QUESTIONNAIRE_DATA_INPUT_TEXT3.copy()
    ques_title = helper.random_title()
    time.sleep(3)
    DATA = helper.update_dictionary(D_CP, title=ques_title)
    status, data = API_Calls.post_create_questionnaire_api(BASE_URL, DATA, ACCESS_TOKEN, CONTENT_TYPE_APPLICATION_JSON)
    assert status == 201
    print(status, data)


def test_post_create_questionnaire_api_with_single_input_text_question_having_input_datatype_as_string():
    D_CP = CREATE_QUESTIONNAIRE_DATA_INPUT_TEXT4.copy()
    ques_title = helper.random_title()
    time.sleep(3)
    DATA = helper.update_dictionary(D_CP, title=ques_title)
    status, data = API_Calls.post_create_questionnaire_api(BASE_URL, DATA, ACCESS_TOKEN, CONTENT_TYPE_APPLICATION_JSON)
    assert status == 201
    print(status, data)


def test_post_create_questionnaire_api_with_max_length_of_question_set_to_1000():
    D_CP = CREATE_QUESTIONNAIRE_DATA_INPUT_TEXT5.copy()
    ques_title = helper.random_title()
    time.sleep(3)
    DATA = helper.update_dictionary(D_CP, title=ques_title)
    status, data = API_Calls.post_create_questionnaire_api(BASE_URL, DATA, ACCESS_TOKEN, CONTENT_TYPE_APPLICATION_JSON)
    assert status == 201
    print(status, data)


def test_post_create_questionnaire_api_with_max_length_of_question_set_to_beyond_1000():
    D_CP = CREATE_QUESTIONNAIRE_DATA_INPUT_TEXT6.copy()
    ques_title = helper.random_title()
    time.sleep(3)
    DATA = helper.update_dictionary(D_CP, title=ques_title)
    status, data = API_Calls.post_create_questionnaire_api(BASE_URL, DATA, ACCESS_TOKEN, CONTENT_TYPE_APPLICATION_JSON)
    assert status == 400
    print(status, data)



def test_post_create_questionnaire_api_with_max_length_of_option_set_to_beyond_1000():
    D_CP = CREATE_QUESTIONNAIRE_DATA_MULTISELECT3.copy()
    ques_title = helper.random_title()
    time.sleep(3)
    DATA = helper.update_dictionary(D_CP, title=ques_title)
    status, data = API_Calls.post_create_questionnaire_api(BASE_URL, DATA, ACCESS_TOKEN, CONTENT_TYPE_APPLICATION_JSON)
    assert status == 400
    print(status, data)


def test_post_create_questionnaire_api_with_single_multi_select_question():
    D_CP = CREATE_QUESTIONNAIRE_DATA_MULTISELECT1.copy()
    ques_title = helper.random_title()
    time.sleep(3)
    DATA = helper.update_dictionary(D_CP, title=ques_title)
    status, data = API_Calls.post_create_questionnaire_api(BASE_URL, DATA, ACCESS_TOKEN, CONTENT_TYPE_APPLICATION_JSON)
    assert status == 201
    print(status, data)


def test_post_create_questionnaire_api_with_two_multi_select_question():
    D_CP = CREATE_QUESTIONNAIRE_DATA_MULTISELECT2.copy()
    ques_title = helper.random_title()
    time.sleep(3)
    DATA = helper.update_dictionary(D_CP, title=ques_title)
    status, data = API_Calls.post_create_questionnaire_api(BASE_URL, DATA, ACCESS_TOKEN, CONTENT_TYPE_APPLICATION_JSON)
    assert status == 201
    print(status, data)


def test_post_create_questionnaire_api_with_single_multi_choice_question():
    D_CP = CREATE_QUESTIONNAIRE_DATA_MULTICHOICE1.copy()
    ques_title = helper.random_title()
    time.sleep(3)
    DATA = helper.update_dictionary(D_CP, title=ques_title)
    status, data = API_Calls.post_create_questionnaire_api(BASE_URL, DATA, ACCESS_TOKEN, CONTENT_TYPE_APPLICATION_JSON)
    assert status == 201
    print(status, data)


def test_post_create_questionnaire_api_with_two_multi_choice_question():
    D_CP = CREATE_QUESTIONNAIRE_DATA_MULTICHOICE2.copy()
    ques_title = helper.random_title()
    time.sleep(3)
    DATA = helper.update_dictionary(D_CP, title=ques_title)
    status, data = API_Calls.post_create_questionnaire_api(BASE_URL, DATA, ACCESS_TOKEN, CONTENT_TYPE_APPLICATION_JSON)
    assert status == 201
    print(status, data)



def test_post_create_questionnaire_api_with_multiple_select_multi_choice_question():
    D_CP = CREATE_QUESTIONNAIRE_DATA_MULTIPLE_SELECT_CHOICE.copy()
    ques_title = helper.random_title()
    time.sleep(3)
    DATA = helper.update_dictionary(D_CP, title=ques_title)
    status, data = API_Calls.post_create_questionnaire_api(BASE_URL, DATA, ACCESS_TOKEN, CONTENT_TYPE_APPLICATION_JSON)
    assert status == 201
    print(status, data)


def test_post_create_questionnaire_api_with_multi_choice_input_text_question():
    D_CP = CREATE_QUESTIONNAIRE_DATA_MULTIPLE_CHOICE_INPUT_TEXT.copy()
    ques_title = helper.random_title()
    time.sleep(3)
    DATA = helper.update_dictionary(D_CP, title=ques_title)
    status, data = API_Calls.post_create_questionnaire_api(BASE_URL, DATA, ACCESS_TOKEN, CONTENT_TYPE_APPLICATION_JSON)
    assert status == 201
    print(status, data)


def test_post_create_questionnaire_api_with_two_multi_select_input_text_question():
    D_CP = CREATE_QUESTIONNAIRE_DATA_MULTIPLE_SELECT_INPUT_TEXT.copy()
    ques_title = helper.random_title()
    time.sleep(3)
    DATA = helper.update_dictionary(D_CP, title=ques_title)
    status, data = API_Calls.post_create_questionnaire_api(BASE_URL, DATA, ACCESS_TOKEN, CONTENT_TYPE_APPLICATION_JSON)
    assert status == 201
    print(status, data)

def test_post_create_questionnaire_api_with_all_type_question():
    D_CP = CREATE_QUESTIONNAIRE_DATA_ALL_TYPE_Q.copy()
    ques_title = helper.random_title()
    time.sleep(3)
    DATA = helper.update_dictionary(D_CP, title=ques_title)
    status, data = API_Calls.post_create_questionnaire_api(BASE_URL, DATA, ACCESS_TOKEN, CONTENT_TYPE_APPLICATION_JSON)
    assert status == 201
    print(status, data)

def test_post_create_questionnaire_api_with_all_type_question_large_text_questions():
    D_CP = CREATE_QUESTIONNAIRE_DATA_ALL_LARGE_TEXT_QUESTIONS.copy()
    ques_title = helper.random_title()
    time.sleep(3)
    DATA = helper.update_dictionary(D_CP, title=ques_title)
    status, data = API_Calls.post_create_questionnaire_api(BASE_URL, DATA, ACCESS_TOKEN, CONTENT_TYPE_APPLICATION_JSON)
    assert status == 201
    print(status, data)


def test_post_create_questionnaire_api_with_all_type_question_large_text_options():
    D_CP = CREATE_QUESTIONNAIRE_DATA_ALL_LARGE_TEXT_QUESTIONS.copy()
    ques_title = helper.random_title()
    time.sleep(3)
    DATA = helper.update_dictionary(D_CP, title=ques_title)
    status, data = API_Calls.post_create_questionnaire_api(BASE_URL, DATA, ACCESS_TOKEN, CONTENT_TYPE_APPLICATION_JSON)
    assert status == 201
    print(status, data)


def test_post_create_questionnaire_api_with_all_type_questions_10():
    D_CP = CREATE_QUESTIONNAIRE_DATA_ALL_TYPE_Q_10.copy()
    ques_title = helper.random_title()
    time.sleep(3)
    DATA = helper.update_dictionary(D_CP, title=ques_title)
    status, data = API_Calls.post_create_questionnaire_api(BASE_URL, DATA, ACCESS_TOKEN, CONTENT_TYPE_APPLICATION_JSON)
    assert status == 201
    print(status, data)

def test_post_create_questionnaire_api_with_single_multi_choice_question_which_is_already_exist():
    D_CP = CREATE_QUESTIONNAIRE_DATA_MULTICHOICE1.copy()
    ques_title = helper.random_title()
    time.sleep(3)
    DATA = helper.update_dictionary(D_CP, title=ques_title)
    status, data = API_Calls.post_create_questionnaire_api(BASE_URL, DATA, ACCESS_TOKEN, CONTENT_TYPE_APPLICATION_JSON)
    assert status == 201
    print(status, data)


def test_post_create_questionnaire_api_with_single_multi_choice_question_which_is_already_exist_duplicate_questionnaire_same_client():
    D_CP = CREATE_QUESTIONNAIRE_DATA_MULTICHOICE1.copy()
    ques_title = helper.random_title()
    time.sleep(3)
    DATA = helper.update_dictionary(D_CP, title=ques_title)
    status, data = API_Calls.post_create_questionnaire_api(BASE_URL, DATA, ACCESS_TOKEN, CONTENT_TYPE_APPLICATION_JSON)
    assert status == 201
    print(status, data)


def test_post_create_questionnaire_api_with_same_title_by_different_partner():
    D_CP = CREATE_QUESTIONNAIRE_DATA_DIFF_PARTNER.copy()
    ques_title = helper.random_title()
    time.sleep(3)
    DATA = helper.update_dictionary(D_CP, title=ques_title)
    status, data = API_Calls.post_create_questionnaire_api(BASE_URL, DATA, ACCESS_TOKEN_19OCT1, CONTENT_TYPE_APPLICATION_JSON)
    assert status == 201
    print(status, data)


def test_post_create_questionnaire_api_partner_not_having_access_to_create_questionnaire():
    D_CP = CREATE_QUESTIONNAIRE_DATA_MULTICHOICE1.copy()
    ques_title = helper.random_title()
    time.sleep(3)
    DATA = helper.update_dictionary(D_CP, title=ques_title)
    status, data = API_Calls.post_create_questionnaire_api(BASE_URL, DATA, ACCESS_TOKEN_WQ, CONTENT_TYPE_APPLICATION_JSON)
    assert status == 401
    print(status, data)


def test_post_create_questionnaire_api_same_question_with_all_3_type_question_types():
    D_CP = CREATE_QUESTIONNAIRE_DATA_ALL_TYPE_Q_SINGLE_Q.copy()
    ques_title = helper.random_title()
    time.sleep(3)
    DATA = helper.update_dictionary(D_CP, title=ques_title)
    status, data = API_Calls.post_create_questionnaire_api(BASE_URL, DATA, ACCESS_TOKEN, CONTENT_TYPE_APPLICATION_JSON)
    assert status == 201
    print(status, data)




def test_whether_ques_created_by_live_client_is_accessible_by_test_client():

    #login with token
    status_code, json_data = API_Calls.token_api(BASE_URL, VALID_TOKEN_DATA, BASE_TOKEN, CONTENT_TYPE_URL_ENCODED)
    print("token api result:",status_code)
    #assert status_code == 200
    ACCESS_TOKEN = json_data['access_token']

    # #create subject
    # status, subject_json = API_Calls.subject_api(BASE_URL, VALID_SUBJECT_DATA, ACCESS_TOKEN,CONTENT_TYPE_APPLICATION_JSON)
    # print("subject api result:",status, subject_json )
    # SUB_IDENTIFIER1 = subject_json['userIdentifier']

    D_CP = CREATE_QUESTIONNAIRE_DATA.copy()
    ques_title = helper.random_title()
    time.sleep(3)
    DATA = helper.update_dictionary(D_CP, title=ques_title)
    status,createq_json = API_Calls.post_create_questionnaire_api(BASE_URL, DATA, ACCESS_TOKEN,CONTENT_TYPE_APPLICATION_JSON)
    print("create questionnaire api result:", status, createq_json)
    Q_ID=createq_json['id']
    Q_LANGUAGE=createq_json['language']

    time.sleep(10)

    status,getq_json=API_Calls.get_questionnaire_required_for_measure(BASE_URL,ACCESS_TOKEN_TEST,Q_LANGUAGE,Q_ID)
    assert status==401



def test_whether_ques_created_by_partner1_is_not_accessible_by_partner2():

    #login with token
    status_code, json_data = API_Calls.token_api(BASE_URL, VALID_TOKEN_DATA, BASE_TOKEN, CONTENT_TYPE_URL_ENCODED)
    print("token api result:",status_code)
    #assert status_code == 200
    ACCESS_TOKEN = json_data['access_token']

    #create subject
    # status, subject_json = API_Calls.subject_api(BASE_URL, VALID_SUBJECT_DATA, ACCESS_TOKEN,CONTENT_TYPE_APPLICATION_JSON)
    # print("subject api result:",status, subject_json )
    # SUB_IDENTIFIER1 = subject_json['userIdentifier']
    D_CP = CREATE_QUESTIONNAIRE_DATA.copy()
    ques_title = helper.random_title()
    time.sleep(3)
    DATA = helper.update_dictionary(D_CP, title=ques_title)
    status,createq_json = API_Calls.post_create_questionnaire_api(BASE_URL,DATA,ACCESS_TOKEN,CONTENT_TYPE_APPLICATION_JSON)
    print("create questionnaire api result:", status, createq_json)
    Q_ID=createq_json['id']
    Q_LANGUAGE=createq_json['language']

    time.sleep(10)

    status,getq_json=API_Calls.get_questionnaire_required_for_measure(BASE_URL,Q_ID,Q_LANGUAGE,ACCESS_TOKEN_TEST)
    print("get questionnaire result:",status,getq_json)
    assert status==403




def test_E2E_use_case_flow():

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

    status,createq_json = API_Calls.post_create_questionnaire_api(BASE_URL,DATA,ACCESS_TOKEN,CONTENT_TYPE_APPLICATION_JSON)
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
    print("get questionnaire api result:", status, submit_q_response_json)
    assert status == 201



#--------- Negative Cases --------#
def test_post_create_questionnaire_api_request_contains_no_body():
    status, data = API_Calls.post_create_questionnaire_api(BASE_URL, CREATE_QUESTIONNAIRE_DATA_NO_BODY, ACCESS_TOKEN,
                                                           CONTENT_TYPE_APPLICATION_JSON)
    assert status == 400


def test_post_create_questionnaire_invalid_end_point():
    headers1 = {'Authorization': ACCESS_TOKEN, 'Content-Type': CONTENT_TYPE_APPLICATION_JSON}
    INVALID_END_POINT = '/XYZ'
    res = requests.post(url=BASE_URL + INVALID_END_POINT, data=json.dumps(CREATE_QUESTIONNAIRE_DATA), headers=headers1)
    print(res)
    assert res.status_code == 403


def test_post_create_questionnaire_api_incorrect_ACCESS_TOKEN():
    INCORRECT_ACCESS_TOKEN = 'xyz'
    status, data = API_Calls.post_create_questionnaire_api(BASE_URL, CREATE_QUESTIONNAIRE_DATA, INCORRECT_ACCESS_TOKEN,CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 401


def test_post_create_questionnaire_api_expired_access_token():
    status, data = API_Calls.post_create_questionnaire_api(BASE_URL, CREATE_QUESTIONNAIRE_DATA, EXPIRED_ACCESS_TOKEN,CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 401

def test_post_create_questionnaire_api_access_token_with_bearer_in_small_case():
    ACCESS_TOKEN_BEARER1 = 'bearer ' + ACCESS_TOKEN
    print(ACCESS_TOKEN_BEARER1)
    status, data = API_Calls.post_create_questionnaire_api(BASE_URL, CREATE_QUESTIONNAIRE_DATA,
                                                               ACCESS_TOKEN_BEARER1, CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 401

    # ACCESS DENIED


def test_post_create_questionnaire_api_missing_authorization():
    headers = {'Content-Type': CONTENT_TYPE_APPLICATION_JSON}
    res = requests.post(url=BASE_URL + CREATE_QUESTIONNAIRE_ENDPOINT, data=json.dumps(CREATE_QUESTIONNAIRE_DATA), headers=headers)
    print(res)
    assert res.status_code == 401


def test_post_create_questionnaire_api_blank_access_token():
    headers = {'Authorization': '', 'Content-Type': CONTENT_TYPE_APPLICATION_JSON}
    res = requests.post(url=BASE_URL + CREATE_QUESTIONNAIRE_ENDPOINT, data=json.dumps(CREATE_QUESTIONNAIRE_DATA), headers=headers)
    print(res)
    assert res.status_code == 401



def test_post_create_questionnaire_api_incorrect_content_type():
    status, data = API_Calls.post_create_questionnaire_api(BASE_URL, CREATE_QUESTIONNAIRE_DATA, ACCESS_TOKEN,CONTENT_TYPE_URL_ENCODED)
    print(status, data)
    assert status == 415

def test_post_create_questionnaire_api_request_body_title_blank():
    D_CP = CREATE_QUESTIONNAIRE_DATA.copy()
    DATA = helper.update_dictionary(D_CP, title='')
    status, data = API_Calls.post_create_questionnaire_api(BASE_URL, DATA, ACCESS_TOKEN,CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 400

def test_post_create_questionnaire_api_request_body_language_blank():
    D_CP = CREATE_QUESTIONNAIRE_DATA.copy()
    DATA = helper.update_dictionary(D_CP, language='')
    status, data = API_Calls.post_create_questionnaire_api(BASE_URL, DATA, ACCESS_TOKEN,CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 400

def test_post_create_questionnaire_api_request_body_questions_blank():
    D_CP = CREATE_QUESTIONNAIRE_DATA.copy()
    DATA = helper.update_dictionary(D_CP, questions='')
    status, data = API_Calls.post_create_questionnaire_api(BASE_URL, DATA, ACCESS_TOKEN,CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 400


def test_post_create_questionnaire_api_request_body_type_blank():
    CREATE_QUESTIONNAIRE_DATA_REQUEST_BODY_TYPE_BLANK = {
        "title": "covid_19",
        "language": "en",
        "questions": [
            {
                "type": " ",
                "text": "Have you been within 6 feet of a person with a lab confirmed case of COVID-19 or with symptoms of COVID-19 for at least 15 minutes, or had direct contact with their mucus or saliva,in the past 14 days?",
                "isSkippable": False,
                "options": [
                    {
                        "text": "No",
                        "score": 0
                    },
                    {
                        "text": "Yes",
                        "score": 1
                    }
                ]
            },
            {
                "type": "MULTIPLE_SELECT",
                "text": "In the last 48 hours, have you had any of the following NEW symptoms? Select all that apply.",
                "isSkippable": False,
                "options": [
                    {
                        "text": "Fever of 100.4° F or above",
                        "score": 3
                    },
                    {
                        "text": "Cough",
                        "score": 2
                    },
                    {
                        "text": "Trouble breathing",
                        "score": 1
                    },
                    {
                        "text": "None of the above",
                        "score": 0
                    }
                ]
            },
            {
                "type": "TEXT_FIELD",
                "text": "How many covid center do you have in your city?",
                "isSkippable": True,
                "inputDataType": "INTEGER"
            },
            {
                "type": "TEXT_FIELD",
                "text": "What is your text temperature?",
                "isSkippable": True,
                "inputDataType": "BODY_TEMPERATURE"
            }
        ]
    }


    status, data = API_Calls.post_create_questionnaire_api(BASE_URL, CREATE_QUESTIONNAIRE_DATA_REQUEST_BODY_TYPE_BLANK, ACCESS_TOKEN,CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 400


def test_post_create_questionnaire_api_request_body_text_blank():
    CREATE_QUESTIONNAIRE_DATA_REQUEST_BODY_TEXT_BLANK = {
        "title": "covid_19",
        "language": "en",
        "questions": [
            {
                "type": "MULTIPLE_CHOICE ",
                "text": "",
                "isSkippable": False,
                "options": [
                    {
                        "text": "No",
                        "score": 0
                    },
                    {
                        "text": "Yes",
                        "score": 1
                    }
                ]
            },
            {
                "type": "MULTIPLE_SELECT",
                "text": "In the last 48 hours, have you had any of the following NEW symptoms? Select all that apply.",
                "isSkippable": False,
                "options": [
                    {
                        "text": "Fever of 100.4° F or above",
                        "score": 3
                    },
                    {
                        "text": "Cough",
                        "score": 2
                    },
                    {
                        "text": "Trouble breathing",
                        "score": 1
                    },
                    {
                        "text": "None of the above",
                        "score": 0
                    }
                ]
            },
            {
                "type": "TEXT_FIELD",
                "text": "How many covid center do you have in your city?",
                "isSkippable": True,
                "inputDataType": "INTEGER"
            },
            {
                "type": "TEXT_FIELD",
                "text": "What is your text temperature?",
                "isSkippable": True,
                "inputDataType": "BODY_TEMPERATURE"
            }
        ]
    }
    status, data = API_Calls.post_create_questionnaire_api(BASE_URL, CREATE_QUESTIONNAIRE_DATA_REQUEST_BODY_TEXT_BLANK, ACCESS_TOKEN,CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 400


def test_post_create_questionnaire_api_request_body_isskippable_blank():
    CREATE_QUESTIONNAIRE_DATA_REQUEST_BODY_SKIPPABLE_BLANK = {
        "title": "covid_19",
        "language": "en",
        "questions": [
            {
                "type": "MULTIPLE_CHOICE ",
                "text": "Have you been within 6 feet of a person with a lab confirmed case of COVID-19 or with symptoms of COVID-19 for at least 15 minutes, or had direct contact with their mucus or saliva,in the past 14 days?",
                "isSkippable":'' ,
                "options": [
                    {
                        "text": "No",
                        "score": 0
                    },
                    {
                        "text": "Yes",
                        "score": 1
                    }
                ]
            },
            {
                "type": "MULTIPLE_SELECT",
                "text": "In the last 48 hours, have you had any of the following NEW symptoms? Select all that apply.",
                "isSkippable": False,
                "options": [
                    {
                        "text": "Fever of 100.4° F or above",
                        "score": 3
                    },
                    {
                        "text": "Cough",
                        "score": 2
                    },
                    {
                        "text": "Trouble breathing",
                        "score": 1
                    },
                    {
                        "text": "None of the above",
                        "score": 0
                    }
                ]
            },
            {
                "type": "TEXT_FIELD",
                "text": "How many covid center do you have in your city?",
                "isSkippable": True,
                "inputDataType": "INTEGER"
            },
            {
                "type": "TEXT_FIELD",
                "text": "What is your text temperature?",
                "isSkippable": True,
                "inputDataType": "BODY_TEMPERATURE"
            }
        ]
    }

    status, data = API_Calls.post_create_questionnaire_api(BASE_URL, CREATE_QUESTIONNAIRE_DATA_REQUEST_BODY_SKIPPABLE_BLANK, ACCESS_TOKEN,CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 400


def test_post_create_questionnaire_api_request_body_option_array_blank():
    CREATE_QUESTIONNAIRE_DATA_REQUEST_BODY_OPTION_ARRAY_BLANK = {
        "title": "covid_19",
        "language": "en",
        "questions": [
            {
                "type": "MULTIPLE_CHOICE ",
                "text": "Have you been within 6 feet of a person with a lab confirmed case of COVID-19 or with symptoms of COVID-19 for at least 15 minutes, or had direct contact with their mucus or saliva,in the past 14 days?",
                "isSkippable": False,
                "options": [

                ]
            },
            {
                "type": "MULTIPLE_SELECT",
                "text": "In the last 48 hours, have you had any of the following NEW symptoms? Select all that apply.",
                "isSkippable": False,
                "options": [
                    {
                        "text": "Fever of 100.4° F or above",
                        "score": 3
                    },
                    {
                        "text": "Cough",
                        "score": 2
                    },
                    {
                        "text": "Trouble breathing",
                        "score": 1
                    },
                    {
                        "text": "None of the above",
                        "score": 0
                    }
                ]
            },
            {
                "type": "TEXT_FIELD",
                "text": "How many covid center do you have in your city?",
                "isSkippable": True,
                "inputDataType": "INTEGER"
            },
            {
                "type": "TEXT_FIELD",
                "text": "What is your text temperature?",
                "isSkippable": True,
                "inputDataType": "BODY_TEMPERATURE"
            }
        ]
    }

    status, data = API_Calls.post_create_questionnaire_api(BASE_URL, CREATE_QUESTIONNAIRE_DATA_REQUEST_BODY_OPTION_ARRAY_BLANK, ACCESS_TOKEN,CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 400



def test_post_create_questionnaire_api_request_body_options_text_blank():
    CREATE_QUESTIONNAIRE_DATA_REQUEST_BODY_OPTIONS_TEXT_BLANK = {
        "title": "covid_19",
        "language": "en",
        "questions": [
            {
                "type": "MULTIPLE_CHOICE ",
                "text": "Have you been within 6 feet of a person with a lab confirmed case of COVID-19 or with symptoms of COVID-19 for at least 15 minutes, or had direct contact with their mucus or saliva,in the past 14 days?",
                "isSkippable": False,
                "options": [
                    {
                        "text": " ",
                        "score": 0
                    },
                    {
                        "text": "Yes",
                        "score": 1
                    }
                ]
            },
            {
                "type": "MULTIPLE_SELECT",
                "text": "In the last 48 hours, have you had any of the following NEW symptoms? Select all that apply.",
                "isSkippable": False,
                "options": [
                    {
                        "text": "Fever of 100.4° F or above",
                        "score": 3
                    },
                    {
                        "text": "Cough",
                        "score": 2
                    },
                    {
                        "text": "Trouble breathing",
                        "score": 1
                    },
                    {
                        "text": "None of the above",
                        "score": 0
                    }
                ]
            },
            {
                "type": "TEXT_FIELD",
                "text": "How many covid center do you have in your city?",
                "isSkippable": True,
                "inputDataType": "INTEGER"
            },
            {
                "type": "TEXT_FIELD",
                "text": "What is your text temperature?",
                "isSkippable": True,
                "inputDataType": "BODY_TEMPERATURE"
            }
        ]
    }

    status, data = API_Calls.post_create_questionnaire_api(BASE_URL, CREATE_QUESTIONNAIRE_DATA_REQUEST_BODY_OPTIONS_TEXT_BLANK, ACCESS_TOKEN,CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 400


def test_post_create_questionnaire_api_request_body_options_score_blank():
    CREATE_QUESTIONNAIRE_DATA_REQUEST_BODY_OPTIONS_SCORE_BLANK = {
        "title": "covid_19",
        "language": "en",
        "questions": [
            {
                "type": "MULTIPLE_CHOICE ",
                "text": "Have you been within 6 feet of a person with a lab confirmed case of COVID-19 or with symptoms of COVID-19 for at least 15 minutes, or had direct contact with their mucus or saliva,in the past 14 days?",
                "isSkippable": False,
                "options": [
                    {
                        "text": "No",

                    },
                    {
                        "text": "Yes",
                        "score": 1
                    }
                ]
            },
            {
                "type": "MULTIPLE_SELECT",
                "text": "In the last 48 hours, have you had any of the following NEW symptoms? Select all that apply.",
                "isSkippable": False,
                "options": [
                    {
                        "text": "Fever of 100.4° F or above",
                        "score": 3
                    },
                    {
                        "text": "Cough",
                        "score": 2
                    },
                    {
                        "text": "Trouble breathing",
                        "score": 1
                    },
                    {
                        "text": "None of the above",
                        "score": 0
                    }
                ]
            },
            {
                "type": "TEXT_FIELD",
                "text": "How many covid center do you have in your city?",
                "isSkippable": True,
                "inputDataType": "INTEGER"
            },
            {
                "type": "TEXT_FIELD",
                "text": "What is your text temperature?",
                "isSkippable": True,
                "inputDataType": "BODY_TEMPERATURE"
            }
        ]
    }

    status, data = API_Calls.post_create_questionnaire_api(BASE_URL, CREATE_QUESTIONNAIRE_DATA_REQUEST_BODY_OPTIONS_SCORE_BLANK, ACCESS_TOKEN,CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 400


def test_post_create_questionnaire_api_request_body_inputDataType_blank():
    CREATE_QUESTIONNAIRE_DATA_REQUEST_BODY_INPUT_DATA_TYPE_BLANK = {
        "title": "covid_19",
        "language": "en",
        "questions": [
            {
                "type": "MULTIPLE_CHOICE",
                "text": "Have you been within 6 feet of a person with a lab confirmed case of COVID-19 or with symptoms of COVID-19 for at least 15 minutes, or had direct contact with their mucus or saliva,in the past 14 days?",
                "isSkippable": False,
                "options": [
                    {
                        "text": "No",
                        "score": 0
                    },
                    {
                        "text": "Yes",
                        "score": 1
                    }
                ]
            },
            {
                "type": "MULTIPLE_SELECT",
                "text": "In the last 48 hours, have you had any of the following NEW symptoms? Select all that apply.",
                "isSkippable": False,
                "options": [
                    {
                        "text": "Fever of 100.4° F or above",
                        "score": 3
                    },
                    {
                        "text": "Cough",
                        "score": 2
                    },
                    {
                        "text": "Trouble breathing",
                        "score": 1
                    },
                    {
                        "text": "None of the above",
                        "score": 0
                    }
                ]
            },
            {
                "type": "TEXT_FIELD",
                "text": "How many covid center do you have in your city?",
                "isSkippable": True,
                "inputDataType": "INTEGER"
            },
            {
                "type": "TEXT_FIELD",
                "text": "What is your text temperature?",
                "isSkippable": True,
                "inputDataType": " "
            }
        ]
    }
    status, data = API_Calls.post_create_questionnaire_api(BASE_URL, CREATE_QUESTIONNAIRE_DATA_REQUEST_BODY_INPUT_DATA_TYPE_BLANK, ACCESS_TOKEN,CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 400



def test_post_create_questionnaire_api_request_body_title_input_as_integer():
    D_CP = CREATE_QUESTIONNAIRE_DATA.copy()
    DATA = helper.update_dictionary(D_CP,title=123)
   # DATA = {'questions':D}
    status, data = API_Calls.post_create_questionnaire_api(BASE_URL, DATA, ACCESS_TOKEN,CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 400


def test_post_create_questionnaire_api_request_body_language_input_as_integer():
    D_CP = CREATE_QUESTIONNAIRE_DATA.copy()
    DATA = helper.update_dictionary(D_CP,langugae=123)
    #DATA = {'questions':D}
    status, data = API_Calls.post_create_questionnaire_api(BASE_URL, DATA, ACCESS_TOKEN,CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 400


def test_post_create_questionnaire_api_request_body_not_suported_language():
    D_CP = CREATE_QUESTIONNAIRE_DATA.copy()
    DATA = helper.update_dictionary(D_CP,langugae='ma')
    #DATA = {'questions':D}
    status, data = API_Calls.post_create_questionnaire_api(BASE_URL, DATA, ACCESS_TOKEN,CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 400


def test_post_create_questionnaire_api_request_body_questions_type_as_integer():
    CREATE_QUESTIONNAIRE_DATA_REQUEST_BODY_QUESTION_TYPE_BLANK = {
        "title": "covid_19",
        "language": "en",
        "questions": [
            {
                "type": 1,
                "text": "Have you been within 6 feet of a person with a lab confirmed case of COVID-19 or with symptoms of COVID-19 for at least 15 minutes, or had direct contact with their mucus or saliva,in the past 14 days?",
                "isSkippable": False,
                "options": [
                    {
                        "text": "No",
                        "score": 0
                    },
                    {
                        "text": "Yes",
                        "score": 1
                    }
                ]
            },
            {
                "type": "MULTIPLE_SELECT",
                "text": "In the last 48 hours, have you had any of the following NEW symptoms? Select all that apply.",
                "isSkippable": False,
                "options": [
                    {
                        "text": "Fever of 100.4° F or above",
                        "score": 3
                    },
                    {
                        "text": "Cough",
                        "score": 2
                    },
                    {
                        "text": "Trouble breathing",
                        "score": 1
                    },
                    {
                        "text": "None of the above",
                        "score": 0
                    }
                ]
            },
            {
                "type": "TEXT_FIELD",
                "text": "How many covid center do you have in your city?",
                "isSkippable": True,
                "inputDataType": "INTEGER"
            },
            {
                "type": "TEXT_FIELD",
                "text": "What is your text temperature?",
                "isSkippable": True,
                "inputDataType": "BODY_TEMPERATURE"
            }
        ]
    }
    status, data = API_Calls.post_create_questionnaire_api(BASE_URL, CREATE_QUESTIONNAIRE_DATA_REQUEST_BODY_QUESTION_TYPE_BLANK, ACCESS_TOKEN,CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 400



def test_post_create_questionnaire_api_request_body_questions_type_other_than_multi_choice_multi_select_text_field():
    CREATE_QUESTIONNAIRE_DATA_REQUEST_BODY_TYPE_DIFF = {
        "title": "covid_19",
        "language": "en",
        "questions": [
            {
                "type": "MULTIPLE_CHOICE1",
                "text": "Have you been within 6 feet of a person with a lab confirmed case of COVID-19 or with symptoms of COVID-19 for at least 15 minutes, or had direct contact with their mucus or saliva,in the past 14 days?",
                "isSkippable": False,
                "options": [
                    {
                        "text": "No",
                        "score": 0
                    },
                    {
                        "text": "Yes",
                        "score": 1
                    }
                ]
            },
            {
                "type": "MULTIPLE_SELECT",
                "text": "In the last 48 hours, have you had any of the following NEW symptoms? Select all that apply.",
                "isSkippable": False,
                "options": [
                    {
                        "text": "Fever of 100.4° F or above",
                        "score": 3
                    },
                    {
                        "text": "Cough",
                        "score": 2
                    },
                    {
                        "text": "Trouble breathing",
                        "score": 1
                    },
                    {
                        "text": "None of the above",
                        "score": 0
                    }
                ]
            },
            {
                "type": "TEXT_FIELD",
                "text": "How many covid center do you have in your city?",
                "isSkippable": True,
                "inputDataType": "INTEGER"
            },
            {
                "type": "TEXT_FIELD",
                "text": "What is your text temperature?",
                "isSkippable": True,
                "inputDataType": "BODY_TEMPERATURE"
            }
        ]
    }
    status, data = API_Calls.post_create_questionnaire_api(BASE_URL, CREATE_QUESTIONNAIRE_DATA_REQUEST_BODY_TYPE_DIFF, ACCESS_TOKEN,CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 400

#
# def test_post_create_questionnaire_api_request_body_questions_type_other_than_multi_choice_multi_select_text_field():
#     D_CP = CREATE_QUESTIONNAIRE_DATA['QUESTIONS'].copy()
#     D = helper.update_dictionary(D_CP,type='abc')
#     DATA = {'questions':D}
#     status, data = API_Calls.post_create_questionnaire_api(BASE_URL, DATA, ACCESS_TOKEN,CONTENT_TYPE_APPLICATION_JSON)
#     print(status, data)
#     assert status == 400

def test_post_create_questionnaire_api_request_body_questions_type_multi_choice_has_spell_mistake():
    CREATE_QUESTIONNAIRE_DATA_REQUEST_BODY_TYPE_HAS_SPELL_MISTAKE= {
        "title": "covid_19",
        "language": "en",
        "questions": [
            {
                "type": "MULTIPLE_CHOOICE",
                "text": "Have you been within 6 feet of a person with a lab confirmed case of COVID-19 or with symptoms of COVID-19 for at least 15 minutes, or had direct contact with their mucus or saliva,in the past 14 days?",
                "isSkippable": False,
                "options": [
                    {
                        "text": "No",
                        "score": 0
                    },
                    {
                        "text": "Yes",
                        "score": 1
                    }
                ]
            },
            {
                "type": "MULTIPLE_SELECT",
                "text": "In the last 48 hours, have you had any of the following NEW symptoms? Select all that apply.",
                "isSkippable": False,
                "options": [
                    {
                        "text": "Fever of 100.4° F or above",
                        "score": 3
                    },
                    {
                        "text": "Cough",
                        "score": 2
                    },
                    {
                        "text": "Trouble breathing",
                        "score": 1
                    },
                    {
                        "text": "None of the above",
                        "score": 0
                    }
                ]
            },
            {
                "type": "TEXT_FIELD",
                "text": "How many covid center do you have in your city?",
                "isSkippable": True,
                "inputDataType": "INTEGER"
            },
            {
                "type": "TEXT_FIELD",
                "text": "What is your text temperature?",
                "isSkippable": True,
                "inputDataType": "BODY_TEMPERATURE"
            }
        ]
    }
    status, data = API_Calls.post_create_questionnaire_api(BASE_URL, CREATE_QUESTIONNAIRE_DATA_REQUEST_BODY_TYPE_HAS_SPELL_MISTAKE, ACCESS_TOKEN,CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 400




def test_post_create_questionnaire_api_request_body_questions_text_as_integer():
    CREATE_QUESTIONNAIRE_DATA_REQUEST_BODY_QUESTIONS_TEXT_AS_INTEGER = {
        "title": "covid_19",
        "language": "en",
        "questions": [
            {
                "type": "MULTIPLE_CHOICE",
                "text": 1,
                "isSkippable": False,
                "options": [
                    {
                        "text": "No",
                        "score": 0
                    },
                    {
                        "text": "Yes",
                        "score": 1
                    }
                ]
            },
            {
                "type": "MULTIPLE_SELECT",
                "text": "In the last 48 hours, have you had any of the following NEW symptoms? Select all that apply.",
                "isSkippable": False,
                "options": [
                    {
                        "text": "Fever of 100.4° F or above",
                        "score": 3
                    },
                    {
                        "text": "Cough",
                        "score": 2
                    },
                    {
                        "text": "Trouble breathing",
                        "score": 1
                    },
                    {
                        "text": "None of the above",
                        "score": 0
                    }
                ]
            },
            {
                "type": "TEXT_FIELD",
                "text": "How many covid center do you have in your city?",
                "isSkippable": True,
                "inputDataType": "INTEGER"
            },
            {
                "type": "TEXT_FIELD",
                "text": "What is your text temperature?",
                "isSkippable": True,
                "inputDataType": "BODY_TEMPERATURE"
            }
        ]
    }
    status, data = API_Calls.post_create_questionnaire_api(BASE_URL, CREATE_QUESTIONNAIRE_DATA_REQUEST_BODY_QUESTIONS_TEXT_AS_INTEGER, ACCESS_TOKEN,CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 400



def test_post_create_questionnaire_api_request_body_questions_text_which_exceeds_max_length_limit():
    D_CP = CREATE_QUESTIONNAIRE_DATA_TEXT_1001.copy()
    ques_title = helper.random_title()
    time.sleep(3)
    DATA = helper.update_dictionary(D_CP, title=ques_title)

    status, data = API_Calls.post_create_questionnaire_api(BASE_URL, DATA, ACCESS_TOKEN, CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 400



def test_post_create_questionnaire_api_request_body_isskippable_other_than_true_or_false():
    CREATE_QUESTIONNAIRE_DATA_REQUEST_ISSKIPPABLE_OTHER_THAN_TRUE_OR_FALSE = {
        "title": "covid_19",
        "language": "en",
        "questions": [
            {
                "type": "MULTIPLE_CHOICE",
                "text": "Have you been within 6 feet of a person with a lab confirmed case of COVID-19 or with symptoms of COVID-19 for at least 15 minutes, or had direct contact with their mucus or saliva,in the past 14 days?",
                "isSkippable": "string",
                "options": [
                    {
                        "text": "No",
                        "score": 0
                    },
                    {
                        "text": "Yes",
                        "score": 1
                    }
                ]
            },
            {
                "type": "MULTIPLE_SELECT",
                "text": "In the last 48 hours, have you had any of the following NEW symptoms? Select all that apply.",
                "isSkippable": False,
                "options": [
                    {
                        "text": "Fever of 100.4° F or above",
                        "score": 3
                    },
                    {
                        "text": "Cough",
                        "score": 2
                    },
                    {
                        "text": "Trouble breathing",
                        "score": 1
                    },
                    {
                        "text": "None of the above",
                        "score": 0
                    }
                ]
            },
            {
                "type": "TEXT_FIELD",
                "text": "How many covid center do you have in your city?",
                "isSkippable": True,
                "inputDataType": "INTEGER"
            },
            {
                "type": "TEXT_FIELD",
                "text": "What is your text temperature?",
                "isSkippable": True,
                "inputDataType": "BODY_TEMPERATURE"
            }
        ]
    }
    status, data = API_Calls.post_create_questionnaire_api(BASE_URL, CREATE_QUESTIONNAIRE_DATA_REQUEST_ISSKIPPABLE_OTHER_THAN_TRUE_OR_FALSE, ACCESS_TOKEN,CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 400


def test_post_create_questionnaire_api_request_body_isskippable_value_as_integer():
    CREATE_QUESTIONNAIRE_DATA_REQUEST_BODY_ISSKIPPABLE_VALUE_AS_INTEGER = {
        "title": "covid_19",
        "language": "en",
        "questions": [
            {
                "type": "MULTIPLE_CHOICE",
                "text": "Have you been within 6 feet of a person with a lab confirmed case of COVID-19 or with symptoms of COVID-19 for at least 15 minutes, or had direct contact with their mucus or saliva,in the past 14 days?",
                "isSkippable": 3,
                "options": [
                    {
                        "text": "No",
                        "score": 0
                    },
                    {
                        "text": "Yes",
                        "score": 1
                    }
                ]
            },
            {
                "type": "MULTIPLE_SELECT",
                "text": "In the last 48 hours, have you had any of the following NEW symptoms? Select all that apply.",
                "isSkippable": False,
                "options": [
                    {
                        "text": "Fever of 100.4° F or above",
                        "score": 3
                    },
                    {
                        "text": "Cough",
                        "score": 2
                    },
                    {
                        "text": "Trouble breathing",
                        "score": 1
                    },
                    {
                        "text": "None of the above",
                        "score": 0
                    }
                ]
            },
            {
                "type": "TEXT_FIELD",
                "text": "How many covid center do you have in your city?",
                "isSkippable": True,
                "inputDataType": "INTEGER"
            },
            {
                "type": "TEXT_FIELD",
                "text": "What is your text temperature?",
                "isSkippable": True,
                "inputDataType": "BODY_TEMPERATURE"
            }
        ]
    }
    status, data = API_Calls.post_create_questionnaire_api(BASE_URL, CREATE_QUESTIONNAIRE_DATA_REQUEST_BODY_ISSKIPPABLE_VALUE_AS_INTEGER, ACCESS_TOKEN,CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 400


def test_post_create_questionnaire_api_request_body_options_score_as_string():
    CREATE_QUESTIONNAIRE_DATA_REQUEST_BODY_SCORE_AS_STRING = {
        "title": "covid_19",
        "language": "en",
        "questions": [
            {
                "type": "MULTIPLE_CHOICE",
                "text": "Have you been within 6 feet of a person with a lab confirmed case of COVID-19 or with symptoms of COVID-19 for at least 15 minutes, or had direct contact with their mucus or saliva,in the past 14 days?",
                "isSkippable": False,
                "options": [
                    {
                        "text": "No",
                        "score": "abc"
                    },
                    {
                        "text": "Yes",
                        "score": 1
                    }
                ]
            },
            {
                "type": "MULTIPLE_SELECT",
                "text": "In the last 48 hours, have you had any of the following NEW symptoms? Select all that apply.",
                "isSkippable": False,
                "options": [
                    {
                        "text": "Fever of 100.4° F or above",
                        "score": 3
                    },
                    {
                        "text": "Cough",
                        "score": 2
                    },
                    {
                        "text": "Trouble breathing",
                        "score": 1
                    },
                    {
                        "text": "None of the above",
                        "score": 0
                    }
                ]
            },
            {
                "type": "TEXT_FIELD",
                "text": "How many covid center do you have in your city?",
                "isSkippable": True,
                "inputDataType": "INTEGER"
            },
            {
                "type": "TEXT_FIELD",
                "text": "What is your text temperature?",
                "isSkippable": True,
                "inputDataType": "BODY_TEMPERATURE"
            }
        ]
    }
    status, data = API_Calls.post_create_questionnaire_api(BASE_URL, CREATE_QUESTIONNAIRE_DATA_REQUEST_BODY_SCORE_AS_STRING, ACCESS_TOKEN,CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 400


def test_post_create_questionnaire_api_request_body_options_score_beyond_defined_range_11():

    CREATE_QUESTIONNAIRE_DATA_REQUEST_BODY_TYPE_OPTIONS_SCORE_BEYOND_DEFINED_RANGE_11 = {
        "title": "covid_19",
        "language": "en",
        "questions": [
            {
                "type": "MULTIPLE_CHOICE",
                "text": "Have you been within 6 feet of a person with a lab confirmed case of COVID-19 or with symptoms of COVID-19 for at least 15 minutes, or had direct contact with their mucus or saliva,in the past 14 days?",
                "isSkippable": False,
                "options": [
                    {
                        "text": "No",
                        "score": 11
                    },
                    {
                        "text": "Yes",
                        "score": 1
                    }
                ]
            },
            {
                "type": "MULTIPLE_SELECT",
                "text": "In the last 48 hours, have you had any of the following NEW symptoms? Select all that apply.",
                "isSkippable": False,
                "options": [
                    {
                        "text": "Fever of 100.4° F or above",
                        "score": 3
                    },
                    {
                        "text": "Cough",
                        "score": 2
                    },
                    {
                        "text": "Trouble breathing",
                        "score": 1
                    },
                    {
                        "text": "None of the above",
                        "score": 0
                    }
                ]
            },
            {
                "type": "TEXT_FIELD",
                "text": "How many covid center do you have in your city?",
                "isSkippable": True,
                "inputDataType": "INTEGER"
            },
            {
                "type": "TEXT_FIELD",
                "text": "What is your text temperature?",
                "isSkippable": True,
                "inputDataType": "BODY_TEMPERATURE"
            }
        ]
    }

    D_CP = CREATE_QUESTIONNAIRE_DATA_REQUEST_BODY_TYPE_OPTIONS_SCORE_BEYOND_DEFINED_RANGE_11.copy()
    ques_title = helper.random_title()
    time.sleep(3)
    DATA = helper.update_dictionary(D_CP, title=ques_title)
    status, data = API_Calls.post_create_questionnaire_api(BASE_URL, DATA, ACCESS_TOKEN,CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 201


# def test_post_create_questionnaire_api_request_body_options_score_beyond_defined_range_0():
#     D_CP = CREATE_QUESTIONNAIRE_DATA['QUESTIONS']['options'].copy()
#     D = helper.update_dictionary(D_CP,score=0)
#     DATA = {'options':D}
#     status, data = API_Calls.post_create_questionnaire_api(BASE_URL, DATA, ACCESS_TOKEN,CONTENT_TYPE_APPLICATION_JSON)
#     print(status, data)
#     assert status == 400



def test_post_create_questionnaire_api_request_body_inputDataType_as_random_string():
    CREATE_QUESTIONNAIRE_DATA_REQUEST_BODY_INPUT_DATA_TYPE_AS_RANDOM_STRING = {
        "title": "covid_19",
        "language": "en",
        "questions": [
            {
                "type": "MULTIPLE_CHOICE",
                "text": "Have you been within 6 feet of a person with a lab confirmed case of COVID-19 or with symptoms of COVID-19 for at least 15 minutes, or had direct contact with their mucus or saliva,in the past 14 days?",
                "isSkippable": False,
                "options": [
                    {
                        "text": "No",
                        "score": 0
                    },
                    {
                        "text": "Yes",
                        "score": 1
                    }
                ]
            },
            {
                "type": "MULTIPLE_SELECT",
                "text": "In the last 48 hours, have you had any of the following NEW symptoms? Select all that apply.",
                "isSkippable": False,
                "options": [
                    {
                        "text": "Fever of 100.4° F or above",
                        "score": 3
                    },
                    {
                        "text": "Cough",
                        "score": 2
                    },
                    {
                        "text": "Trouble breathing",
                        "score": 1
                    },
                    {
                        "text": "None of the above",
                        "score": 0
                    }
                ]
            },
            {
                "type": "TEXT_FIELD",
                "text": "How many covid center do you have in your city?",
                "isSkippable": True,
                "inputDataType": "INTEGER"
            },
            {
                "type": "TEXT_FIELD",
                "text": "What is your text temperature?",
                "isSkippable": True,
                "inputDataType": "abc"
            }
        ]
    }
    status, data = API_Calls.post_create_questionnaire_api(BASE_URL, CREATE_QUESTIONNAIRE_DATA_REQUEST_BODY_INPUT_DATA_TYPE_AS_RANDOM_STRING, ACCESS_TOKEN,CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 400



def test_post_create_questionnaire_api_with_extra_field_added():
    D_CP = CREATE_QUESTIONNAIRE_DATA.copy()
    DATA = helper.update_dictionary(D_CP, test='test')
    status, data = API_Calls.post_create_questionnaire_api(BASE_URL, DATA, ACCESS_TOKEN,CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 400


###### -------missing keys -------#####
def test_post_create_questionnaire_with_multiple_variable_missing():
    D_CP = CREATE_QUESTIONNAIRE_DATA.copy()
    n = helper.factorial(len(D_CP))
    for key in range(n):
        DATA = helper.get_random_pairs(D_CP)
        #DATA = {'questionnaire': D}
        status, data = API_Calls.post_create_questionnaire_api(BASE_URL, DATA, ACCESS_TOKEN,CONTENT_TYPE_APPLICATION_JSON)
        print(status, data)
        assert status == 400



def test_post_create_questionnaire_title_key_missing():
    D_CP = CREATE_QUESTIONNAIRE_DATA.copy()
    DATA = helper.delete_key(D_CP, 'title')
    status, data = API_Calls.post_create_questionnaire_api(BASE_URL, DATA, ACCESS_TOKEN,
                                       CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 400


def test_post_create_questionnaire_language_key_missing():
    D_CP = CREATE_QUESTIONNAIRE_DATA.copy()
    DATA = helper.delete_key(D_CP, 'language')
    status, data = API_Calls.post_create_questionnaire_api(BASE_URL, DATA, ACCESS_TOKEN,
                                       CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 400


def test_post_create_questionnaire_questions_key_missing():
    D_CP = CREATE_QUESTIONNAIRE_DATA.copy()
    DATA = helper.delete_key(D_CP, 'questions')
    status, data = API_Calls.post_create_questionnaire_api(BASE_URL, DATA, ACCESS_TOKEN,
                                       CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 400


def test_post_create_questionnaire_questions_type_key_missing():
    D_CP = CREATE_QUESTIONNAIRE_DATA['questions'].copy()
    DATA = helper.delete_key(D_CP, 'type')
    status, data = API_Calls.post_create_questionnaire_api(BASE_URL, DATA, ACCESS_TOKEN,
                                       CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 400

def test_post_create_questionnaire_questions_text_key_missing():
    D_CP = CREATE_QUESTIONNAIRE_DATA['questions'].copy()
    DATA = helper.delete_key(D_CP, 'text')
    status, data = API_Calls.post_create_questionnaire_api(BASE_URL, DATA, ACCESS_TOKEN,
                                       CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 400

def test_post_create_questionnaire_questions_isSkippable_key_missing():
        D_CP = CREATE_QUESTIONNAIRE_DATA['questions'].copy()
        DATA = helper.delete_key(D_CP, 'isSkippable')
        status, data = API_Calls.post_create_questionnaire_api(BASE_URL, DATA, ACCESS_TOKEN,
                                           CONTENT_TYPE_APPLICATION_JSON)
        print(status, data)
        assert status == 400



def test_post_create_questionnaire_questions_options_key_missing():
    D_CP = CREATE_QUESTIONNAIRE_DATA['questions'].copy()
    DATA = helper.delete_key(D_CP, 'options')
    status, data = API_Calls.post_create_questionnaire_api(BASE_URL, DATA, ACCESS_TOKEN,
                                       CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 400


def test_post_create_questionnaire_questions_options_text_missing():
    CREATE_QUESTIONNAIRE_DATA_REQUEST_QUESTIONS_OPTIONS_TEXT_MISSING = {
        "title": "covid_19",
        "language": "en",
        "questions": [
            {
                "type": "MULTIPLE_CHOICE",
                "text": "Have you been within 6 feet of a person with a lab confirmed case of COVID-19 or with symptoms of COVID-19 for at least 15 minutes, or had direct contact with their mucus or saliva,in the past 14 days?",
                "isSkippable": False,
                "options": [
                    {

                        "score": 0
                    },
                    {
                        "text": "Yes",
                        "score": 1
                    }
                ]
            },
            {
                "type": "MULTIPLE_SELECT",
                "text": "In the last 48 hours, have you had any of the following NEW symptoms? Select all that apply.",
                "isSkippable": False,
                "options": [
                    {
                        "text": "Fever of 100.4° F or above",
                        "score": 3
                    },
                    {
                        "text": "Cough",
                        "score": 2
                    },
                    {
                        "text": "Trouble breathing",
                        "score": 1
                    },
                    {
                        "text": "None of the above",
                        "score": 0
                    }
                ]
            },
            {
                "type": "TEXT_FIELD",
                "text": "How many covid center do you have in your city?",
                "isSkippable": True,
                "inputDataType": "INTEGER"
            },
            {
                "type": "TEXT_FIELD",
                "text": "What is your text temperature?",
                "isSkippable": True,
                "inputDataType": "BODY_TEMPERATURE"
            }
        ]
    }
    status, data = API_Calls.post_create_questionnaire_api(BASE_URL, CREATE_QUESTIONNAIRE_DATA_REQUEST_QUESTIONS_OPTIONS_TEXT_MISSING, ACCESS_TOKEN,
                                       CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 400


def test_post_create_questionnaire_questions_options_score_missing():
    CREATE_QUESTIONNAIRE_DATA_REQUEST_BODY_QUESTIONS_OPTIONS_SCORE_MISSING = {
        "title": "covid_19",
        "language": "en",
        "questions": [
            {
                "type": "MULTIPLE_CHOICE",
                "text": "Have you been within 6 feet of a person with a lab confirmed case of COVID-19 or with symptoms of COVID-19 for at least 15 minutes, or had direct contact with their mucus or saliva,in the past 14 days?",
                "isSkippable": False,
                "options": [
                    {
                        "text": "No",

                    },
                    {
                        "text": "Yes",
                        "score": 1
                    }
                ]
            },
            {
                "type": "MULTIPLE_SELECT",
                "text": "In the last 48 hours, have you had any of the following NEW symptoms? Select all that apply.",
                "isSkippable": False,
                "options": [
                    {
                        "text": "Fever of 100.4° F or above",
                        "score": 3
                    },
                    {
                        "text": "Cough",
                        "score": 2
                    },
                    {
                        "text": "Trouble breathing",
                        "score": 1
                    },
                    {
                        "text": "None of the above",
                        "score": 0
                    }
                ]
            },
            {
                "type": "TEXT_FIELD",
                "text": "How many covid center do you have in your city?",
                "isSkippable": True,
                "inputDataType": "INTEGER"
            },
            {
                "type": "TEXT_FIELD",
                "text": "What is your text temperature?",
                "isSkippable": True,
                "inputDataType": "BODY_TEMPERATURE"
            }
        ]
    }
    status, data = API_Calls.post_create_questionnaire_api(BASE_URL, CREATE_QUESTIONNAIRE_DATA_REQUEST_BODY_QUESTIONS_OPTIONS_SCORE_MISSING, ACCESS_TOKEN,
                                       CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 400


def test_post_create_questionnaire_questions_inputDataType_missing():
    D_CP = CREATE_QUESTIONNAIRE_DATA['questions'].copy()
    DATA = helper.delete_key(D_CP, 'inputDataType')
    status, data = API_Calls.post_create_questionnaire_api(BASE_URL, DATA, ACCESS_TOKEN,
                                       CONTENT_TYPE_APPLICATION_JSON)
    print(status, data)
    assert status == 400


###### --------- 422 status code ----------------######


def test_post_create_questionnaire_api_input_text_questionnaire_with_options():
    D_CP = CREATE_QUESTIONNAIRE_DATA_INPUT_TEXT_WITH_OPTIONS.copy()
    ques_title = helper.random_title()
    time.sleep(3)
    DATA = helper.update_dictionary(D_CP, title=ques_title)
    status, data = API_Calls.post_create_questionnaire_api(BASE_URL, DATA, ACCESS_TOKEN, CONTENT_TYPE_APPLICATION_JSON)
    assert status == 422
    print(status, data)



def test_post_create_questionnaire_api_multi_choice_questionnaire_with_inputDataType():
    D_CP = CREATE_QUESTIONNAIRE_DATA_MULTIPLE_CHOICE_SENDING_INPUT_FIELD.copy()
    ques_title = helper.random_title()
    time.sleep(3)
    DATA = helper.update_dictionary(D_CP, title=ques_title)
    status, data = API_Calls.post_create_questionnaire_api(BASE_URL, DATA, ACCESS_TOKEN, CONTENT_TYPE_APPLICATION_JSON)
    assert status == 422
    print(status, data)


def test_post_create_questionnaire_api_multi_select_questionnaire_with_inputDataType():
    D_CP = CREATE_QUESTIONNAIRE_DATA_MULTIPLE_SELECT_SENDING_INPUT_FIELD.copy()
    ques_title = helper.random_title()
    time.sleep(3)
    DATA = helper.update_dictionary(D_CP, title=ques_title)
    status, data = API_Calls.post_create_questionnaire_api(BASE_URL, DATA, ACCESS_TOKEN, CONTENT_TYPE_APPLICATION_JSON)
    assert status == 422
    print(status, data)


def test_post_create_questionnaire_api_same_question_with_other_language():
    D_CP = CREATE_QUESTIONNAIRE_DATA_HI.copy()
    ques_title = helper.random_title()
    time.sleep(3)
    DATA = helper.update_dictionary(D_CP, title=ques_title)
    status, data = API_Calls.post_create_questionnaire_api(BASE_URL, DATA, ACCESS_TOKEN, CONTENT_TYPE_APPLICATION_JSON)
    assert status == 422
    print(status, data)


def test_post_create_questionnaire_api_missing_attribute_for_multiple_choice():
    D_CP = CREATE_QUESTIONNAIRE_DATA_MULTIPLE_CHOICE_MISSING_ATTRIBUTE_OPTIONS.copy()
    ques_title = helper.random_title()
    time.sleep(3)
    DATA = helper.update_dictionary(D_CP, title=ques_title)
    status, data = API_Calls.post_create_questionnaire_api(BASE_URL, DATA, ACCESS_TOKEN, CONTENT_TYPE_APPLICATION_JSON)
    assert status == 422
    print(status, data)


####### -------- invalid request ----------#######

def test_post_create_questionnaire_api_get_request(input_url2,get_token):
    headers_post_create_questionnaire_api = {'Authorization': get_token,'content-type' : CONTENT_TYPE_APPLICATION_JSON}
    res = requests.get(url=input_url2 + CREATE_QUESTIONNAIRE_ENDPOINT, headers=headers_post_create_questionnaire_api)
    print(res)
    assert res.status_code == 403


def test_post_create_questionnaire_api_put_request(input_url2,get_token):
    headers_post_create_questionnaire_api = {'Authorization': get_token,'content-type' : CONTENT_TYPE_APPLICATION_JSON}
    res = requests.put(url=input_url2 + CREATE_QUESTIONNAIRE_ENDPOINT, headers=headers_post_create_questionnaire_api)
    print(res)
    assert res.status_code == 403

def test_post_create_questionnaire_api_delete_request(input_url2, get_token):
        headers_post_create_questionnaire_api = {'Authorization': get_token,
                                                 'content-type': CONTENT_TYPE_APPLICATION_JSON}
        res = requests.delete(url=input_url2 + CREATE_QUESTIONNAIRE_ENDPOINT, headers=headers_post_create_questionnaire_api)
        print(res)
        assert res.status_code == 403

