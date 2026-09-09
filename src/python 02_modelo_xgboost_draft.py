import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, log_loss
import xgboost as xgb

df = pd.read_parquet('nfl_draft_1999_2025.parquet')

df = pd.get_dummies(df, columns=['position'], prefix='pos', dummy_na=False)

pos_cols = [c for c in df.columns if c.startswith('pos_')]

features = ['round', 'pick', 'age', 'ht', 'wt', 'forty', 'bench', 'vertical', 'broad_jump', 'cone', 'shuttle'] + pos_cols
features = [f for f in features if f in df.columns]

train_df = df[df['known_outcome']].copy()

X = train_df[features]
y = train_df['hit']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

model = xgb.XGBClassifier(
    n_estimators=500,
    max_depth=4,
    learning_rate=0.03,
    subsample=0.8,
    colsample_bytree=0.8,
    min_child_weight=10,
    reg_lambda=2.0,
    random_state=42,
    n_jobs=-1,
    early_stopping_rounds=30,
    eval_metric='logloss'
)

model.fit(X_train, y_train, eval_set=[(X_test, y_test)], verbose=False)

pred_proba_test = model.predict_proba(X_test)[:, 1]
print('AUC:', roc_auc_score(y_test, pred_proba_test))
print('LogLoss:', log_loss(y_test, pred_proba_test))

df['hit_probability'] = model.predict_proba(df[features])[:, 1]

model.save_model('edq_draft_xgboost_model.json')

df.to_parquet('nfl_draft_scored_1999_2025.parquet', index=False)
df.to_csv('nfl_draft_scored_1999_2025.csv', index=False)

seahawks = df[df['is_seahawks'] == 1].copy()
seahawks.to_parquet('seahawks_draft_scored_1999_2025.parquet', index=False)
seahawks.to_csv('seahawks_draft_scored_1999_2025.csv', index=False)

importances = pd.Series(model.feature_importances_, index=features)
print(importances.sort_values(ascending=False).head(15))

print(seahawks[['season', 'round', 'pick', 'pfr_player_name', 'w_av', 'draft_status', 'hit_probability']].sort_values('season').to_string())