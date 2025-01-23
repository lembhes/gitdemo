from datetime import datetime, timedelta
from sqlalchemy import create_engine, MetaData, select, Table, text
import gspread
from google.oauth2.service_account import Credentials
import os
import json
import sys
import boto3
import yaml
import pkg_resources
import xlsxwriter
import pandas as pd
import pdb


CONFIG_FILE_PATH = pkg_resources.resource_filename(__name__, 'config.yaml')


with open(CONFIG_FILE_PATH) as f:
    Stack_config = yaml.safe_load(f)

EMAIL_FROM                  = Stack_config['EMAIL_FROM']
USERNAME                    = Stack_config['USERNAME']
PASSWORD                    = Stack_config['PASSWORD']
WRITE_ON_DASHBOARD          = Stack_config['WRITE_ON_DASHBOARD']
SENT_MAIL                   = Stack_config['SENT_MAIL']
META_VALIDATE                   = Stack_config['META_VALIDATE']


INSTRUCTION_JSON_FILE_PATH = pkg_resources.resource_filename(__name__, Stack_config['INSTRUCTION_JSON_FILE'])

GOOGLE_CREDENTIAL_JSON_FILE_PATH = pkg_resources.resource_filename(__name__, Stack_config['GOOGLE_CREDENTIAL_JSON_FILE'])

STUDY_REFERENCE_FILE_PATH = pkg_resources.resource_filename(__name__, Stack_config['STUDY_REFERENCE_FILE'])





ACCOUNT                     = Stack_config['Account_To_Use']

INCOMING_BUCKET             = Stack_config[ACCOUNT]['INCOMING_BUCKET']
STUDY_PREFIX                = Stack_config[ACCOUNT]['STUDY_PREFIX']
MEASURE_PREFIX              = Stack_config[ACCOUNT]['MEASURE_PREFIX']
DB_USERNAME                 = Stack_config[ACCOUNT]['DB_USERNAME']
DBPASSWORD                  = Stack_config[ACCOUNT]['DBPASSWORD']
HOSTNAME                    = Stack_config[ACCOUNT]['HOSTNAME']
DB_NAME                     = Stack_config[ACCOUNT]['DB_NAME']
BACKDATED_REPORT_DURATION       = Stack_config[ACCOUNT]['BACKDATED_REPORT_DURATION']
STACK_NAME_TO_SHOW_IN_REPORT    = Stack_config[ACCOUNT]['STACK_NAME_TO_SHOW_IN_REPORT']
EMAIL_TO                        = Stack_config[ACCOUNT]['EMAIL_TO']
GOOGLE_SHEET_TO_UPDATE      = Stack_config[ACCOUNT]['GOOGLE_SHEET_TO_UPDATE']

def init(date=None, mail_flag=None):

    global START_DATE
    global END_DATE
    global Report_Date
    global s4
    global REPORT_NAME
    global SENT_MAIL
    if date:
        START_DATE = date + 'T00:00:00Z'
        END_DATE = date + 'T23:59:59Z'
        Report_Date = START_DATE.split('T')[0]
    else:
        date = (datetime.now() - timedelta(BACKDATED_REPORT_DURATION)).strftime('%Y-%m-%d') #Gives yesterdays date
        START_DATE = date + 'T00:00:00Z'
        END_DATE = date + 'T23:59:59Z'
        Report_Date = START_DATE.split('T')[0]

    REPORT_NAME = 'Study_HC_Report_' + date + '.xlsx'
    
    if mail_flag == 'False':
        SENT_MAIL = False
        
    
   
    s4 = boto3.client('s3')
    
    set_up_db_connection()
    
    set_up_google_sheets()
    
    set_up_instruction_file()
    
    set_up_reference_study_json_file()
    
    open_xls_sheet()



def getjson(filename):
    metaObj = s4.get_object(Bucket=INCOMING_BUCKET, Key=filename)
    filedata = metaObj['Body'].read()
    if filedata == '':
        return None, None
    try:
        local_json = json.loads(filedata)
        return local_json, filedata
    except:
        print("json was encrypted")
    

def set_up_instruction_file():

    global INSTRUCTION_DATA

    if os.path.isfile(INSTRUCTION_JSON_FILE_PATH):
        with open(INSTRUCTION_JSON_FILE_PATH) as json_file:
            INSTRUCTION_DATA = json.loads(json_file.read())
        if INSTRUCTION_DATA is not None :
            print ('Instruction data loading is done')
        else:
            print ("Error in getting the instruction data")
    else:
        print ("Pleas provide the Insturction file")
        sys.exit (1)

def set_up_reference_study_json_file():
    global STUDY_REFERENCE_DATA

    if os.path.isfile(STUDY_REFERENCE_FILE_PATH):
        with open(STUDY_REFERENCE_FILE_PATH) as json_file:
            STUDY_REFERENCE_DATA = json.loads(json_file.read())
        if STUDY_REFERENCE_DATA is not None :
            print ('STUDY_REFERENCE_DATA loading is done')
        else:
            print ("Error in getting the STUDY_REFERENCE_DATA")
    else:
        print ("Pleas provide the Insturction file")
        sys.exit (1)

def set_up_google_sheets():
    #import pdb; pdb.set_trace()
    global GOOGLE_SHEET
    print ('google file path',GOOGLE_CREDENTIAL_JSON_FILE_PATH)
    if os.path.isfile(GOOGLE_CREDENTIAL_JSON_FILE_PATH):
        scope = ["https://www.googleapis.com/auth/drive", "https://www.googleapis.com/auth/spreadsheets"]
        credentials = Credentials.from_service_account_file(GOOGLE_CREDENTIAL_JSON_FILE_PATH, scopes=scope)
        print(credentials)
        gc = gspread.authorize(credentials)
        GOOGLE_SHEET = gc.open(GOOGLE_SHEET_TO_UPDATE)
        #worksheet_list = sh.worksheets()
 
    else:
        print ("Pleas provide the standard file for GOOGLE_CREDENTIAL")
        sys.exit (1)

def set_up_db_connection():
    global ENGINE
    DB_URL = 'postgres://{}:{}@{}/{}'.format(DB_USERNAME, DBPASSWORD, HOSTNAME, DB_NAME)
    
    ENGINE = create_engine(DB_URL, echo=False, pool_size=1)

def open_xls_sheet():
    global writer
    global workbook

    writer = pd.ExcelWriter(REPORT_NAME, engine='xlsxwriter')
    workbook = writer.book