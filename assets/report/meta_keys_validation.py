#README
#This file is for validating the Meta and Answer file against the standard JSON file provided
#Output will be True or Fail 
import os
import sys
from uuid import UUID
import base64
from sqlalchemy import create_engine, MetaData, select, Table, text
import settings
import pdb


def validate_UUID(uuid_list, file_name):
    global SUCCESS
    try:
        for uuid_string in uuid_list:
            val = UUID(uuid_string, version=4)
        return True
    except:
        print ('UUID string is not in correct format, file name :%s, key %s' %(file_name,uuid_string))
        SUCCESS = False
        return False

def get_user_role( user_id):
    
    sql = 'select role from "user" where id = :user_id'
    stmt = text(sql)
    stmt = stmt.bindparams(user_id=user_id)
    result_set = settings.ENGINE.execute(stmt)
    response = []

    for row in result_set:
        response.append(dict(row))
    
    if len(response) < 1:
        return None
    else:
        return response[0]['role']

def get_meta_mode(json_data):
    keys = json_data.keys()
    Mode = None
    if 'study_name' in keys and ('measures' in keys or 'measure_id' in keys) :
        Mode = 'HC_AT_STUDY_MODE'
    elif 'study_name' in keys and not ('measures' in keys or 'measure_id' in keys):
        Mode = 'STUDY_MODE'
    elif ('measures' in keys or 'measure_id' in keys) and not 'study_name' in keys:
        Mode = 'MEASURE_MODE'
    return Mode


def study_role_wise_validation(file_name, json_data, user_role):
    global SUCCESS
    meta_keys = json_data.keys()
    
    if user_role == 'technician':
        if not 'site_name' in meta_keys and 'site_id' in meta_keys and 'site_specific_id' in meta_keys:
            print ('One of the key from site_name, site_id, site_specific_id missing from the technicians meta file', file_name)
            SUCCESS = False
            return
    
    if user_role == 'participant':
        if 'site_name' in meta_keys or 'site_id' in meta_keys or 'site_specific_id' in meta_keys:
            print ('One of the key from site_name, site_id, site_specific_id present in the user meta file', file_name)
            SUCCESS = False
            return

def compare_with_standard(json_data, file_name, flow, category ):
    global SUCCESS

    try:
        #print ("verifyin key type : %s"%category)
        if category not in settings.STUDY_REFERENCE_DATA[flow].keys():
            print ('category name \'%s\' is not available in Standard JSON file :%s'%(category,file_name))
            print ("Error in validation for file name %s"%file_name)
            SUCCESS = False
            return 

        for key in settings.STUDY_REFERENCE_DATA[flow][category].keys():
            if key in json_data.keys():
                if type(json_data[key]) == type(settings.STUDY_REFERENCE_DATA[flow][category][key]):
                    pass
                else:
                    print ("data type of key \'%s\' mismatched file : %s" %(key,file_name))
                    SUCCESS = False
            else:
                print ("key \'%s\' is not present in file %s" %(key,file_name))
                SUCCESS = False
    except:
        print ("Error in validation for file name %s"%file_name)
        SUCCESS = False


def study_answer_validation(list_of_answer_data, file_name ):
    global SUCCESS
    q_response_id = []

    try:
        for sequence in range(len(list_of_answer_data)):
            if 'question_responses' in list_of_answer_data[sequence].keys():
                for question_no in range(len(list_of_answer_data[sequence]['question_responses'])):
                    compare_with_standard(list_of_answer_data[sequence]['question_responses'][question_no], file_name, 'STUDY_KEYS', "question_responses" )
            else:
                print ("key \"question_responses\" not present in file name : %s is not matching standard" %(file_name))
                SUCCESS = False

            #for keys except 'question_responses'
            compare_with_standard(list_of_answer_data[sequence], file_name, 'STUDY_KEYS', 'questionnaire_data' )
            if 'questionnaire_response_id' in list_of_answer_data[sequence].keys():
                validate_UUID([list_of_answer_data[sequence]['questionnaire_response_id']], file_name)
            q_response_id.append(list_of_answer_data[sequence]['questionnaire_response_id'])
        
        if len(set(q_response_id)) > 1:
            SUCCESS = False
            print ("Getting multiple \'q_response_id\' in single file"%file_name)
    except:
        print ("Error in validation for file name %s"%file_name)
        SUCCESS = False



def study_validation(json_data, file_name, file_type):

    global SUCCESS
    global META_STATUS

    activity_name = json_data['activity']
    
    #for common keys 
    compare_with_standard(json_data, file_name, 'STUDY_KEYS', 'COMMON_META_KEYS' )
    if 'performed_activity_group_id' in json_data.keys():
        validate_UUID([json_data['performed_activity_group_id']], file_name)

    #for audio activity related keys
    if file_type == 'META_FILE':
        compare_with_standard(json_data, file_name, 'STUDY_KEYS', activity_name )
        
    #For Answer File Verification
    elif file_type == 'ANSWER_FILE':
        if 'questionnaire_data' in json_data.keys():
            study_answer_validation(json_data['questionnaire_data'], file_name)
        else:
            print ('\'questionnaire_data\' is not present in file name %s' % file_name)


    #Technician mode
    if 'site_id' in json_data.keys():
        compare_with_standard(json_data, file_name, 'STUDY_KEYS', 'TECHNICIAN_MODE' )
    #User mode
    else:
        compare_with_standard(json_data, file_name, 'STUDY_KEYS', 'USER_MODE' )

    if SUCCESS == False :
        META_STATUS = False
        print ('Key mismatch in File: %s' %file_name)


def hc_validation(json_data, file_name, file_type):
    global SUCCESS
    global META_STATUS

    json_keys = json_data.keys()
    
    #for common keys 
    compare_with_standard(json_data, file_name, 'HC_KEYS', 'COMMON_KEYS' )

    #for audio activity related keys
    if file_type == 'META_FILE':
        compare_with_standard(json_data, file_name, 'HC_KEYS', 'META_ONLY_KEYS' )
        validate_UUID([json_data['performed_activity_group_id']], file_name)
        

    #For Answer File Verification
    elif file_type == 'ANSWER_FILE':

        compare_with_standard(json_data, file_name, 'HC_KEYS', 'ANSWERS_ONLY_KEYS' )

        if 'questionnaire_data' in json_keys and  'inference_data' in json_keys and  'question_responses' in json_data['questionnaire_data'][0].keys():
            compare_with_standard(json_data['questionnaire_data'][0], file_name, 'HC_KEYS', 'QUESTIONNAIRE_DATA' )

            question_responses = json_data['questionnaire_data'][0]["question_responses"][0]
            compare_with_standard(question_responses, file_name, 'HC_KEYS', 'QUESTION_RESPONSES' )

            compare_with_standard(json_data['inference_data'], file_name, 'HC_KEYS', 'INFERANCE_DATA' )

        else:
            
            SUCCESS = False
            print ('\'questionnaire_data\' or \'inference_data\' or \' question_responses\' is not present in file name %s' % file_name)

        #Verification of the UUID 
        refinement_of_inference_id  = json_data['refinement_of_inference_id'] 
        performed_activity_group_id = json_data['performed_activity_group_id']
        questionnaire_response_id   = json_data['questionnaire_data'][0]['questionnaire_response_id']
        inference_data_id           = json_data['inference_data']['id']
        inference_data_performed_activity_group_id = json_data['inference_data']['performed_activity_group_id']
        
        uuid_list = [refinement_of_inference_id, performed_activity_group_id, questionnaire_response_id, inference_data_id, inference_data_performed_activity_group_id]

        validate_UUID(uuid_list, file_name)


    if SUCCESS == False :
        META_STATUS = False


def meta_keys_validation(json_data, file_type,file_name):
    global SUCCESS
    global META_STATUS
    global MODE 
    
    META_STATUS = True
    SUCCESS = True

    MODE = get_meta_mode(json_data)
    
    if MODE == None:
        print ('Error in file, not able to calcluate the Capture Mode', file_name)
    
    if MODE == 'STUDY_MODE':
        try:
            #This part of code design for capturing issue such as user mode meta files should never have few keys and vice versa.
            user_role = None
            if 'user_id' in json_data.keys() and 'exercise_id' in json_data.keys():
                user_role = get_user_role( json_data['user_id']) #user role can be technician or participant
                if user_role:
                    study_role_wise_validation(file_name, json_data, user_role)
                else:
                    print('Not able to get the user role from the DB for user id', json_data['user_id'])
                study_validation(json_data, file_name, file_type)
            else:
                print ('user id and exercise_id is not present in the meta file')
        except:
            print ("Getting error in Validating the Meta or Answer file:", file_name)

    if MODE == 'MEASURE_MODE':
        hc_validation(json_data, file_name, file_type)

    if MODE == 'HC_AT_STUDY_MODE':
        hc_validation(json_data, file_name, file_type)
        compare_with_standard(json_data, file_name, 'STUDY_SCORING', 'COMMON_KEYS' )


    if META_STATUS == False:
        print ('Meta validation get failed for file', file_name)
    return META_STATUS



if __name__ == "__main__":
    print ("Getting Started")
    if len (sys.argv) != 2 :
        print ('Usage: python script_data_sanity.py <enter Study name>')
        sys.exit (1)
    study_name = sys.argv[1]
    prefix='activities/study/' + study_name
    main()
    
