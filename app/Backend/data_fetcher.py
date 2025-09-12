import requests
import pandas as pd
import os
from datetime import datetime
from city import City
from aqi_data import RealTimeAQIData, HistoricalAQIData
from abc import ABC, abstractmethod

class DataFetcher(ABC):
    """Abstract base class for data fetching operations."""
    
    def __init__(self):
        self._last_fetch_time = None
        self._cache = {}
    
    @property
    def last_fetch_time(self):
        return self._last_fetch_time
    
    @abstractmethod
    def fetch_data(self, city_name: str, **kwargs):
        """Abstract method to fetch data - must be implemented by subclasses"""
        pass
    
    def _update_fetch_time(self):
        """Private method to update last fetch time"""
        self._last_fetch_time = datetime.now()

class APIDataFetcher(DataFetcher):
    """Fetches data from an external AQI API."""
    def __init__(self):
        super().__init__()
        self._api_base_url = "https://api.data.gov.in/resource/3b01bcb8-0b14-4abf-b6f2-c1bfd384ba69"
        self._api_key = "579b464db66ec23bdd0000015c03f042adea49b65994467de221bf09"

    def fetch_data(self, city_name: str, **kwargs):
        """
        Fetches real-time air pollution data for a given city name from data.gov.in.
        """
        return self.fetch_realtime_data(city_name)
    
    def fetch_realtime_data(self, city_name: str):
        """
           Fetches real-time air pollution data for a given city name from data.gov.in.
        """
        self._update_fetch_time()
        
        # Check cache first
        cache_key = f"realtime_{city_name}"
        if cache_key in self._cache:
            cached_data, cache_time = self._cache[cache_key]
            # Use cached data if less than 30 minutes old
            if (datetime.now() - cache_time).total_seconds() < 1800:
                return cached_data
        
        params = {
            "api-key": self._api_key,
            "format": "json",
            "limit": 5,  # Fetch multiple records to get different pollutants
            "filters[city]": city_name
        }
        try:
            response = requests.get(self._api_base_url, params=params, timeout=10)
            print(f"Status Code: {response.status_code}")
            
            if response.status_code != 200:
                print(f"API Error: {response.text}")
                return None
            
            data = response.json()
            records = data.get("records", [])
            
            if not records:
                print(f"No data found for {city_name}")
                return None

            print(f"Found {len(records)} records for {city_name}")
            
            # Process all records to get comprehensive pollutant data
            pollutants = {}
            station = "Unknown Station"
            aqi_value = 0  # We'll calculate a simple average or use the first available
            
            for record in records:
                pollutant_id = record.get('pollutant_id', 'unknown')
                avg_value = record.get('avg_value')  # Correct field name
                
                if avg_value is not None:
                    try:
                        pollutants[pollutant_id] = float(avg_value)
                    except (ValueError, TypeError):
                        pollutants[pollutant_id] = avg_value
                
                # Get station name from first record
                if station == "Unknown Station":
                    station = record.get('station', 'Unknown Station')
            
            # Calculate a simple AQI approximation based on PM2.5 if available
            if 'PM2.5' in pollutants:
                pm25 = pollutants['PM2.5']
                if isinstance(pm25, (int, float)):
                    if pm25 <= 12:
                        aqi_value = 50
                    elif pm25 <= 35.4:
                        aqi_value = 100
                    elif pm25 <= 55.4:
                        aqi_value = 150
                    else:
                        aqi_value = 200
            elif pollutants:
                aqi_value = 100  # Default moderate value
            
            result = RealTimeAQIData(city_name, aqi_value, pollutants, station)
            
            # Cache the result
            self._cache[cache_key] = (result, datetime.now())
            
            return result

        except requests.exceptions.RequestException as e:
            print(f"Request failed for {city_name}: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error for {city_name}: {e}")
            return None


class CSVDataFetcher(DataFetcher):
    """Fetches historical data from CSV files."""
    
    def __init__(self, data_directory="../Data"):
        super().__init__()
        self._data_directory = data_directory
        self._csv_data = None
        self._load_csv_data()
    
    def _load_csv_data(self):
        """Private method to load CSV data"""
        try:
            csv_path = os.path.join(self._data_directory, "city_day.csv")
            # For now, we'll use a simple CSV reading approach without pandas
            self._csv_data = []
            
            with open(csv_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()
                if lines:
                    headers = lines[0].strip().split(',')
                    for line in lines[1:]:
                        values = line.strip().split(',')
                        if len(values) == len(headers):
                            row_dict = dict(zip(headers, values))
                            self._csv_data.append(row_dict)
                            
            print(f"Loaded {len(self._csv_data)} records from CSV")
            
        except FileNotFoundError:
            print(f"CSV file not found at {csv_path}")
            self._csv_data = []
        except Exception as e:
            print(f"Error loading CSV data: {e}")
            self._csv_data = []
    
    def fetch_data(self, city_name: str, date_str=None, **kwargs):
        """Fetch historical data for a city"""
        return self.fetch_historical_data(city_name, date_str)
    
    def fetch_historical_data(self, city_name: str, date_str=None):
        """
        Fetches historical AQI data for a given city from CSV data.
        If date_str is provided, returns data for that specific date.
        Otherwise, returns the most recent available data.
        """
        self._update_fetch_time()
        
        if not self._csv_data:
            print("No CSV data available")
            return None
        
        # Filter data for the specified city
        city_data = [row for row in self._csv_data if row.get('City', '').lower() == city_name.lower()]
        
        if not city_data:
            print(f"No data found for city: {city_name}")
            return None
        
        # If specific date requested, filter by date
        if date_str:
            target_data = [row for row in city_data if row.get('Date') == date_str]
            if not target_data:
                print(f"No data found for {city_name} on {date_str}")
                return None
            selected_row = target_data[0]
        else:
            # Get the most recent data (assuming data is sorted by date)
            selected_row = city_data[-1]
        
        # Extract pollutant data
        pollutants = {}
        pollutant_columns = ['PM2.5', 'PM10', 'NO', 'NO2', 'NOx', 'NH3', 'CO', 'SO2', 'O3', 'Benzene', 'Toluene', 'Xylene']
        
        for pollutant in pollutant_columns:
            value = selected_row.get(pollutant, '')
            if value and value != '':
                try:
                    pollutants[pollutant] = float(value)
                except ValueError:
                    pollutants[pollutant] = value
        
        # Get AQI value
        aqi_value = selected_row.get('AQI', '')
        if aqi_value and aqi_value != '':
            try:
                aqi_value = float(aqi_value)
            except ValueError:
                aqi_value = None
        else:
            aqi_value = None
        
        # Create and return HistoricalAQIData object
        date = selected_row.get('Date', datetime.now().strftime('%Y-%m-%d'))
        
        return HistoricalAQIData(city_name, aqi_value, pollutants, date)
    
    def get_available_cities(self):
        """Get list of all available cities in the dataset"""
        if not self._csv_data:
            return []
        
        cities = set()
        for row in self._csv_data:
            city = row.get('City', '').strip()
            if city:
                cities.add(city)
        
        return sorted(list(cities))
    
    def get_date_range_for_city(self, city_name):
        """Get the date range available for a specific city"""
        city_data = [row for row in self._csv_data if row.get('City', '').lower() == city_name.lower()]
        
        if not city_data:
            return None, None
        
        dates = [row.get('Date') for row in city_data if row.get('Date')]
        dates = sorted([date for date in dates if date])
        
        return dates[0] if dates else None, dates[-1] if dates else None