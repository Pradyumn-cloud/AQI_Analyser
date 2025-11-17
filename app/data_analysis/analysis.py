import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

#%%
# Load station and hourly data
stations_df = pd.read_csv('./Data/stations.csv')
hourly_df = pd.read_csv('./Data/station_hour.csv')

#%%
# Preview data
print(stations_df.head(20))
print(hourly_df.head(10))

#%%
# Merge city information into hourly data
merged_data = pd.merge(hourly_df, stations_df[['StationId', 'City']], on='StationId', how='left')
print(merged_data.head(10))
print('Merged data shape:', merged_data.shape)

#%%
# Extract datetime if not present
if 'Datetime' not in merged_data.columns and 'Date' in merged_data.columns:
    merged_data['Datetime'] = pd.to_datetime(merged_data['Date'])
    if 'Hour' in merged_data.columns:
        merged_data['Datetime'] += pd.to_timedelta(merged_data['Hour'], unit='h')

# Identify numeric columns (excluding StationId)
numeric_cols = merged_data.select_dtypes(include=['number']).columns.tolist()
if 'StationId' in numeric_cols:
    numeric_cols.remove('StationId')

# Group by City and Datetime, calculate mean
city_hourly_data = merged_data.groupby(['City', 'Datetime'])[numeric_cols].mean().reset_index()
city_hourly_data['Datetime'] = pd.to_datetime(city_hourly_data['Datetime'])

# Ensure complete time series for each city (hourly data for 5 years)
cities = city_hourly_data['City'].unique()
start_date = city_hourly_data['Datetime'].min()
end_date = start_date + pd.DateOffset(years=5)
complete_dates = pd.date_range(start=start_date, end=end_date, freq='H')

# Create complete city-hour combinations
total_combinations = [(city, date) for city in cities for date in complete_dates]
complete_df = pd.DataFrame(total_combinations, columns=['City', 'Datetime'])

# Merge with aggregated data
complete_city_hourly = pd.merge(complete_df, city_hourly_data, on=['City', 'Datetime'], how='left')

#%%
# Preview processed data
print(city_hourly_data.head())
print('City-hourly data shape:', city_hourly_data.shape)

#%%
# Load main data for analysis
df = pd.read_csv('./Data/data.csv')
print(df.head())

#%%
# Convert datetime and extract features
df['Datetime'] = pd.to_datetime(df['Datetime'])
df['Year'] = df['Datetime'].dt.year
df['Month'] = df['Datetime'].dt.month
df['Hour'] = df['Datetime'].dt.hour

# List of pollutants
pollutants = [
    'PM2.5', 'PM10', 'NO', 'NO2', 'NOx', 'NH3', 'CO', 'SO2',
    'O3', 'Benzene', 'Toluene', 'Xylene'
]

#%%
# User input for city
city = input('Enter city name: ').strip()

# Filter dataset for the selected city
city_df = df[df['City'].str.lower() == city.lower()]

if city_df.empty:
    print(f'No data available for city: {city}')
else:
    print(f'Analysis for city: {city}')
    # Handle missing values
    city_df = city_df.fillna(method='ffill')

    # Yearly Trend
    yearly = city_df.groupby('Year')[pollutants].mean()
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=yearly)
    plt.title(f'Yearly Trend of Pollutants in {city}')
    plt.ylabel('Average Concentration')
    plt.show()

    # Monthly Trend + Best/Worst Month
    monthly = city_df.groupby('Month')[pollutants].mean()
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=monthly)
    plt.title(f'Monthly Average Pollutants in {city}')
    plt.show()

    best_month = monthly.mean(axis=1).idxmin()
    worst_month = monthly.mean(axis=1).idxmax()
    print('✅ Best Month to Visit:', best_month)
    print('❌ Worst Month to Visit:', worst_month)

    # Hourly Pattern
    hourly = city_df.groupby('Hour')[pollutants].mean()
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=hourly)
    plt.title(f'Hourly Pollution Pattern in {city}')
    plt.show()

    # Most Toxic Pollutant
    avg_pollutants = city_df[pollutants].mean().sort_values(ascending=False)
    plt.figure(figsize=(10, 6))
    sns.barplot(x=avg_pollutants.index, y=avg_pollutants.values)
    plt.xticks(rotation=45)
    plt.title(f'Most Toxic Pollutants in {city} (5-Year Average)')
    plt.show()
    print('Most toxic pollutant overall:', avg_pollutants.index[0])

    # Peak Month for Each Pollutant
    peak_months = city_df.groupby('Month')[pollutants].mean().idxmax()
    print('📌 Peak month for each pollutant:\n', peak_months)

    # Correlation Heatmap
    plt.figure(figsize=(10, 8))
    sns.heatmap(city_df[pollutants].corr(), annot=True, cmap='coolwarm')
    plt.title(f'Correlation between Pollutants in {city}')
    plt.show()