"""
Backend Service for AQI Analyzer UI
This service layer connects the Flet UI with the OOP backend implementation.
"""

import sys
import os
from datetime import datetime
from typing import Optional, List, Dict, Any

# Add backend path to sys.path
backend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Backend')
sys.path.append(backend_path)

try:
    from city import City
    from aqi_data import AQIData, RealTimeAQIData, HistoricalAQIData
    from data_fetcher import CSVDataFetcher, APIDataFetcher
    from analysis import Analysis
except ImportError as e:
    print(f"Backend import error: {e}")
    # Fallback for development
    pass


class BackendService:
    """
    Service layer that encapsulates backend operations for the UI.
    Implements the Facade pattern to simplify backend interaction.
    """
    
    def __init__(self):
        """Initialize backend components"""
        self._csv_fetcher = None
        self._api_fetcher = None
        self._analyzer = None
        self._initialize_backend()
    
    def _initialize_backend(self):
        """Private method to initialize backend components"""
        try:
            # Fix CSV path - Data folder is in the app directory
            data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Data')
            print(f"Looking for CSV data at: {data_path}")
            self._csv_fetcher = CSVDataFetcher(data_path)
            self._api_fetcher = APIDataFetcher()
            self._analyzer = Analysis()
            print("✓ Backend service initialized successfully")
        except Exception as e:
            print(f"❌ Backend initialization failed: {e}")
            # Initialize with None for graceful fallback
            self._csv_fetcher = None
            self._api_fetcher = None
            self._analyzer = None
    
    def is_backend_available(self) -> bool:
        """Check if backend is properly initialized"""
        return all([self._csv_fetcher, self._api_fetcher, self._analyzer])
    
    def get_available_cities(self) -> List[str]:
        """Get list of cities available in the dataset"""
        if not self._csv_fetcher:
            return ["Delhi", "Mumbai", "Gandhinagar"]  # Fallback cities
        
        try:
            cities = self._csv_fetcher.get_available_cities()
            return cities if cities else ["Delhi", "Mumbai", "Gandhinagar"]
        except Exception as e:
            print(f"Error getting cities: {e}")
            return ["Delhi", "Mumbai", "Gandhinagar"]
    
    def get_realtime_aqi_data(self, city_name: str) -> Dict[str, Any]:
        """
        Get real-time AQI data for a city
        Returns a dictionary with UI-friendly data structure
        """
        if not self._api_fetcher:
            return self._get_fallback_data(city_name, is_realtime=True)
        
        try:
            aqi_data = self._api_fetcher.fetch_realtime_data(city_name)
            
            if aqi_data and isinstance(aqi_data, RealTimeAQIData):
                return self._format_aqi_data(aqi_data)
            else:
                print(f"No real-time data found for {city_name}, using historical data")
                return self.get_historical_aqi_data(city_name)
                
        except Exception as e:
            print(f"Error fetching real-time data for {city_name}: {e}")
            return self._get_fallback_data(city_name, is_realtime=True)
    
    def get_historical_aqi_data(self, city_name: str, date_str: Optional[str] = None) -> Dict[str, Any]:
        """
        Get historical AQI data for a city
        Returns a dictionary with UI-friendly data structure
        """
        if not self._csv_fetcher:
            return self._get_fallback_data(city_name, is_realtime=False)
        
        try:
            aqi_data = self._csv_fetcher.fetch_historical_data(city_name, date_str)
            
            if aqi_data and isinstance(aqi_data, HistoricalAQIData):
                return self._format_aqi_data(aqi_data)
            else:
                return self._get_fallback_data(city_name, is_realtime=False)
                
        except Exception as e:
            print(f"Error fetching historical data for {city_name}: {e}")
            return self._get_fallback_data(city_name, is_realtime=False)
    
    def get_health_recommendation(self, city_name: str, use_realtime: bool = True) -> str:
        """Get health recommendation for a city"""
        if not self._analyzer:
            return "Unable to provide recommendation. Please check backend connection."
        
        try:
            # Get AQI data
            if use_realtime and self._api_fetcher:
                aqi_data = self._api_fetcher.fetch_realtime_data(city_name)
            else:
                aqi_data = self._csv_fetcher.fetch_historical_data(city_name) if self._csv_fetcher else None
            
            if aqi_data:
                return self._analyzer.get_health_recommendation(aqi_data)
            else:
                return "No data available for health recommendation."
                
        except Exception as e:
            print(f"Error getting health recommendation: {e}")
            return "Unable to provide recommendation at this time."
    
    def compare_cities(self, city_names: List[str]) -> Dict[str, Any]:
        """Compare AQI data across multiple cities"""
        if not self._analyzer or not self._csv_fetcher:
            return {"error": "Backend not available for comparison"}
        
        try:
            aqi_data_list = []
            
            for city in city_names:
                data = self._csv_fetcher.fetch_historical_data(city)
                if data:
                    aqi_data_list.append(data)
            
            if aqi_data_list:
                comparison = self._analyzer.compare_aqi_data(aqi_data_list)
                return {
                    "comparison_text": comparison,
                    "cities_data": [self._format_aqi_data(data) for data in aqi_data_list]
                }
            else:
                return {"error": "No data found for the selected cities"}
                
        except Exception as e:
            print(f"Error comparing cities: {e}")
            return {"error": f"Comparison failed: {str(e)}"}
    
    def get_pollutant_analysis(self, city_name: str) -> str:
        """Get detailed pollutant analysis for a city"""
        if not self._analyzer or not self._csv_fetcher:
            return "Pollutant analysis not available"
        
        try:
            aqi_data = self._csv_fetcher.fetch_historical_data(city_name)
            if aqi_data:
                return self._analyzer.analyze_pollutant_levels(aqi_data)
            else:
                return "No pollutant data available"
                
        except Exception as e:
            print(f"Error in pollutant analysis: {e}")
            return "Pollutant analysis failed"
    
    def _format_aqi_data(self, aqi_data: AQIData) -> Dict[str, Any]:
        """
        Convert AQIData object to UI-friendly dictionary
        """
        return {
            "city": aqi_data.city,
            "aqi_value": aqi_data.aqi_value or 0,
            "status": aqi_data.get_aqi_category(),
            "timestamp": aqi_data.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "data_source": aqi_data.get_data_source(),
            "pollutants": aqi_data.pollutant_data,
            "is_realtime": isinstance(aqi_data, RealTimeAQIData),
            "color": self._get_color_for_status(aqi_data.get_aqi_category())
        }
    
    def _get_color_for_status(self, status: str) -> str:
        """Get color code for AQI status"""
        status_lower = status.lower()
        if "good" in status_lower:
            return "#4CAF50"  # Green
        elif "moderate" in status_lower:
            return "#FF9800"  # Orange
        elif "unhealthy for sensitive" in status_lower:
            return "#FF5722"  # Deep Orange
        elif "unhealthy" in status_lower:
            return "#F44336"  # Red
        elif "very unhealthy" in status_lower:
            return "#9C27B0"  # Purple
        elif "hazardous" in status_lower:
            return "#795548"  # Brown
        else:
            return "#757575"  # Grey for unknown
    
    def _get_fallback_data(self, city_name: str, is_realtime: bool = True) -> Dict[str, Any]:
        """Provide fallback data when backend is not available"""
        fallback_aqi = 75  # Moderate level
        return {
            "city": city_name,
            "aqi_value": fallback_aqi,
            "status": "Moderate",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "data_source": "Fallback Data (Backend Unavailable)",
            "pollutants": {
                "PM2.5": 25.0,
                "PM10": 50.0,
                "O3": 80.0,
                "NO2": 20.0
            },
            "is_realtime": is_realtime,
            "color": "#FF9800"  # Orange for moderate
        }


# Global service instance
backend_service = BackendService()
