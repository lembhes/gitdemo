## This file_path will be segrgate the measures data and prepare one dictonary which will have key as perform actiivty group ID"

import json
import boto3
import pandas as pd
import sys
import segregation
import pdb
import study_wise_report
import settings
import meta_keys_validation
from sqlalchemy import create_engine, MetaData, select, Table, text



META_DICT = {}
ANS_DICT = {}
JSON_FILE_DATA = {}

AUDIO_ACTIVITIES = ['SENTENCE_READING', 'TIMED_RECORDING', 'BASELINE', 'FOCUS', 'FREE_SPEECH', 'PASSAGE_READING', 'MEMORY' ]

def get_system_score_from_db(key):
    sql = 'select score from inference where performed_activity_group_id=:performed_activity_group_id'
    stmt = text(sql)
    stmt = stmt.bindparams(performed_activity_group_id=key)
    result_set = settings.ENGINE.execute(stmt)
    score= ''
    for row in result_set:
        score = str(float(round(row[0], 2)))
    return score

def get_study_performed_information(key):
    sql = 'select distinct(study_name) from performed_activity_master where performed_activity_group_id= :performed_activity_group_id AND study_name NOT IN (\'-1\')'
    stmt = text(sql)
    stmt = stmt.bindparams(performed_activity_group_id=key)
    result_set = settings.ENGINE.execute(stmt)
    flag = 0
    for row in result_set:
        return row[0]

    if not flag:
        response = ''
        return response


def get_qos_status(raw_data_name):
    
    sql = 'select reject from manual_qos where performed_activity_id in (select id from performed_activity_master where raw_data_name = :raw_data_name)'

    stmt = text(sql)
    stmt = stmt.bindparams(raw_data_name=raw_data_name)
    result_set = settings.ENGINE.execute(stmt)
    status = []
    for row in result_set:
        if row[0] == True:
            return 'QoS_Rejected'
        else:
            return 'QoS_Accepted'
            
    return 'QoS_Pending' 

def get_db_status_for_this_file(key, raw_data_name):
    sql = 'select count(user_id) from performed_activity_master where performed_activity_group_id = :key and raw_data_name = :raw_data_name'

    stmt = text(sql)
    stmt = stmt.bindparams(key=key, raw_data_name=raw_data_name)
    result_set = settings.ENGINE.execute(stmt)
    flag = 0
    for row in result_set:
        return row[0]

    if not flag:
        return flag 


def measure_update_dictonary_as_per_PAGI_id(file_type, file_path ):
    json_data, raw_meta = study_wise_report.getjson(file_path)
    json_data_keys = json_data.keys()
    if 'performed_activity_group_id' in json_data_keys:
        JSON_FILE_DATA[file_path] = json_data
        
        pagi = json_data['performed_activity_group_id']
        if file_type == 'meta_file':
            if pagi in META_DICT.keys():
                META_DICT[pagi].append(file_path)
            else:
                META_DICT[pagi] = [file_path]
        else:
            #Update ANS_DICT as below:  
            local_ans_dict = {}
            measure_id = json_data['measure_id']
            
            if 'inference_data' in json_data_keys:
                system_inference_score = json_data['inference_data']['inference_score']
                system_inference_score = str(float(round(system_inference_score, 2)))
            else:
                system_inference_score = ''

            if 'questionnaire_data' in json_data_keys:
                user_refined_score = json_data['questionnaire_data'][0]['question_responses'][0]['score']
            else:
                user_refined_score = ''

            json_data['user_refined_score'] = user_refined_score
            json_data['system_inference_score'] = system_inference_score
            json_data['answer_file_path'] = file_path
            
            local_ans_dict.update({measure_id:json_data})
            
            
            #local_ans_dict.update({measure_id:{'measure_id':measure_id, 'user_refined_score': user_refined_score, 'system_inference_score':system_inference_score}})
            #
            if pagi in ANS_DICT.keys():
                ANS_DICT[pagi].update(local_ans_dict)
            else:
                ANS_DICT[pagi] = local_ans_dict

    else:
        print("meta file not contains the performed_activity_group_id:", file_path)

def measure_each_meta_releated_data(key, meta_data, audio_count_dict):
    try:
        meta_data_keys = meta_data.keys()
        audio_count_dict_keys = audio_count_dict.keys()

        audio_count_dict['performed_activity_group_id'] = key

        #Validating the meta file
        meta_status = meta_keys_validation.meta_keys_validation(meta_data, 'META_FILE', meta_data['meta_file_path'])
        if meta_status == True:
            if 'meta_validation_pass' not in audio_count_dict_keys:
                audio_count_dict['meta_validation_pass'] = 1
            else:
                audio_count_dict['meta_validation_pass'] += 1
        else:
            if 'meta_validation_fail' not in audio_count_dict_keys:
                audio_count_dict['meta_validation_fail'] = 1
            else:
                audio_count_dict['meta_validation_fail'] += 1



        if 'activity' in meta_data_keys:
            activity = meta_data['activity']
        else:
            activity = 'UNKONWN'
        qos_status = get_qos_status(meta_data['raw_data_name'])
        if qos_status not in audio_count_dict_keys:
            audio_count_dict[qos_status] = 1
        else:
            audio_count_dict[qos_status] += 1

        activity_count = 1
        for s in audio_count_dict_keys:
            if activity in s:
                activity_count += 1

        if meta_data['audio_file_size'] == "Audio File with Zero Byte":
            audio_count_dict[str(activity) + '_' + str(activity_count)] = 0
        else:
            audio_count_dict[str(activity) + '_' + str(activity_count)] = 1

        if 'access_code' in meta_data_keys:
            audio_count_dict['study_Name'] = meta_data['access_code']
            audio_count_dict['study_version_id'] = meta_data['study_version_id']
            audio_count_dict['mode'] = 'Research Mode'

        else:
            audio_count_dict['study_Name'] = 'NA'
            audio_count_dict['mode'] = 'Measure Mode'
    

        if 'measure_names' in meta_data_keys:
            audio_count_dict['HealthCheckName'] = ','.join(meta_data['measure_names'])

        if 'measures' in meta_data_keys:
            audio_count_dict['measure_ids'] = meta_data['measures']


        if 'measure_version_ids' in meta_data_keys:
            #audio_count_dict['measure_version_ids'] = ','.join(meta_data['measure_version_ids'])
            audio_count_dict['measure_version_ids'] = ','.join([str(i) for i in meta_data['measure_version_ids']])

        if 'manufacturer' in meta_data_keys:
            audio_count_dict['manufacturer'] = meta_data['manufacturer']

        if 'device_time_zone' in meta_data_keys:
            audio_count_dict['device_time_zone'] = meta_data['device_time_zone']
    
        if 'device_local_country_code' in meta_data_keys:
            audio_count_dict['device_local_country_code'] = meta_data['device_local_country_code']
    
        if 'app_version' in meta_data_keys:
            audio_count_dict['app_version'] = meta_data['app_version']
    
        if 'user_id' in meta_data_keys:
            audio_count_dict['user_id'] = meta_data['user_id']

        if 'start_time' in meta_data_keys:
            audio_count_dict['start_time'] = meta_data['start_time']
    
        if 'token' in meta_data_keys:
            audio_count_dict['token_name'] = meta_data['token']
        else:
            audio_count_dict['token_name'] = 'NA'
            
        audio_count_dict['Total_Audio_files_in_DB'] = get_db_status_for_this_file(key, meta_data['raw_data_name'])



        return audio_count_dict

    except:
        print ( 'Method name is audio_count_per_session_per_activity ')
        print (key)

# logic for total audio files per session
def total_measure_audio_count_per_session(key, audio_count_dict):

    audio_file_count = 0
    audio_count_dict_keys = audio_count_dict.keys()
    for audio_count_dict_key in audio_count_dict_keys:
        if audio_count_dict_key[:-2] in AUDIO_ACTIVITIES:
            audio_file_count += audio_count_dict[audio_count_dict_key]
    audio_count_dict['Total_Audio_files_on_S3'] = audio_file_count

    if 'QoS_Rejected' not in audio_count_dict_keys:
        audio_count_dict['QoS_Rejected'] = ''

    if 'QoS_Accepted' not in audio_count_dict_keys:
        audio_count_dict['QoS_Accepted'] = ''

    if 'QoS_Pending' not in audio_count_dict_keys:
        audio_count_dict['QoS_Pending'] = ''

    #Calculate the user_refined_score and system_inference_score
    #{'01e4fc7a-ab26-4231-93d3-8ba2079c669b': {8: {'measure_id': 8, 'user_refined_score': 74, 'system_inference_score': ''}}, '69dcdb6a-3b1f-4f0d-9df3-346d08e48a4a': {8: {'measure_id': 8, 'user_refined_score': 92, 'system_inference_score': ''}}}

    if key in ANS_DICT:
        for measure_id in audio_count_dict['measure_ids']:
            if measure_id in ANS_DICT[key].keys():
                audio_count_dict['user_refined_score'] = ANS_DICT[key][measure_id]['user_refined_score']
                audio_count_dict['system_inference_score'] = ANS_DICT[key][measure_id]['system_inference_score']
                meta_status = meta_keys_validation.meta_keys_validation(ANS_DICT[key][measure_id], 'ANSWER_FILE', ANS_DICT[key][measure_id]['answer_file_path'])
                if meta_status == True:
                    if 'meta_validation_pass' not in audio_count_dict_keys:
                        audio_count_dict['meta_validation_pass'] = 1
                    else:
                        audio_count_dict['meta_validation_pass'] += 1
                else:
                    if 'meta_validation_fail' not in audio_count_dict_keys:
                        audio_count_dict['meta_validation_fail'] = 1
                    else:
                        audio_count_dict['meta_validation_fail'] += 1




    else:
        audio_count_dict['system_inference_score'] = get_system_score_from_db(key)
        audio_count_dict['user_refined_score'] = ''

    #Adding study performed with this session
    audio_count_dict['study_performed_in_this_session'] = get_study_performed_information(key)


    if 'meta_validation_pass' not in audio_count_dict.keys():
        audio_count_dict['meta_validation_pass'] = ''

    if 'meta_validation_fail' not in audio_count_dict.keys():
        audio_count_dict['meta_validation_fail'] = ''



    #Changing from list to string
    
    try:
        audio_count_dict['measure_ids'] = ','.join([str(i) for i in audio_count_dict['measure_ids']])
    except:
        pass
    
    if audio_count_dict['QoS_Rejected'] != '':
        audio_count_dict['REJECTED_SESSION'] = 1
    else:
        audio_count_dict['REJECTED_SESSION'] = 0

    return audio_count_dict


def update_measure_summary_df(measure_final_df):
    measure_summary_df = pd.DataFrame()
    total_session = 0
    total_unique_users_per_hc = 0
    total_audio_file_with_score = 0
    total_refinement_done_by_users = 0
    total_audio_file = 0
    total_qos_accepted = 0
    tota_qos_rejected = 0
    total_qos_pending = 0
    total_rejected_session = 0
    total_user_who_performed_more_than_5_session = 0
    summary_dict = {}
    final_summary_df = pd.DataFrame()
    hc_list = measure_final_df['HealthCheckName'].unique()
    

    for hc_name in hc_list:    
        summary_dict['Health Check'] = hc_name
        DF_EACH_HC  = measure_final_df.loc[measure_final_df['HealthCheckName'] == hc_name]
        summary_dict['# Session']= len(DF_EACH_HC.index)
        summary_dict['# Unique Users']= DF_EACH_HC['user_id'].nunique()
        summary_dict['# Audio Files on S3']= DF_EACH_HC['Total_Audio_files_on_S3'].sum()
        summary_dict['# Audio Files in DB']= DF_EACH_HC['Total_Audio_files_in_DB'].sum()
        summary_dict['# Audio file with score']= len(DF_EACH_HC[(DF_EACH_HC['system_inference_score'].apply(str) != '')].index)
        summary_dict['# Audio file without score'] = summary_dict['# Audio Files on S3'] - summary_dict['# Audio file with score']
        summary_dict['# Refinement done by users']= len(DF_EACH_HC[(DF_EACH_HC['user_refined_score'].apply(str) != '')].index)

        summary_dict['# Session with Study Perfomed']= len(DF_EACH_HC[(DF_EACH_HC['study_performed_in_this_session'].apply(str) != '')].index)        
        
        summary_dict['# QoS Accepted']= len(DF_EACH_HC[(DF_EACH_HC['QoS_Accepted'].apply(str) != '')].index)        
        summary_dict['# QoS Rejected']= len(DF_EACH_HC[(DF_EACH_HC['QoS_Rejected'].apply(str) != '')].index)        
        summary_dict['# QoS Pending']= len(DF_EACH_HC[(DF_EACH_HC['QoS_Pending'].apply(str) != '')].index)        
        summary_dict['# Rejected Session']= len(DF_EACH_HC[(DF_EACH_HC['REJECTED_SESSION'] != 0)].index)

        summary_dict['Date'] = settings.Report_Date
        #total_user_who_performed_more_than_5_session = 

        #col_uni_val={}
        #for i in DF_EACH_HC['user_id'].unique():
        #    col_uni_val[i] = len(DF_EACH_HC[i].unique())    
        #DF_EACH_HC['user_id'].value_counts() >= 5#


        summary_df = pd.DataFrame.from_dict([summary_dict], orient='columns')
        final_summary_df = final_summary_df.append(summary_df)        

    
    return final_summary_df



def extract_measures_data( input_measure_dict):

    measure_final_df = pd.DataFrame()
    
    print ('measure analysis started')
    input_measure_dict_keys = input_measure_dict.keys()
    for file_path in input_measure_dict_keys:

        if file_path.endswith('.meta'):
            audio_file_name = file_path.replace('meta', 'wav')
            if audio_file_name not in input_measure_dict_keys:
                print('Only Measure Meta present, Measure Audio file_path not present, expecting audio file_path: ',audio_file_name)
                continue
            measure_update_dictonary_as_per_PAGI_id('meta_file', file_path)

        if file_path.endswith('.answers'):
            measure_update_dictonary_as_per_PAGI_id('ans_file', file_path)

    for key in META_DICT.keys():
        audio_count_dict = {}
        for meta_file_path in META_DICT[key]:
            try:
                meta_data = JSON_FILE_DATA[meta_file_path]
                meta_data['meta_file_path_name'] = meta_file_path.split('/')[-1]
                meta_data['meta_file_path'] = meta_file_path
                
                # Logic for file_size
                audio_file_name = meta_file_path.replace('meta', 'wav')
                if input_measure_dict[audio_file_name]['Size'] == 0:
                    meta_data['audio_file_size'] = "Audio File with Zero Byte"
                    print ('Audio File with Zero Byte',audio_file_name )
                else:
                    meta_data['audio_file_size'] = input_measure_dict[audio_file_name]['Size']
   
                # Here come the logic to calculate the total audio sample collected
                audio_count_dict = measure_each_meta_releated_data(key, meta_data, audio_count_dict)
            except:
                print('Issue in recording entry for audio file_path :', meta_file_path.split('.')[0])
                continue
        
        audio_count_dict = total_measure_audio_count_per_session(key, audio_count_dict)
        audio_count_dict_df = pd.DataFrame.from_dict([audio_count_dict], orient='columns')
        measure_final_df = measure_final_df.append(audio_count_dict_df)
        
    final_summary_df = update_measure_summary_df(measure_final_df)
    
    
    return measure_final_df, final_summary_df
