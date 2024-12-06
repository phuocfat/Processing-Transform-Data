from datetime import datetime

def convert_date(strings):
    """
    Converts a date string from a specified format to a standard format.

    Parameters:
        strings (str): The input string containing a date in a specific format.

    Returns:
        str: The formatted date string in the "YYYY-MM-DD" format.
    """
    try:
        # Extracts the date part from the input string
        date_part = strings.split('_')[-1].split('.')[0].strip()

        # Parses the date string using the specified format ("%Y%m%d")
        parsed_date = datetime.strptime(date_part, "%Y%m%d")

        # Formats the parsed date to the desired format ("%Y-%m-%d")
        formatted_date = parsed_date.strftime("%Y-%m-%d")

        # Returns the formatted date string
        return formatted_date
    except:
        print("Error file name need to format again: " + strings)
        return False

def convert_date_(string):
    try:
        # Extract numeric part from the input string
        numeric_part = ''.join(char for char in string if char.isdigit())

        # Parse the numeric part as a date
        date_object = datetime.strptime(numeric_part, '%Y%m%d')

        # Format the date as 'YYYY-MM-DD'
        formatted_date = date_object.strftime('%Y-%m-%d')
        return formatted_date
    except:
        print("Error file name need to format again: " + string)
        return False
    
import re
def take_percent(string):
    pattern = r"\b\d+,\d+\s*%"

    # Use re.search to find the first match in the string
    match = re.search(pattern, string)

    # Check if a match is found
    if match:
        result = match.group(0)
        return result
    else:
        print("No match found")
        return 0
            