
# README
# This file is for processing Study data 


import os
import json
import boto3
import pandas as pd
import sys
from sqlalchemy import create_engine, MetaData, select, Table, text
import pdb
import datetime
from datetime import date
import study_wise_report
import settings
import meta_keys_validation

AUDIO_ACTIVITIES = ['SENTENCE_READING', 'TIMED_RECORDING', 'BASELINE', 'FOCUS', 'FREE_SPEECH', 'PASSAGE_READING', 'MEMORY' ]




def get_user_questionnaire(key):

    sql = 'select title from questionnaire where id in (select distinct questionnaire_id from questionnaire_response_item where performed_activity_group_id = :performed_activity_group_id AND study_name NOT IN (\'-1\'))'
    stmt = text(sql)
    stmt = stmt.bindparams(performed_activity_group_id=key)
    result_set = settings.ENGINE.execute(stmt)
    user_questionnaire = []
    for row in result_set:
        user_questionnaire.append(dict(row)['title'])
    return user_questionnaire


def get_activity_questionnaire(list_of_ids):
    ids = []
    for id in list_of_ids:
        ids.append(int(id))

    sql = 'select title from questionnaire where id in (' + ','.join(map(str, ids)) + ')'
    stmt = text(sql)
    result_set = settings.ENGINE.execute(stmt)
    activity_questionnaire = []
    for row in result_set:
        activity_questionnaire.append(dict(row)['title'])
    return activity_questionnaire


# for getting the activity count language wise
def get_activity_language_count(key, token, ind):
    try:
        sql = 'select a.title,t.specific_content,language,act_expression from activity a inner join study_version_activity sva on a.id = sva.activity_id inner ' \
            'join task t on a.id = t.activity_id and sva.study_version_id = ' \
            '(select id from study_version where study_id = (select id from study where token = :token_name) and index = :index)'
    
        stmt = text(sql)
        stmt = stmt.bindparams(token_name=token, index=ind)
        result_set = settings.ENGINE.execute(stmt)
        response = []
        for row in result_set:
            response.append(dict(row))
        audio_dic = {}
        questionnaire_dict = {}
    
        for activity_content in response:
    
            activity_language_count = 0
    
            if len(activity_content['act_expression']) == 0:
                activity_day_list = ['ALL_DAY']
            else:
                activity_day_list = activity_content['act_expression']['value'][0]['values']
    
    
            if 'Check In (Remote)' in activity_content['title']:
                if activity_content['specific_content']['questionnaire_ids']: # this condition for studies without questionnaire ID's
                    for each_day in activity_day_list:
                        questionnaire_dict.update({each_day:{}})
                        questionnaire_dict[each_day][activity_content['language']] = get_activity_questionnaire(activity_content['specific_content']['questionnaire_ids'])
                continue
            
            elif 'Focus' in activity_content['title'] or 'Memory' in activity_content['title']:
                activity_language_count += activity_content['specific_content']['number_of_required_run-throughs']
            
            else:
                activity_language_count += 1
            
            #New code for Expression and Language
            # {12: {'WEDNESDAY': {'ENGLISH': 1, 'HINDI':2, None:4 }, 'ALL_DAY': {'ENGLISH': 1, None:2, 'HINDI':2} } } 
            for each_day in activity_day_list:
                if each_day not in audio_dic.keys():
                    audio_dic.update({each_day:{}})
    
                if activity_content['language'] in audio_dic[each_day].keys():
                    audio_dic[each_day][activity_content['language']] += activity_language_count
                else:
                    audio_dic[each_day][activity_content['language']] = activity_language_count
    
        return audio_dic, questionnaire_dict
    except:
        pdb.set_trace()
        print ( 'Getting error in method name "get_activity_language_count" ' ) 
        print (key)
        

# to get the laguages selected by user or technician
def get_user_language(meta_data):
    if 'site_id' not in meta_data.keys():
        # get the language for user
        sql = 'select language from public.user u,person_language p where p.personinfo_id=u.personinfo_id and id= :userid'
        stmt = text(sql)
        stmt = stmt.bindparams(userid=meta_data['user_id'])
    
    else:
        # get the language for technician
        sql = 'select p.language from site_participant S , person_language p where p.personinfo_id =s.personinfo_id and s.site_id = :siteid and s.site_specific_id= :sitename'
        stmt = text(sql)
        stmt = stmt.bindparams(siteid=meta_data['site_id'], sitename=meta_data['site_specific_id'])
    
    result_set = settings.ENGINE.execute(stmt)
    user_language = []
    for row in result_set:
        user_language.append(dict(row)['language'])
    #user_language = ['ENGLISH','MARATHI','HINDI','KANNADA','BENGALI','TAMIL','TELUGU','MALAYALAM','GUJARATI']
    
    return user_language

def get_site_specific_site_name(user_id):
    
    sql = 'select sp.site_specific_id,site.name from site_participant sp inner join "user" u on sp.personinfo_id = u.personinfo_id inner join site site on site.id = sp.site_id where u.id = :user_id'
    
    #sql = 'select title from questionnaire where id in (select distinct questionnaire_id from questionnaire_response_item where performed_activity_group_id = :performed_activity_group_id)'
    stmt = text(sql)
    stmt = stmt.bindparams(user_id=user_id)
    result_set = settings.ENGINE.execute(stmt)

    response = []    
    rows_amount = 0

    for row in result_set:
        response.append(row[0])
        response.append(row[1])
        return response

    if not rows_amount:
        response = ['Unknown Site Specific ID', 'Unknown Site Name'] 
        return response


def get_qos_status(raw_data_name):
    
    #sql = 'select title from questionnaire where id in (select distinct questionnaire_id from questionnaire_response_item where performed_activity_group_id = :performed_activity_group_id)'

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

# to calculate the session end time
def get_completed_time(exer_id):
    sql = 'select completed_at from exercise_details where id = :id'
    stmt = text(sql)
    stmt = stmt.bindparams(id=exer_id)
    result_set = settings.ENGINE.execute(stmt)
    response = []
    for row in result_set:
        response = dict(row)

    if response['completed_at'] == None:
        return ''
    else:
        response['completed_at'] = response['completed_at'].strftime("%Y-%m-%d %H:%M:%S")
        return response['completed_at']

def get_skip_questionnaire_status(key):
    sql = 'select count(user_did_skip) from questionnaire_response_item where performed_activity_group_id = :performed_activity_group_id AND user_did_skip = :skip_status'

    stmt = text(sql)
    stmt = stmt.bindparams(performed_activity_group_id=key, skip_status='t')
    result_set = settings.ENGINE.execute(stmt)
    response = []
    for row in result_set:
        response.append(dict(row))
    
    if len(response) == 0:
        return 0
    else:
        return response[0]['count']

def get_skip_questionnaire_count_as_per_set(key, q_set):
    sql = 'select count(user_did_skip) from questionnaire_response_item where performed_activity_group_id = :performed_activity_group_id AND user_did_skip = :skip_status AND test_type= :q_set'

    stmt = text(sql)
    stmt = stmt.bindparams(performed_activity_group_id=key, skip_status='t', q_set=q_set)
    result_set = settings.ENGINE.execute(stmt)
    response = []
    for row in result_set:
        response.append(dict(row))
    
    if len(response) == 0:
        return 0
    else:
        return response[0]['count']


def get_number_of_files(key, file_type):
    if file_type == 'audio_file_path':
        sql = 'select audio_file_path from performed_activity_master where performed_activity_group_id = :performed_activity_group_id AND study_name NOT IN (\'-1\')'
    elif file_type == 'answers_s3_path':
        sql = 'select answers_s3_path from questionnaire_response_item where performed_activity_group_id = :performed_activity_group_id'

    stmt = text(sql)
    stmt = stmt.bindparams(performed_activity_group_id=key)
    result_set = settings.ENGINE.execute(stmt)
    response = []
    for row in result_set:
        response.append(dict(row))
    return len(response)

def get_actual_session_performed (study_name):

    START_DATE_1 = settings.START_DATE.replace('T', ' ').replace('Z','')
    END_DATE_1 = settings.END_DATE.replace('T', ' ').replace('Z','')
    sql = 'select count(id) from exercise_details where study_version_id IN (select id from study_version where study_id in ( select id from study where token = :s_name)) and started_at between :START_DATE_1 and :END_DATE_1'
    

    stmt = text(sql)
    #stmt = stmt.bindparams(s_name=study_name)
    stmt = stmt.bindparams(s_name=study_name, START_DATE_1=START_DATE_1, END_DATE_1=END_DATE_1)
    result_set = settings.ENGINE.execute(stmt)
    response = []
    for row in result_set:
        response.append(dict(row))
    return response[0]['count']

def update_dictonary_as_per_pagi_id(file_type, file_name, META_DICT, ANS_DICT):
    json_data, raw_meta = settings.getjson(file_name)
    #json_data, raw_meta = study_wise_report.getjson(file_name)
    if 'performed_activity_group_id' in json_data.keys():
        performed_activity_group_id = json_data['performed_activity_group_id']
        if file_type == 'meta_file':
            if performed_activity_group_id in META_DICT.keys():
                META_DICT[performed_activity_group_id].append(file_name)
            else:
                META_DICT[performed_activity_group_id] = [file_name]
        else:
            if performed_activity_group_id in ANS_DICT.keys():
                ANS_DICT[performed_activity_group_id].append(file_name)
            else:
                ANS_DICT[performed_activity_group_id] = [file_name]
    else:
        print("meta file not contains the performed_activity_group_id:", file_name)

def process_each_audio_meta(key, meta_data, audio_count_dict):
    try:
        meta_data_keys = meta_data.keys()
        audio_count_dict_keys = audio_count_dict.keys()
        if 'activity' in meta_data_keys:
            activity = meta_data['activity']
        else:
            activity = 'UNKONWN'

        #logic for META CHECK will goes here
        
        if meta_data['meta_check'] == False:
            if 'meta_validation_fail' not in audio_count_dict_keys:
                audio_count_dict['meta_validation_fail'] = 1
            else:
                audio_count_dict['meta_validation_fail'] += 1
        else:
            if 'meta_validation_pass' not in audio_count_dict_keys:
                audio_count_dict['meta_validation_pass'] = 1
            else:
                audio_count_dict['meta_validation_pass'] += 1


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

    
        if 'study_version_id' in meta_data_keys:
            audio_count_dict['study_version_id'] = meta_data['study_version_id']
        
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
    
        if 'exercise_id' in meta_data_keys:
            audio_count_dict['exercise_id'] = meta_data['exercise_id']
        


        if 'site_name' in meta_data_keys and 'site_specific_id' in meta_data_keys:
            audio_count_dict['mode'] = 'Technician Mode'
            audio_count_dict['site_specific_id'] = meta_data['site_specific_id']
            audio_count_dict['site_Name'] = meta_data['site_name']
        else:
            audio_count_dict['mode'] = 'User Mode'
            audio_count_dict['site_specific_id'], audio_count_dict['site_Name'] = get_site_specific_site_name(audio_count_dict['user_id'])

        if 'meta_check' in meta_data_keys:
            audio_count_dict['meta_check'] = meta_data['meta_check']
        else:
            audio_count_dict['meta_check'] = 'Not_Performed'

            
            
        if 'token' in meta_data_keys:
            audio_count_dict['token_name'] = meta_data['token']
        else:
            audio_count_dict['token_name'] = 'NA'

        audio_count_dict['performed_activity_group_id'] = key
        return audio_count_dict
    except:
        pdb.set_trace()
        print ( 'Method name is process_each_audio_meta ')
        print (key)

# logic for total audio files per session
def process_a_complete_session(key, audio_count_dict, META_DICT, ANS_DICT):
    
    try:
        audio_file_count = 0
        audio_count_dict_keys = audio_count_dict.keys()
        for audio_count_dict_key in audio_count_dict_keys:
            if audio_count_dict_key[:-2] in AUDIO_ACTIVITIES:
                audio_file_count += audio_count_dict[audio_count_dict_key]
        audio_count_dict['Total_Audio_files_ON_S3'] = audio_file_count


        # to get the language count and questionaire count for activity
        # to get the questionnaire user performed
        user_questionnaire_list = get_user_questionnaire(key)
        audio_count_dict['Questionnaires_User_Performed'] = ",".join(user_questionnaire_list)

        #Get skip questionnaire count for each questionnaire set
        for q_set in user_questionnaire_list:
            Q_SET = 'Q ' + q_set + ' skip_count'
            audio_count_dict[Q_SET] = get_skip_questionnaire_count_as_per_set(key, q_set)

            if audio_count_dict['study_Name'] not in LIST_STUDY_Q_SET.keys():
                LIST_STUDY_Q_SET[audio_count_dict['study_Name']] = [Q_SET]
            elif Q_SET not in LIST_STUDY_Q_SET[audio_count_dict['study_Name']]:
                LIST_STUDY_Q_SET[audio_count_dict['study_Name']].append(Q_SET)

        # to get the user language
        user_total_languages = [x.upper() for x in get_user_language(audio_count_dict)] #['MARATHI','ENGLISH']    
        user_total_languages.append(None)
        # logic to calculate the expected count for the languages users has selected
        audio_count_dict['Expected_Audio_Count'] = 0
        audio_count_dict['Questinnaire_Configured_In_Study'] = ''
        audio_count_dict['Incomplete_Answer_File'] = ''
    
        year, month, day= (int (x) for x in  audio_count_dict['start_time'].split('T')[0].split('-'))
    
        dayAsPerMeta = datetime.date(year, month, day).strftime("%A")
    
        s_v_id = audio_count_dict['study_version_id']

        if s_v_id not in study_audio_content.keys():
            study_audio_content[s_v_id], study_ques_content[s_v_id] = get_activity_language_count(key, audio_count_dict['study_Name'], s_v_id)
        

        for day in [dayAsPerMeta, 'ALL_DAY']:
            if day in study_audio_content[s_v_id].keys():       #Block for Processing audio data
                for language in user_total_languages:
                    if language in study_audio_content[s_v_id][day].keys():
                        audio_count_dict['Expected_Audio_Count'] += study_audio_content[s_v_id][day][language]
        
            if day in study_ques_content[s_v_id].keys():       #Block for Processing Questionnaire data
                for language in user_total_languages:
                    if language in study_ques_content[s_v_id][day].keys():
                        # Set Questinnaire_Configured_In_Study as per the language of the user and language of the activity
                        audio_count_dict['Questinnaire_Configured_In_Study'] = ",".join(study_ques_content[s_v_id][day][language])
    
                        # to get the incomplete questionnaire
                        list_incomplete_questionnaire = list(set(study_ques_content[s_v_id][day][language]) - set(user_questionnaire_list))
                        audio_count_dict['Incomplete_Answer_File'] = ",".join(list_incomplete_questionnaire)


        if 'QoS_Rejected' not in audio_count_dict_keys:
            audio_count_dict['QoS_Rejected'] = ''
    
        if 'QoS_Accepted' not in audio_count_dict_keys:
            audio_count_dict['QoS_Accepted'] = ''
    
        if 'QoS_Pending' not in audio_count_dict_keys:
            audio_count_dict['QoS_Pending'] = ''
    
        # to get session end time
        audio_count_dict['completed_at'] = get_completed_time(audio_count_dict['exercise_id'])
        
        #Calculate the answer file count
        if key in ANS_DICT:
            #pdb.set_trace()
            audio_count_dict['CHECK_IN'] = len(ANS_DICT[key])
            answer_file_path = ANS_DICT[key][0]
            answer_data, raw_meta = settings.getjson(answer_file_path)
            meta_status = meta_keys_validation.meta_keys_validation(answer_data, 'ANSWER_FILE', answer_file_path)
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
            if get_number_of_files(key, 'answers_s3_path') > 0:
                audio_count_dict['CHECK_IN'] = 1
            else:
                audio_count_dict['CHECK_IN'] = 0
    
        #Calculate the number of questions skip
        if audio_count_dict['CHECK_IN'] > 0:
            audio_count_dict['Number_of_Questions_Skipped'] = get_skip_questionnaire_status(key)
        else:
            audio_count_dict['Number_of_Questions_Skipped'] = 0
    
        # Finding the audio count from the DB
        if key:
            audio_count_dict['DB_Audio_files_Count'] = get_number_of_files(key, 'audio_file_path')
            audio_count_dict['Missing audio files count'] = audio_count_dict['Expected_Audio_Count'] - audio_count_dict['DB_Audio_files_Count']
    
        if audio_count_dict['CHECK_IN'] == 0 and audio_count_dict['Questinnaire_Configured_In_Study'] != '':
            audio_count_dict['MISSING_ANS_FILE'] = 1
            audio_count_dict['Incomplete_Answer_File'] = 'NA'
        else :
            audio_count_dict['MISSING_ANS_FILE']=''
        
        if audio_count_dict['Missing audio files count'] > 0 or audio_count_dict['MISSING_ANS_FILE'] != '' or audio_count_dict['Incomplete_Answer_File'] != '' or audio_count_dict['Number_of_Questions_Skipped'] > 0:
            audio_count_dict['INCOMPLETE_SESSION'] = 1
        else:
            audio_count_dict['INCOMPLETE_SESSION'] = 0
    

        #if audio_count_dict['INCOMPLETE_SESSION'] == 0 and audio_count_dict['QoS_Rejected'] == '':
        
        if audio_count_dict['INCOMPLETE_SESSION'] == 0 and audio_count_dict['DB_Audio_files_Count'] == audio_count_dict['QoS_Accepted']:
            audio_count_dict['PERFECT_SESSION'] = 1
        else:
            audio_count_dict['PERFECT_SESSION'] = 0

        if audio_count_dict['Missing audio files count'] <= 0 and audio_count_dict['MISSING_ANS_FILE'] == 1:
            audio_count_dict['ALL_AUDIO_PRESENT_BUT_NOT_ANSER_FILE'] = 1
        else:
            audio_count_dict['ALL_AUDIO_PRESENT_BUT_NOT_ANSER_FILE'] = 0

        
        if 'meta_validation_pass' not in audio_count_dict.keys():
            audio_count_dict['meta_validation_pass'] = ''

        if 'meta_validation_fail' not in audio_count_dict.keys():
            audio_count_dict['meta_validation_fail'] = ''

    
        #Logic for finding out the session with health check details 
        HC_FLAG = False
        if not DF_MEASURES_ALL_FILES.empty:
            if not DF_MEASURES_ALL_FILES[DF_MEASURES_ALL_FILES['performed_activity_group_id'].str.match(key)].empty:
                audio_count_dict['HC_Performed'] = DF_MEASURES_ALL_FILES[DF_MEASURES_ALL_FILES['performed_activity_group_id'].str.match(key)]['HealthCheckName'].item()
                HC_FLAG = True

        if not HC_FLAG:
            audio_count_dict['HC_Performed'] = ''

        return audio_count_dict
    except:
        pdb.set_trace()
        return None
        
        




#This method will update the Summary DF out of every study
def Update_Summary_DF( final_audio_count_df):
    global DF_FINAL_QUESTIONNAIRE_SUMMARY
    study_name = final_audio_count_df['study_Name'].iloc[0]
    complete_session = 0
    perfect_session = 0
    incomplete_sessions = 0
    missing_session_count_from_incomplete_session = 0
    missing_ans_file_count = 0
    skipped_questionnaire_session = 0
    incomplete_questionnaire_count = 0
    total_audio_file = 0
    total_qos_accepted = 0
    tota_qos_rejected = 0
    total_qos_pending = 0
    total_hc_performed = 0
    list_users_ids = []
    qos_rejected_session = 0
    all_audio_without_answer_file = 0
    
    
    Q_DICT = {}
    # logic to calculate the numbers of perfect sessions and incomplete session
    try:
        #pdb.set_trace()
        for index, session in final_audio_count_df.iterrows():
           
            if session['INCOMPLETE_SESSION'] == 0:
                complete_session += 1
            else:
                incomplete_sessions += 1
                if session['completed_at'] == '':# to get the count of unfinished sessions out of incomplete sessions
                    missing_session_count_from_incomplete_session += 1

            if session['PERFECT_SESSION'] == 1:
                perfect_session += 1

            if session['ALL_AUDIO_PRESENT_BUT_NOT_ANSER_FILE'] == 1:
                all_audio_without_answer_file += 1


            #If Answer file present and if not present
            if session['MISSING_ANS_FILE'] == '':
                if session['Number_of_Questions_Skipped'] != 0:
                    skipped_questionnaire_session += 1
                
                for key in session.keys():
                    if key.startswith('Q '):
                        q_aas = key.split('skip_count')[0] + 'All Attempted Sesssions'
                        q_aoss = key.split('skip_count')[0] + 'Atleast One Skipped Sessions'
                        
                        if session[key] == 0:
                            if q_aas not in Q_DICT.keys():
                                Q_DICT[q_aas] = 1
                            else:
                                Q_DICT[q_aas] += 1
    
                        elif not pd.isnull(session[key]):
                            if q_aoss not in Q_DICT.keys():
                                Q_DICT[q_aoss] = 1
                            else:
                                Q_DICT[q_aoss] += 1
            else:   
                missing_ans_file_count += 1
            #pdb.set_trace()
            #Calculating the total Number of audio files in the study

            total_audio_file += session['DB_Audio_files_Count']
            if not session['QoS_Accepted'] == '':
                total_qos_accepted += session['QoS_Accepted']
            
            if not session['QoS_Pending'] == '':
                total_qos_pending += session['QoS_Pending']

            if not session['QoS_Rejected'] == '':
                tota_qos_rejected += session['QoS_Rejected']
                qos_rejected_session += 1
            
            if session['HC_Performed'] != '':
                total_hc_performed += 1

            list_users_ids.append( session['user_id'])

            if session['Incomplete_Answer_File'] != '' and session['Incomplete_Answer_File'] != 'NA':
                incomplete_questionnaire_count += 1
    except:
        pdb.set_trace()
        print('none')

    total_unique_user_ids = len(set(tuple(list_users_ids)))
    

    # data for each study
    # appending the data study wise
    d_sheet = {study_name: final_audio_count_df}
    Dict_Study_Sheet.update(d_sheet)


    # summary data for each study
    db_sessions = get_actual_session_performed (study_name)
    missing_session_on_s3 = db_sessions - len(final_audio_count_df)

    d_summary = [settings.Report_Date, study_name,db_sessions, len(final_audio_count_df), missing_session_on_s3, total_hc_performed, complete_session, perfect_session, incomplete_sessions, missing_session_count_from_incomplete_session,all_audio_without_answer_file, skipped_questionnaire_session,  missing_ans_file_count,incomplete_questionnaire_count, qos_rejected_session, total_unique_user_ids, total_audio_file, total_qos_accepted, tota_qos_rejected, total_qos_pending]
    DF_STUDY_SUMMARY.append(d_summary)
 
    Q_DICT.update({'Date':settings.Report_Date, 'Study Name' : study_name, 'Total Sessions present on S3':len(final_audio_count_df), 'Complete Session (With all Audio Performed and All Questions Attempted)':complete_session})
    

    df_questionnaire_summary = pd.DataFrame.from_dict([Q_DICT], orient='columns')
    DF_FINAL_QUESTIONNAIRE_SUMMARY = DF_FINAL_QUESTIONNAIRE_SUMMARY.append(df_questionnaire_summary)


def process_individual_study(dict_study_files, META_DICT, ANS_DICT ):

    final_audio_count_df = pd.DataFrame()
    file_keys = dict_study_files.keys()

    for file in file_keys:
        if file.endswith('.meta'):
            audio_file_name = file.replace('.meta', '.wav')
            if audio_file_name not in file_keys:
                print('Only Meta present, Audio File not present, expecting audio file: ',audio_file_name)            
                continue

            update_dictonary_as_per_pagi_id('meta_file', file, META_DICT, ANS_DICT)

        if file.endswith('.answers'):
            update_dictonary_as_per_pagi_id('ans_file', file, META_DICT, ANS_DICT)


    for key in META_DICT.keys():
        audio_count_dict = {}
        for meta_file_path in META_DICT[key]:
            try:
                #meta_data, raw_meta = study_wise_report.getjson(meta_file_path)
                meta_data, raw_meta = settings.getjson(meta_file_path)
                meta_data['meta_file_name'] = meta_file_path.split('/')[-1]

                # Logic for file_size
                audio_file_name = meta_file_path.replace('.meta', '.wav')
                
                if dict_study_files[audio_file_name]['Size'] == 0:
                    meta_data['audio_file_size'] = "Audio File with Zero Byte"
                    print ('Size of the audio file is Zero Byte', audio_file_name)
                else:
                    meta_data['audio_file_size'] = dict_study_files[audio_file_name]['Size']

                #Logic to validate the Meta file
                if settings.META_VALIDATE == True:
                    meta_data['meta_check'] = meta_keys_validation.meta_keys_validation(meta_data, 'META_FILE', meta_file_path)

                # Here come the logic to calculate the total audio sample collected
                audio_count_dict = process_each_audio_meta(key, meta_data, audio_count_dict)

            except:
                pdb.set_trace()
                print('Issue in recording entry for audio file :', meta_file_path.split('.')[0])
                continue


        # Here come the logic to calculate the total audio audio count per activity
        audio_count_dict = process_a_complete_session(key, audio_count_dict, META_DICT, ANS_DICT)
        audio_count_dict_df = pd.DataFrame.from_dict([audio_count_dict], orient='columns')
        final_audio_count_df = final_audio_count_df.append(audio_count_dict_df)

        print('key: ' + key + ' - Done')
    if not final_audio_count_df.empty:
        Update_Summary_DF(final_audio_count_df)
    else:
        return

def exctract_all_study_data(dict_study_files, DF_MEASURES_ALL_FILES_LOCAL):
    
    print ('Study Analysis started')

    try:
        global LIST_STUDY_Q_SET
        global DF_STUDY_SUMMARY
        global DF_FINAL_QUESTIONNAIRE_SUMMARY
        global Dict_Study_Sheet
        global DF_MEASURES_ALL_FILES
        global study_ques_content
        global study_audio_content


        DF_MEASURES_ALL_FILES = DF_MEASURES_ALL_FILES_LOCAL


        
        DF_STUDY_SUMMARY = []  # to append the data in the summary sheet for each study
        DF_FINAL_QUESTIONNAIRE_SUMMARY = pd.DataFrame()
        Dict_Study_Sheet = {}  # to append the data study wise
        LIST_STUDY_Q_SET = {}
        STUDY_COUNT = 0  # to get the count of the studies processed
    
        for study_name, file_details in dict_study_files.items():
            STUDY_COUNT += 1
            dict_study_files = {}
            # dictonary used for keeping the meta and answer file data
            META_DICT = {}
            ANS_DICT = {}
            study_ques_content = {}
            study_audio_content = {}
    
            for file_name, value in file_details.items():
                d_file = {file_name: value}
                dict_study_files.update(d_file)
            
            
            process_individual_study(dict_study_files, META_DICT, ANS_DICT)
        

        return DF_STUDY_SUMMARY, DF_FINAL_QUESTIONNAIRE_SUMMARY,LIST_STUDY_Q_SET, Dict_Study_Sheet

    except:
        pdb.set_trace()
        return None
    
