# README
# command to execute the scipt python session_details_data_athena.py <study_name>
# Output will be spreadsheet report genererated at the end

import json

import pandas as pd
import sys

import pdb

import segregation
import extract_measures_data
import exctract_all_study_data
import send_email
import settings

ACTIVITY_LIST_SEQUENCE = ['INCOMPLETE_SESSION','BASELINE', 'FREE_SPEECH', 'FOCUS', 'MEMORY', 'PASSAGE_READING', 'SENTENCE_READING','TIMED_RECORDING','CHECK_IN']

DEFAULT_LIST_1    = ['Number_of_Questions_Skipped', 'Total_Audio_files_ON_S3', 'DB_Audio_files_Count', 'Expected_Audio_Count','Missing audio files count', 'QoS_Accepted', 'QoS_Rejected', 'QoS_Pending', 'completed_at', 'start_time', 'HC_Performed', 'mode', 'study_Name', 'token_name', 'site_specific_id', 'site_Name', 'exercise_id','user_id', 'study_version_id', 'app_version','manufacturer', 'device_time_zone', 'device_local_country_code']

DEFAULT_LIST_2 = ['MISSING_ANS_FILE', 'Questinnaire_Configured_In_Study', 'Questionnaires_User_Performed', 'Incomplete_Answer_File', 'meta_validation_pass', 'meta_validation_fail', 'performed_activity_group_id']

SUMMARY_COLOUMN_LIST = ['Date', 'Study Name','# Starts Session as per DB','# Sessions present on S3', '# Missing Sessions from S3','# HC Performed in same session with this study' ,'# Complete Session ( With all Audio Performed and All Questions Attempted)', '# Perfect Session (Complete session having all QoS Accepted)', '# Incomplete Session', '# Abandoned sessions from total incomplete sessions', '# Sessions with all audio and without answer file', '# Sessions with atleast one question skipped', '# Sessions without answer file', '# Sessions with Partial uploaded of questionnaire file', '# Sessions with atleast one sample Rejected', '# Unique Users','# Audio Files','# QoS Accepted','# QoS Rejected', '# QoS Pending' ]


MAIL_SUMMARY_TABLE_TITLES = ['Study Name', '#Sessions', '#Complete Session','#Incomplete Sessions', '#Sessions with atleast one question skipped', '#Audio files', '#Unique users']

Q_SUMMARY_COLOUMN_LIST = ['Date', 'Study Name', 'Total Sessions present on S3', 'Complete Session (With all Audio Performed and All Questions Attempted)']

HC_PAGE_COLOUMS = ['REJECTED_SESSION', 'HealthCheckName', 'measure_version_ids', 'system_inference_score', 'user_refined_score', 'Total_Audio_files_on_S3', 'Total_Audio_files_in_DB','study_performed_in_this_session', 'start_time', 'user_id', 'token_name', 'mode', 'study_Name',  'measure_ids', 'app_version', 'device_local_country_code', 'device_time_zone', 'manufacturer', 'QoS_Accepted', 'QoS_Pending', 'QoS_Rejected','meta_validation_pass', 'meta_validation_fail', 'performed_activity_group_id']


HC_SUMMARY_PAGE_COLOUMS = ['Date','Health Check','# Session','# Audio Files on S3','# Audio Files in DB','# Audio file with score', '# Audio file without score', '# Session with Study Perfomed', '# Unique Users', '# Refinement done by users','# QoS Accepted','# QoS Rejected','# QoS Pending','# Rejected Session']




def getjson(filename):
    metaObj = settings.s4.get_object(Bucket=settings.INCOMING_BUCKET, Key=filename)
    filedata = metaObj['Body'].read()
    if filedata == '':
        return None, None
    try:
        local_json = json.loads(filedata)
        return local_json, filedata
    except:
        print("json was encrypted")

def report_write_headers(sheet_name, row_number, df):
    try:
        summary_header_fmt = settings.workbook.add_format({'bold': 1,'border': 1,'align': 'left', 'valign': 'top', 'text_wrap': True, 'fg_color': '#C0C0C0'})

        worksheet = settings.writer.sheets[sheet_name]

        for col_num, value in enumerate(df.columns.values):
            worksheet.write(row_number, col_num, value, summary_header_fmt)
            col_num += 1

    except:
        print('error in report_write_headers')


def add_instruction_data(df, sheet_name, number_rows):
    fmt_bold = settings.workbook.add_format({'bold': True})
    number_rows = number_rows + 2
    df.to_excel(settings.writer, sheet_name=sheet_name, index=False, startrow=number_rows+3, header=False)
    report_write_headers(sheet_name, number_rows+2, df)
    worksheet = settings.writer.sheets[sheet_name]
    worksheet.set_column('A:A', None, fmt_bold)

def create_instruction_dataframes(STUDY_SHEET):
    df = pd.DataFrame()
    df['Headers Title'] = settings.INSTRUCTION_DATA[STUDY_SHEET].keys()
    df['What it Means'] = settings.INSTRUCTION_DATA[STUDY_SHEET].values()
    return df

def write_on_bashboard(df, sheet_name):
    try:
        google_worksheet = settings.GOOGLE_SHEET.worksheet(sheet_name)
    except:
        google_worksheet = settings.GOOGLE_SHEET.add_worksheet(title=sheet_name, rows="100", cols="20")
        google_worksheet.update([df.columns.values.tolist()])
    
    google_worksheet.append_rows(list(zip(*[df[c].values.tolist() for c in df])))


def writing_data_frames_to_xls(df, df_coloumn_list, sheet_name, startrow):
    if not isinstance(df, pd.DataFrame):
        df = pd.DataFrame(df, columns=df_coloumn_list)
    else:
        df = df[df_coloumn_list]
    df.to_excel(settings.writer, sheet_name=sheet_name, index=False,startrow=startrow, header=False)
    report_write_headers( sheet_name, 1, df)
    return df 


def Genrate_HC_Report(DF_MEASURES_ALL_FILES, FINAL_HC_SUMMARY_DF):
    writer = settings.writer
    workbook = settings.workbook

    #Instruction Data Frames to be used for Summary and Study sheet
    insturction_hc_summary_df = create_instruction_dataframes('HC_SUMMARY_HEADERS')
    insturction_each_hc_df = create_instruction_dataframes('HC_SHEET_HEADERS')

    #Writing healh check summary sheet
    if not FINAL_HC_SUMMARY_DF.empty:
        #import pdb; pdb.set_trace()
        FINAL_HC_SUMMARY_DF = writing_data_frames_to_xls(FINAL_HC_SUMMARY_DF, HC_SUMMARY_PAGE_COLOUMS, 'HC_Summary',startrow=2 )
        add_instruction_data(insturction_hc_summary_df, 'HC_Summary', len(FINAL_HC_SUMMARY_DF))


    if settings.WRITE_ON_DASHBOARD:
        #writing the health check summary sheet
        if not FINAL_HC_SUMMARY_DF.empty:
            FINAL_HC_SUMMARY_DF = FINAL_HC_SUMMARY_DF[HC_SUMMARY_PAGE_COLOUMS]
            write_on_bashboard(FINAL_HC_SUMMARY_DF, 'HC_Summary')


    #Writing Health check sheet
    if not DF_MEASURES_ALL_FILES.empty:
        #import pdb; pdb.set_trace()
        hc_list = DF_MEASURES_ALL_FILES['HealthCheckName'].unique()
        for hc_name in hc_list:
            DF_EACH_HC = DF_MEASURES_ALL_FILES.loc[DF_MEASURES_ALL_FILES['HealthCheckName'] == hc_name]
            writing_data_frames_to_xls(DF_EACH_HC, HC_PAGE_COLOUMS, hc_name, startrow=2 )
            add_instruction_data(insturction_each_hc_df, hc_name, len(DF_EACH_HC))

    writer.save()
    
    if settings.SENT_MAIL == True:
        df_hc_email_body = pd.DataFrame(FINAL_HC_SUMMARY_DF, columns=HC_SUMMARY_PAGE_COLOUMS)
        html_df_hc_email_body = df_hc_email_body.to_html(na_rep = "", index = False, justify='center').replace('<th>','<th style = "background-color: grey">')
       
        send_email.send_mail(settings.REPORT_NAME, html_df_hc_email_body, None)

    print('Report name created as :', settings.REPORT_NAME)

    
    

    
# Create a Pandas Excel writer using XlsxWriter as the engine.
def Genrate_Report(DF_STUDY_SUMMARY, DF_FINAL_Q_SUMMARY, LIST_STUDY_Q_SET, Dict_Study_Sheet, DF_MEASURES_ALL_FILES, FINAL_HC_SUMMARY_DF):

    #pdb.set_trace()
    writer = settings.writer
    workbook = settings.workbook

    #Different formats used in below code
    fmt_bold = workbook.add_format({'bold': True})
    fmt_yellow_colour = workbook.add_format({'bg_color': '#FFFF00'})
    merge_format = workbook.add_format({'bold': 1,'border': 1,'align': 'center', 'valign': 'vcenter'})

    #Instruction Data Frames to be used for Summary and Study sheet
    #Create df for instructions formats
    insturction_study_df = create_instruction_dataframes('STUDY_SHEET')
    insturction_summary_df = create_instruction_dataframes('STUDY_SUMMARY')
    insturction_questionnaire_df = create_instruction_dataframes('QUESTIONNAIRE_SUMMARY')
    insturction_hc_summary_df = create_instruction_dataframes('HC_SUMMARY_HEADERS')
    insturction_each_hc_df = create_instruction_dataframes('HC_SHEET_HEADERS')

    #Writing healh check summary sheet
    if not FINAL_HC_SUMMARY_DF.empty:
        #import pdb; pdb.set_trace()
        FINAL_HC_SUMMARY_DF = writing_data_frames_to_xls(FINAL_HC_SUMMARY_DF, HC_SUMMARY_PAGE_COLOUMS, 'HC_Summary',startrow=2 )
        add_instruction_data(insturction_hc_summary_df, 'HC_Summary', len(FINAL_HC_SUMMARY_DF))


    #Writting Summary sheet
    summary_dataframe = writing_data_frames_to_xls(DF_STUDY_SUMMARY, SUMMARY_COLOUMN_LIST, 'Study_Summary',startrow=2 )
    
    #Writing Study and HC data on the Dashboard 
    if settings.WRITE_ON_DASHBOARD:
        #writing the study summary sheet
        if len(DF_STUDY_SUMMARY) > 0:
            write_on_bashboard(summary_dataframe, 'Study_Summary')

        #writing the health check summary sheet
        if not FINAL_HC_SUMMARY_DF.empty:
            FINAL_HC_SUMMARY_DF = FINAL_HC_SUMMARY_DF[HC_SUMMARY_PAGE_COLOUMS]
            write_on_bashboard(FINAL_HC_SUMMARY_DF, 'HC_Summary')
    
    #Writting Questionnaire Summary sheet
    desired_columns = []
    q_columns_list = list(DF_FINAL_Q_SUMMARY.columns)
    desired_columns.extend(Q_SUMMARY_COLOUMN_LIST)
    #To make sure dataframes is having at least single entry for questionnaire's
    if len(q_columns_list) > 3:
        t_list_all_attempted = []
        t_list_one_skipped = []
        
        for key in q_columns_list:
            if 'All Attempted' in key:
                t_list_all_attempted.append(key)
            if 'Skipped' in key:
                t_list_one_skipped.append(key)
    
        desired_columns.extend(t_list_all_attempted)
        desired_columns.extend(t_list_one_skipped)

        DF_FINAL_Q_SUMMARY.fillna("NA", inplace=True)
        writing_data_frames_to_xls(DF_FINAL_Q_SUMMARY, desired_columns, 'Study_Questionnaire_Summary', startrow=2 )
        add_instruction_data(insturction_questionnaire_df, 'Study_Questionnaire_Summary', len(DF_FINAL_Q_SUMMARY))

    #Writing Health check sheet
    if not DF_MEASURES_ALL_FILES.empty:
        import pdb; pdb.set_trace()
        hc_list = DF_MEASURES_ALL_FILES['HealthCheckName'].unique()
        for hc_name in hc_list:
            DF_EACH_HC = DF_MEASURES_ALL_FILES.loc[DF_MEASURES_ALL_FILES['HealthCheckName'] == hc_name]
            hc_name_sheet_name= hc_name[:30]
            writing_data_frames_to_xls(DF_EACH_HC, HC_PAGE_COLOUMS, hc_name_sheet_name, startrow=2 )
            add_instruction_data(insturction_each_hc_df, hc_name_sheet_name, len(DF_EACH_HC))

    #Writting each study sheet
    for s_name, frames in Dict_Study_Sheet.items():
        if len(frames) > 0:
            desired_columns = []
            columns_list = list(frames.columns)
            for a_columns in ACTIVITY_LIST_SEQUENCE:
                for c_columns in columns_list:
                    if c_columns.startswith(a_columns):
                        desired_columns.append(c_columns)
    
            desired_columns.extend(DEFAULT_LIST_1)
            
            if s_name in LIST_STUDY_Q_SET.keys():
                desired_columns.extend(LIST_STUDY_Q_SET[s_name])
            
            desired_columns.extend(DEFAULT_LIST_2)
            frames = frames[desired_columns]
        frames.to_excel(writer, sheet_name=s_name, index=False,startrow=1, header=False)
        report_write_headers(s_name, 0, frames)
    
    
        worksheet = writer.sheets[s_name]
        number_rows = len(frames)+1
    
        #Yello background for incomplete row for inside study page
        worksheet.conditional_format("$A$2:$AZ$%d" % (number_rows), {"type": "formula", "criteria": '=INDIRECT("A"&ROW())>0', "format": fmt_yellow_colour})
        add_instruction_data(insturction_study_df, s_name, number_rows)


    STUDY_COUNT = len(Dict_Study_Sheet.keys())        
    worksheet = writer.sheets['Study_Summary']
    number_rows = STUDY_COUNT + 3
    
    # Merge 3 cells. Create a format to use in the merged range.
    worksheet.set_column('D:T', 12)
    worksheet.merge_range('D1:T1', 'Analysis of the Data Present on S3 bucket/ Cloud', merge_format)
    
    #Yello color for incomplete condition
    worksheet.conditional_format("$A$3:$T$%d" % (number_rows),{"type": "formula", "criteria": '=INDIRECT("F"&ROW())>0', "format": fmt_yellow_colour})
    add_instruction_data(insturction_summary_df, 'Study_Summary', number_rows)
    
    writer.save()
    
    if settings.SENT_MAIL == True:
        df_hc_email_body = pd.DataFrame(FINAL_HC_SUMMARY_DF, columns=HC_SUMMARY_PAGE_COLOUMS)
        html_df_hc_email_body = df_hc_email_body.to_html(na_rep = "", index = False, justify='center').replace('<th>','<th style = "background-color: grey">')
        
        df_study_email_body = pd.DataFrame(DF_STUDY_SUMMARY, columns=SUMMARY_COLOUMN_LIST)
        html_df_study_email_body = df_study_email_body.to_html(na_rep = "", index = False, justify='center').replace('<th>','<th style = "background-color: grey">')
    
        if FINAL_HC_SUMMARY_DF.empty and len(DF_STUDY_SUMMARY) < 1:
            send_email.send_mail(settings.REPORT_NAME, None, None)
            return
        
        if FINAL_HC_SUMMARY_DF.empty:
            send_email.send_mail(settings.REPORT_NAME, None, html_df_study_email_body)
            return
    
        if len(DF_STUDY_SUMMARY) < 1:
            send_email.send_mail(settings.REPORT_NAME, html_df_hc_email_body, None)
            return
    
        send_email.send_mail(settings.REPORT_NAME, html_df_hc_email_body, html_df_study_email_body)

    print('Report name created as :', settings.REPORT_NAME)


def main():
    DF_MEASURES_ALL_FILES = pd.DataFrame()
    FINAL_HC_SUMMARY_DF = pd.DataFrame()
    DF_STUDY_SUMMARY = pd.DataFrame()
    HEALTH_CHECK_PRESENT = False
    measure_files = segregation.hc_file_collector_as_per_date()  # to get the files from healthcheck mode
    if len(measure_files) > 0:
        DF_MEASURES_ALL_FILES, FINAL_HC_SUMMARY_DF = extract_measures_data.extract_measures_data(measure_files)
        if len(DF_MEASURES_ALL_FILES) > 0 and len(FINAL_HC_SUMMARY_DF):
            HEALTH_CHECK_PRESENT = True

    STUDY_PRESENT = False
    study_files = segregation.study_file_collector_as_per_date()  # to get the files of single day from last to last day
    if len(study_files) > 0:
        DF_STUDY_SUMMARY, DF_FINAL_Q_SUMMARY,LIST_STUDY_Q_SET, Dict_Study_Sheet = exctract_all_study_data.exctract_all_study_data(study_files, DF_MEASURES_ALL_FILES)
        STUDY_PRESENT = True
    
    
    if STUDY_PRESENT == True:
        Genrate_Report(DF_STUDY_SUMMARY, DF_FINAL_Q_SUMMARY,LIST_STUDY_Q_SET, Dict_Study_Sheet, DF_MEASURES_ALL_FILES, FINAL_HC_SUMMARY_DF)

    else: #Generating the report for measure only
        print ('only measure data present')    
        Genrate_HC_Report(DF_MEASURES_ALL_FILES, FINAL_HC_SUMMARY_DF)

    
    
if __name__ == '__main__':
    args = sys.argv
    #pdb.set_trace()
    if len(args) == 3:
        settings.init(args[1],args[2])
        #settings.init('2020-05-14', False)
    elif len(args) == 2:
        settings.init(args[1])
        #settings.init('2020-05-14')
    else:
        settings.init()

    main()


#if __name__ == '__main__':
#    args = sys.argv
#    if len(args) > 1:
#        settings.init(args[1])
#        #settings.init('2020-05-14')
#    else:
#        settings.init()
#
#    main()
    