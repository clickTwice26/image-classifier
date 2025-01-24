from datetime import datetime
import pytz

dhaka_tz = pytz.timezone('Asia/Dhaka')

def format_datetime_to_dhaka(value):
    if value is None:
        return ''
    
    if value.tzinfo is None:
        value = pytz.utc.localize(value)
    
    value_in_dhaka = value.astimezone(dhaka_tz)
    
    return value_in_dhaka.strftime('%I:%M %p, %b %d, %Y') 