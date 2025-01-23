import json
import boto3
import xlsxwriter
import pandas as pd
import sys
import dateutil.parser
from datetime import datetime, timezone
import settings

s4 = boto3.client('s3')

# Create a reusable Paginator
paginator = s4.get_paginator('list_objects')

d_dict ={}

def study_file_collector_as_per_date():
    start_date = dateutil.parser.parse(settings.START_DATE)
    end_date = dateutil.parser.parse(settings.END_DATE)
    
    page_iterator = paginator.paginate(Bucket=settings.INCOMING_BUCKET, Prefix=settings.STUDY_PREFIX)
    for page in page_iterator:
        if "Contents" in page:
            for key in page["Contents"]:
                file_date = dateutil.parser.parse(str(key['LastModified'])).replace(tzinfo=timezone.utc)
                if start_date < file_date < end_date:
                    study_id = key['Key'].split('/')[2]
                    dict_of_file = {key['Key']: key}
                    if study_id not in d_dict.keys():
                        d_dict[study_id] = dict_of_file
                    else:
                        d_dict[study_id].update(dict_of_file)
    
                    continue

    return  d_dict


        
def hc_file_collector_as_per_date():
    measures_all_files = {}
    try:
        start_date = dateutil.parser.parse(settings.START_DATE)
        end_date = dateutil.parser.parse(settings.END_DATE)
    
        # Create a PageIterator from the Paginator
        page_iterator = paginator.paginate(Bucket=settings.INCOMING_BUCKET, Prefix=settings.MEASURE_PREFIX)
        for page in page_iterator:
            if "Contents" in page:
                for key in page["Contents"]:
                    file_date = dateutil.parser.parse(str(key['LastModified'])).replace(tzinfo=timezone.utc)
                    if start_date < file_date < end_date:
                        measures_all_files[key['Key']] = key
        return measures_all_files
    except:
        return measures_all_files
        