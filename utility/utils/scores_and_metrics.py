import pandas as pd

def get_top_n_planes_by_sizes(plane_inventory_2F, n=10):
    small, medium, large = 'small', 'medium', 'large'
    make_model_size = plane_inventory_2F['make_model'] + ' ' + plane_inventory_2F['plane_size']
    small_top_10 = make_model_size[make_model_size.str.contains(small)].value_counts()[:n]
    medium_top_10 = make_model_size[make_model_size.str.contains(medium)].value_counts()[:n]
    large_top_10 = make_model_size[make_model_size.str.contains(large)].value_counts()[:n]
    return (small_top_10, small), (medium_top_10, medium), (large_top_10, large)

def make_df(top_planes_and_sizes):
    series, size = top_planes_and_sizes
    df = series.reset_index()
    df = df.rename(columns={0: 'number_of_planes', 'index': 'make_model'})
    df['make_model'] = df['make_model'].apply(lambda mm: mm.replace(f' {size}', ''))
    df['size'] = [size]*len(df)
    df['make_model'] = df['make_model'].apply(lambda x: str(x))
    df['number_of_planes'] = df['number_of_planes'].apply(lambda x: int(x))
    df['size'] = df['size'].apply(lambda x: str(x))
    df = df[['size', 'make_model', 'number_of_planes']]
    return df

def make_big_df(plane_inventory_2F):
    sizes = get_top_n_planes_by_sizes(plane_inventory_2F)
    dfs = []
    for size_data in sizes:
        df = make_df(size_data)
        dfs.append(df)
    return pd.concat(dfs)

def ult_df(plane_accidents_4F, plane_inventory_2F):
    big_df = make_big_df(plane_inventory_2F)
    make_model = plane_accidents_4F['make_model']
    num_accidents = make_model[make_model.isin(big_df['make_model'].values)]
    num_accidents = num_accidents.value_counts()
    big_df = big_df.set_index('make_model')
    big_df['recorded_accidents_for_plane_model'] = num_accidents
    big_df = big_df.reset_index()
    
    danger_scores_make_model = plane_accidents_4F[['make_model', 'danger_score', 'human_injury_numeric', 'aircraft_damage_numeric']]
    select_makes_models = big_df['make_model'].to_list()
    mean_danger = []
    mean_human_injury = []
    mean_aircraft_damage = []
    for make_and_model in select_makes_models:
        mean_danger.append(danger_scores_make_model[danger_scores_make_model['make_model'] == make_and_model]['danger_score'].mean())
        mean_human_injury.append(danger_scores_make_model[danger_scores_make_model['make_model'] == make_and_model]['human_injury_numeric'].mean())
        mean_aircraft_damage.append(danger_scores_make_model[danger_scores_make_model['make_model'] == make_and_model]['aircraft_damage_numeric'].mean())
    big_df['mean_human_injury_score'] = mean_human_injury
    big_df['mean_aircraft_damage_score'] = mean_aircraft_damage
    big_df['mean_danger_score'] = mean_danger
    big_df['recorded_accidents_per_plane_in_inventory'] = big_df['recorded_accidents_for_plane_model'] / big_df['number_of_planes']
    
    return big_df