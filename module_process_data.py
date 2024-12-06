import re
import numpy as np


def clear_junk_data(data_frame, position_from):
    for column in range(position_from, data_frame.shape[1]):
        for row in range(data_frame.shape[0]):
            temp_val = str(data_frame.iloc[row, column])
            check = re.sub(r'-', '', temp_val)
            if check is not None:
                data_frame.iloc[row ,column] = check
    return data_frame
def get_row(data_frame, content, p):
    """
    Finds the index of the first row where a specified content is found in a specific column (p) of the data frame.

    Parameters:
        data_frame (pandas.DataFrame): The input data frame.
        content (str): The content to search for in the specified column.
        p (int): The index of the column to search in.

    Returns:
        int: The index of the first row where the specified content is found, or 0 if not found.
    """
    process_search = data_frame.iloc[:, p].str.contains(content, na=False)
    index = np.where(process_search == True)[0][0]
    if index > 0:
        return index
    return 0

def add_catalog_1(data_frame, catalog_position, regax):
    """
    Adds catalog information to a specified column based on a regular expression (regax).

    Parameters:
        data_frame (pandas.DataFrame): The input data frame.
        catalog_position (int): The index of the column where catalog information will be added.
        regax (str): The regular expression to match for catalog information.

    Returns:
        pandas.DataFrame: The modified data frame with added catalog information.
    """
    filtered_df_catalog = data_frame.iloc[:, 1].str.contains(regax)
    value_catalog = ''
    for i in range(0, len(filtered_df_catalog)):
        if filtered_df_catalog.iloc[i] == True:
            value_catalog = data_frame.iloc[i, 1].rsplit('.', 1)[-1].strip()
            data_frame.iloc[i, catalog_position] = value_catalog
        else:
            data_frame.iloc[i, catalog_position] = value_catalog
    return data_frame

def add_catalog_2(data_frame, catalog_position, regax_2, regax_1):
    """
    Adds catalog information to a specified column based on two regular expressions (regax_1 and regax_2).

    Parameters:
        data_frame (pandas.DataFrame): The input data frame.
        catalog_position (int): The index of the column where catalog information will be added.
        regax_2 (str): The second regular expression to match for catalog information.
        regax_1 (str): The first regular expression to check for exclusion.

    Returns:
        pandas.DataFrame: The modified data frame with added catalog information.
    """
    filtered_df_catalog = data_frame.iloc[:, 1].str.contains(regax_2)
    check = data_frame.iloc[:, 1].str.contains(regax_1)
    value_catalog = ''
    for i in range(0, len(filtered_df_catalog)):
        if filtered_df_catalog.iloc[i] == True:
            value_catalog = data_frame.iloc[i, 1].rsplit('.', 1)[-1].strip()
            data_frame.iloc[i, catalog_position] = value_catalog
        if check.iloc[i] == False:
            data_frame.iloc[i, catalog_position] = value_catalog
    return data_frame

def add_catalog_3(data_frame, catalog_position, regax_3, regax_1, regax_2):
    """
    Adds catalog information to a specified column based on three regular expressions (regax_1, regax_2, and regax_3).

    Parameters:
        data_frame (pandas.DataFrame): The input data frame.
        catalog_position (int): The index of the column where catalog information will be added.
        regax_3 (str): The third regular expression to match for catalog information.
        regax_1 (str): The first regular expression to check for exclusion.
        regax_2 (str): The second regular expression to check for exclusion.

    Returns:
        pandas.DataFrame: The modified data frame with added catalog information.
    """
    filtered_df_catalog = data_frame.iloc[:, 1].str.contains(regax_3)
    check_1 = data_frame.iloc[:, 1].str.contains(regax_1)
    check_2 = data_frame.iloc[:, 1].str.contains(regax_2)
    value_catalog = ''
    
    for i in range(0, len(filtered_df_catalog)):
            if filtered_df_catalog.iloc[i] == True:
                pattern = r'^\d+\.[1-9][0-9]?\s*'
                value_catalog = re.sub(pattern, '', data_frame.iloc[i,1])
                data_frame.iloc[i, catalog_position] = value_catalog
            if check_1.iloc[i] == False and check_2.iloc[i] == False :
                data_frame.iloc[i, catalog_position] = value_catalog
            
    return data_frame
def add_catalog_3_(data_frame, catalog_position, regax_3, regax_1, regax_2, regax_4):
    """
    Adds catalog information to a specified column based on three regular expressions (regax_1, regax_2, and regax_3).

    Parameters:
        data_frame (pandas.DataFrame): The input data frame.
        catalog_position (int): The index of the column where catalog information will be added.
        regax_3 (str): The third regular expression to match for catalog information.
        regax_1 (str): The first regular expression to check for exclusion.
        regax_2 (str): The second regular expression to check for exclusion.

    Returns:
        pandas.DataFrame: The modified data frame with added catalog information.
    """
    filtered_df_catalog = data_frame.iloc[:, 1].str.contains(regax_3)
    check_1 = data_frame.iloc[:, 1].str.contains(regax_1)
    check_2 = data_frame.iloc[:, 1].str.contains(regax_2)
    check_3 = data_frame.iloc[:, 1].str.contains(regax_4)
    value_catalog = ''
    
    for i in range(0, len(filtered_df_catalog)):
            if filtered_df_catalog.iloc[i] == True:
                pattern = r'^\d+\.[1-9][0-9]?\s*'
                value_catalog = re.sub(pattern, '', data_frame.iloc[i,1])
                data_frame.iloc[i, catalog_position] = value_catalog
            if check_1.iloc[i] == False and check_2.iloc[i] == False:
                data_frame.iloc[i, catalog_position] = value_catalog

            
    return data_frame

def add_catalog_4(data_frame, catalog_position, regax):
    """
    Adds catalog information to a specified column based on a regular expression (regax).

    Parameters:
        data_frame (pandas.DataFrame): The input data frame.
        catalog_position (int): The index of the column where catalog information will be added.
        regax (str): The regular expression to match for catalog information.

    Returns:
        pandas.DataFrame: The modified data frame with added catalog information.
    """
    filtered_df_catalog = data_frame.iloc[:, 1].str.contains(regax)
    value_catalog = ''
    for i in range(0, len(filtered_df_catalog)):
  
        if filtered_df_catalog.iloc[i] == True:
            value_catalog = re.sub(regax, '', data_frame.iloc[i,1])
            data_frame.iloc[i, catalog_position] = value_catalog
    return data_frame


def insert_many_columns(data_frame,len_catalog):
    for i in range(len_catalog):
        data_frame.insert(i+2, 'DANH MỤC {0}'.format(i+1),'')
    return data_frame

def insert_many_columns_(data_frame,title,len_catalog):
    for i in range(len_catalog):
        data_frame.insert(i+2, '{0} {1}'.format(title,i+1),'')
    return data_frame

def move_value_column(data_frame, index_column_from, index_column_to, index_row):
    data_frame.iloc[index_row, index_column_to] = data_frame.iloc[index_row, index_column_from]
    data_frame.iloc[index_row, index_column_from] = ''
    return data_frame


def replace_val_row(df, arr_val, arr_val_replace, index_column):
    for i in range(0,3):
        index = get_row(df, arr_val[i], 0)
        df.iloc[index, 0] = arr_val_replace[i]
    return df