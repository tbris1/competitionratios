import sklearn
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import Ridge
from sklearn.ensemble import RandomForestRegressor
import pandas as pd

model = make_pipeline(PolynomialFeatures(degree=4), LinearRegression())

df = pd.read_csv("CompRatios.csv")
# df = df[df["Year"] >= 2019]
specialties = df['Specialty'].unique()
predictions = []

for spec in specialties:
    sub_df = df[df['Specialty'] == spec]
    X = sub_df[['Year']]
    y = sub_df['Ratio']
    model.fit(X, y)

    y_pred_2025 = model.predict([[2025]])[0]
    y_pred_2026 = model.predict([[2026]])[0]

    predictions.append({'Specialty': spec, 'Predicted_Ratio_2025': y_pred_2025, 'Predicted_Ratio_2026': y_pred_2026})

predicted_df = pd.DataFrame(predictions)
print(predicted_df)

predicted_df.to_csv('predictions.csv', index=False)
