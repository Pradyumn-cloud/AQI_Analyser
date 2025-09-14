from dataclasses import dataclass
from typing import List, Dict, Optional
from datetime import datetime

@dataclass
class PollutantData:
    """Represents data for a specific pollutant at a station."""
    pollutant_id: str
    min_value: float
    max_value: float
    avg_value: float

@dataclass
class StationData:
    """Represents all data from a monitoring station."""
    station: str
    latitude: float
    longitude: float
    last_update: str
    pollutants: List[PollutantData]

@dataclass
class City:
    """Represents a city with its basic information."""
    def __init__(self, name: str, country: str = "", state: str = ""):
        self._name = name
        self._country = country
        self._state = state
    
    def get_name(self) -> str:
        return self._name
    
    def get_country(self) -> str:
        return self._country
    
    def get_state(self) -> str:
        return self._state

@dataclass
class AQIData:
    """Base class for AQI data."""
    def __init__(self, aqi_value: int, timestamp: str = ""):
        self._aqi_value = aqi_value
        self._timestamp = timestamp
    
    def get_aqi_value(self) -> int:
        return self._aqi_value
    
    def display(self) -> str:
        return f"AQI: {self._aqi_value}"

@dataclass
class RealTimeAQIData(AQIData):
    """Represents real-time AQI data for a city."""
    def __init__(self, city: City, aqi_value: int, stations: List[StationData], timestamp: str = ""):
        super().__init__(aqi_value, timestamp)
        self.city = city
        self.stations = stations
    
    def display(self) -> str:
        return f"Real-time AQI for {self.city.get_name()}: {self._aqi_value} ({len(self.stations)} stations)"

@dataclass
class CityAQISummary:
    """Comprehensive summary of city AQI data."""
    city: City
    overall_aqi: int
    dominant_pollutant: str
    stations: List[StationData]
    air_quality_level: str
    health_recommendation: str
    color_code: str