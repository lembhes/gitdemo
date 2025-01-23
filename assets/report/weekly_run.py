import sys
import subprocess
import settings
import pdb
from datetime import datetime, timedelta
import study_wise_report

CLEAN_DATE = 10
Study_Sheet_Name  = 'Study_Summary'
HC_Sheet_Name  = 'HC_Summary'
BACKDATED_REPORT_DURATION = 1
DATE_FORMAT = '%Y-%m-%d'


settings.init()
SH = settings.GOOGLE_SHEET
STUDY_WORKSHEET = settings.GOOGLE_SHEET.worksheet(Study_Sheet_Name)
HC_WORKSHEET = settings.GOOGLE_SHEET.worksheet(HC_Sheet_Name)





def generate_list_of_days(date_string):
    list_of_days = []
    #date_string = '2020-05-19'
    formated_date = datetime.strptime(date_string, DATE_FORMAT)
    yesterday = datetime.now() - timedelta(BACKDATED_REPORT_DURATION)
    delta = yesterday - formated_date
    
    for i in range(delta.days + 1):
        day = formated_date + timedelta(days=i)
        list_of_days.append(day.strftime(DATE_FORMAT))

    print (list_of_days)
    return list_of_days



def select_single_day_present_eveywhere(study_dates_present, hc_dates_present):
    global CLEAN_DATE
    CLEAN_DATE = (-1) * CLEAN_DATE
    for x in range(10):
        if study_dates_present[CLEAN_DATE] in hc_dates_present:
            return study_dates_present[CLEAN_DATE]
        CLEAN_DATE -= 1
    
    return None


def get_cell_value(WORKSHEET, choosen_date):
    values_list = WORKSHEET.col_values(1)
    value_set = set(values_list[1:])
    updated_value_list=  list(value_set)
    updated_value_list.sort()
    cell = WORKSHEET.find(choosen_date)
    return cell.row


def delete_gspread_entries(choosen_date):
    
    study_cell_index = get_cell_value(STUDY_WORKSHEET, choosen_date)
    hc_cell_index = get_cell_value(HC_WORKSHEET, choosen_date)
    
    STUDY_WORKSHEET.delete_rows(study_cell_index, study_cell_index+30)
    HC_WORKSHEET.delete_rows(hc_cell_index, hc_cell_index+30)


def get_list_of_dates(WORKSHEET):

    values_list = WORKSHEET.col_values(1)
    value_set = set(values_list[1:])
    updated_value_list=  list(value_set)
    updated_value_list.sort()
    return updated_value_list


def run_study_report(list_of_dates):
    #script1 = str(sys.path[0]) + "/support_script.py"
    #for x in list_of_dates:
    #    subprocess.call(["python3.6", script1, x])

    #Drawback is Setting getting initialise two times, dont want it
    script1 = str(sys.path[0]) + "/study_wise_report.py"
    for x in list_of_dates:
        subprocess.call(["python3.6", script1, x, 'False'])

    #Drawback is Code is getting break if variables not resetd before calling it
    #for x in list_of_dates:
    #    settings.init(x)
    #    settings.EMAIL_TO = ['nikhil.jagshettiwar@gslab.com', 'n.jagshettiwar@gmail.com']
    #    study_wise_report.main()



if __name__ == '__main__':
    pdb.set_trace()
    study_dates_present = get_list_of_dates(STUDY_WORKSHEET)
    hc_dates_present = get_list_of_dates(HC_WORKSHEET)
    choosen_date = select_single_day_present_eveywhere(study_dates_present, hc_dates_present)

    print ('choosen_date',choosen_date)
    delete_gspread_entries(choosen_date)
    
    list_of_dates_to_run_report = generate_list_of_days(choosen_date)
    
    run_study_report(list_of_dates_to_run_report)

