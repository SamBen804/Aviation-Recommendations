import pandas as pd
import numpy as np

def clean_manufacturer_PA(name):

    """

    Parameters:
    - name (str): The manufacturer name to be cleaned.

    Returns:
    - str: The cleaned manufacturer name.

    Logic:
        This function takes a string as input and returns a cleaned version of the string. 
        It first converts the string to lower case and strips any leading or trailing white spaces. 
        Then it replaces certain separators (such as '/', '-', '&', 'and', ',') with a space. 
        It also removes certain vehicle type indicators (such as 'helicopter', 'aircraft', 'aviacija', 'balloon', 
        'balloons', 'aviation', 'gmbh', 'co.', 'llc', 'leasing', 'limited', 'ltd', 'inc', 'corp', 
        'corporation', 'company', 'sa', 'sas', 'bv', 'plc', 'pte', 'kg') from the string.
        Finally, it returns the cleaned string.
    """

    name = str(name)

    separators = [
        '/', 
        '-', 
        '&', 
        ' and ', 
        ' and', 
        'and ', 
        ','
    ]

    vehicle_types = [
        'helicopter', 
        'aircraft', 
        'aviacija', 
        'balloon', 
        'balloons', 
        'aviation', 
        'gmbh', 
        'co.', 
        'llc', 
        'leasing', 
        'limited', 
        'ltd', 
        'inc', 
        'corp', 
        'corporation', 
        'company', 
        'sa', 
        'sas', 
        'bv', 
        'plc', 
        'pte', 
        'kg'
    ]

    name = name.lower().strip()

    for sep in separators:
        if sep in name:
            name = name.replace(sep, ' ')
            break

    for vehicle_type in vehicle_types:
        name = name.replace(' ' + vehicle_type, '')
        name = name.replace(vehicle_type + ' ', '')
        name = name.replace(vehicle_type, '')

    return name.strip()

def clean_data_PA(plane_accidents_raw):

    """

    Parameters:
    - plane_accidents_raw (pandas.DataFrame): The raw dataframe of plane accidents data to be cleaned.

    Returns:
    - pandas.DataFrame: The cleaned dataframe of plane accidents data.

    Logic:
        This function takes a dataframe of plane accident data and returns a cleaned version of it.
        It first creates a copy of the dataframe and then renames the columns to remove any '.' characters and to make them lower case.
        It also renames the 'event_date' column to 'year' and converts the dates to years.
        It then selects the relevant columns and removes any rows where 'amateur_built' is 'No'.
        It applies the clean_manufacturer_PA function to the 'make' column and cleans the 'model' column by removing '-' and '/' characters, 
        converting the string to lower case, and taking only the first 3 digits.
        Finally, it resets the index and returns the cleaned dataframe.
    """

    relevant_columns = [
        'year',
        'aircraft_damage',
        'make',
        'model',
        'amateur_built',
        'total_fatal_injuries',
        'total_serious_injuries',
        'total_minor_injuries',
    ]

    plane_accidents = plane_accidents_raw.copy()

    column_map = {col: col.replace('.', '_').lower() for col in plane_accidents.columns}
    plane_accidents.rename(columns=column_map, inplace=True)
    plane_accidents.rename(columns={'event_date': 'year'}, inplace=True)
    plane_accidents = plane_accidents[relevant_columns]
    plane_accidents = plane_accidents[plane_accidents['amateur_built'] == 'No'].drop(columns='amateur_built')
    plane_accidents['year'] = plane_accidents['year'].apply(lambda date: pd.to_datetime(date).year)
    plane_accidents['make'] = plane_accidents['make'].apply(clean_manufacturer_PA).apply(
        lambda make: 'boeing' if 'boeing' in make else make
    )

    plane_accidents['model'] = plane_accidents['model'].astype(str).apply(
        lambda model: model.strip().replace('-', '').replace('/', '').lower()
    ).apply(
        lambda model: ''.join(filter(str.isdigit, str(model)))
    ).apply(
        lambda model: model[:3]
    )

    return plane_accidents.reset_index().drop(columns='index')

def clean_manufacturer_PI(name):

    """

    Parameters:
    - name (str): The manufacturer name to be cleaned.

    Returns:
    - str: The cleaned manufacturer name.

    Logic:
        This function takes a string as input and returns a cleaned version of the string.
        It first removes leading or trailing spaces and converts the string to lower case.
        It also replaces '/' and '-' characters with spaces.
        If the string starts with 'iberia', it removes 'iberia'. 
        If 'iberia' is present anywhere in the string, it removes it.
        Similarly, if 'vueling' is present anywhere in the string or if the string starts with 'vueling', it removes 'vueling'.
        If the string is 'philippineairlines', it replaces it with NaN.
        It then checks if the string contains any of the old values specified in the 'replacements' dictionary.
        If it does, it replaces the old value with the corresponding new value.
        If 'gulf' is present in the string, it replaces it with 'gulfstream'.
        Finally, it replaces spaces with '/' and returns the cleaned string.
    """

    replacements = {
    'boeing': ['boeing'],
    'mcdonnell douglas': ['mcd', 'md'],
    'raytheon': ['raetheon'],
    'airbus': ['airbus', 'industr', 'company'],
    'gecas': ['gecas'],
    'alitalia': ['alitalia'],
    'alc': ['alc'],
    'learjet': ['lear'],
    'saab': ['saab aircraft', 'saabaircraft'],
    'jplease': ['jplease'],
    'beechcraft': ['beech'],
    'smbc': ['smbc'],
    'gulfstreamaerospace': ['gulf'],
    'unknown': ['kuban oakhill'],
    'dassault': ['dassult'],
    'douglas': ['douglas'],
    'iailtd': ['israelaircraftindustries'],
    'fokker': ['fokker'],
    'bombardier': ['bombardier']
    }

    name = name.strip().lower().replace('/', ' ').replace('-', ' ')
    if name.startswith('iberia'):
        name = name[7:]
    if 'iberia' in name:
        name = name.replace('easyjet ', '').replace('easyjet', '')
    if 'vueling' in name or name.startswith('vueling'):
        name = name.replace('vueling ', '')
    if name == 'philippineairlines':
        name = str(np.nan)
    for new_value, old_values in replacements.items():
        if any(old_value in name for old_value in old_values):
            return new_value
        
    return name.replace(' ', '/')

def clean_data_PI(plane_inventory_raw):

    """

    Parameters:
    - plane_inventory_raw (pandas.DataFrame): The raw dataframe of plane inventory data to be cleaned.

    Returns:
    - pandas.DataFrame: The cleaned dataframe of plane inventory data.

    Logic:
        This function takes a dataframe of plane inventory data and returns a cleaned version of it.
        It first creates a copy of the dataframe and then renames the columns to make them lower case.
        It resets the index and applies the clean_manufacturer_PI function to the 'manufacturer' column.
        It also cleans the 'model' column by removing '-' and '/' characters, converting the string to lower case, 
        and taking only the first 3 digits.
        Finally, it selects the relevant columns and returns the cleaned dataframe.
    """

    relevant_columns = [
        'year',
        'make',
        'model',
        'number_of_seats'

    ]

    plane_inventory = plane_inventory_raw.copy()
    column_map = {col: col.lower() for col in plane_inventory.columns}
    plane_inventory.rename(columns=column_map, inplace=True)

    # plane_inventory = plane_inventory.drop_duplicates(subset=['serial_number'], keep='last')
    plane_inventory = plane_inventory.reset_index().drop(columns='index')
    plane_inventory['manufacturer'] = plane_inventory['manufacturer'].apply(clean_manufacturer_PI)
    plane_inventory['manufacturer'] = plane_inventory['manufacturer'].apply(
        lambda name: 'gulfstream' if 'gulf' in name else name
    ).apply(
        lambda name: name.replace(' ', '/')
    )
    
    plane_inventory.rename(columns={'manufacturer': 'make'}, inplace=True)
    
    plane_inventory['model'] = plane_inventory['model'].astype(str).apply(
        lambda x: x.strip().replace('-', '').replace('/', '').lower()
    ).apply(
        lambda x: ''.join(filter(str.isdigit, str(x)))
    ).apply(
        lambda x: x[:3]
    )

    return plane_inventory[relevant_columns]