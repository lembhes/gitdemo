import requests
import json
import logging
from Variables.variable import *


def token_api(URL, DATA, TOKEN, CONTENT_TYPE_URL_ENCODED):
    headers = {'Authorization': TOKEN, 'Content-Type': CONTENT_TYPE_URL_ENCODED}
    response = requests.post(url=URL + TOKEN_END_POINT, data=DATA, headers=headers)
    return response.status_code, response.json()


def subject_api(URL, DATA, ACCESS_TOKEN, CONTENT_TYPE_APPLICATION_JSON):
    headers_subject = {'Authorization': ACCESS_TOKEN, 'Content-Type': CONTENT_TYPE_APPLICATION_JSON}
    res = requests.post(url=URL + SUBJECT_END_POINT, data=json.dumps(DATA), headers=headers_subject)
    return res.status_code, res.json()


def update_subject_details(BASE_URL, USER_IDENTIFIER, DATA, ACCESS_TOKEN):
    headers_subject_update = {'Authorization': ACCESS_TOKEN, 'Content-Type': CONTENT_TYPE_APPLICATION_JSON}
    res = requests.put(url=BASE_URL + '/users/' + USER_IDENTIFIER + '/device', data=json.dumps(DATA),
                       headers=headers_subject_update)
    return res.status_code, res.json()


def measures_api(BASE_URL, ACCESS_TOKEN):
    headers_measure = {'Authorization': ACCESS_TOKEN}
    res = requests.get(url=BASE_URL + '/measures', headers=headers_measure)
    return res.status_code, res.json()


def measure_id_api(BASE_URL, MEASURE_ID, ACCESS_TOKEN):
    headers_measure_id = {'Authorization': ACCESS_TOKEN}
    res = requests.get(url=BASE_URL + '/measures/' + str(MEASURE_ID), headers=headers_measure_id)
    return res.status_code, res.json()


def storage_api(BASE_URL, DATA, ACCESS_TOKEN, CONTENT_TYPE_APPLICATION_JSON):
    headers_storage = {'Authorization': ACCESS_TOKEN, 'Content-Type': CONTENT_TYPE_APPLICATION_JSON}
    res = requests.post(url=BASE_URL + STORAGE_END_POINT, data=json.dumps(DATA), headers=headers_storage)
    return res.status_code, res.json()


def upload_sample_file(STORAGE_SIGNED_URL, file_path):
    logging.info('uploading sample file {} on signed_url'.format(file_path))
    data = open(file_path, 'rb')
    url = STORAGE_SIGNED_URL
    headers = {'Content-Type': 'audio/wave'}
    r = requests.put(url, data=data, headers=headers)
    return r.status_code


def get_audio_file(BASE_URL, FILE_PATH_URL_ENCODED, ACCESS_TOKEN):
    headers = {'Authorization': ACCESS_TOKEN}
    res = requests.get(url=BASE_URL + '/storage/files/' + FILE_PATH_URL_ENCODED, headers=headers)
    return res.status_code, res.json()


def get_questionnaire_ID_required_for_measure(BASE_URL, MEASURE_NAME, ACCESS_TOKEN):
    headers_get = {'Authorization': ACCESS_TOKEN}
    res_get = requests.get(url=BASE_URL + '/measures/name/' + MEASURE_NAME, headers=headers_get)
    return res_get.status_code, res_get.json()


def get_questionnaire_required_for_measure(BASE_URL, QUESTIONNAIRE_ID, QUESTIONNAIRE_LANGUAGES, ACCESS_TOKEN):
    headers = {'Authorization': ACCESS_TOKEN}
    parameters = {'language': QUESTIONNAIRE_LANGUAGES}
    res_get = requests.get(url=BASE_URL + '/questionnaires/' + QUESTIONNAIRE_ID, headers=headers, params=parameters)
    return res_get.status_code, res_get.json()


def submit_questionnaire_response(BASE_URL, DATA, ACCESS_TOKEN):
    header = {'Authorization': ACCESS_TOKEN, 'Content-Type': CONTENT_TYPE_APPLICATION_JSON}
    response = requests.post(url=BASE_URL + '/questionnaire-responses', data=json.dumps(DATA),
                             headers=header)
    return response.status_code, response.json()


def score_api(BASE_URL, DATA, ACCESS_TOKEN, CONTENT_TYPE_APPLICATION_JSON):
    headers_scores = {'Authorization': ACCESS_TOKEN, 'Content-Type': CONTENT_TYPE_APPLICATION_JSON}
    res = requests.post(url=BASE_URL + SCORE_END_POINT, data=json.dumps(DATA), headers=headers_scores)
    return res.status_code, res.json()



def get_inference_scores_api_duration(BASE_URL,ACCESS_TOKEN):
    params = {'from': FROM_TIME ,'to': TO_TIME}
    headers_scores = {'Authorization': ACCESS_TOKEN }
    res = requests.get(url=BASE_URL + SCORE_END_POINT, headers=headers_scores,params=params)
    return res.status_code, res.json()


def get_inference_scores_api_userIdentifier(BASE_URL,ACCESS_TOKEN,SUB_IDENTIFIER):
    parameters = {'userIdentifier': SUB_IDENTIFIER }
    headers_scores = {'Authorization': ACCESS_TOKEN }
    res = requests.get(url=BASE_URL + SCORE_END_POINT, headers=headers_scores,params=parameters)
    return res.status_code, res.json()




#--------------------------- API 3.0 -----------------------


def post_async_score_api(ASYNC_URL, DATA, ACCESS_TOKEN, CONTENT_TYPE_APPLICATION_JSON):
    headers_scores = {'Authorization': ACCESS_TOKEN, 'Content-Type': CONTENT_TYPE_APPLICATION_JSON}
    res = requests.post(url=ASYNC_URL + ASYNC_SCORE_ENDPOINT, data=json.dumps(DATA), headers=headers_scores)
    return res.status_code, res.json()


def get_async_score_api(ASYNC_URL,ACCESS_TOKEN,JOB_ID):
    headers_get_score_api = {'Authorization': ACCESS_TOKEN}
    res = requests.get(url=ASYNC_URL + '/inference/voice-feature-scores/'+ JOB_ID ,headers=headers_get_score_api)
    return res.status_code, res.json()

def get_voice_feature_by_measure_api(BASE_URL,ACCESS_TOKEN):
    headers_get_voice_feature_by_measure = {'Authorization': ACCESS_TOKEN}
    res = requests.get(url=BASE_URL + '/measures/name/'+FEATURE_BY_MEASURE_NAME+'/voice-features',headers=headers_get_voice_feature_by_measure)
    return res.status_code, res.json()



#-----newly added APIs ------------#


def get_score_by_voice_feature_score_id_api(BASE_URL,ACCESS_TOKEN,VOICE_FEATURE_SCORE_ID):
    headers_get_score_api = {'Authorization': ACCESS_TOKEN}
    res = requests.get(url=BASE_URL + '/inference/voice-feature-scores/'+ VOICE_FEATURE_SCORE_ID ,headers=headers_get_score_api)
    return res.status_code, res.json()


def get_voice_feature_scores_api(BASE_URL,ACCESS_TOKEN):
    headers_get_score_api = {'Authorization': ACCESS_TOKEN}
    res = requests.get(url=BASE_URL + '/inference/voice-feature-scores',headers=headers_get_score_api)
    return res.status_code, res.json()



# def get_questionnaire_required_for_measure(BASE_URL, QUESTIONNAIRE_ID, QUESTIONNAIRE_LANGUAGES, ACCESS_TOKEN):
#     headers = {'Authorization': ACCESS_TOKEN}
#     parameters = {'language': QUESTIONNAIRE_LANGUAGES}
#     res_get = requests.get(url=BASE_URL + '/questionnaires/' + QUESTIONNAIRE_ID, headers=headers, params=parameters)
#     return res_get.status_code, res_get.json()


def get_voice_feature_scores_api_all_params(BASE_URL,ACCESS_TOKEN,SUB_IDENTIFIER):
    parameters = {'pageIndex': 1 ,'from': FROM_TIME,'to': TO_TIME,'userIdentifier':SUB_IDENTIFIER}
    headers_get_score_api = {'Authorization': ACCESS_TOKEN}
    res = requests.get(url=BASE_URL + '/inference/voice-feature-scores', headers=headers_get_score_api,params=parameters)
    return res.status_code, res.json()

def get_voice_feature_scores_api_page_index(BASE_URL,ACCESS_TOKEN):
    headers_get_score_api = {'Authorization': ACCESS_TOKEN}
    parameters = {'pageIndex': 1}
    res = requests.get(url=BASE_URL + '/inference/voice-feature-scores', headers=headers_get_score_api,params=parameters)
    return res.status_code, res.json()


def get_voice_feature_scores_api_sub_identifier(BASE_URL,ACCESS_TOKEN,SUB_IDENTIFIER):
    headers_get_score_api = {'Authorization': ACCESS_TOKEN}
    parameters = {'userIdentifier': SUB_IDENTIFIER}
    res = requests.get(url=BASE_URL + '/inference/voice-feature-scores',headers=headers_get_score_api,params=parameters)
    return res.status_code, res.json()

def get_voice_feature_scores_api_duration(BASE_URL,ACCESS_TOKEN):
    headers_get_score_api = {'Authorization': ACCESS_TOKEN}
    parameters = {'from': FROM_TIME_ALL,'to': TO_TIME_ALL}
    res = requests.get(url=BASE_URL + '/inference/voice-feature-scores',headers=headers_get_score_api,params=parameters)
    return res.status_code, res.json()


def get_voice_feature_scores_api_pageIndex_duration(BASE_URL,ACCESS_TOKEN):
    parameters = {'pageIndex': 0 ,'from': FROM_TIME_ALL,'to': TO_TIME_ALL }
    headers_get_score_api = {'Authorization': ACCESS_TOKEN}
    res = requests.get(url=BASE_URL + '/inference/voice-feature-scores', headers=headers_get_score_api,params=parameters)
    return res.status_code, res.json()


def get_voice_feature_scores_api_pageIndex_subIdentifier(BASE_URL,ACCESS_TOKEN,SUB_IDENTIFIER):
    parameters = {'pageIndex': 0 ,'userIdentifier':SUB_IDENTIFIER_A}
    headers_get_score_api = {'Authorization': ACCESS_TOKEN}
    res = requests.get(url=BASE_URL + '/inference/voice-feature-scores', headers=headers_get_score_api,params=parameters)
    return res.status_code, res.json()


def get_voice_feature_scores_api_duration_subIdentifier(BASE_URL,ACCESS_TOKEN,SUB_IDENTIFIER):
    parameters = {'from': FROM_TIME_ALL,'to': TO_TIME_ALL,'userIdentifier':SUB_IDENTIFIER_A}
    headers_get_score_api = {'Authorization': ACCESS_TOKEN}
    res = requests.get(url=BASE_URL + '/inference/voice-feature-scores', headers=headers_get_score_api,params=parameters)
    return res.status_code, res.json()

#---- API 3.1 TranscriptionService api -----#

def post_async_transcriptions_api(ASYNC_URL, DATA, ACCESS_TOKEN, CONTENT_TYPE_APPLICATION_JSON):
    headers_transcriptions = {'Authorization': ACCESS_TOKEN, 'Content-Type': CONTENT_TYPE_APPLICATION_JSON}
    res = requests.post(url=ASYNC_URL + TRANSCRIPTION_ENDPOINT, data=json.dumps(DATA), headers=headers_transcriptions)
    return res.status_code, res.json()


def get_async_transcription_api(ASYNC_URL,ACCESS_TOKEN,ASYNC_JOB_ID):
    headers_transcriptions_get_api = {'Authorization': ACCESS_TOKEN}
    res = requests.get(url=ASYNC_URL + GET_TRANSCRIPTION_ENDPOINT + ASYNC_JOB_ID ,headers=headers_transcriptions_get_api)
    return res.status_code, res.json()

def get_audio_file_transcription(BASE_URL, FILE_PATH_URL_ENCODED, ACCESS_TOKEN):
    headers = {'Authorization': ACCESS_TOKEN}
    res = requests.get(url=BASE_URL + '/storage/files/' + FILE_PATH_URL_ENCODED + '/transcriptions', headers=headers)
    return res.status_code, res.json()

def get_transcriptions(BASE_URL, ACCESS_TOKEN):
    headers = {'Authorization': ACCESS_TOKEN}
    parameters = {'filePath': FILE_PATH_ENCODED_SAVED}
    res = requests.get(url=BASE_URL + '/storage/files/'+'transcriptions', headers=headers,params=parameters)
    return res.status_code, res.json()

def get_transcriptions_multiple_params(BASE_URL, ACCESS_TOKEN):
    headers = {'Authorization': ACCESS_TOKEN, 'Content-Type': CONTENT_TYPE_MULTIPART_FORM_DATA}
    parameters = {'filePath': FILE_PATH_ENCODED_SAVED,'filePath':FILE_PATH_ENCODED_SAVED1}
    res = requests.get(url=BASE_URL + '/storage/files/'+'transcriptions', headers=headers,params=parameters)
    return res.status_code, res.json()

#get_transcriptions.json
#
# def get_audio_file(BASE_URL, FILE_PATH_URL_ENCODED, ACCESS_TOKEN):
#     headers = {'Authorization': ACCESS_TOKEN}
#     res = requests.get(url=BASE_URL + '/storage/files/' + FILE_PATH_URL_ENCODED, headers=headers)
#     return res.status_code, res.json()


# def get_voice_feature_scores_api_all_params(BASE_URL,ACCESS_TOKEN,SUB_IDENTIFIER):
#     parameters = {'pageIndex': 1 ,'from': FROM_TIME,'to': TO_TIME,'userIdentifier':SUB_IDENTIFIER}
#     headers_get_score_api = {'Authorization': ACCESS_TOKEN}
#     res = requests.get(url=BASE_URL + '/inference/voice-feature-scores', headers=headers_get_score_api,params=parameters)
#     return res.status_code, res.json()


#---------------- Two sample sscoring API -----------------------#


def post_inference_parameters_api(BASE_URLV2, DATA, ACCESS_TOKEN, CONTENT_TYPE_APPLICATION_JSON):
    headers_inference_parameters= {'Authorization': ACCESS_TOKEN, 'Content-Type': CONTENT_TYPE_APPLICATION_JSON}
    res = requests.post(url=BASE_URLV2 + INFERENCE_PARAMETER_ENDPOINT, data=json.dumps(DATA), headers=headers_inference_parameters)
    return res.status_code, res.json()

def put_inference_parameters_api(BASE_URLV2, ACCESS_TOKEN,INFERENCE_PARAMETER_ID,DATA, CONTENT_TYPE_APPLICATION_JSON):
    headers_inference_parameters= {'Authorization': ACCESS_TOKEN, 'Content-Type': CONTENT_TYPE_APPLICATION_JSON}
    res = requests.put(url=BASE_URLV2 + INFERENCE_PARAMETER_PUTENDPOINT + INFERENCE_PARAMETER_ID,data=json.dumps(DATA),  headers=headers_inference_parameters)
    return res.status_code, res.json()

def post_inference_scorev2_api(BASE_URLV2, DATA, ACCESS_TOKEN, CONTENT_TYPE_APPLICATION_JSON):
    headers_scores = {'Authorization': ACCESS_TOKEN, 'Content-Type': CONTENT_TYPE_APPLICATION_JSON}
    res = requests.post(url=BASE_URLV2 + INFERENCE_ENDPOINT, data=json.dumps(DATA), headers=headers_scores)
    return res.status_code, res.json()

def get_inference_scorev2_api(BASE_URLV2, SCOREID, ACCESS_TOKEN, CONTENT_TYPE_APPLICATION_JSON):
    headers_scores = {'Authorization': ACCESS_TOKEN, 'Content-Type': CONTENT_TYPE_APPLICATION_JSON}
    res = requests.get(url=BASE_URLV2 + INFERENCE_ENDPOINT + '/' +SCOREID, headers=headers_scores)
    return res.status_code, res.json()



# #---------------- Two sample sscoring API -----------------------#
#
#
# def post_inference_parameters_api(BASE_URLV2, DATA, ACCESS_TOKEN, CONTENT_TYPE_APPLICATION_JSON):
#    headers_inference_parameters= {'Authorization': ACCESS_TOKEN, 'Content-Type': CONTENT_TYPE_APPLICATION_JSON}
#    res = requests.post(url=BASE_URLV2 + INFERENCE_PARAMETER_ENDPOINT, data=json.dumps(DATA), headers=headers_inference_parameters)
#    return res.status_code, res.json()
#
# def put_inference_parameters_api(BASE_URLV2, ACCESS_TOKEN,INFERENCE_PARAMETER_ID,DATA, CONTENT_TYPE_APPLICATION_JSON):
#    headers_inference_parameters= {'Authorization': ACCESS_TOKEN, 'Content-Type': CONTENT_TYPE_APPLICATION_JSON}
#    res = requests.put(url=BASE_URLV2 + INFERENCE_PARAMETER_PUTENDPOINT + INFERENCE_PARAMETER_ID,data=json.dumps(DATA),  headers=headers_inference_parameters)
#    return res.status_code, res.json()
#
# def post_inference_scorev2_api(BASE_URLV2, DATA, ACCESS_TOKEN, CONTENT_TYPE_APPLICATION_JSON):
#    headers_scores = {'Authorization': ACCESS_TOKEN, 'Content-Type': CONTENT_TYPE_APPLICATION_JSON}
#    res = requests.post(url=BASE_URLV2 + INFERENCE_ENDPOINT, data=json.dumps(DATA), headers=headers_scores)
#    return res.status_code, res.json()
#
# def get_inference_scorev2_api(BASE_URLV2, SCOREID, ACCESS_TOKEN, CONTENT_TYPE_APPLICATION_JSON):
#    headers_scores = {'Authorization': ACCESS_TOKEN, 'Content-Type': CONTENT_TYPE_APPLICATION_JSON}
#    res = requests.get(url=BASE_URLV2 + INFERENCE_ENDPOINT + '/' +SCOREID, headers=headers_scores)
#    return res.status_code, res.json()
#



#---------- create questionnaire API --------------#

def post_create_questionnaire_api(BASE_URL, DATA, ACCESS_TOKEN, CONTENT_TYPE_APPLICATION_JSON):
    headers_create_questionnaire= {'Authorization': ACCESS_TOKEN, 'Content-Type': CONTENT_TYPE_APPLICATION_JSON}
    res = requests.post(url=BASE_URL + CREATE_QUESTIONNAIRE_ENDPOINT, data=json.dumps(DATA), headers=headers_create_questionnaire)
    return res.status_code, res.json()
