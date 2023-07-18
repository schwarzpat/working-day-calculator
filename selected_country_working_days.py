import pandas as pd
from datetime import datetime

# Load the file
df = pd.read_csv('/data/generated_holidays.csv')

# Display the first few rows of the dataframe to understand its structure
df.head()

# Filter out the holidays of specified countries
countries = ['UK', 'DK', 'SE', 'FI', 'NO']
df = df[df['country'].isin(countries)]

# Convert the 'ds' column to datetime
df['ds'] = pd.to_datetime(df['ds'])

# Drop duplicates (keep the first occurrence)
df = df.drop_duplicates(subset=['ds', 'country'], keep='first')

# Set the 'ds' column as the index
df.set_index('ds', inplace=True)

# Count the weekdays that are not holidays
weekday_count = {}

for country in countries:
    df_country = df[df['country'] == country]
    start_date = df_country.index.min()
    end_date = df_country.index.max()
    
    all_days = pd.date_range(start=start_date, end=end_date, freq='B')
    all_days = pd.Series(all_days, name='ds')
    all_days = all_days.to_frame()
    
    all_days['month'] = all_days['ds'].dt.to_period('M')
    all_days['weekday'] = all_days['ds'].dt.weekday
    all_days = all_days[all_days['weekday'] < 5]  # Only include weekdays
    
    holidays = df_country.index
    all_days['holiday'] = all_days['ds'].isin(holidays)
    
    weekday_count[country] = all_days.groupby('month')['holiday'].apply(lambda x: (~x).sum())

weekday_count

