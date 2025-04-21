import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error

# Load data
comp_df = pd.read_csv("CompRatios.csv")
comp_df = comp_df[['Specialty', 'Year', 'Ratio']].dropna()

# Store future predictions
all_predictions = []

# Store MAE scores
mae_scores = []

# Future years to predict
future_years = [2025, 2026]

# Models to train
models = {
    "Linear": lambda: LinearRegression(),
    "Polynomial2": lambda: make_pipeline(PolynomialFeatures(degree=2), LinearRegression()),
    "Ridge": lambda: Ridge(alpha=1.0),
    "RandomForest": lambda: RandomForestRegressor(n_estimators=100, random_state=42)
}

# Loop through specialties and models
for specialty in comp_df['Specialty'].unique():
    df_spec = comp_df[comp_df['Specialty'] == specialty].copy()
    X_train = df_spec[['Year']]
    y_train = df_spec['Ratio']

    for model_name, model_func in models.items():
        model = model_func()
        model.fit(X_train, y_train)

        # Predict for future years
        for year in future_years:
            pred = model.predict(np.array([[year]]))[0]
            all_predictions.append({
                "Specialty": specialty,
                "Year": year,
                "Model": model_name,
                "Predicted_Ratio": pred
            })

        # Predict on training years for MAE
        y_pred_train = model.predict(X_train)
        mae = mean_absolute_error(y_train, y_pred_train)
        mae_scores.append({
            "Specialty": specialty,
            "Model": model_name,
            "MAE": mae
        })

# Save future predictions
predictions_df = pd.DataFrame(all_predictions)
predictions_df.to_csv("model_predictions_2025_2026.csv", index=False)
print("✅ Model predictions saved to 'model_predictions_2025_2026.csv'")

# Visualise MAE
mae_df = pd.DataFrame(mae_scores)
fig = px.bar(mae_df, x='Specialty', y='MAE', color='Model', barmode='group',
             title='Model MAE per Specialty (2013–2024)',
             labels={'MAE': 'Mean Absolute Error'})
fig.update_layout(xaxis_tickangle=-45, height=600)
fig.show()
