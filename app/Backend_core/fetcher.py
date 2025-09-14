
import requests
import os
from typing import List, Optional
from dotenv import load_dotenv
from .config import API_URL, API_KEY
from .models import City, RealTimeAQIData


class AQIFetcher:
    """Handles fetching and parsing of AQI data from the API."""
    def __init__(self, api_url: str, api_key: str):
        self.__api_url = api_url
        self.__api_key = api_key

    def fetch_data_for_city(self, city: City) -> Optional[List[RealTimeAQIData]]:
        """
        Fetches AQI data for a given City object.

        Args:
            city (City): The city object to fetch data for.

        Returns:
            Optional[List[RealTimeAQIData]]: A list of RealTimeAQIData objects
                                             if successful, otherwise None.
        """
        params = {
            "api-key": self.__api_key,
            "format": "json",
            "limit": 10,  # Fetch a few records for demonstration
            "filters[city]": city.get_name()
        }
        
        try:
            response = requests.get(self.__api_url, params=params, timeout=15)
            # Raise an exception for bad status codes (4xx or 5xx)
            response.raise_for_status()
            
            data = response.json()
            records = data.get("records", [])
            
            # Convert raw JSON records into a list of RealTimeAQIData objects
            aqi_data_list = [
                RealTimeAQIData(
                    station=r.get('station', 'N/A'),
                    pollutant_id=r.get('pollutant_id', 'N/A'),
                    avg_value=r.get('avg_value', 'N/A'),
                    last_update=r.get('last_update', 'N/A')
                ) for r in records
            ]
            return aqi_data_list

        except requests.exceptions.RequestException as e:
            print(f"❌ Error during API request: {e}")
            return None
        except Exception as e:
            print(f"❌ An unexpected error occurred: {e}")
            return None

    def get_realtime_aqi(self, city_name: str) -> dict:
        """
        Fetches real-time AQI data for a city name and returns it in a standardized format.
        
        Args:
            city_name (str): The name of the city
            
        Returns:
            dict: A dictionary containing status and data
        """
        try:
            city = City(city_name)
            aqi_data = self.fetch_data_for_city(city)
            
            if aqi_data and len(aqi_data) > 0:
                # Get the first record and extract AQI value
                first_record = aqi_data[0]
                aqi_value = first_record.get_avg_value()
                
                return {
                    'status': 'ok',
                    'data': {
                        'aqi': int(float(aqi_value)) if aqi_value.replace('.', '').isdigit() else 0,
                        'station': first_record.get_station(),
                        'last_update': first_record.get_last_update()
                    }
                }
            else:
                return {
                    'status': 'error',
                    'data': f'No AQI data found for {city_name}'
                }
                
        except Exception as e:
            return {
                'status': 'error',
                'data': f'Error fetching data: {str(e)}'
            }