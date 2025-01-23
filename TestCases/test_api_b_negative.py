# import json
# import pytest
# import requests
# from TestCases import Api_functions
# from Variables.variable import *
# from TestCases.Support import helper
# # ---------------- Get the Base64 --------------------------------#
#
# base64secrets = helper.get_base64secrets(CLIENT_ID, CLIENT_SECRET)
# print(base64secrets)
#
# BASE_TOKEN = 'Basic ' + base64secrets
#
# # FIRST TOKEN API CALL TO GET ACCESS TOKEN #
#
# status_code, json_data = Api_functions.token_api(BASE_URL, VALID_TOKEN_DATA, BASE_TOKEN, CONTENT_TYPE_URL_ENCODED)
# print("Token API", status_code)
# ACCESS_TOKEN = json_data['access_token']
#
#
# # SECOND MEASURES API CALL TO GET MEASURE ID #
#
# status, measure_json = Api_functions.measure_api(BASE_URL, MEASURE_END_POINT, ACCESS_TOKEN)
# MEASURE_ID_END_POINT = measure_json['measures']
#
#
# # TOKEN API NEGATIVE TEST CASES #
#
# @pytest.mark.token_api
# def test_token_api_invalid_endpoint():
#     status, data = Api_functions.token_api(INVALID_BASE_URL, VALID_TOKEN_DATA, BASE_TOKEN, CONTENT_TYPE_URL_ENCODED)
#     assert status == 403
#
#
# #################   SCOPE AND CLIENT ID IS NOT WORKING FOR DEMO API's ###########
#
#
# @pytest.mark.token_api
# def test_token_api_request_body_scope_key_blank():
#     status, data = Api_functions.token_api(BASE_URL, REQUEST_SCOPE_KEY_BLANK, BASE_TOKEN, CONTENT_TYPE_URL_ENCODED)
#     assert status == 400
#
#
# # assert data == INVALID_REQUEST_RESPONSE
#
# @pytest.mark.token_api
# def test_token_api_request_body_scope_key_invalid():
#     status, data = Api_functions.token_api(BASE_URL, REQUEST_SCOPE_KEY_INVALID, BASE_TOKEN, CONTENT_TYPE_URL_ENCODED)
#     assert status == 400
#
#
# # assert data == INVALID_REQUEST_RESPONSE
#
# @pytest.mark.token_api
# def test_token_api_request_body_scope_key_missing():
#     status, data = Api_functions.token_api(BASE_URL, REQUEST_SCOPE_KEY_MISSING, BASE_TOKEN, CONTENT_TYPE_URL_ENCODED)
#     assert status == 400
#
#
# #  assert data == INVALID_REQUEST_RESPONSE
#
# @pytest.mark.token_api
# def test_token_api_request_body_client_id_key_blank():
#     status, data = Api_functions.token_api(BASE_URL, REQUEST_CLIENT_ID_KEY_BLANK, BASE_TOKEN, CONTENT_TYPE_URL_ENCODED)
#     assert status == 400
#     # assert data == INVALID_REQUEST_RESPONSE
#
#
# @pytest.mark.token_api
# def test_token_api_request_body_client_id_key_invalid():
#     status, data = Api_functions.token_api(BASE_URL, REQUEST_CLIENT_ID_KEY_INVALID, BASE_TOKEN,
#                                            CONTENT_TYPE_URL_ENCODED)
#     assert status == 400
#
#
# # assert data == INVALID_REQUEST_RESPONSE
#
# @pytest.mark.token_api
# def test_token_api_request_body_client_id_key_missing():
#     status, data = Api_functions.token_api(BASE_URL, REQUEST_CLIENT_ID_KEY_MISSING, BASE_TOKEN,
#                                            CONTENT_TYPE_URL_ENCODED)
#     assert status == 400
#     assert data == INVALID_REQUEST_RESPONSE
#
#
# @pytest.mark.token_api
# def test_token_api_request_body_grant_type_key_blank():
#     status, data = Api_functions.token_api(BASE_URL, REQUEST_GRANT_TYPE_KEY_BLANK, BASE_TOKEN, CONTENT_TYPE_URL_ENCODED)
#     assert status == 400
#
#
# #  assert data == INVALID_REQUEST_RESPONSE
#
# @pytest.mark.token_api
# def test_token_api_request_body_grant_type_key_invalid():
#     status, data = Api_functions.token_api(BASE_URL, REQUEST_GRANT_TYPE_KEY_INVALID, BASE_TOKEN,
#                                            CONTENT_TYPE_URL_ENCODED)
#     assert status == 400
#     # assert data == INVALID_GRANT_TYPE_RESPONSE
#
#
# @pytest.mark.token_api
# def test_token_api_request_body_grant_type_key_missing():
#     status, data = Api_functions.token_api(BASE_URL, REQUEST_GRANT_TYPE_KEY_MISSING, BASE_TOKEN,
#                                            CONTENT_TYPE_URL_ENCODED)
#     assert status == 400
#
#
# #  assert data == INVALID_REQUEST_RESPONSE
#
# @pytest.mark.token_api
# def test_token_api_request_extra_key_added():
#     status, data = Api_functions.token_api(BASE_URL, REQUEST_EXTRA_KEY_ADDED, BASE_TOKEN, CONTENT_TYPE_URL_ENCODED)
#     assert status == 400
#
#
# #   assert data == INVALID_GRANT_TYPE_RESPONSE
#
# @pytest.mark.token_api
# def test_token_api_auth_header_missing():
#     headers1 = {'Content-Type': CONTENT_TYPE_URL_ENCODED}
#     r = requests.post(BASE_URL + '/oauth2/token', data=DATA_VALID, headers=headers1)
#     assert r.status_code == 400
#
#
# #  assert r == INVALID_HEADER_RESPONSE
# #
# # @pytest.mark.token_api
# # def test_token_auth_header_value_missing():
# #     status, data = Api_functions.token_api(BASE_URL, DATA_VALID, HEADER_KEY_BLANK_VALUE, CONTENT_TYPE_URL_ENCODED)
# #     assert status == 400
# #     # assert data == INVALID_HEADER_RESPONSE
#
#
# @pytest.mark.token_api
# def test_token_auth_header_value_invalid():
#     status, data = Api_functions.token_api(BASE_URL, DATA_VALID, INVALID_BASE_TOKEN, CONTENT_TYPE_URL_ENCODED)
#     assert status == 400
#
#
# #  assert data == INVALID_HEADER_RESPONSE
#
# @pytest.mark.token_api
# def test_token_api_Content_type_header_missing():
#     headers1 = {'Authorization': BASE_TOKEN}
#     r = requests.post(BASE_URL + '/oauth2/token', data=DATA_VALID, headers=headers1)
#     assert r.status_code == 400
#
#
# # assert r == INVALID_HEADER_RESPONSE
#
# # @pytest.mark.token_api
# # def test_token_api_contentType_header_value_missing():
# #     status, data = Api_functions.token_api(BASE_URL, DATA_VALID, BASE_TOKEN, HEADER_KEY_BLANK_VALUE)
# #     assert status == 400
# #     # assert data == INVALID_HEADER_RESPONSE
#
#
# ###############   giving json instead of url encoded #####################
# #############   CONTENT TYPE NOT WORKING YET ##################
#
# # @pytest.mark.token_api
# # def test_token_api_contentType_header_value_invalid():
# #     status, data = Api_functions.token_api(BASE_URL, DATA_VALID, BASE_TOKEN, CONTENT_TYPE_APPLICATION_JSON)
# #     assert status == 400
#
#
# # assert data == INVALID_HEADER_RESPONSE
#
# @pytest.mark.token_api
# def test_token_api_with_put_request():
#     headers1 = {'Authorization': BASE_TOKEN, 'Content-Type': CONTENT_TYPE_URL_ENCODED}
#     r = requests.put(BASE_URL + '/oauth2/token', data=DATA_VALID, headers=headers1)
#     assert r.status_code == 405
#
#
# @pytest.mark.token_api
# def test_token_api_with_get_request():
#     headers1 = {'Authorization': BASE_TOKEN, 'Content-Type': CONTENT_TYPE_URL_ENCODED}
#     r = requests.get(BASE_URL + '/oauth2/token', data=DATA_VALID, headers=headers1)
#     assert r.status_code == 403
#
#
# @pytest.mark.token_api
# def test_token_api_with_delete_request():
#     headers1 = {'Authorization': BASE_TOKEN, 'Content-Type': CONTENT_TYPE_URL_ENCODED}
#     r = requests.delete(BASE_URL + '/oauth2/token', data=DATA_VALID, headers=headers1)
#     assert r.status_code == 405
#
#
# ####################################################################################
#
#
# ########################## STORAGE API NEGATIVE TEST CASES #########################
#
# @pytest.mark.storage_api
# def test_storage_api_invalid_endpoint():
#     headers_storage = {'Authorization': ACCESS_TOKEN, 'Content-Type': CONTENT_TYPE_APPLICATION_JSON}
#     res = requests.post(BASE_URL + '/stouiuerage/files', data=json.dumps(VALID_STORAGE_DATA),
#                         headers=headers_storage)
#     assert res.status_code == 403
#
#
# @pytest.mark.storage_api
# def test_storage_api_request_body_countryCode_key_blank():
#     status, data = Api_functions.storage_api(BASE_URL, REQUEST_COUNTRY_CODE_KEY_BLANK, BASE_TOKEN,
#                                              CONTENT_TYPE_APPLICATION_JSON)
#     assert status == 401
#     # assert data == MISSING_COUNTRY_CODE_RESPONSE
#
#
# @pytest.mark.storage_api
# def test_storage_api_request_body_countryCode_invalid():
#     status, data = Api_functions.storage_api(BASE_URL, REQUEST_COUNTRY_CODE_KEY_INVALID, BASE_TOKEN,
#                                              CONTENT_TYPE_APPLICATION_JSON)
#     assert status == 401
#
#
# #   assert data == INVALID_COUNTRY_CODE_RESPONSE
#
#
# @pytest.mark.storage_api
# def test_storage_api_request_body_countryCode_key_missing():
#     status, data = Api_functions.storage_api(BASE_URL, REQUEST_COUNTRY_CODE_KEY_MISSING, BASE_TOKEN,
#                                              CONTENT_TYPE_APPLICATION_JSON)
#     assert status == 401
#
#
# #  assert data == MISSING_COUNTRY_CODE_RESPONSE
#
# @pytest.mark.storage_api
# def test_storage_api_request_body_countryCode_not_supported():
#     status, data = Api_functions.storage_api(BASE_URL, REQUEST_COUNTRY_CODE_NOT_SUPPORTED, BASE_TOKEN,
#                                              CONTENT_TYPE_APPLICATION_JSON)
#     assert status == 401
#
#
# #   assert data == COUNTRY_CODE_NOT_SUPPORTED_RESPONSE
#
# @pytest.mark.storage_api
# def test_storage_api_request_body_countryCode_not_registered():
#     status, data = Api_functions.storage_api(BASE_URL, REQUEST_COUNTRY_CODE_NOT_REGISTERED, BASE_TOKEN,
#                                              CONTENT_TYPE_APPLICATION_JSON)
#     assert status == 401
#
#
# # assert data == COUNTRY_NOT_REGISTERED_RESPONSE
#
# @pytest.mark.storage_api
# def test_storage_api_request_body_subject_identifier_key_blank():
#     status, data = Api_functions.storage_api(BASE_URL, REQUEST_SUBJECT_IDENTIFIER_KEY_BLANK, BASE_TOKEN,
#                                              CONTENT_TYPE_APPLICATION_JSON)
#     assert status == 401
#
#
# #  assert data == MISSING_SUBJECT_IDENTIFIER_RESPONSE
#
# @pytest.mark.storage_api
# def test_storage_api_request_body_subject_identifier_key_invalid():
#     status, data = Api_functions.storage_api(BASE_URL, REQUEST_SUBJECT_IDENTIFIER_KEY_INVALID, BASE_TOKEN,
#                                              CONTENT_TYPE_URL_ENCODED)
#     assert status == 401
#
#
# # assert data == INVALID_SUBJECT_IDENTIFIER_RESPONSE
#
# @pytest.mark.storage_api
# def test_storage_api_request_body_subject_identifier_key_missing():
#     status, data = Api_functions.storage_api(BASE_URL, REQUEST_SUBJECT_IDENTIFIER_KEY_MISSING, BASE_TOKEN,
#                                              CONTENT_TYPE_URL_ENCODED)
#     assert status == 401
#
#
# # assert data == MISSING_SUBJECT_IDENTIFIER_RESPONSE
#
# @pytest.mark.storage_api
# def test_storage_api_request_body_file_type_key_blank():
#     status, data = Api_functions.storage_api(BASE_URL, REQUEST_FILE_TYPE_KEY_BLANK, BASE_TOKEN,
#                                              CONTENT_TYPE_APPLICATION_JSON)
#     assert status == 401
#     # assert data == MISSING_FILE_TYPE_RESPONSE
#
#
# @pytest.mark.storage_api
# def test_storage_api_request_body_file_type_key_invalid():
#     status, data = Api_functions.storage_api(BASE_URL, REQUEST_FILE_TYPE_KEY_VALUE_INVALID, BASE_TOKEN,
#                                              CONTENT_TYPE_URL_ENCODED)
#     assert status == 401
#
#
# #  assert data == INVALID_FILE_TYPE_RESPONSE
#
# @pytest.mark.storage_api
# def test_storage_api_request_body_file_type_key_missing():
#     status, data = Api_functions.storage_api(BASE_URL, REQUEST_FILE_TYPE_KEY_MISSING, BASE_TOKEN,
#                                              CONTENT_TYPE_URL_ENCODED)
#     assert status == 401
#     # assert data == MISSING_FILE_TYPE_RESPONSE
#
#
# @pytest.mark.storage_api
# def test_storage_api_request_extra_key_added():
#     status, data = Api_functions.storage_api(BASE_URL, STORAGE_REQUEST_EXTRA_KEY_ADDED, BASE_TOKEN,
#                                              CONTENT_TYPE_APPLICATION_JSON)
#     assert status == 401
#     # assert data == INVALID_GRANT_TYPE_RESPONSE
#
#
# @pytest.mark.storage_api
# def test_storage_api_auth_header_missing():
#     headers1 = {'Content-Type': CONTENT_TYPE_APPLICATION_JSON}
#     r = requests.post(BASE_URL + '/storage/files', data=json.dumps(STORAGE_REQUEST_BODY), headers=headers1)
#     assert r.status_code == 401
#
#
# @pytest.mark.storage_api
# def test_storage_api_auth_header_expired():
#     headers1 = {'Authorization': EXPIRED_ACCESS_TOKEN, 'Content-Type': CONTENT_TYPE_APPLICATION_JSON}
#     r = requests.post(BASE_URL + '/storage/files', data=json.dumps(STORAGE_REQUEST_BODY), headers=headers1)
#     assert r.status_code == 401
#     # assert r == STORAGE_API_AUTH_HEADER_EXPIRED_ACCESS_TOKEN_RESPONSE
#
#
# @pytest.mark.storage_api
# def test_storage_api_Content_type_header_missing():
#     headers1 = {'Authorization': BASE_TOKEN}
#     r = requests.post(BASE_URL + '/storage/files', data=json.dumps(STORAGE_REQUEST_BODY), headers=headers1)
#     assert r.status_code == 401
#
#
# @pytest.mark.storage_api
# def test_storage_api_contentType_header_value_missing():
#     status, data = Api_functions.storage_api(BASE_URL, STORAGE_REQUEST_BODY, BASE_TOKEN, HEADER_KEY_BLANK_VALUE)
#     assert status == 401
#
#
# @pytest.mark.storage_api
# def test_storage_api_contentType_header_value_invalid():
#     status, data = Api_functions.storage_api(BASE_URL, STORAGE_REQUEST_BODY, BASE_TOKEN, CONTENT_TYPE_URL_ENCODED)
#     assert status == 401
#
#
# @pytest.mark.storage_api
# def test_storage_api_with_put_request():
#     status_code, jsondata = Api_functions.token_api(BASE_URL, DATA_VALID, BASE_TOKEN, CONTENT_TYPE_URL_ENCODED)
#     headers_storage = {'Authorization': jsondata['access_token'], 'Content-Type': CONTENT_TYPE_APPLICATION_JSON}
#     res = requests.put(BASE_URL + '/storage/files', data=json.dumps(STORAGE_REQUEST_BODY), headers=headers_storage)
#     assert res.status_code == 403
#
#
# @pytest.mark.storage_api
# def test_storage_api_with_get_request():
#     status_code, jsondata = Api_functions.token_api(BASE_URL, DATA_VALID, BASE_TOKEN, CONTENT_TYPE_URL_ENCODED)
#     headers_storage = {'Authorization': jsondata['access_token'], 'Content-Type': CONTENT_TYPE_APPLICATION_JSON}
#     res = requests.get(BASE_URL + '/storage/files', data=json.dumps(STORAGE_REQUEST_BODY), headers=headers_storage)
#     assert res.status_code == 403
#
#
# ####################################################################################################
#
# ############################## SUBJECT API NEGATIVE TEST CASES #####################################
#
#
# @pytest.mark.subject_api
# def test_subject_api_request_body_gender_key_blank():
#     status, data = Api_functions.subject_api(BASE_URL, REQUEST_GENDER_KEY_BLANK, BASE_TOKEN,
#                                              CONTENT_TYPE_APPLICATION_JSON)
#     assert status == 400
#
#
# # assert data == INVALID_REQUEST_RESPONSE
#
# @pytest.mark.subject_api
# def test_subject_api_request_body_gender_key_invalid():
#     status, data = Api_functions.subject_api(BASE_URL, REQUEST_GENDER_KEY_INVALID, BASE_TOKEN,
#                                              CONTENT_TYPE_APPLICATION_JSON)
#     assert status == 400
#
#
# # assert data == INVALID_REQUEST_RESPONSE
#
# @pytest.mark.subject_api
# def test_subject_api_request_body_gender_key_missing():
#     status, data = Api_functions.subject_api(BASE_URL, REQUEST_GENDER_KEY_MISSING, BASE_TOKEN,
#                                              CONTENT_TYPE_APPLICATION_JSON)
#     assert status == 400
#
#
# #  assert data == INVALID_REQUEST_RESPONSE
#
# @pytest.mark.subject_api
# def test_subject_api_request_body_gender_key_invalid_data_type():
#     status, data = Api_functions.subject_api(BASE_URL, REQUEST_GENDER_KEY_INVALID_DATA_TYPE, BASE_TOKEN,
#                                              CONTENT_TYPE_APPLICATION_JSON)
#     assert status == 400
#
#
# @pytest.mark.subject_api
# def test_subject_api_request_body_year_of_birth_key_blank():
#     status, data = Api_functions.subject_api(BASE_URL, REQUEST_YEAROFBIRTH_KEY_BLANK, BASE_TOKEN,
#                                              CONTENT_TYPE_APPLICATION_JSON)
#     assert status == 400
#     # assert data == INVALID_REQUEST_RESPONSE
#
#
# @pytest.mark.subject_api
# def test_subject_api_request_body_year_of_birth_key_invalid():
#     status, data = Api_functions.subject_api(BASE_URL, REQUEST_YEAROFBIRTH_KEY_INVALID, BASE_TOKEN,
#                                              CONTENT_TYPE_APPLICATION_JSON)
#     assert status == 400
#
#
# # assert data == INVALID_REQUEST_RESPONSE
#
# @pytest.mark.subject_api
# def test_subject_api_request_body_year_of_birth_key_missing():
#     status, data = Api_functions.subject_api(BASE_URL, REQUEST_YEAROFBIRTH_KEY_MISSING, BASE_TOKEN,
#                                              CONTENT_TYPE_APPLICATION_JSON)
#     assert status == 400
#
#
# #  assert data == INVALID_REQUEST_RESPONSE
#
# @pytest.mark.subject_api
# def test_subject_api_request_body_year_of_birth_key_invalid_data_type():
#     status, data = Api_functions.subject_api(BASE_URL, REQUEST_YEAROFBIRTH_KEY_INVALID_DATA_TYPE, BASE_TOKEN,
#                                              CONTENT_TYPE_APPLICATION_JSON)
#     assert status == 400
#
#
# @pytest.mark.subject_api
# def test_subject_api_request_body_language_key_blank():
#     status, data = Api_functions.subject_api(BASE_URL, REQUEST_LANGUAGE_KEY_BLANK, BASE_TOKEN,
#                                              CONTENT_TYPE_APPLICATION_JSON)
#     assert status == 400
#
#
# #  assert data == INVALID_REQUEST_RESPONSE
#
# @pytest.mark.subject_api
# def test_subject_api_request_body_language_key_invalid():
#     status, data = Api_functions.subject_api(BASE_URL, REQUEST_LANGUAGE_KEY_INVALID, BASE_TOKEN,
#                                              CONTENT_TYPE_APPLICATION_JSON)
#     assert status == 400
#     # assert data == INVALID_GRANT_TYPE_RESPONSE
#
#
# @pytest.mark.subject_api
# def test_subject_api_request_body_language_key_missing():
#     status, data = Api_functions.subject_api(BASE_URL, REQUEST_LANGUAGE_KEY_MISSING, BASE_TOKEN,
#                                              CONTENT_TYPE_APPLICATION_JSON)
#     assert status == 400
#
#
# #  assert data == INVALID_REQUEST_RESPONSE
#
# @pytest.mark.subject_api
# def test_subject_api_request_extra_key_added():
#     status, data = Api_functions.subject_api(BASE_URL, REQUEST_SUBJECT_API_EXTRA_KEY, BASE_TOKEN,
#                                              CONTENT_TYPE_APPLICATION_JSON)
#     assert status == 400
#
#
# ########### SUBJECT API HEADERS VALIDATION ############
#
# # @pytest.mark.subject_api
# # def test_subject_api_invalid_End_Point():
# #     status, data = Api_functions.subject_api(BASE_URL, VALID_SUBJECT_DATA, ACCESS_TOKEN, CONTENT_TYPE_APPLICATION_JSON)
# #     assert status == 403
# #
#
#
# @pytest.mark.subject_api
# def test_subject_api_with_put_request():
#     headers_storage = {'Authorization': ACCESS_TOKEN, 'Content-Type': 'Application/json'}
#     res = requests.put(BASE_URL + '/storage/files', data=json.dumps(VALID_SUBJECT_DATA), headers=headers_storage)
#     assert res.status_code == 403
#
#
# @pytest.mark.subject_api
# def test_subject_api_with_get_request():
#     headers = {'Authorization': ACCESS_TOKEN, 'Content-Type': 'Application/json'}
#     res = requests.get(BASE_URL + '/storage/files', data=json.dumps(VALID_SUBJECT_DATA), headers=headers)
#     assert res.status_code == 403
#
#
# @pytest.mark.subject_api
# def test_subject_api_with_delete_request():
#     headers = {'Authorization': ACCESS_TOKEN, 'Content-Type': 'Application/json'}
#     res = requests.delete(BASE_URL + '/storage/files', data=json.dumps(VALID_SUBJECT_DATA), headers=headers)
#     assert res.status_code == 403
#
#
# ########################## SUBJECT API WITH OTHER REQUEST CALLS ( GET, PUT, DELETE) #########
#
# @pytest.mark.subject_api
# def test_subject_access_token_missing():
#     header1 = {'Content-Type': CONTENT_TYPE_APPLICATION_JSON}
#     r = requests.post(BASE_URL + SUBJECT_END_POINT, data=VALID_SUBJECT_DATA, headers=header1)
#     assert r.status_code == 401
#     # assert data == INVALID_HEADER_RESPONSE
#
#
# @pytest.mark.subject_api
# def test_subject_access_token_value_invalid():
#     status, data = Api_functions.subject_api(BASE_URL, VALID_SUBJECT_DATA, INVALID_ACCESS_TOKEN,
#                                              CONTENT_TYPE_URL_ENCODED)
#     assert status == 401
#
#
# #  assert data == INVALID_HEADER_RESPONSE
#
# @pytest.mark.subject_api
# def test_subject_api_content_type_header_missing():
#     header1 = {'Authorization': ACCESS_TOKEN}
#     r = requests.post(BASE_URL + SCORE_END_POINT, data=VALID_SCORE_DATA, headers=header1)
#     assert r.status_code == 500
#
#
# # assert r == INVALID_HEADER_RESPONSE
#
# # @pytest.mark.subject_api
# # def test_subject_api_contentType_header_value_missing():
# #     status, data = Api_functions.subject_api(BASE_URL, VALID_SUBJECT_DATA, ACCESS_TOKEN, HEADER_KEY_BLANK_VALUE)
# #     assert status == 400
# #     # assert data == INVALID_HEADER_RESPONSE
#
#
# @pytest.mark.subject_api
# def test_subject_api_contentType_header_value_invalid():
#     status, data = Api_functions.subject_api(BASE_URL, VALID_SUBJECT_DATA, ACCESS_TOKEN, CONTENT_TYPE_URL_ENCODED)
#     assert status == 502
#
#
# ##########################################  SCORE  #####################################################################
#
#
# @pytest.mark.score_api
# def test_score_api_request_body_subjectIdentifier_key_blank():
#     status, data = Api_functions.score_api(BASE_URL, REQUEST_SCORE_SUBJECT_IDENTIFIER_KEY_BLANK, ACCESS_TOKEN,
#                                            CONTENT_TYPE_APPLICATION_JSON)
#     assert status == 400
#
#
# # assert data == INVALID_REQUEST_RESPONSE
#
# @pytest.mark.score_api
# def test_score_api_request_body_subjectIdentifier_key_invalid():
#     status, data = Api_functions.score_api(BASE_URL, REQUEST_SCORE_SUBJECT_IDENTIFIER_KEY_INVALID, ACCESS_TOKEN,
#                                            CONTENT_TYPE_APPLICATION_JSON)
#     assert status == 400
#
#
# # assert data == INVALID_REQUEST_RESPONSE
#
# @pytest.mark.score_api
# def test_score_api_request_body_subjectIdentifier_key_missing():
#     status, data = Api_functions.score_api(BASE_URL, REQUEST_SCORE_SUBJECT_IDENTIFIER_KEY_MISSING, ACCESS_TOKEN,
#                                            CONTENT_TYPE_APPLICATION_JSON)
#     assert status == 400
#
#
# #  assert data == INVALID_REQUEST_RESPONSE
#
# @pytest.mark.score_api
# def test_score_api_request_body_subjectIdentifier_key_invalid_data_type():
#     status, data = Api_functions.score_api(BASE_URL, REQUEST_SCORE_SUBJECT_IDENTIFIER_INVALID_DATA_TYPE, ACCESS_TOKEN,
#                                            CONTENT_TYPE_APPLICATION_JSON)
#     assert status == 400
#
#
# @pytest.mark.score_api
# def test_score_api_request_body_fileLocation_key_blank():
#     status, data = Api_functions.score_api(BASE_URL, REQUEST_FILE_LOCATION_KEY_BLANK, ACCESS_TOKEN,
#                                            CONTENT_TYPE_APPLICATION_JSON)
#     assert status == 400
#     # assert data == INVALID_REQUEST_RESPONSE
#
#
# @pytest.mark.score_api
# def test_score_api_request_body_fileLocation_key_invalid():
#     status, data = Api_functions.score_api(BASE_URL, REQUEST_FILE_LOCATION_KEY_INVALID, ACCESS_TOKEN,
#                                            CONTENT_TYPE_APPLICATION_JSON)
#     assert status == 400
#
#
# # assert data == INVALID_REQUEST_RESPONSE
#
# @pytest.mark.score_api
# def test_score_api_request_body_fileLocation_key_missing():
#     status, data = Api_functions.score_api(BASE_URL, REQUEST_FILE_LOCATION_KEY_MISSING, ACCESS_TOKEN,
#                                            CONTENT_TYPE_APPLICATION_JSON)
#     assert status == 400
#
#
# #  assert data == INVALID_REQUEST_RESPONSE
#
#
# @pytest.mark.score_api
# def test_score_api_request_body_measureName_key_blank():
#     status, data = Api_functions.score_api(BASE_URL, REQUEST_MEASURE_NAME_KEY_BLANK, ACCESS_TOKEN,
#                                            CONTENT_TYPE_APPLICATION_JSON)
#     assert status == 400
#
#
# #  assert data == INVALID_REQUEST_RESPONSE
#
# @pytest.mark.score_api
# def test_score_api_request_body_measureName_key_invalid():
#     status, data = Api_functions.score_api(BASE_URL, REQUEST_MEASURE_NAME_KEY_INVALID, ACCESS_TOKEN,
#                                            CONTENT_TYPE_APPLICATION_JSON)
#     assert status == 400
#     # assert data == INVALID_GRANT_TYPE_RESPONSE
#
#
# @pytest.mark.score_api
# def test_score_api_request_body_measureName_key_missing():
#     status, data = Api_functions.score_api(BASE_URL, REQUEST_MEASURE_NAME_KEY_MISSING, ACCESS_TOKEN,
#                                            CONTENT_TYPE_APPLICATION_JSON)
#     assert status == 400
#
#
# #  assert data == INVALID_REQUEST_RESPONSE
#
# @pytest.mark.score_api
# def test_score_api_request_extra_key_added():
#     status, data = Api_functions.score_api(BASE_URL, REQUEST_SCORE_API_EXTRA_KEY, ACCESS_TOKEN,
#                                            CONTENT_TYPE_APPLICATION_JSON)
#     assert status == 400
#
#
# ####### INVALID END POINT ############
#
# # @pytest.mark.score_api
# # def test_score_api_invalid_end_point():
# #     status, data = Api_functions.measure_api(BASE_URL, INVALID_SCORE_END_POINT, ACCESS_TOKEN)
# #     assert status == 403
#
#
# ####################################################  HEADERS ############################
#
# @pytest.mark.score_api
# def test_score_access_token_missing():
#     header1 = {'Content-Type': CONTENT_TYPE_APPLICATION_JSON}
#     r = requests.post(BASE_URL + SCORE_END_POINT, data=VALID_SCORE_DATA, headers=header1)
#     assert r.status_code == 401
#     # assert data == INVALID_HEADER_RESPONSE
#
#
# @pytest.mark.score_api
# def test_score_access_token_value_invalid():
#     status, data = Api_functions.score_api(BASE_URL, VALID_SCORE_DATA, INVALID_ACCESS_TOKEN, CONTENT_TYPE_URL_ENCODED)
#     assert status == 401
#
#
# #  assert data == INVALID_HEADER_RESPONSE
#
# @pytest.mark.score_api
# def test_score_api_content_type_header_missing():
#     header1 = {'Authorization': ACCESS_TOKEN}
#     r = requests.post(BASE_URL + SCORE_END_POINT, data=VALID_SCORE_DATA, headers=header1)
#     assert r.status_code == 404
#
#
# # assert r == INVALID_HEADER_RESPONSE
#
# # @pytest.mark.score_api
# # def test_score_api_contentType_header_value_missing():
# #     status, data = Api_functions.score_api(BASE_URL, VALID_SCORE_DATA, ACCESS_TOKEN, HEADER_KEY_BLANK_VALUE)
# #     assert status == 400
# #     # assert data == INVALID_HEADER_RESPONSE
#
#
# @pytest.mark.score_api
# def test_score_api_contentType_header_value_invalid():
#     status, data = Api_functions.score_api(BASE_URL, VALID_SCORE_DATA, ACCESS_TOKEN, CONTENT_TYPE_URL_ENCODED)
#     assert status == 500
#
#
# ########################## SUBJECT API WITH OTHER REQUEST CALLS ( GET, PUT, DELETE) #########
#
#
# #################################################   SCORE END  ################################################################
#
#
# ################## MEASURE API #################################
#
#
# @pytest.mark.measure_api
# def test_measure_api_invalid_end_point():
#     status, data = Api_functions.measure_api(BASE_URL, INVALID_MEASURE_END_POINT, ACCESS_TOKEN)
#     assert status == 403
#
#
# @pytest.mark.measure_api
# def test_measure_header_missing():
#     r = requests.post(BASE_URL + SCORE_END_POINT)
#     assert r.status_code == 400
#     # assert data == INVALID_HEADER_RESPONSE
#
#
# @pytest.mark.measure_api
# def test_measure_api_invalid_access_token():
#     status, data = Api_functions.measure_api(BASE_URL, MEASURE_END_POINT, INVALID_ACCESS_TOKEN)
#     assert status == 403
#
#
# ########################## MEASURES API WITH OTHER REQUEST CALLS ( GET, PUT, DELETE) #########
#
#
# @pytest.mark.measure_api
# def test_measure_api_with_put_request():
#     headers1 = {'Authorization': ACCESS_TOKEN}
#     r = requests.put(BASE_URL + '/measures', headers=headers1)
#     assert r.status_code == 405
#
#
# @pytest.mark.measure_api
# def test_measure_api_with_get_request():
#     headers1 = {'Authorization': ACCESS_TOKEN}
#     r = requests.get(BASE_URL + '/measures', headers=headers1)
#     assert r.status_code == 403
#
#
# @pytest.mark.measure_api
# def test_measure_api_with_delete_request():
#     headers1 = {'Authorization': ACCESS_TOKEN}
#     r = requests.delete(BASE_URL + '/measures', headers=headers1)
#     assert r.status_code == 405
#
#
# ############################ MEASURE ID API ################################
#
#
# @pytest.mark.measure_id_api
# def test_measure_id_api_invalid_end_point():
#     status, data = Api_functions.measure_id_api(BASE_URL, INVALID_MEASURE_ID_END_POINT, ACCESS_TOKEN)
#     assert status == 403
#
#
# @pytest.mark.measure_id_api
# def test_measure_id_header_missing():
#     r = requests.get(BASE_URL + '/measures/' + str(MEASURE_ID_END_POINT))
#     assert r.status_code == 401
#     # assert data == INVALID_HEADER_RESPONSE
#
#
# @pytest.mark.measure_id_api
# def test_measure_id_api_invalid_access_token():
#     status, data = Api_functions.measure_id_api(BASE_URL, MEASURE_ID_END_POINT, INVALID_ACCESS_TOKEN)
#     assert status == 401
#
#
# ########################## MEASURES ID API WITH OTHER REQUEST CALLS ( GET, PUT, DELETE) #########
#
# @pytest.mark.measure_id_api
# def test_measure_id_api_with_put_request():
#     headers1 = {'Authorization': ACCESS_TOKEN}
#     r = requests.put(BASE_URL + '/measures/' + str(MEASURE_ID_END_POINT), headers=headers1)
#     assert r.status_code == 403
#
#
# @pytest.mark.measure_id_api
# def test_measure_id_api_with_get_request():
#     headers1 = {'Authorization': ACCESS_TOKEN}
#     r = requests.post(BASE_URL + '/measures/' + str(MEASURE_ID_END_POINT), headers=headers1)
#     assert r.status_code == 403
#
#
# @pytest.mark.measure_id_api
# def test_measure_id_api_with_delete_request():
#     headers1 = {'Authorization': ACCESS_TOKEN}
#     r = requests.delete(BASE_URL + '/measures/' + str(MEASURE_ID_END_POINT), headers=headers1)
#     assert r.status_code == 403
