import pandas as pd

df = pd.read_csv("CompRatios.csv")
# For purpose of adding predicted data later, add 'Source' column
df['Source'] = 'Historical'
# Rename core medical training
df.loc[df['Specialty'] == 'Core Medical Training', 'Specialty'] = 'Core Medical Training (IMT)'

# Load and reshape predictions
df_predictions = pd.read_csv("predictions.csv")
df_predictions.rename(columns={'Predicted_Ratio_2025': 2025, 'Predicted_Ratio_2026': 2026}, inplace=True)
# Melt df as currently in wrong format [[Specialty, Predictions for 2025, Predictions for 2026]]
df_predictions_long = df_predictions.melt(id_vars='Specialty', var_name='Year', value_name='Ratio')
df_predictions_long['Year'] = df_predictions_long['Year'].astype(int)
df_predictions_long['Source'] = 'Predicted'

# Create average excluding outliers (as defined as either fewer than 100 applicants or by 1.5 * IQR
df_outliers_removed = df[df['Applicants'] > 100]

Q1 = df_outliers_removed['Ratio'].quantile(0.25)
Q3 = df_outliers_removed['Ratio'].quantile(0.75)
IQR = Q3 - Q1

lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

df_outliers_removed = df_outliers_removed[(df_outliers_removed['Ratio'] >= lower_bound) & (df_outliers_removed['Ratio'] <= upper_bound)]
outliers_removed = df_outliers_removed.groupby('Year', as_index=False)['Ratio'].mean()
outliers_removed['Specialty'] = 'Average (outliers removed)'
outliers_removed['Source'] = 'Historical'
outliers_removed['Year'] = outliers_removed['Year'].astype(int)

# Create blanket average across all specialties for each year (including outliers)
df_total_ave = df.groupby('Year', as_index=False)['Ratio'].mean()
df_total_ave['Specialty'] = 'Average (all specialties)'
df_total_ave['Source'] = 'Historical'
merged_df = pd.concat([df, df_total_ave, df_predictions_long, outliers_removed], ignore_index=True)