import smtplib,ssl
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import formatdate
from email import encoders
from datetime import datetime,date,timedelta

import settings

SERVER='smtp.gmail.com'
PORT= 587



def send_mail(files, df_hc_summary, df_study_summary,  isTls=True):
    msg = MIMEMultipart()
    msg['From'] = settings.EMAIL_FROM
    msg['To'] = ", ".join(settings.EMAIL_TO)
    msg['Date'] = formatdate(localtime = True)

    date_to_show = settings.Report_Date

    subject = settings.STACK_NAME_TO_SHOW_IN_REPORT + ' for data collected against all Studies and Health Check on ' + date_to_show
    msg['Subject'] = subject
    
    text1 ='Hi Team,' + '\n\n' + 'Find the report attached. Report contains data sheet for each Study and Health Check, for which data collected from the field on:' + date_to_show + '\n'
    msg.attach(MIMEText(text1))

    if df_hc_summary != None:
        #This code will run for only culprit sessions
        text1B = '\n'+ 'Health Check summary table:'
        msg.attach(MIMEText(text1B))
        msg.attach(MIMEText(df_hc_summary, 'html'))
    else:
        #This code will run for only culprit sessions
        text1B = '\n'+ 'Not a single session present against Health Check \n' 
        msg.attach(MIMEText(text1B))

        
    if df_study_summary != None:
        #This code will run for only culprit sessions
        text1C = '\n'+ 'Study summary table:'
        msg.attach(MIMEText(text1C))
        msg.attach(MIMEText(df_study_summary, 'html'))
    else:
        text1C = '\n'+ 'Not a single session present against Study \n'
        msg.attach(MIMEText(text1C))


        

    text1D = '\n\n'+ 'For detailed analysis, refer to the attached report.'
    msg.attach(MIMEText(text1D))

    part = MIMEBase('application', "octet-stream")
    part.set_payload(open(files, "rb").read())
    encoders.encode_base64(part)
    
    part.add_header('Content-Disposition', 'attachment; filename=' + settings.STACK_NAME_TO_SHOW_IN_REPORT + ' ' + date_to_show + '.xlsx')
    
    msg.attach(part)
    smtp = smtplib.SMTP(SERVER, PORT)
    if isTls:
        smtp.starttls()
    smtp.login(settings.USERNAME, settings.PASSWORD )
    smtp.sendmail(settings.EMAIL_FROM, settings.EMAIL_TO, msg.as_string())
    smtp.quit()
    print ('Mail sent successfully')
