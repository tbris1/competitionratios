import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from data import merged_df

model = Pipeline([
    ("poly", PolynomialFeatures(degree=2, include_bias=False)),
    ("lin", LinearRegression())
])

WINDOW_YEARS = 5
specialties = merged_df['Specialty'].unique()
predictions = []
fallback_naive = 0

for spec in specialties:
    df_spec = merged_df[merged_df['Specialty'] == spec].sort_values('Year')
    sub_df = df_spec.tail(WINDOW_YEARS)             

    if len(sub_df) < 2:
        # not enough data to fit even a line; use naive carry-forward
        last_ratio = df_spec['Ratio'].iloc[-1] if len(df_spec) else np.nan
        y_pred_2026 = float(last_ratio) if pd.notna(last_ratio) else np.nan
        fallback_naive += 1
    else:
        X = sub_df[['Year']].to_numpy()
        y = sub_df['Ratio'].to_numpy()
        # optional stability tweak: use degree=1 if fewer than 3 points
        if len(sub_df) < 3:
            model.steps[0] = ("poly", PolynomialFeatures(degree=1, include_bias=False))
        model.fit(X, y)
        y_pred_2026 = float(model.predict(np.array([[2026]]))[0])

    predictions.append({'Specialty': spec, 'Predicted_Ratio_2026': y_pred_2026})

predicted_df = pd.DataFrame(predictions)
print(f"{len(predicted_df)} specialties predicted (fallback_naive={fallback_naive})")
predicted_df.to_csv('predictions.csv', index=False)

