import nflreadpy as nfl
import pandas as pd
import numpy as np

draft = nfl.load_draft_picks().to_pandas()
combine = nfl.load_combine().to_pandas()

draft = draft[draft['season'].between(1999, 2025)].copy()

draft_cols = [
    'season', 'round', 'pick', 'team', 'pfr_player_id', 'pfr_player_name',
    'position', 'age', 'to', 'allpro', 'probowls', 'seasons_started',
    'w_av', 'dr_av', 'games', 'college'
]
draft_cols = [c for c in draft_cols if c in draft.columns]
draft = draft[draft_cols].copy()
draft = draft.drop_duplicates(subset=['season', 'round', 'pick'])

combine_cols = [
    'pfr_id', 'player_name', 'pos', 'school', 'ht', 'wt',
    'forty', 'bench', 'vertical', 'broad_jump', 'cone', 'shuttle'
]
combine_cols = [c for c in combine_cols if c in combine.columns]
combine = combine[combine_cols].copy()
combine = combine.dropna(subset=['pfr_id'])
combine = combine.drop_duplicates(subset='pfr_id', keep='first')

df = draft.merge(combine, left_on='pfr_player_id', right_on='pfr_id', how='left', validate='many_to_one')

df['known_outcome'] = df['season'] <= 2020
df['w_av'] = df['w_av'].fillna(0)
df['games'] = df['games'].fillna(0)
df['seasons_started'] = df['seasons_started'].fillna(0)

round_median = df.loc[df['known_outcome']].groupby('round')['w_av'].transform('median')
df.loc[df['known_outcome'], 'round_median_wav'] = round_median

df['draft_status'] = 'em_avaliacao'
df.loc[df['known_outcome'] & (df['w_av'] > df['round_median_wav']), 'draft_status'] = 'hit'
df.loc[df['known_outcome'] & (df['w_av'] <= df['round_median_wav']), 'draft_status'] = 'bust'

df['hit'] = np.where(df['draft_status'] == 'hit', 1, np.where(df['draft_status'] == 'bust', 0, np.nan))

df['is_seahawks'] = (df['team'] == 'SEA').astype(int)

df.to_parquet('nfl_draft_1999_2025.parquet', index=False)
df.to_csv('nfl_draft_1999_2025.csv', index=False)

seahawks = df[df['is_seahawks'] == 1].copy()
seahawks.to_parquet('seahawks_draft_1999_2025.parquet', index=False)
seahawks.to_csv('seahawks_draft_1999_2025.csv', index=False)

print(df.shape)
print(df['draft_status'].value_counts())
print(df[['pfr_player_name', 'season', 'round', 'w_av', 'draft_status']].sort_values('w_av', ascending=False).head(10).to_string())
print(seahawks.shape)
print(seahawks[['season', 'round', 'pick', 'pfr_player_name', 'position', 'w_av', 'draft_status']].to_string())