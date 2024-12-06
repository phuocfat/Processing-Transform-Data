import json
import os
import re
def read_json_file(path):
    """
    Reads a JSON file and returns the loaded data.

    Parameters:
        path (str): The path to the JSON file.

    Returns:
        dict or None: The loaded JSON data if successful, None otherwise.
    """
    try:
        with open(path, 'r', encoding='utf-8') as file:
            data_config = json.load(file)
    except FileNotFoundError:
        print(f"The file config was not found.")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON in file config:{e}.")
    else:
        print("JSON file config loaded successfully.")
    finally:
        print("This code always runs, whether an exception occurred or not.")

    if 'data_config' in locals():
        return data_config


def remove_dot(array_name_file):
    arr = []
    for i in range(len(array_name_file)):
        file_name = array_name_file[i].rsplit('.', 1)[0]
        arr.append(file_name)
    return arr

def check_file(array_file, is_clear_name):
    """
    Filters a list of filenames to include only those with a '.xlsx' extension.

    Parameters:
        array_file (list): List of filenames.

    Returns:
        list: Filtered list containing only filenames with the '.xlsx' extension.
    """
    
    if is_clear_name == True:
        for i in range(len(array_file)):
                array_file[i] = re.sub('RESULT_','',array_file[i])
    temp_array = []
    for i in range(len(array_file)):
        if str.lower(array_file[i].rsplit('.', 1)[1]) == 'xlsx':
            temp_array.append(array_file[i])
    temp_array = [file for file in temp_array if '~$' not in file]
    return temp_array

def check_file_(array_file, is_clear_name):
    """
    Filters a list of filenames to include only those with a '.xlsx' extension.

    Parameters:
        array_file (list): List of filenames.

    Returns:
        list: Filtered list containing only filenames with the '.xlsx' extension.
    """
    if is_clear_name == True:
        for i in range(len(array_file)):
                array_file[i] = re.sub('RESULT_','',array_file[i])
    temp_array = []
    for i in range(len(array_file)):
        if str.lower(array_file[i].rsplit('.', 1)[1]) == 'xls':
            temp_array.append(array_file[i])
    temp_array = [file for file in temp_array if '~$' not in file]
    return temp_array

def list_files(directory):
    try:
        return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    except OSError as e:
        print(f"Error accessing directory '{directory}': {e}")
        return []
    

def list_files_pvcfcco(directory):
    """Lists files with extensions .xlsx or starting with 'update' (excluding 'updated').

    Args:
        directory: The directory path to search for files.

    Returns:
        A list of filenames that match the criteria, or an empty list if there's an error.
    """

    try:
        files_filter_1 = [f for f in os.listdir(directory) if (f.endswith(".xlsx")) and os.path.isfile(os.path.join(directory, f))]
        files_filter_2 = []
        
        for file in files_filter_1:
            if not file.lower().startswith('_updated'):
                files_filter_2.append(file)
        return files_filter_2
    
    except OSError as e:
        print(f"Error accessing directory '{directory}': {e}")
        return []


def list_files_v_2(directory):
    """Liệt kê các file có đuôi .xlsx trong thư mục đã cho.

    Args:
        directory (str): Đường dẫn đến thư mục cần liệt kê file.

    Returns:
        list: Danh sách các file .xlsx trong thư mục, nếu thành công.
        []: Danh sách rỗng, nếu có lỗi truy cập thư mục.
    """

    try:
        return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f)) and f.endswith(".xlsx")]
    except OSError as e:
        print(f"Error accessing directory '{directory}': {e}")
        return []


import win32com.client as client
import threading
import pythoncom

def convert_xls_to_xlsx(file_path_input, file_path_output):
    try:
        if threading.currentThread():
            pythoncom.CoInitialize()
            print("Converting from xls to xlsx.................!")
            excel = client.Dispatch("excel.application")
            wb = excel.Workbooks.open(file_path_input)
            # 51: XLSX (Excel Workbook)
            # 52: XLSM (Excel Macro-Enabled Workbook)
            # 56: XLS (Excel 97-2003 Workbook)
            wb.SaveAs(file_path_output,51)
            wb.Close()
            excel.Quit()
    except Exception as e:
        print(e)
 

def check_file_and_convert(result_list, file_path_raw_data, file_path_data_formated):
    try:
       if len(result_list) == 0:
            print("No new file convert !!!!")
       else:
            for i in range(len(result_list)):
                convert_xls_to_xlsx(file_path_raw_data + "\\"+ result_list[i], file_path_data_formated + "\\" + result_list[i] )
    except Exception as e:
        print(e)



def comparison_folder(folder_path_from, folder_path_to, is_file_from_xlsx):
    try:
        if  is_file_from_xlsx == False:
            files_raw_data_file_xls      = remove_dot(check_file_(list_files(folder_path_from), False))
            files_raw_data_file_xlsx     = remove_dot(check_file(list_files(folder_path_to), False))

            set_one = set(files_raw_data_file_xls)
            set_two = set(files_raw_data_file_xlsx)
            
            elements_not_in_array_one = set_one - set_two
            result_list = list(elements_not_in_array_one)
            return result_list
        
        elif is_file_from_xlsx == True:
            files_raw_data_file_xlsx      = remove_dot(check_file(list_files(folder_path_from), False))
            files_data_format             = remove_dot(check_file(list_files(folder_path_to), True))
            set_one = set(files_raw_data_file_xlsx)
            set_two = set(files_data_format)

            elements_not_in_array_one = set_one - set_two
            result_list = list(elements_not_in_array_one)
            return result_list
    except Exception as e:
        print(e)