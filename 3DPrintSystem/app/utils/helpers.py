import pytz
from datetime import datetime

def format_printer_name(printer_name):
    """Convert database printer names to display format"""
    if not printer_name:
        return 'Not specified'
    
    printer_map = {
        'prusa_mk4s': 'Prusa MK4S',
        'prusa_xl': 'Prusa XL', 
        'raise3d_pro2plus': 'Raise3D Pro 2 Plus',
        'formlabs_form3': 'Formlabs Form 3'
    }
    return printer_map.get(printer_name.lower(), printer_name)

def format_color_name(color_name):
    """Convert database color names to display format"""
    if not color_name:
        return 'Not specified'
    
    color_map = {
        'true_red': 'True Red',
        'true_orange': 'True Orange',
        'light_orange': 'Light Orange',
        'true_yellow': 'True Yellow',
        'dark_yellow': 'Dark Yellow',
        'lime_green': 'Lime Green',
        'green': 'Green',
        'forest_green': 'Forest Green',
        'blue': 'Blue',
        'electric_blue': 'Electric Blue',
        'midnight_purple': 'Midnight Purple',
        'light_purple': 'Light Purple',
        'clear': 'Clear',
        'true_white': 'True White',
        'gray': 'Gray',
        'true_black': 'True Black',
        'brown': 'Brown',
        'copper': 'Copper',
        'bronze': 'Bronze',
        'true_silver': 'True Silver',
        'true_gold': 'True Gold',
        'glow_in_dark': 'Glow in the Dark',
        'color_changing': 'Color Changing',
        'white': 'White',
        'black': 'Black'
    }
    return color_map.get(color_name.lower(), color_name.replace('_', ' ').title())

def format_discipline_name(discipline):
    """Convert database discipline to proper display format"""
    if not discipline:
        return 'Not specified'
    
    discipline_map = {
        'landscape_architecture': 'Landscape Architecture',
        'interior_design': 'Interior Design',
        'hobby_personal': 'Hobby/Personal'
    }
    return discipline_map.get(discipline.lower(), discipline)

def to_local_datetime(utc_datetime):
    """Convert UTC datetime to Central Time"""
    if utc_datetime is None:
        return None
    
    utc = pytz.UTC
    central = pytz.timezone('America/Chicago')
    
    if utc_datetime.tzinfo is None:
        utc_datetime = utc.localize(utc_datetime)
    
    return utc_datetime.astimezone(central)

def format_local_datetime(utc_datetime):
    """Format datetime in Central Time as MM/DD/YYYY at HH:MM AM/PM"""
    local_dt = to_local_datetime(utc_datetime)
    if local_dt is None:
        return 'N/A'
    return local_dt.strftime('%m/%d/%Y at %I:%M %p')

def detailed_local_datetime(utc_datetime):
    """Detailed format with timezone abbreviation"""
    local_dt = to_local_datetime(utc_datetime)
    if local_dt is None:
        return 'N/A'
    return local_dt.strftime('%m/%d/%Y at %I:%M %p %Z') 