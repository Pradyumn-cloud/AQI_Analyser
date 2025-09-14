# models.py
"""
Defines the data models for the application, including City and AQIData.
This file demonstrates encapsulation and inheritance.
"""

class City:
    """Represents a city for which AQI data is requested."""
    def __init__(self, name: str):
        # Encapsulation: __name is a private attribute.
        self.__name = name

    def get_name(self) -> str:
        """Getter for the city name."""
        return self.__name

    def set_name(self, name: str):
        """Setter for the city name."""
        if isinstance(name, str) and name.strip():
            self.__name = name
        else:
            print("Error: City name must be a non-empty string.")

class AQIData:
    """A base class representing generic Air Quality Index data."""
    def __init__(self, station: str, pollutant_id: str, avg_value: str, last_update: str):
        # Encapsulation: Private attributes for data integrity.
        self.__station = station
        self.__pollutant_id = pollutant_id
        self.__avg_value = avg_value
        self.__last_update = last_update

    # --- Getters for private attributes ---
    def get_station(self) -> str:
        return self.__station

    def get_pollutant_id(self) -> str:
        return self.__pollutant_id

    def get_avg_value(self) -> str:
        return self.__avg_value

    def get_last_update(self) -> str:
        return self.__last_update

    def display(self) -> str:
        """
        Polymorphism: A base method to represent the object as a string.
        Subclasses can override this for more specific behavior.
        """
        return (f"Station: {self.__station}, "
                f"Pollutant: {self.__pollutant_id}, "
                f"Avg: {self.__avg_value}, "
                f"Updated: {self.__last_update}")

# --- Inheritance ---
class RealTimeAQIData(AQIData):
    """
    Inherits from AQIData. Represents AQI data fetched from a real-time source.
    This class can be extended with real-time specific attributes or methods.
    """
    def __init__(self, station: str, pollutant_id: str, avg_value: str, last_update: str):
        # Call the parent class constructor
        super().__init__(station, pollutant_id, avg_value, last_update)

    # --- Polymorphism ---
    def display(self) -> str:
        """
        Overrides the parent's display method to add a "Real-time" context.
        """
        base_display_string = super().display()
        return f"[Real-time] {base_display_string}"