import pandas as pd

df = pd.read_csv("CompRatios.csv")

# Find average competition ratios
ave_ratio = df['Ratio'].mean()
print(f'Average competition ratio across all specialties since 2013 = {ave_ratio}')

# Top 10 most competitive jobs (specialty and year) since 2013
sorted_ratios = df.sort_values('Ratio', ascending=False)
max_ratios = sorted_ratios[:10]
print(f'Top 10 most competitive specialties since 2013: {max_ratios}')

# Specialties ranked by competition ratio averages since 2013 (highest to lowest)
sorted_by_specialty = df.groupby('Specialty').mean()
sorted_by_specialty_and_ratio = sorted_by_specialty.sort_values('Ratio', ascending=False)
print(sorted_by_specialty_and_ratio['Specialty' and 'Ratio'])

# Competition ratio average from 2013 to 2023 compared to 2024
# Split data
prev_years_data = df[df['Year'] < 2024]
last_year_data = df[df['Year'] == 2024][['Specialty', 'Ratio']]
# Calculate average ratio for 2013–2023
prev_years_data_ave = prev_years_data.groupby('Specialty')['Ratio'].mean().reset_index()
prev_years_data_ave.rename(columns={'Ratio': 'AverageRatio2013to2023'}, inplace=True)
# Rename 2024 ratio column
last_year_data.rename(columns={'Ratio': 'Ratio2024'}, inplace=True)
# Merge to compare
comparison = pd.merge(prev_years_data_ave, last_year_data, on='Specialty')
comparison['Change'] = comparison['Ratio2024'] - comparison['AverageRatio2013to2023']


# Display results
print('Competition ratios average between 2013 and 2023 compared to 2024:')
print(comparison)

