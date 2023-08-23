from dateutil.parser import parse
from datetime import datetime, timedelta
import re
def date_handler(input_string):
    output_date = convert_to_dd_mm_yyyy(input_string)
    if output_date == "Invalid date format":
        output_date = invalid_date_helper(input_string)
        
    return output_date
def calculate_date(input_string):
    if input_string == "today":
        return datetime.today().strftime('%d-%m-%Y')
    input_string = input_string.replace(" ","")
    pattern = r'(today)([+-])(\d+).*'
    match = re.match(pattern, input_string)

    if match:
        operator = match.group(2)
        days = int(match.group(3))

        if operator == '+':
            result_date = datetime.today() + timedelta(days=days)
        elif operator == '-':
            result_date = datetime.today() - timedelta(days=days)
        else:
            return None

        return result_date.strftime('%d-%m-%Y')
    else:
        return None
def convert_to_dd_mm_yyyy(date_string):
    try:
        date_object = parse(date_string)
        formatted_date = date_object.strftime('%d-%m-%Y')
        return formatted_date
    except ValueError:
        return "Invalid date format"

def invalid_date_helper(date_string):
    if "today" in date_string:
        result = calculate_date(date_string)
        if result != "None":
            return result
    return "Date time picker"
            
    

