from datetime import datetime
from abc import ABC, abstractmethod

class AQIData(ABC):
    """Base abstract class to hold Air Quality Index (AQI) data. (Parent Class)"""
    def __init__(self, city, aqi_value, pollutant_data, timestamp=None):
        # Private attributes for encapsulation
        self._city = city
        self._aqi_value = self._validate_aqi(aqi_value)
        self._pollutant_data = pollutant_data or {}
        self._timestamp = timestamp or datetime.now()

    # --- Getters to access private data (Encapsulation) ---
    @property
    def city(self):
        return self._city

    @property
    def aqi_value(self):
        return self._aqi_value
    
    @property
    def timestamp(self):
        return self._timestamp
    
    @property
    def pollutant_data(self):
        return self._pollutant_data.copy()  # Return copy to prevent external modification

    # --- Setters with validation (Encapsulation) ---
    @city.setter
    def city(self, value):
        if value:
            self._city = value
        else:
            raise ValueError("City cannot be empty")

    @aqi_value.setter 
    def aqi_value(self, value):
        self._aqi_value = self._validate_aqi(value)

    def _validate_aqi(self, value):
        """Private method to validate AQI value"""
        if value is not None:
            try:
                aqi = float(value)
                if 0 <= aqi <= 500:
                    return aqi
                else:
                    raise ValueError("AQI must be between 0 and 500")
            except (ValueError, TypeError):
                return None
        return None

    def get_pollutant_level(self, pollutant_name):
        """Gets the level of a specific pollutant."""
        return self._pollutant_data.get(pollutant_name, "N/A")
    
    def add_pollutant(self, name, value):
        """Add or update a pollutant value"""
        if name and value is not None:
            self._pollutant_data[name] = value

    def get_aqi_category(self):
        """Returns AQI category based on value"""
        if self._aqi_value is None:
            return "Unknown"
        elif self._aqi_value <= 50:
            return "Good"
        elif self._aqi_value <= 100:
            return "Moderate"
        elif self._aqi_value <= 150:
            return "Unhealthy for Sensitive Groups"
        elif self._aqi_value <= 200:
            return "Unhealthy"
        elif self._aqi_value <= 300:
            return "Very Unhealthy"
        else:
            return "Hazardous"

    @abstractmethod
    def get_data_source(self):
        """Abstract method to be implemented by subclasses"""
        pass

    def __str__(self):
        """A user-friendly string representation of the object."""
        return f"AQI for {self.city}: {self.aqi_value or 'N/A'} ({self.get_aqi_category()}) at {self._timestamp.strftime('%Y-%m-%d %H:%M')}"

class RealTimeAQIData(AQIData):
    """Subclass for real-time AQI data."""
    def __init__(self, city, aqi_value, pollutant_data, source_station="Unknown"):
        super().__init__(city, aqi_value, pollutant_data)
        self._source_station = source_station
        self._data_freshness = datetime.now()

    @property
    def source_station(self):
        return self._source_station
    
    @property
    def data_freshness(self):
        return self._data_freshness

    @source_station.setter
    def source_station(self, value):
        self._source_station = value or "Unknown"

    def get_data_source(self):
        """Implementation of abstract method"""
        return f"Real-time from {self._source_station}"
    
    def is_data_fresh(self, max_age_minutes=60):
        """Check if real-time data is still fresh"""
        age = datetime.now() - self._data_freshness
        return age.total_seconds() / 60 <= max_age_minutes
    
    def refresh_timestamp(self):
        """Update the data freshness timestamp"""
        self._data_freshness = datetime.now()

    def __str__(self):
        """Overriding the parent method to add more detail (Polymorphism)"""
        base_info = super().__str__()
        freshness = "Fresh" if self.is_data_fresh() else "Stale"
        return f"{base_info} (Live from: {self.source_station}, Status: {freshness})"

class HistoricalAQIData(AQIData):
    """Subclass for historical AQI data."""
    def __init__(self, city, aqi_value, pollutant_data, date):
        # For historical data, the timestamp is the specific date
        if isinstance(date, str):
            timestamp = datetime.strptime(date, '%Y-%m-%d')
        elif isinstance(date, datetime):
            timestamp = date
        else:
            raise ValueError("Date must be a string in 'YYYY-MM-DD' format or datetime object")
        
        super().__init__(city, aqi_value, pollutant_data, timestamp=timestamp)
        self._date = self._timestamp
        self._data_source = "Historical CSV Data"

    @property
    def date(self):
        return self._date
    
    @property
    def data_source_info(self):
        return self._data_source

    def get_data_source(self):
        """Implementation of abstract method"""
        return self._data_source
    
    def get_age_in_days(self):
        """Calculate how many days old this historical data is"""
        return (datetime.now() - self._date).days
    
    def is_recent(self, days_threshold=30):
        """Check if historical data is within recent threshold"""
        return self.get_age_in_days() <= days_threshold

    def __str__(self):
        """Overriding the parent method for historical context (Polymorphism)"""
        category = self.get_aqi_category()
        age_days = self.get_age_in_days()
        return f"Historical AQI for {self.city} on {self.date.strftime('%Y-%m-%d')}: {self.aqi_value or 'N/A'} ({category}) [{age_days} days ago]"
