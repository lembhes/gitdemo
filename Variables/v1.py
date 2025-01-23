BASE_URL = "https://d2p2crbjmhql12.cloudfront.net/platform/v1"

BASE_TOKEN = 'Basic NzFzdnN1dmU1YTJvcnQ5NGN0Ym9uZjBqbGo6OW1kZjFya3Y5cHRzYmY3cTVvajgzNjE2cnU5djVhM3I0aDYzbTk0bWtibm9mN3VvZXAw'


TOKEN_END_POINT = '/oauth2/token'

VALID_TOKEN_DATA = {
    'grant_type': 'client_credentials',
    'scope': 'sonde-platform/storage.write sonde-platform/measures.list sonde-platform/'
             'measures.read sonde-platform/subject.write sonde-platform/scores.write'}

SUBJECT_END_POINT = '/subjects'

VALID_SUBJECT_DATA = {
    "gender": "MALE/FEMALE",
    "yearOfBirth": 1985,
    "language": "ENGLISH"
}

STORAGE_END_POINT = '/storage/files'
VALID_STORAGE_DATA = {
    "fileType": "wav",
    "countryCode": "US",
    "subjectIdentifier": "fz6xlATjw"
}

SCORE_END_POINT = '/inference/scores'
VALID_SCORE_DATA = {
  "subjectIdentifier": "wiNODNcmI",
  "fileLocation": "s3://dev-sondeplatform-x-subject-metadata/1b147047-4431-4488-82bb-aabdaae182de/voice-samples/da12a2b4-7755-408d-842e-74d5b379a325.wav",
  "measureName": "emotional-resilience"
}
MEASURE_END_POINT = '/measures'


INVALID_BASE_URL = "https://api.stage.sondeservices.com/platform/v1"

INVALID_TOKEN_END_POINT = '/oauth2/token'
INVALID_TOKEN_DATA = {
    'grant_type': 'client_credentials',
    'scope': 'sonde-platform/storage.write sonde-platform/measures.list sonde-platform/'
             'measures.read sonde-platform/subject.write sonde-platform/scores.write'}

INVALID_BASE_TOKEN = "Basic MzFjcG81Y2dyMGxqb3B2dW9lN28yMnVuYmw6cjg3aHJrbGp1OXY4OTMxZTZiNXUxZXNjZDNrampqaTlmMGVhamloM3N2cDRkZ2pocWs5"

INVALID_SUBJECT_END_POINT = '/invalid'
INVALID_SUBJECT_DATA = {
    "gender": 123,
    "yearOfBirth": 1985,
    "language": "ENGLISH"
}

INVALID_STORAGE_END_POINT = '/storage/files'
INVALID_STORAGE_DATA = {
    "fileType": "wav",
    "countryCode": "US",
    "subjectIdentifier": "fz6xlATjw"
}

INVALID_SCORE_END_POINT = '/inference/scores'

INVALID_SCORE_DATA = {
    "subjectIdentifier": "wiNODNcmI",
    "fileLocation": "https://s3.aws.sonde-default-samples/activities/65e56d22498f.wav",

}

INVALID_MEASURE_END_POINT ='dfsdsjdgsd'
INVALID_MEASURE_ID_END_POINT ='gdhsgds'

# files = {'command': open(r'C:\Users\gsc-30427\Desktop\audio\c45164f2-cdc7-48f9-ad08-0fd621ae3be9_82da7ad9-bdeb-4fe6-bc80-138fdb7038d1_1247_1613_Nikhil_marathi_alz', 'rb')}
#
#


AUTHORIZATION = BASE_TOKEN

CONTENT_TYPE_URL_ENCODED = 'application/x-www-form-urlencoded'

CONTENT_TYPE_APPLICATION_JSON = 'application/json'



DATA_VALID = {'grant_type': 'client_credentials', 'client_id': '39433422erweerww',
              'scope': 'sonde-platform/storage.write sonde-platform/measures.list sonde-platform/measures.read sonde-platform/subject.write sonde-platform/scores.write'}


STORAGE_REQUEST_BODY = {"fileType": "wav", "countryCode": "US", "subjectIdentifier": "wiNODNXcm"}



INVALID_BASE_URL = "https://api.stage.sondeservices.com/platform1/v1"


REQUEST_SCOPE_KEY_BLANK = {'grant_type': 'client_credentials', 'client_id': '39433422erweerww', 'scope': ''}

REQUEST_SCOPE_KEY_INVALID = {'grant_type': 'client_credentials', 'client_id': '39433422erweerww',
                             'scope': 'sonde-platform/storage123.write sonde-platform/measures.list sonde-platform/measures.read sonde-platform/subject.write sonde-platform/scores.write'}

REQUEST_SCOPE_KEY_MISSING = {'grant_type': 'client_credentials', 'client_id': '39433422erweerww'}

REQUEST_EXTRA_KEY_ADDED = {'auth': 'testauth', 'grant_type': 'client_credentials', 'client_id': '39433422erweerww',
                           'scope': 'sonde-platform/storage.write sonde-platform/measures.list sonde-platform/measures.read sonde-platform/subject.write sonde-platform/scores.write'}

REQUEST_CLIENT_ID_KEY_BLANK = {'grant_type': 'client_credentials', 'client_id': '',
                               'scope': 'sonde-platform/storage.write sonde-platform/measures.list sonde-platform/measures.read sonde-platform/subject.write sonde-platform/scores.write'}

REQUEST_CLIENT_ID_KEY_INVALID = {'grant_type': 'client_credentials', 'client_id': '39433422erweeeerww',
                                 'scope': 'sonde-platform/storage.write sonde-platform/measures.list sonde-platform/measures.read sonde-platform/subject.write sonde-platform/scores.write'}

REQUEST_CLIENT_ID_KEY_MISSING = {'grant_type': 'client_credentials',
                                 'scope': 'sonde-platform/storage.write sonde-platform/measures.list sonde-platform/measures.read sonde-platform/subject.write sonde-platform/scores.write'}

REQUEST_GRANT_TYPE_KEY_BLANK = {'grant_type': '', 'client_id': '39433422erweerww',
                                'scope': 'sonde-platform/storage.write sonde-platform/measures.list sonde-platform/measures.read sonde-platform/subject.write sonde-platform/scores.write'}

REQUEST_GRANT_TYPE_KEY_INVALID = {'grant_type': 'client_credentials123', 'client_id': '39433422erweerww',
                                  'scope': 'sonde-platform/storage.write sonde-platform/measures.list sonde-platform/measures.read sonde-platform/subject.write sonde-platform/scores.write'}

REQUEST_GRANT_TYPE_KEY_MISSING = {'client_id': '39433422erweerww',
                                  'scope': 'sonde-platform/storage.write sonde-platform/measures.list sonde-platform/measures.read sonde-platform/subject.write sonde-platform/scores.write'}

INVALID_REQUEST_RESPONSE = {"error": "invalid_request"}

INVALID_GRANT_TYPE_RESPONSE = {
    "error": "unsupported_grant_type"
}

INVALID_BASE_TOKEN = 'Basic MzFjcG81Y2dyMGxqb3B2dW9lN28yMnVuYmw6cjg3aHJrbGp1OXY4OTMxZTZiNXUxZXNjZDNrampqaThlmMGVhamloM3N2cDRkZ2pocWs51'

EXPIRED_ACCESS_TOKEN = 'eyJraWQiOiIwcDEyN1FaMkhFc1FibWZJaEdxNU95M05jelhQZDE1MmtmKzZtZDByYlwvdz0iLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiIzMWNwbzVjZ3IwbGpvcHZ1b2U3bzIydW5ibCIsInRva2VuX3VzZSI6ImFjY2VzcyIsInNjb3BlIjoic29uZGUtcGxhdGZvcm1cL3N1YmplY3Qud3JpdGUgc29uZGUtcGxhdGZvcm1cL3Njb3Jlcy53cml0ZSBzb25kZS1wbGF0Zm9ybVwvc3RvcmFnZS53cml0ZSBzb25kZS1wbGF0Zm9ybVwvbWVhc3VyZXMubGlzdCBzb25kZS1wbGF0Zm9ybVwvbWVhc3VyZXMucmVhZCIsImF1dGhfdGltZSI6MTU4MjcwMDAyMSwiaXNzIjoiaHR0cHM6XC9cL2NvZ25pdG8taWRwLnVzLWVhc3QtMS5hbWF6b25hd3MuY29tXC91cy1lYXN0LTFfdFpjSWRuS1hiIiwiZXhwIjoxNTgyNzAzNjIxLCJpYXQiOjE1ODI3MDAwMjEsInZlcnNpb24iOjIsImp0aSI6ImQwMWY0NmFiLWZjYWMtNGRiYi04ZWM3LWI4MmQxY2UyN2FjOCIsImNsaWVudF9pZCI6IjMxY3BvNWNncjBsam9wdnVvZTdvMjJ1bmJsIn0.NIKT64Uy6EgmnAkVfrKWidu-p7Jm9K2A8L3WPWVEcG6uibga0a3rGH1hOmMMG-iJxOTDuGSNdtmv4S1GebD9x3gjd3RjOi-t-C_RIjx94AChS0hsAC4FEKqJGElDK_HNAomNiRv-mga2g4sch3PAPEYnMdFC9IAMyr-941of3aNijjdZOlxUGKpYEyilnYW6xkHFrsA29jifbIFYpsgc7nfA9KhL8wt4lA1QsSNOIIxX_gaoaGynn2EB4e8N5TWs0CPBwgmjGBDqLOTA7m3aMWWBWHYFnQwhdOowrhnOsEcYYE-XUW0ZJs86_a2jqv0clApQ3DDBjuffngJz6nS_qQ'

HEADER_KEY_BLANK_VALUE = ''

INVALID_HEADER_RESPONSE = {"error": "invalid_client"}

# Invalid data for Storage API

REQUEST_FILE_TYPE_KEY_BLANK = {"fileType": " ", "countryCode": "US", "subjectIdentifier": "wiNODNXcm"}

REQUEST_FILE_TYPE_KEY_VALUE_INVALID = {"fileType": "jpeg ", "countryCode": "US", "subjectIdentifier": "wiNODNXcm"}

REQUEST_FILE_TYPE_KEY_MISSING = {"countryCode": "US", "subjectIdentifier": "wiNODNXcm"}

STORAGE_REQUEST_EXTRA_KEY_ADDED = {"auth": "auth123", "fileType": "wav ", "countryCode": "US",
                                   "subjectIdentifier": "wiNODNXcm"}

REQUEST_COUNTRY_CODE_KEY_BLANK = {"fileType": "wav ", "countryCode": " ", "subjectIdentifier": "wiNODNXcm"}

REQUEST_COUNTRY_CODE_KEY_INVALID = {"fileType": "wav", "countryCode": "EU", "subjectIdentifier": "wiNODNXcm"}

REQUEST_COUNTRY_CODE_KEY_MISSING = {"fileType": "wav", "subjectIdentifier": "wiNODNXcm"}

REQUEST_COUNTRY_CODE_NOT_SUPPORTED = {"fileType": "wav ", "countryCode": "GH", "subjectIdentifier": "wiNODNXcm"}

REQUEST_COUNTRY_CODE_NOT_REGISTERED = {"fileType": " wav", "countryCode": "IN", "subjectIdentifier": "wiNODNXcm"}

REQUEST_SUBJECT_IDENTIFIER_KEY_BLANK = {"fileType": "wav", "countryCode": "US", "subjectIdentifier": " "}

REQUEST_SUBJECT_IDENTIFIER_KEY_INVALID = {"fileType": "wav", "countryCode": "US", "subjectIdentifier": "wiNODNXcccmyu7"}

REQUEST_SUBJECT_IDENTIFIER_KEY_MISSING = {"fileType": "wav", "countryCode": "US"}

STORAGE_API_INVALID_REQUEST_RESPONSE = {"error": "invalid_request"}

INVALID_GRANT_TYPE_RESPONSE = {
    "error": "unsupported_grant_type"
}

INVALID_BASE_TOKEN = 'Basic MzFjcG81Y2dyMGxqb3B2dW9lN28yMnVuYmw6cjg3aHJrbGp1OXY4OTMxZTZiNXUxZXNjZDNrampqaThlmMGVhamloM3N2cDRkZ2pocWs51'

EXPIRED_ACCESS_TOKEN = 'eyJraWQiOiIwcDEyN1FaMkhFc1FibWZJaEdxNU95M05jelhQZDE1MmtmKzZtZDByYlwvdz0iLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiIzMWNwbzVjZ3IwbGpvcHZ1b2U3bzIydW5ibCIsInRva2VuX3VzZSI6ImFjY2VzcyIsInNjb3BlIjoic29uZGUtcGxhdGZvcm1cL3N1YmplY3Qud3JpdGUgc29uZGUtcGxhdGZvcm1cL3Njb3Jlcy53cml0ZSBzb25kZS1wbGF0Zm9ybVwvc3RvcmFnZS53cml0ZSBzb25kZS1wbGF0Zm9ybVwvbWVhc3VyZXMubGlzdCBzb25kZS1wbGF0Zm9ybVwvbWVhc3VyZXMucmVhZCIsImF1dGhfdGltZSI6MTU4MjcwMDAyMSwiaXNzIjoiaHR0cHM6XC9cL2NvZ25pdG8taWRwLnVzLWVhc3QtMS5hbWF6b25hd3MuY29tXC91cy1lYXN0LTFfdFpjSWRuS1hiIiwiZXhwIjoxNTgyNzAzNjIxLCJpYXQiOjE1ODI3MDAwMjEsInZlcnNpb24iOjIsImp0aSI6ImQwMWY0NmFiLWZjYWMtNGRiYi04ZWM3LWI4MmQxY2UyN2FjOCIsImNsaWVudF9pZCI6IjMxY3BvNWNncjBsam9wdnVvZTdvMjJ1bmJsIn0.NIKT64Uy6EgmnAkVfrKWidu-p7Jm9K2A8L3WPWVEcG6uibga0a3rGH1hOmMMG-iJxOTDuGSNdtmv4S1GebD9x3gjd3RjOi-t-C_RIjx94AChS0hsAC4FEKqJGElDK_HNAomNiRv-mga2g4sch3PAPEYnMdFC9IAMyr-941of3aNijjdZOlxUGKpYEyilnYW6xkHFrsA29jifbIFYpsgc7nfA9KhL8wt4lA1QsSNOIIxX_gaoaGynn2EB4e8N5TWs0CPBwgmjGBDqLOTA7m3aMWWBWHYFnQwhdOowrhnOsEcYYE-XUW0ZJs86_a2jqv0clApQ3DDBjuffngJz6nS_qQ'

HEADER_KEY_BLANK_VALUE = ' '

STORAGE_API_AUTH_HEADER_MISSING_RESPONSE = {
    "message": "Missing Authentication Token"
}

STORAGE_API_AUTH_HEADER_INVALID_RESPONSE = {
    "message": "Authorization header requires 'Credential' parameter. Authorization header requires 'Signature' parameter. Authorization header requires 'SignedHeaders' parameter. Authorization header requires existence of either a 'X-Amz-Date' or a 'Date' header. Authorization={{access_token1}}"
}

STORAGE_API_AUTH_HEADER_EXPIRED_ACCESS_TOKEN_RESPONSE = {
    "message": "Authorization header requires 'Credential' parameter. Authorization header requires 'Signature' parameter. Authorization header requires 'SignedHeaders' parameter. Authorization header requires existence of either a 'X-Amz-Date' or a 'Date' header. Authorization={{access_token1}}"
}

STORAGE_API_CONTENT_TYPE_HEADER_MISSING_RESPONSE = {
    "message": "Authorization header requires 'Credential' parameter. Authorization header requires 'Signature' parameter. Authorization header requires 'SignedHeaders' parameter. Authorization header requires existence of either a 'X-Amz-Date' or a 'Date' header. Authorization=eyJraWQiOiIwcDEyN1FaMkhFc1FibWZJaEdxNU95M05jelhQZDE1MmtmKzZtZDByYlwvdz0iLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiIzMWNwbzVjZ3IwbGpvcHZ1b2U3bzIydW5ibCIsInRva2VuX3VzZSI6ImFjY2VzcyIsInNjb3BlIjoic29uZGUtcGxhdGZvcm1cL3N1YmplY3Qud3JpdGUgc29uZGUtcGxhdGZvcm1cL3Njb3Jlcy53cml0ZSBzb25kZS1wbGF0Zm9ybVwvc3RvcmFnZS53cml0ZSBzb25kZS1wbGF0Zm9ybVwvbWVhc3VyZXMubGlzdCBzb25kZS1wbGF0Zm9ybVwvbWVhc3VyZXMucmVhZCIsImF1dGhfdGltZSI6MTU4MjcwMDAyMSwiaXNzIjoiaHR0cHM6XC9cL2NvZ25pdG8taWRwLnVzLWVhc3QtMS5hbWF6b25hd3MuY29tXC91cy1lYXN0LTFfdFpjSWRuS1hiIiwiZXhwIjoxNTgyNzAzNjIxLCJpYXQiOjE1ODI3MDAwMjEsInZlcnNpb24iOjIsImp0aSI6ImQwMWY0NmFiLWZjYWMtNGRiYi04ZWM3LWI4MmQxY2UyN2FjOCIsImNsaWVudF9pZCI6IjMxY3BvNWNncjBsam9wdnVvZTdvMjJ1bmJsIn0.NIKT64Uy6EgmnAkVfrKWidu-p7Jm9K2A8L3WPWVEcG6uibga0a3rGH1hOmMMG-iJxOTDuGSNdtmv4S1GebD9x3gjd3RjOi-t-C_RIjx94AChS0hsAC4FEKqJGElDK_HNAomNiRv-mga2g4sch3PAPEYnMdFC9IAMyr-941of3aNijjdZOlxUGKpYEyilnYW6xkHFrsA29jifbIFYpsgc7nfA9KhL8wt4lA1QsSNOIIxX_gaoaGynn2EB4e8N5TWs0CPBwgmjGBDqLOTA7m3aMWWBWHYFnQwhdOowrhnOsEcYYE-XUW0ZJs86_a2jqv0clApQ3DDBjuffngJz6nS_qQ"
}

COUNTRY_CODE_NOT_SUPPORTED_RESPONSE = {

    "code": "COUNTRY_NOT_SUPPORTED",
    "message": "The input country GH is not supported"
}

COUNTRY_NOT_REGISTERED_RESPONSE = {
    "code": "UNREGISTERED_COUNTRY",
    "message": "You are not registered for country IN"
}

############################################################################
####################### SUBJECT API DATA ###################################
############################################################################




REQUEST_GENDER_KEY_BLANK={
  "gender": "",
  "yearOfBirth": 1985,
  "language": "ENGLISH"
}


REQUEST_GENDER_KEY_INVALID={
  "gender": "GENDER",
  "yearOfBirth": 1985,
  "language": "ENGLISH"
}


REQUEST_GENDER_KEY_INVALID_DATA_TYPE={
  "gender": 1234,
  "yearOfBirth": 1985,
  "language": "ENGLISH"
}


REQUEST_GENDER_KEY_MISSING={
  "yearOfBirth": 1985,
  "language": "ENGLISH"
}


REQUEST_YEAROFBIRTH_KEY_BLANK={
  "gender": "MALE",
  "yearOfBirth": '',
  "language": "ENGLISH"
}


REQUEST_YEAROFBIRTH_KEY_INVALID={
  "gender": "MALE",
  "yearOfBirth": 123456,
  "language": "ENGLISH"
}


REQUEST_YEAROFBIRTH_KEY_MISSING={
  "gender": "MALE",
  "language": "ENGLISH"
}

REQUEST_YEAROFBIRTH_KEY_INVALID_DATA_TYPE={
  "gender": "MALE",
    "yearOfBirth":"2121",
  "language": "ENGLISH"
}






REQUEST_LANGUAGE_KEY_BLANK={
  "gender": "MALE",
  "yearOfBirth": 1985,
  "language": ""
}


REQUEST_LANGUAGE_KEY_INVALID={
  "gender": "MALE",
  "yearOfBirth": 1985,
  "language": 1234
}


REQUEST_LANGUAGE_KEY_MISSING={
  "gender": "MALE",
  "yearOfBirth": 1985
}


REQUEST_SUBJECT_API_EXTRA_KEY={
  "gender": "MALE",
  "yearOfBirth": 1985,
  "language": "ENGLISH",
    "name":"test"
}


############################################################################
####################### SCORE API DATA ###################################
############################################################################



REQUEST_SCORE_SUBJECT_IDENTIFIER_KEY_BLANK={
  "subjectIdentifier": "",
  "fileLocation": "s3://dev-sondeplatform-x-subject-metadata/1b147047-4431-4488-82bb-aabdaae182de/voice-samples/da12a2b4-7755-408d-842e-74d5b379a325.wav",
  "measureName": "emotional-resilience"
}


REQUEST_SCORE_SUBJECT_IDENTIFIER_KEY_INVALID={
  "subjectIdentifier": "wiNODNcmIYWEUWEWDSDS",
  "fileLocation": "s3://dev-sondeplatform-x-subject-metadata/1b147047-4431-4488-82bb-aabdaae182de/voice-samples/da12a2b4-7755-408d-842e-74d5b379a325.wav",
  "measureName": "emotional-resilience"
}


REQUEST_SCORE_SUBJECT_IDENTIFIER_INVALID_DATA_TYPE={
  "subjectIdentifier": 12345,
  "fileLocation": "s3://dev-sondeplatform-x-subject-metadata/1b147047-4431-4488-82bb-aabdaae182de/voice-samples/da12a2b4-7755-408d-842e-74d5b379a325.wav",
  "measureName": "emotional-resilience"
}


REQUEST_SCORE_SUBJECT_IDENTIFIER_KEY_MISSING={
  "fileLocation": "s3://dev-sondeplatform-x-subject-metadata/1b147047-4431-4488-82bb-aabdaae182de/voice-samples/da12a2b4-7755-408d-842e-74d5b379a325.wav",
  "measureName": "emotional-resilience"
}


REQUEST_FILE_LOCATION_KEY_BLANK={
  "subjectIdentifier": "wiNODNcmI",
  "fileLocation": "",
  "measureName": "emotional-resilience"
}

REQUEST_FILE_LOCATION_KEY_INVALID={
  "subjectIdentifier": "wiNODNcmI",
  "fileLocation": "s3://devMDSDKSJDKSDASASAS-sondeplatform-x-subject-metadata/1b147047-4431-4488-82bb-aabdaae182de/voice-samples/da12a2b4-7755-408d-842e-74d5b379a325.wav",
  "measureName": "emotional-resilience"
}

REQUEST_FILE_LOCATION_KEY_MISSING={
  "subjectIdentifier": "wiNODNcmI",
  "measureName": "emotional-resilience"
}



REQUEST_MEASURE_NAME_KEY_BLANK={
  "subjectIdentifier": "wiNODNcmI",
  "fileLocation": "s3://dev-sondeplatform-x-subject-metadata/1b147047-4431-4488-82bb-aabdaae182de/voice-samples/da12a2b4-7755-408d-842e-74d5b379a325.wav",
  "measureName": ""
}

REQUEST_MEASURE_NAME_KEY_INVALID={
  "subjectIdentifier": "wiNODNcmI",
  "fileLocation": "s3://dev-sondeplatform-x-subject-metadata/1b147047-4431-4488-82bb-aabdaae182de/voice-samples/da12a2b4-7755-408d-842e-74d5b379a325.wav",
  "measureName": "INVALID"
}


REQUEST_MEASURE_NAME_KEY_MISSING={
  "subjectIdentifier": "wiNODNcmI",
  "fileLocation": "s3://dev-sondeplatform-x-subject-metadata/1b147047-4431-4488-82bb-aabdaae182de/voice-samples/da12a2b4-7755-408d-842e-74d5b379a325.wav",

}


REQUEST_MEASURE_NAME_KEY_INVALID_DATA_TYPE={
  "subjectIdentifier": "wiNODNcmI",
  "fileLocation": "s3://dev-sondeplatform-x-subject-metadata/1b147047-4431-4488-82bb-aabdaae182de/voice-samples/da12a2b4-7755-408d-842e-74d5b379a325.wav",
  "measureName": 123455
}



REQUEST_SCORE_API_EXTRA_KEY={
  "subjectIdentifier": "wiNODNcmI",
  "fileLocation": "s3://dev-sondeplatform-x-subject-metadata/1b147047-4431-4488-82bb-aabdaae182de/voice-samples/da12a2b4-7755-408d-842e-74d5b379a325.wav",
  "measureName": "emotional-resilience",
    "NAME":"SACHIN"
}

























MISSING_COUNTRY_CODE_RESPONSE = {
    "code": "INVALID_REQUEST",
    "missingFields": [
        {
            "fieldName": "countryCode",
            "message": "countryCodeis required field"
        }
    ]

}

INVALID_COUNTRY_CODE_RESPONSE = {
    "code": "INVALID_REQUEST",
    "invalidFields": [
        {
            "fieldName": "countryCode",
            "message": "It should be exact two charcters"
        }
    ]
}

MISSING_SUBJECT_IDENTIFIER_RESPONSE = {
    "code": "INVALID_REQUEST",
    "missingFields": [
        {
            "fieldName": "subjectIdentifier",
            "message": "subjectIdentifier is  required field"
        }
    ]

}

INVALID_SUBJECT_IDENTIFIER_RESPONSE = {
    "code": "INVALID_REQUEST",
    "invalidFields": [
        {
            "fieldName": "subjectIdentifier",
            "message": "It should be exact two charcters"
        }
    ]
}

MISSING_FILE_TYPE_RESPONSE = {
    "code": "INVALID_REQUEST",
    "missingFields": [
        {
            "fieldName": "fileType",
            "message": "fileType is  required field"
        }
    ]

}

INVALID_FILE_TYPE_RESPONSE = {
    "code": "INVALID_REQUEST",
    "invalidFields": [
        {
            "fieldName": "fileType",
            "message": "It should be exact two charcters"
        }
    ]
}
