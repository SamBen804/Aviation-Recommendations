import pandas as pd
import numpy as np

def engineer_make_model_feature_PAPI(df):
    df = df.copy()
    df['make_model'] = df['make'] + ' ' + df['model']
    return df

def get_injury_feature_PA(plane_accidents):
    fatal_category = (plane_accidents['total_fatal_injuries'] > 0).apply(lambda x: 'Fatal' if x else np.nan)
    serious_category = (plane_accidents['total_serious_injuries'] > 0).apply(lambda x: 'Serious' if x else np.nan)
    minor_category = (plane_accidents['total_minor_injuries'] > 0).apply(lambda x: 'Minor' if x else np.nan)
    categorized_injuries = pd.concat([fatal_category, serious_category, minor_category], axis=1)
    return categorized_injuries.apply(lambda row: next((injury for injury in row if pd.notna(injury)), np.nan), axis=1).fillna('Unknown')

def get_injury_feature_numeric_PA(injury_feature):
    return injury_feature.apply(
        lambda x: 0 if x=='Unknown' else 1 if x=='Minor' else 2 if x=='Serious' else 3 if x=='Fatal' else np.nan
    )

def engineer_accident_features_PA(plane_accidents_1F):
    plane_accidents_2F = plane_accidents_1F.copy()
    plane_accidents_2F['human_injury'] = get_injury_feature_PA(plane_accidents_2F)
    raw_injury_score = get_injury_feature_numeric_PA(plane_accidents_2F['human_injury']).astype(float)
    plane_accidents_2F['human_injury_numeric'] = 10*(
        (raw_injury_score - raw_injury_score.min()) / (raw_injury_score.max() - raw_injury_score.min())
    )
    return plane_accidents_2F

def engineer_damage_feature_PA(plane_accidents_2F):
    plane_accidents_3F = plane_accidents_2F.copy()
    raw_dmg_score = plane_accidents_3F['aircraft_damage'].apply(
        lambda x: 0 if x == 'Unknown' else 1 if x == 'Minor' else 2 if x=='Substantial' else 3 if x=='Destroyed' else np.nan
    )
    plane_accidents_3F['aircraft_damage_numeric'] = 10*((raw_dmg_score - raw_dmg_score.min()) / (raw_dmg_score.max() - raw_dmg_score.min()))
    return plane_accidents_3F

def engineer_danger_score_PA(plane_accidents_3Fs, aircraft_dmg_w=.75, human_injury_w=.25):
    plane_accident_4F = plane_accidents_3Fs.copy()
    aicraft_damage_values = plane_accident_4F['aircraft_damage_numeric'] * aircraft_dmg_w
    human_injury_values = plane_accident_4F['human_injury_numeric'] * human_injury_w
    plane_accident_4F['danger_score'] = aicraft_damage_values + human_injury_values
    return plane_accident_4F

def engineer_numseats_feature_PI(plane_inventory_1F):
    plane_inventory_2F = plane_inventory_1F.copy()
    plane_inventory_2F['plane_size'] = plane_inventory_2F['number_of_seats'].apply(
        lambda x: 'small' if 3 <= x <= 20 else ('medium' if 21 <= x <= 100 else ('large' if 101 <= x <= 524 else ''))
    )
    return plane_inventory_2F