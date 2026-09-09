import nflreadpy as nfl
draft = nfl.load_draft_picks().to_pandas()
draft = draft[draft['season'].between(1999, 2025)]
cols_check = ['car_av', 'w_av', 'dr_av', 'games', 'seasons_started', 'probowls', 'allpro', 'to']
for c in cols_check:
    if c in draft.columns:
        print(c, '-> nao nulos:', draft[c].notna().sum(), 'de', len(draft))
    else:
        print(c, '-> coluna nao existe')