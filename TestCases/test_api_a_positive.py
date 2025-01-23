# import json
# import pytest
# from TestCases import Api_functions
# from TestCases.Support import assertion
# from Variables.variable import *
# from TestCases.Support import helper
#
# # ---------------- Get the Base64 --------------------------------#
#
# base64secrets = helper.get_base64secrets(CLIENT_ID, CLIENT_SECRET)
# print(base64secrets)
#
# BASE_TOKEN = 'Basic ' + base64secrets
# # FIRST TOKEN API CALL TO GET ACCESS TOKEN #
# #
# status_code, json_data = Api_functions.token_api(BASE_URL, VALID_TOKEN_DATA, BASE_TOKEN, CONTENT_TYPE_URL_ENCODED)
# ACCESS_TOKEN = json_data['access_token']
#
#
#
#
# # SECOND MEASURES API CALL TO GET MEASURE ID #
#
# status, measure_json = Api_functions.measure_api(BASE_URL, MEASURE_END_POINT, ACCESS_TOKEN)
# MEASURE_ID_END_POINT = measure_json['measures'][0]['id']
#
# # THIRD SUBJECT API CALL TO GET SUBJECT IDENTIFIER #
#
# status, subject_json = Api_functions.subject_api(BASE_URL, VALID_SUBJECT_DATA, ACCESS_TOKEN,
#                                                  CONTENT_TYPE_APPLICATION_JSON)
# SUB_IDENTIFIER = subject_json['subjectIdentifier']
#
# VALID_STORAGE_DATA = {
#     "fileType": "wav",
#     "countryCode": "US",
#     "subjectIdentifier": SUB_IDENTIFIER
# }
#
#
# @pytest.mark.token_api
# def test_token_api():
#     status, data = Api_functions.token_api(BASE_URL, VALID_TOKEN_DATA, BASE_TOKEN, CONTENT_TYPE_URL_ENCODED)
#     assert status == 200
#     assertion.assert_valid_schema(data, 'token_schema.json')
#
#
# @pytest.mark.measure_api
# def test_get_measure_api():
#     status, data = Api_functions.measure_api(BASE_URL, MEASURE_END_POINT, ACCESS_TOKEN)
#     assert status == 200
#     assertion.assert_valid_schema(data, 'measure_schema.json')
#
#
# @pytest.mark.subject_api
# def test_subject_api():
#     status, data = Api_functions.subject_api(BASE_URL, VALID_STORAGE_DATA, ACCESS_TOKEN, CONTENT_TYPE_APPLICATION_JSON)
#     assert status == 201
#     assertion.assert_valid_schema(data, 'subject_schema.json')
#
#
# @pytest.mark.measure_id_api
# def test_measure_id_api():
#     status, data = Api_functions.measure_id_api(BASE_URL, MEASURE_ID_END_POINT, ACCESS_TOKEN)
#     assert status == 200
#     assertion.assert_valid_schema(data, 'measure_id_schema.json')
#
#
# @pytest.mark.storage_api
# def test_storage_api():
#     status, data = Api_functions.storage_api(BASE_URL, VALID_STORAGE_DATA, ACCESS_TOKEN, CONTENT_TYPE_APPLICATION_JSON)
#     assert status == 201
#     assertion.assert_valid_schema(data, 'storage_schema.json')
#
#
# @pytest.mark.score_api
# def test_score_api():
#     status, score_json_data = Api_functions.score_api(BASE_URL, VALID_SCORE_DATA, ACCESS_TOKEN,
#                                                       CONTENT_TYPE_APPLICATION_JSON)
#     assert status == 201
#     assertion.assert_valid_schema(score_json_data, 'score_schema.json')
#
#
#
#
#
#
# # @pytest.mark.storage_api
# # def test_audio_file_upload():
# #     status_code = Api_functions.audio_file_upload(STORAGE_SIGNED_URL)
# #     assert status_code == 200
#
