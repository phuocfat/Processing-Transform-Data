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
pvcfc_json          = info_json["PVCFC"]
file_path           = pvcfc_json["URI_PVCFC"]
names_columns       = pvcfc_json["NAMES_COLUMNS"]
len_catalog         = pvcfc_json["LEN_CATALOG"]

# URI file path
file_path_raw_data_file_xls     = file_path + '\\New_Input\\File XLS'
file_path_raw_data_file_xlsx    = file_path + '\\New_Input\\File XLSX'
file_path_data_formated         = file_path + '\\\Output'

# files_data_formated = module_process_file.remove_dot(module_process_file.check_file(module_process_file.list_files(file_path_data_formated), True))



def function_formatter(file_path_raw_data, file_path_data_formated, name_file, len_catalog):
    #
    raw_data  = pd.read_excel(file_path_raw_data + "\\" + name_file + '.xlsx', dtype=str, header=None)
    raw_data = raw_data.drop(0, axis=1)
    
    index_start = module_process_data.get_row(raw_data, 'NỘI DUNG', 0) + 1
    index_end = module_process_data.get_row(raw_data, '2. Môi trường', 0) - 12
    df = raw_data.iloc[index_start+1:, :].head(index_end).copy()
    df.rename(columns={1: names_columns[0], 2: names_columns[1], 3: names_columns[2], 4: names_columns[3], 5: names_columns[4], 6: names_columns[5], 7: names_columns[6]}, inplace=True)
    
    search_string = ["4. Tồn kho",".1 Ure rời","4.2 Ure ba", "- Loại bao thương mại", "- Loại bao không thương mại", "4.3 N46Plus bao"]
    from_to = []
    for i in range(len(search_string)):
        index = module_process_data.get_row(df, search_string[i], 0)
        from_to.append(index)
    for i in from_to:
        df = module_process_data.move_value_column(df, 2, 4, i)
    
    string = ['3. NH3 dư về bồn', '4. NH3 xuất bán', '5. NH3 tồn kho']
    string_replace = ['3. Dư về bồn', '4. Xuất bán', '5. Tồn kho']
    df = module_process_data.replace_val_row(df, string, string_replace, 0)
   
   
    df.insert(7, names_columns[7],'')
    # concate 2columns: GHI CHÚ	+ ''
    df[names_columns[5]] = df[names_columns[5]] + " " + df[names_columns[6]]
    df = df.drop(names_columns[6], axis=1)
    
    index =  module_process_data.get_row(df, 'E. CHẤT LƯỢNG SẢN PHẨM', 0) #Chỗ CHẤT LƯỢNG SẢN PHẨM sửa thành 
    df.iloc[index,0] = 'E. CHẤT LƯỢNG SẢN PHẨM - URE HẠT'
    new_row_data = {'NỘI DUNG': 'G. TÌNH HÌNH HOẠT ĐỘNG'}
    df = pd.concat([df.iloc[:index+4, :], pd.DataFrame([new_row_data]) ,df.iloc[index+4:, :]], ignore_index=True)
    index = module_process_data.get_row(df, 'G. AN TOÀN LAO ĐỘNG VÀ MÔI TRƯỜNG', 0)
    df.iloc[index,0] = 'H. AN TOÀN LAO ĐỘNG VÀ MÔI TRƯỜNG'
    
    from_index = module_process_data.get_row(df, 'E. CHẤT LƯỢNG SẢN PHẨM', 0)
    to_index = module_process_data.get_row(df, 'H. AN TOÀN LAO ĐỘNG VÀ MÔI TRƯỜNG', 0)
    
    for i in range(from_index+5,to_index):
        df = module_process_data.move_value_column(df, 1, 5, i)
    
    index = module_process_data.get_row(df, '5. Tồn kho', 0)
    df = module_process_data.move_value_column(df, 3, 5, index)

    df.iloc[index, 5] = df.iloc[index, 5].replace(',', '.')
    df.iloc[index, 5] = df.iloc[index, 5].replace('%', '')
    df.iloc[index, 5] = float(df.iloc[index, 5]) / 100
    
    
    
    # 
    string_replace_1  = 'Tiêu chuẩn'
    index_search_1 = module_process_data.get_row(df, string_replace_1,0)
    string_replace_1 = '1. ' + string_replace_1
    df.iloc[index_search_1, 0] = string_replace_1
    # 
    string_replace_2  = 'Thực tế sản xuất trong ngày'
    index_search_2 = module_process_data.get_row(df, string_replace_2,0)
    string_replace_2 = '2. ' +string_replace_2
    df.iloc[index_search_2, 0] = string_replace_2
    
    string_replace_3  = 'Ure hạt'
    index_search_3 = module_process_data.get_row(df, string_replace_3,0)
    temp_arr = df.iloc[index_search_3:index_search_3+3, :]


    print(temp_arr.iloc[:,:3])
    # 1-4
    new_rows_1 = pd.DataFrame({

        'NỘI DUNG':[temp_arr.iloc[0,1], temp_arr.iloc[0,2], temp_arr.iloc[0,3], temp_arr.iloc[0,4]],
        'ĐƠN VỊ':['%', '%', '%', '%'],
        'NGÀY':[temp_arr.iloc[1,1], temp_arr.iloc[1,2], temp_arr.iloc[1,3], temp_arr.iloc[1,4]]
    })
    new_rows_2 = pd.DataFrame({
        'NỘI DUNG':[temp_arr.iloc[0,1], temp_arr.iloc[0,2], temp_arr.iloc[0,3], temp_arr.iloc[0,4]],
        'ĐƠN VỊ':['%', '%', '%', '%'],
        'NGÀY':[temp_arr.iloc[2,1], temp_arr.iloc[2,2], temp_arr.iloc[2,3], temp_arr.iloc[2,4]]
    })
    print(new_rows_2)
    new_rows_1["NGÀY"] = new_rows_1['NGÀY'].str.replace(',', '.')
    new_rows_2["NGÀY"] = new_rows_2['NGÀY'].str.replace(',', '.')
    
    
    top_temp_df = df.iloc[:index_search_1+1, :]
    bottom_temp_df_2 = df.iloc[index_search_1+1:index_search_1+2, :]
    bottom_temp_df_3 =  df.iloc[index_search_1+2:, :]
    
    
    df = pd.concat([top_temp_df, new_rows_1, bottom_temp_df_2,new_rows_2, bottom_temp_df_3])
    
    
    index_search_1 = module_process_data.get_row(df, string_replace_1,0)
    index_search_2 = module_process_data.get_row(df, string_replace_2,0)
    index_search_3 = module_process_data.get_row(df, string_replace_3,0)
    df.iloc[index_search_1, 1:] = ''
    df.iloc[index_search_2, 1:] = ''
    df = df.drop([index_search_3])
    # # replace columns has value '%' to '-'
    df.iloc[:,0] = df.iloc[:, 0].str.replace('%', '-')


    number_title  = '2.'
    string_replace_4 = number_title + ' Môi trường'
    index_search = module_process_data.get_row(df, string_replace_4, 0) - 1
    
    title_string_1 = df.iloc[index_search+1, 1]
    title_string_2 = df.iloc[index_search+2, 1]
    
    dv_string_1 = 'mg/m3'
    dv_string_2 = 'mg/l'
    
    # # create dataframe tempt
    dataframe_temp = df.iloc[index_search:index_search+4,:]
    
    new_rows_3 = pd.DataFrame({
        'NỘI DUNG':[string_replace_4, number_title + '1' + title_string_1, '- ' + dataframe_temp.iloc[0, 2], '- ' + dataframe_temp.iloc[0, 3]],
        'ĐƠN VỊ':[None,None,dv_string_1, dv_string_1],
        'NGÀY':[None,None,dataframe_temp.iloc[1, 2],dataframe_temp.iloc[1, 3]],
        'GHI CHÚ': [None, None, dataframe_temp.iloc[1, 2] if '≤' in dataframe_temp.iloc[1, 2] else None, dataframe_temp.iloc[1, 4]]
    })
    
    new_rows_3["NGÀY"] = new_rows_3['NGÀY'].str.replace(' mg/m3', '')
    new_rows_3["NGÀY"] = new_rows_3['NGÀY'].str.replace(',', '.')
    new_rows_3["NGÀY"] = new_rows_3['NGÀY'].str.replace('≤ ', '')
    
    new_rows_4 = pd.DataFrame({
        'NỘI DUNG':[number_title + '2 ' + title_string_2, '- ' + dataframe_temp.iloc[0, 2], '- ' + dataframe_temp.iloc[0, 3]],
        'ĐƠN VỊ':[None,dv_string_2, dv_string_2],
        'NGÀY':[None,dataframe_temp.iloc[2, 2],dataframe_temp.iloc[2,3]],
        'GHI CHÚ': [None,  dataframe_temp.iloc[2, 2] if '≤' in dataframe_temp.iloc[2, 2] else None, dataframe_temp.iloc[2, 4]]
    })
    
    new_rows_4["NGÀY"] = new_rows_4['NGÀY'].str.replace(' mg/l', '')
    new_rows_4["NGÀY"] = new_rows_4['NGÀY'].str.replace(',', '.')
    new_rows_4["NGÀY"] = new_rows_4['NGÀY'].str.replace('≤ ', '')
    top_temp_df = df.iloc[:index_search, :]

    df = pd.concat([top_temp_df,new_rows_3, new_rows_4])
    
    date = {
        "date_column": 'NGÀY BÁO CÁO',
        "value_column" : module_process_string.convert_date(name_file)
    }
    
    df.insert(0, date["date_column"], date["value_column"])
    
    df = module_process_data.insert_many_columns_(df, 'CẤP',len_catalog)
    
    df = module_process_data.add_catalog_1(df, 2, '^[A-Z]\\..*')
    df = module_process_data.add_catalog_2(df, 3, '^[1-9]\.\s\D', '^[A-Z]\\..*')
    df = module_process_data.add_catalog_3_(df, 4, '^[1-9]\.[1-9]\s*', '^[A-Z]\\..*','^[1-9]\.\s\D', r'^-\s')
    df = module_process_data.add_catalog_4(df, 5, r'^-\s')
    
    index_start = module_process_data.get_row(df, '2. Tiêu hao', 1)
    index_end = module_process_data.get_row(df,'5. Tình hình cung cấp khí Gas', 1)
    df.iloc[index_start:index_end, 4] = ''
    
    index = module_process_data.get_row(df, 'Khí tự nhiên', 1) + 1
    df.iloc[index, 3] = 'Khí tự nhiên'
    index = module_process_data.get_row(df,'Permeat gas', 1) + 1
    df.iloc[index, 3] = 'Permeat gas'
    df.iloc[:, 7:9] = df.iloc[:, 7:9].apply(lambda x: x.str.replace(',', ''), axis=1)
    
    index = module_process_data.get_row(df,'Công suất thực tế', 10)
   
    val_percent = module_process_string.take_percent(df.iloc[index, 10]) #113,22% => 113.22%
    df.iloc[:10, 10] = ''
    df.iloc[0, 11] = val_percent
    df.iloc[:,11] = df.iloc[:, 11].str.replace(',', '.')
    df.iloc[:,11] = df.iloc[:, 11].str.replace(' %', '')
    df.iloc[0, 11] = float(df.iloc[0, 11]) / 100

    index_check = module_process_data.get_row(df,',', 10)
    df.iloc[index_check, 10] =  df.iloc[index_check, 10].replace(',', '.')

    df = df.drop(columns=['NỘI DUNG'])
    
    df.to_excel(file_path_data_formated + "\\RESULT_"+ name_file + ".xlsx", index=False)



import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

def on_created(event):
    print('created event................................................................!')
    all_new_file_xls = module_process_file.comparison_folder(file_path_raw_data_file_xls, file_path_raw_data_file_xlsx, False)
    module_process_file.check_file_and_convert(all_new_file_xls, file_path_raw_data_file_xls, file_path_raw_data_file_xlsx)
    all_new_file_xlsx = module_process_file.comparison_folder(file_path_raw_data_file_xlsx, file_path_data_formated, True)
    for i in range(len(all_new_file_xlsx)):
        function_formatter(file_path_raw_data_file_xlsx, file_path_data_formated, all_new_file_xlsx[i], len_catalog)

def watch_directory_app_pvcfc(path):
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

watch_directory_app_pvcfc(file_path)