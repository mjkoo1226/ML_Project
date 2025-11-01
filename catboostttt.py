import pandas as pd

FILE_PATH = "datasets/spotify_songs_with_genre_int.csv"
df = pd.read_csv(FILE_PATH)
df = df.dropna()   

X = df[["track_popularity", "danceability", "energy", "key", "loudness", "mode", "speechiness", "acousticness", "instrumentalness", "liveness", "valence", "tempo", "duration_ms"]]
y = df[["genre_int"]]

import numpy as np
from sklearn.preprocessing import StandardScaler, FunctionTransformer, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

log1p = FunctionTransformer(np.log1p, validate=False)

log_cols = ["duration_ms", "tempo"]
std_cols = ["track_popularity", "loudness", 
            "danceability", "energy", "speechiness", 
            "acousticness", "instrumentalness", "liveness", "valence"]
cat_cols = ["key", "mode"]

preprocessor = ColumnTransformer(
    transformers=[
        ("log", Pipeline([("log1p", log1p), ("std", StandardScaler())]), log_cols),
        ("std", StandardScaler(), std_cols),
        ("cat", OneHotEncoder(handle_unknown="ignore"), cat_cols)
    ]
)

X_edit = preprocessor.fit_transform(X)

from sklearn.model_selection import train_test_split

X_train_edit, X_test_edit, y_train, y_test = train_test_split(
    X_edit, y, test_size=0.2, random_state=42
)


from catboost import CatBoostClassifier
from sklearn.metrics import accuracy_score

# CatBoost
cat = CatBoostClassifier(
    iterations=500,       # n_estimators와 동일 개념
    learning_rate=0.05,
    depth=6,              # max_depth에 대응 (기본 6)
    random_seed=42,
    verbose=100           # 100번째마다 로그 출력, 0이면 완전히 무음
)

cat.fit(X_train_edit, y_train)

y_pred_cat = cat.predict(X_test_edit)
print("CatBoost Accuracy:", accuracy_score(y_test, y_pred_cat))