import pandas as pd
from datetime import datetime

# Load the file
df_all = pd.read_csv('data/generated_holidays.csv')

# Convert the 'ds' column to datetime
df_all['ds'] = pd.to_datetime(df_all['ds'])

# Drop duplicates (keep the first occurrence)
df_all = df_all.drop_duplicates(subset=['ds', 'country'], keep='first')

# Set the 'ds' column as the index
df_all.set_index('ds', inplace=True)

# Get all unique country codes
all_countries = df_all['country'].unique()

# Repeat the procedure for all countries
all_weekday_count = {}

for country in all_countries:
    df_country = df_all[df_all['country'] == country]
    start_date = df_country.index.min()
    end_date = df_country.index.max()
    
    # Check if start_date or end_date is NaT
    if pd.isnull(start_date) or pd.isnull(end_date):
        continue

    all_days = pd.date_range(start=start_date, end=end_date, freq='B')
    all_days = pd.Series(all_days, name='ds')
    all_days = all_days.to_frame()
    
    all_days['month'] = all_days['ds'].dt.to_period('M')
    all_days['weekday'] = all_days['ds'].dt.weekday
    all_days = all_days[all_days['weekday'] < 5]  # Only include weekdays
    
    holidays = df_country.index
    all_days['holiday'] = all_days['ds'].isin(holidays)
    
    all_weekday_count[country] = all_days.groupby('month')['holiday'].apply(lambda x: (~x).sum())

# Convert the dictionary to a dataframe
df_working_days = pd.concat(all_weekday_count, names=['country', 'month']).reset_index(name='working_days')

# Write the dataframe to a csv file
df_working_days.to_csv('/working_days_all_countries.csv', index=False)
