# analysis.py
"""
Contains the Analysis class, responsible for processing and presenting
the fetched AQI data.
"""
from typing import List
from .models import City, AQIData

class AQIAnalysis:
    """Provides methods to display and analyze AQI data."""
    
    @staticmethod
    def display_summary(city: City, aqi_records: List[AQIData]):
        """
        Prints a formatted summary of AQI records for a city.

        Args:
            city (City): The city for which data is being displayed.
            aqi_records (List[AQIData]): A list of AQIData objects.
        """
        print("\n" + "="*50)
        print(f"📊 Air Quality Index Summary for: {city.get_name().title()}")
        print("="*50)
        
        if not aqi_records:
            print(f"No AQI data found for {city.get_name()}.")
        else:
            print(f"Found {len(aqi_records)} records:\n")
            # This loop works polymorphically with any subclass of AQIData
            for record in aqi_records:
                print(f"  -> {record.display()}")
        
        print("="*50 + "\n")

    def get_aqi_analysis(self, aqi_value: int) -> dict:
        """
        Analyzes AQI value and returns level and color information.
        
        Args:
            aqi_value (int): The AQI value to analyze
            
        Returns:
            dict: A dictionary containing level and color information
        """
        if aqi_value <= 50:
            return {
                'level': 'Good',
                'color': '#00E400',  # Green
                'description': 'Air quality is satisfactory'
            }
        elif aqi_value <= 100:
            return {
                'level': 'Moderate',
                'color': '#FFFF00',  # Yellow
                'description': 'Air quality is acceptable'
            }
        elif aqi_value <= 150:
            return {
                'level': 'Unhealthy for Sensitive Groups',
                'color': '#FF7E00',  # Orange
                'description': 'Members of sensitive groups may experience health effects'
            }
        elif aqi_value <= 200:
            return {
                'level': 'Unhealthy',
                'color': '#FF0000',  # Red
                'description': 'Everyone may begin to experience health effects'
            }
        elif aqi_value <= 300:
            return {
                'level': 'Very Unhealthy',
                'color': '#8F3F97',  # Purple
                'description': 'Health alert: everyone may experience serious health effects'
            }
        else:
            return {
                'level': 'Hazardous',
                'color': '#7E0023',  # Maroon
                'description': 'Health warnings of emergency conditions'
            }