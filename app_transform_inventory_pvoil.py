import os
import re
import numpy as np
import pandas as pd
import module_process_file
import module_process_string
import module_process_data


#define local variables
config_file_json    = module_process_file.read_json_file(r'C:\Users\phuocth\AppData\Local\app\config.json')
info_json           = config_file_json["APP_TRANSFORM_INVENTORY"]
config_file_json          = info_json["PVOIL"]
file_path           = config_file_json["URI_PVOIL"]
names_columns       = config_file_json["NAMES_COLUMNS"]
len_catalog         = config_file_json["LEN_CATALOG"]

len_columns         = len(names_columns) + len_catalog
# URI file path
file_path_raw_data      = file_path + '\\Input'
file_path_data_formated = file_path + '\\Output'



def function_formatter(file_path_raw_data, file_path_data_formated, name_file, len_catalog, len_columns):

    raw_data = pd.read_excel(file_path_raw_data + '\\' + name_file, dtype=str, header=None, na_filter='')

   
    # search skip rows
    index = module_process_data.get_row(raw_data, 'NỘI DUNG', 0) + 1
    
    # insert field "NGÀY BÁO CÁO" and delete row cotain "NGÀY BÁO CÁO 16/10/2023"
    raw_data.rename(columns={0: names_columns[0], 1: names_columns[1], 2: names_columns[2], 3: names_columns[3], 4: names_columns[4], 5: names_columns[5], 6: names_columns[6]}, inplace=True)
    df = raw_data.iloc[index:, :].copy()

    
    # add date to column with name 'NGÀY BÁO CÁO'
    date_convert = module_process_string.convert_date_(name_file)
    if date_convert != False:
        date = {
            "date_column": 'NGÀY BÁO CÁO',
            "value_column" : date_convert
        }
        df.insert(0, date["date_column"], date["value_column"])



    #     # insert field "DANH MỤC 1"
    #     # insert field "DANH MỤC 2"
        df = module_process_data.insert_many_columns(df,len_catalog)
        
        df = module_process_data.add_catalog_1(df, 2, '^[A-Z]\\..*')
        df = module_process_data.add_catalog_2(df, 3, '^[1-9]\.\s\D', '^[A-Z]\\..*')
    #     df = module_process_data.add_catalog_3(df, 4, '^[1-9]\.[1-9]\s*', '^[A-Z]\\..*','^[1-9]\.\s\D' )
    #     df = module_process_data.add_catalog_4(df, 4, r'^-\s')

        df = df.drop(columns={"NỘI DUNG"})
        df = module_process_data.clear_junk_data(df, 6)
        finally_df = df.iloc[:,:len_columns].copy()
        finally_df.to_excel(file_path_data_formated +  '\\RESULT_' + name_file, index=False)


# function_formatter(file_path_raw_data, file_path_data_formated,"PVOil_SL_TonKho_20240101.xlsx", len_catalog, len_columns)

import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

def on_created(event):
    print('created event................................................................!')
    files_raw_data      = module_process_file.check_file(module_process_file.list_files(file_path_raw_data), False)
    files_data_formated = module_process_file.check_file(module_process_file.list_files(file_path_data_formated), True)
    set_one = set(files_raw_data)
    set_two = set(files_data_formated)
    elements_not_in_array_one = set_one - set_two
    result_list = list(elements_not_in_array_one)
    for i in range(len(result_list)):
        function_formatter(file_path_raw_data, file_path_data_formated,result_list[i], len_catalog, len_columns)



def watch_directory_app_pvoil(path):
    event_handler = FileSystemEventHandler()
    event_handler.on_created    = on_created
    event_handler.on_modified   = on_created
    event_handler.on_deleted    = on_created

    # Create an observer and schedule the handler
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print('Exiting...!')
        observer.stop()
    observer.join()

watch_directory_app_pvoil(file_path)