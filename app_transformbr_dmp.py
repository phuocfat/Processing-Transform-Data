import os
import re
import numpy as np
import pandas as pd
import module_process_file
import module_process_string
import module_process_data

#define local variables
config_file_json    = module_process_file.read_json_file(r'C:\Users\phuocth\AppData\Local\app\config.json')
info_json           = config_file_json["APP_TRANSFORM"]
dpm_json            = info_json["ĐPM"]
file_path           = dpm_json["URI_ĐPM"]
# 
json_sheet_1        = dpm_json["SHEET_1"]
json_sheet_2        = dpm_json["SHEET_2"]
# 
sheet_name_1          = json_sheet_1["SHEET_NAME"]
sheet_name_2          = json_sheet_2["SHEET_NAME"]
# 
names_columns_sheet_1   = json_sheet_1["NAMES_COLUMNS"]
names_columns_sheet_2   = json_sheet_2["NAMES_COLUMNS"]

# to save
to_save_sheet_1 = json_sheet_1["TO_SAVE"]
to_save_sheet_2 = json_sheet_2["TO_SAVE"]
# URI file path
file_path_raw_data      = file_path + '\\Input'
file_path_data_formated_sheet_1 = file_path + '\\Output\\TINH HINH SAN XUAT'
file_path_data_formated_sheet_2 = file_path + '\\Output\\KHO SAN PHAM'
# 
len_catalog_1 = json_sheet_1["LEN_CATALOG"]
len_catalog_2 = json_sheet_2["LEN_CATALOG"]


# Convert the arrays to sets
def check_folder(folder_raw, folder_formated):
    
    set_one = set(folder_raw)
    set_two = set(folder_formated)

    # Find elements in array_two that are not in array_one
    elements_not_in_array_one = set_one - set_two

    # Convert the result back to a list and check file
    result_list = list(elements_not_in_array_one)
    return result_list



def function_formatter(file_path_raw_data, file_path_data_formated, name_file, sheet_name, len_catalog, names_columns_sheet):

    raw_data = pd.read_excel(file_path_raw_data + '\\' + name_file, dtype=str, header=None, sheet_name=sheet_name)
    # # search skip rows
    index = module_process_data.get_row(raw_data, 'NỘI DUNG', 0) + 1
    # # insert field "NGÀY BÁO CÁO" and delete row cotain "NGÀY BÁO CÁO 16/10/2023"
    print(name_file)
    for i in range(0,len(names_columns_sheet)):
        raw_data.rename(columns={i: names_columns_sheet[i]}, inplace=True)
   
    df = raw_data.iloc[index:, :len(names_columns_sheet)].copy()
    date = {
        "date_column": 'NGÀY BÁO CÁO',
        "value_column" : module_process_string.convert_date(name_file)
    }
    df.insert(0, date["date_column"], date["value_column"])
    
    # # insert field "DANH MỤC 1"
    # # insert field "DANH MỤC 2"
    # # insert field "DANH MỤC 3"
    df = module_process_data.insert_many_columns(df,len_catalog)
    
    df = module_process_data.add_catalog_1(df, 2, '^[A-Z]\\..*')
    df = module_process_data.add_catalog_2(df, 3, '^[1-9]\.\s\D', '^[A-Z]\\..*')
    df = module_process_data.add_catalog_3(df, 4, '^[1-9]\.[1-9]\s*', '^[A-Z]\\..*','^[1-9]\.\s\D' )
    df = module_process_data.add_catalog_4(df, 5, '^-\s*')
    df = df.drop(columns={"NỘI DUNG"})
    finally_df = df.copy()
    finally_df.to_excel(file_path_data_formated +  '\\RESULT_' + name_file, index=False)





import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


def on_created(event):
    print('created event................................................................!')
    # List of files by type
    print(module_process_file.list_files(file_path_raw_data))
    files_raw_data      = module_process_file.check_file(module_process_file.list_files(file_path_raw_data),False)

    files_data_formated_sheet_1 = module_process_file.check_file(module_process_file.list_files(file_path_data_formated_sheet_1),True)
    files_data_formated_sheet_2 = module_process_file.check_file(module_process_file.list_files(file_path_data_formated_sheet_2),True)
    result_list_sheet_1 = check_folder(files_raw_data, files_data_formated_sheet_1)
    
    for i in range(len(result_list_sheet_1)):
        function_formatter(file_path_raw_data, file_path_data_formated_sheet_1,result_list_sheet_1[i], sheet_name_1, len_catalog_1, names_columns_sheet_1)

    result_list_sheet_2 = check_folder(files_raw_data, files_data_formated_sheet_2)
    for i in range(len(result_list_sheet_2)):
        function_formatter(file_path_raw_data, file_path_data_formated_sheet_2,result_list_sheet_2[i], sheet_name_2, len_catalog_2, names_columns_sheet_2)
        

def watch_directory_app_pvcfcco(path):
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
            time.sleep(0)
    except KeyboardInterrupt:
        print('Exiting...!')
        observer.stop()
    observer.join()

watch_directory_app_pvcfcco(file_path)