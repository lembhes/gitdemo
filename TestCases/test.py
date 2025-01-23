# # import json
# # import pytest
# # from TestCases import API_Calls
# # from TestCases.Support import assertion
# # from Variables.variable import *
# from TestCases.Support import helper
#
# # base64secrets = helper.get_base64secrets(CLIENT_ID, CLIENT_SECRET)
# #
# # BASE_TOKEN = 'Basic ' + base64secrets
# #
# # # FIRST TOKEN API CALL TO GET ACCESS TOKEN #
# #
# # status_code, json_data = API_Calls.token_api(BASE_URL, VALID_TOKEN_DATA, BASE_TOKEN, CONTENT_TYPE_URL_ENCODED)
# # print(status_code)
# # ACCESS_TOKEN = json_data['access_token']
# #
# # print("Access token-> ", ACCESS_TOKEN)
# # # SECOND MEASURES API CALL TO GET MEASURE ID #
# #
# # # status, measure_json = API_Calls.mea(BASE_URL, MEASURE_END_POINT, ACCESS_TOKEN)
# # # print(status)
# # # MEASURE_ID_END_POINT = measure_json['measures'][0]['id']
# #
# # # THIRD SUBJECT API CALL TO GET SUBJECT IDENTIFIER #
# #
# #
# # VALID_SUBJECT_DATA = {
# #     "yearOfBirth": "1900",
# #     "gender": "male",
# #     "language": "Hindi"
# # }
# #
# # status, subject_json = API_Calls.subject_api(BASE_URL, VALID_SUBJECT_DATA, ACCESS_TOKEN,
# #                                              CONTENT_TYPE_APPLICATION_JSON)
# # print(status)
# #
# # SUB_IDENTIFIER = subject_json['userIdentifier']
# #
# # # --------------------------------- #
# #
# # status, data = API_Calls.update_subject_details(BASE_URL, SUB_IDENTIFIER, UPDATE_SUBJECT_DATA, ACCESS_TOKEN)
# # print(status)
# # print(data)
# #
# # VALID_STORAGE_DATA = {
# #     "fileType": "wav",
# #     "countryCode": "US",
# #     "userIdentifier": SUB_IDENTIFIER
# # }
# #
# # status_code, response_json = API_Calls.storage_api(BASE_URL, VALID_STORAGE_DATA, ACCESS_TOKEN,
# #                                                    CONTENT_TYPE_APPLICATION_JSON)
# #
# # STORAGE_SIGNED_URL = response_json['signedURL']
# # FILE_PATH = response_json['filePath']
# #
# # AUDIO_FILE_PATH = 'C:\\Users\\gs-2509\\Desktop\\Postman\\14611201-B2DD-49FA-91F7-75FD368AC050_34_42.wav'
# #
# # status_code = API_Calls.upload_sample_file(STORAGE_SIGNED_URL, AUDIO_FILE_PATH)
# #
# #
# # def test():
# #     file = helper.urlEncoder(FILE_PATH)
# #     print(file)
# #     res = API_Calls.get_audio_file(BASE_URL, file, ACCESS_TOKEN)
# #     return res
# #
# #
# # print("yes:", test())
# #
# # # MEASURE_NAME = 'emotional-resilience'
# # #
# # # status, data = API_Calls.get_questionnaire_ID_required_for_measure(BASE_URL, MEASURE_NAME, ACCESS_TOKEN)
# # # QUESTIONNAIRE_ID = data['questionnaire']['id']
# # # QUESTIONNAIRE_LANGUAGES = data['questionnaire']['languages'][0]
# # # print(status)
# # # print(data)
# # #
# # # status, response_json = API_Calls.get_questionnaire_required_for_measure(BASE_URL, QUESTIONNAIRE_ID,
# # #                                                                          QUESTIONNAIRE_LANGUAGES,
# # #                                                                          ACCESS_TOKEN)
# # # print(status, response_json)
# # #
# # # QUES_ID = response_json['id']
# # # LANGUAGE = response_json['language']
# # #
# # # QUESTIONNAIRE_BODY = {
# # #     "questionnaire": {
# # #         "id": QUES_ID,
# # #         "language": LANGUAGE,
# # #         "userIdentifier": SUB_IDENTIFIER,
# # #         "respondedAt": "1994-11-05T13:15:30Z",
# # #         "questionResponses": [
# # #             {
# # #                 "optionIndex": 1
# # #             },
# # #             {
# # #                 "optionIndexes": [
# # #                     0,
# # #                     1
# # #                 ]
# # #             },
# # #             {
# # #                 "response": 3
# # #             },
# # #             {
# # #                 "response": "36C"
# # #             }
# # #         ]
# # #     }
# # # }
# # #
# # # st, da = API_Calls.submit_questionnaire_response(BASE_URL, QUESTIONNAIRE_BODY, ACCESS_TOKEN)
# # # print(st, da)
# # # QUESTIONNAIRE_RESPONSE_ID = response_json['id']
# # #
# # # # ----------------------------------------
# # #
# # # VALID_SCORE_DATA = {
# # #     "userIdentifier": SUB_IDENTIFIER,
# # #     "filePath": FILE_PATH,
# # #     "questionnaireResponseId": QUESTIONNAIRE_RESPONSE_ID,
# # #     "measureName": MEASURE_NAME
# # # }
# # #
# # # status_code, response_json = API_Calls.score_api(BASE_URL, VALID_SCORE_DATA, ACCESS_TOKEN,
# # #                                                  CONTENT_TYPE_APPLICATION_JSON)
# # # print(status_code, response_json)
# # #
#
# QUESTIONNAIRE_BODY = {
#     "questionnaire": {
#         "id": "12ac123",
#         "language": "hindi",
#         "userIdentifier": "Id123Ide",
#         "respondedAt": "1994-11-05T13:15:30Z",
#         "questionResponses": [
#             {
#                 "optionIndex": 1
#             },
#             {
#                 "optionIndexes": [
#                     0,
#                     2
#                 ]
#             },
#             {
#                 "isSkipped": True
#             },
#             {
#                 "response": "36C"
#             }
#         ]
#     }
# }
#
# D_CP = QUESTIONNAIRE_BODY['questionnaire'].copy()
# #
# # for i in range(len(D_CP)):
# #     D = helper.get_random_pairs(D_CP)
# #     DATA = {'questionnaire': D}
# #     print(DATA)
#
# # n = helper.factorial(len(D_CP))
# # for i in range(n):
# #     print(i)
#
#
#
#
# # a = {'d2844857-5498-40f9-b00b-4d19ffa8c9c8': {'name': 'sh', 'username': '5aug1@yopmail.net', 'phone_number': '+18044064234', 'year_of_birth': '0000001982', 'gender': 'Female'}, '36b8955e-369f-493e-a9f7-6943af0fdb8a': {'name': 'Shruti', 'username': 'pager13@yopmail.com', 'phone_number': '+15417083275', 'year_of_birth': '0000002002', 'gender': 'Female'}}
# #
# # for data in a:
# #     print(a.values())
# #     print(a[0])
# #     print(data['name'])
# #     print(data['username'])
# #     print(data['phone_number'])
# #     print(data['year_of_birth'])
# #     print(data['gender'])
# #
# #
#
# # c = []
# # a = {'Username': '065971bc-5784-4c51-929d-e3901949ee57', 'Attributes': [{'Name': 'sub', 'Value': '065971bc-5784-4c51-929d-e3901949ee57'}, {'Name': 'birthdate', 'Value': '0000002001'}, {'Name': 'email_verified', 'Value': 'false'}, {'Name': 'gender', 'Value': 'Male'}, {'Name': 'custom:created_by', 'Value': 'self'}, {'Name': 'profile', 'Value': '0'}, {'Name': 'phone_number_verified', 'Value': 'true'}, {'Name': 'name', 'Value': 'sachin'}, {'Name': 'nickname', 'Value': 'participant'}, {'Name': 'phone_number', 'Value': '+12075737634'}, {'Name': 'email', 'Value': 'teston26@yopmail.com'}], 'UserCreateDate': 'datetime.datetime(2019, 12, 13, 14, 12, 57, 806000, tzinfo=tzlocal())', 'UserLastModifiedDate': 'datetime.datetime(2020, 8, 6, 20, 27, 31, 859000, tzinfo=tzlocal())', 'Enabled': True, 'UserStatus': 'RESET_REQUIRED'}
# # print(a['Attributes'])
# # for b in a['Attributes']:
# #     c.append(b['Name'])
# #     if 'email' in c and 'phone_number' in c:
# #         print('YES')
# #
# #
# # dicts = [
# #      { "name": "Tom", "age": 10 },
# #      { "name": "Mark", "age": 5 },
# #      { "name": "Pam", "age": 7 },
# #      { "name": "Dick", "age": 12 }
# #  ]
# # for key in dicts:
# #     if "Tom" in key["name"] and "Pam" in key["name"]:
# #         print('YES')
#
#
# #!/bin/python
# #
# # import math
# # import os
# # import random
# # import re
# # import sys
# #
# # # Complete the hourglassSum function below.
# # def hourglassSum(arr):
# #     pass
# #
# # matrix = []
# # print("Enter the entries row-wise:")
# #
# # for i in range(6):  # A for loop for row entries
# #     a = []
# #     for j in range(6):  # A for loop for column entries
# #         a.append(int(input()))
# #     matrix.append(a)
# #
# # for i in range(6):
# #     for j in range(6):
# #         print(matrix[i][j], end=" ")
# #     print()
#
#
#
#
# a = ["[ c9ec9eda-2969-43cf-bf95-99d7c7d41971 ] [ INFO ] 2021-01-18 11:25:04,778 - root.get_inference_data:139 - inference_data : {'id': 'd997a9eb-3604-4c1b-a3a6-5fe36b270e5d', 'score': Decimal('98.83333333333333'), 'inferred_at': datetime.datetime(2021, 1, 18, 11, 25, 4), 'performed_activity_group_id': '8eb97202-6d5c-4f2b-a98b-7cb5187b1131'}", "[ 79a55d2d-f95a-47e8-b699-821aa11fbf4e ] [ INFO ] 2021-01-18 11:30:04,299 - root.get_inference_data:139 - inference_data : {'id': 'd997a9eb-3604-4c1b-a3a6-5fe36b270e5d', 'score': Decimal('98.83333333333333'), 'inferred_at': datetime.datetime(2021, 1, 18, 11, 25, 4), 'performed_activity_group_id': '8eb97202-6d5c-4f2b-a98b-7cb5187b1131'}", '[ 79a55d2d-f95a-47e8-b699-821aa11fbf4e ] [ INFO ] 2021-01-18 11:30:04,316 - chalicelib.session_outcome_service.get_session_details:235 - calculating screening result for performed_activity_group_id: 8eb97202-6d5c-4f2b-a98b-7cb5187b1131']
# print(a[0].split(' ')[1])
# print(a[1].split(' ')[1])
#
# b = ["[ ba3b2239-ac91-4f9e-8ee9-db0203ea6f96 ] [ INFO ] 2021-01-18 11:07:42,199 - root.get_inference_data:139 - inference_data : {'id': 'cd5ca24a-db17-4e53-a107-5f5660f90959', 'score': Decimal('97.66666666666667'), 'inferred_at': datetime.datetime(2021, 1, 18, 11, 7, 36), 'performed_activity_group_id': 'd719192c-dd21-44d5-bfd8-21c4e4dd4b7e'}"]
# print(len(b))
#
#
#
#
#
#
#
