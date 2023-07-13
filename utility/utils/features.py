import pandas as pd
import numpy as np

def engineer_make_model_feature_PAPI(df):

    """
    Parameters:
    - df (pandas.DataFrame): The dataframe which contains columns 'make' and 'model'.

    Returns:
    - pandas.DataFrame: The dataframe with a new column 'make_model' which is a combination of 'make' and 'model' columns.

    Logic:
    This function takes a dataframe as input and returns the dataframe with a new column 'make_model'. 
    The new column is a combination of 'make' and 'model' columns.
    """

    df = df.copy()
    df['make_model'] = df['make'] + ' ' + df['model']
    return df

def get_injury_feature_PA(plane_accidents):

    """
    Parameters:
    - plane_accidents (pandas.DataFrame): The dataframe which contains injury data.

    Returns:
    - pandas.Series: A series of injury categories based on the injury data in the dataframe.

    Logic:
    This function categorizes injuries into 'Fatal', 'Serious', 'Minor', or 'Unknown' based on the injury data in the dataframe.
    'Fatal' category is for rows where 'total_fatal_injuries' is greater than 0.
    'Serious' category is for rows where 'total_serious_injuries' is greater than 0.
    'Minor' category is for rows where 'total_minor_injuries' is greater than 0.
    'Unknown' category is for rows where all the above conditions are not met.
    """

    fatal_category = (plane_accidents['total_fatal_injuries'] > 0).apply(lambda x: 'Fatal' if x else np.nan)
    serious_category = (plane_accidents['total_serious_injuries'] > 0).apply(lambda x: 'Serious' if x else np.nan)
    minor_category = (plane_accidents['total_minor_injuries'] > 0).apply(lambda x: 'Minor' if x else np.nan)
    categorized_injuries = pd.concat([fatal_category, serious_category, minor_category], axis=1)
    return categorized_injuries.apply(lambda row: next((injury for injury in row if pd.notna(injury)), np.nan), axis=1).fillna('Unknown')

def get_injury_feature_numeric_PA(injury_feature):

    """
    Parameters:
    - injury_feature (pandas.Series): The series of injury categories.

    Returns:
    - pandas.Series: A series of numeric values corresponding to the injury categories.

    Logic:
    This function assigns numeric values to injury categories. 
    'Unknown' category is assigned a value of 0.
    'Minor' category is assigned a value of 1.
    'Serious' category is assigned a value of 2.
    'Fatal' category is assigned a value of 3.
    """

    return injury_feature.apply(
        lambda x: 0 if x=='Unknown' else 1 if x=='Minor' else 2 if x=='Serious' else 3 if x=='Fatal' else np.nan
    )

def engineer_accident_features_PA(plane_accidents_1F):

    """
    Parameters:
    - plane_accidents_1F (pandas.DataFrame): The dataframe of plane accidents data.

    Returns:
    - pandas.DataFrame: The dataframe with engineered accident features.

    Logic:
    This function engineers accident features by creating two new columns: 'human_injury' and 'human_injury_numeric'.
    'human_injury' column contains injury categories based on the injury data in the dataframe.
    'human_injury_numeric' column contains numeric values corresponding to the injury categories.
    """

    plane_accidents_2F = plane_accidents_1F.copy()
    plane_accidents_2F['human_injury'] = get_injury_feature_PA(plane_accidents_2F)
    raw_injury_score = get_injury_feature_numeric_PA(plane_accidents_2F['human_injury']).astype(float)
    plane_accidents_2F['human_injury_numeric'] = 10*(
        (raw_injury_score - raw_injury_score.min()) / (raw_injury_score.max() - raw_injury_score.min())
    )
    return plane_accidents_2F

def engineer_damage_feature_PA(plane_accidents_2F):

    """
    Parameters:
    - plane_accidents_2F (pandas.DataFrame): The dataframe of plane accidents data with engineered accident features.

    Returns:
    - pandas.DataFrame: The dataframe with an engineered damage feature.

    Logic:
    This function engineers damage feature by creating a new column: 'aircraft_damage_numeric'.
    'aircraft_damage_numeric' column contains numeric values corresponding to the 'aircraft_damage' categories.
    'Unknown' category is assigned a value of 0.
    'Minor' category is assigned a value of 1.
    'Substantial' category is assigned a value of 2.
    'Destroyed' category is assigned a value of 3.
    """

    plane_accidents_3F = plane_accidents_2F.copy()
    raw_dmg_score = plane_accidents_3F['aircraft_damage'].apply(
        lambda x: 0 if x == 'Unknown' else 1 if x == 'Minor' else 2 if x=='Substantial' else 3 if x=='Destroyed' else np.nan
    )
    plane_accidents_3F['aircraft_damage_numeric'] = 10*((raw_dmg_score - raw_dmg_score.min()) / (raw_dmg_score.max() - raw_dmg_score.min()))
    return plane_accidents_3F

def engineer_danger_score_PA(plane_accidents_3Fs, aircraft_dmg_w=.75, human_injury_w=.25):

    """
    Parameters:
    - plane_accidents_3Fs (pandas.DataFrame): The dataframe of plane accidents data with engineered accident and damage features.
    - aircraft_dmg_w (float): The weight for 'aircraft_damage_numeric' in calculating the danger score. Default value is 0.75.
    - human_injury_w (float): The weight for 'human_injury_numeric' in calculating the danger score. Default value is 0.25.

    Returns:
    - pandas.DataFrame: The dataframe with an engineered danger score.

    Logic:
    This function engineers danger score by creating a new column: 'danger_score'.
    'danger_score' is a combination of 'aircraft_damage_numeric' and 'human_injury_numeric', weighted by 'aircraft_dmg_w' and 'human_injury_w' respectively.
    """

    plane_accident_4F = plane_accidents_3Fs.copy()
    aicraft_damage_values = plane_accident_4F['aircraft_damage_numeric'] * aircraft_dmg_w
    human_injury_values = plane_accident_4F['human_injury_numeric'] * human_injury_w
    plane_accident_4F['danger_score'] = aicraft_damage_values + human_injury_values
    return plane_accident_4F

def engineer_plane_size_feature_PI(plane_inventory_1F):
    
    """
    Parameters:
    - plane_inventory_1F (pandas.DataFrame): The dataframe which contains 'number_of_seats' column.

    Returns:
    - pandas.DataFrame: The dataframe with an engineered 'plane_size' feature.

    Logic:
    This function engineers 'plane_size' feature by creating a new column: 'plane_size'.
    'plane_size' is categorized into 'small', 'medium', 'large' based on the 'number_of_seats' in the plane.
    'small' category is for rows where 'number_of_seats' is between 3 and 20 inclusive.
    'medium' category is for rows where 'number_of_seats' is between 21 and 100 inclusive.
    'large' category is for rows where 'number_of_seats' is between 101 and 524 inclusive.
    """

    plane_inventory_2F = plane_inventory_1F.copy()
    plane_inventory_2F['plane_size'] = plane_inventory_2F['number_of_seats'].apply(
        lambda x: 'small' if 3 <= x <= 20 else ('medium' if 21 <= x <= 100 else ('large' if 101 <= x <= 524 else ''))
    )
    return plane_inventory_2F