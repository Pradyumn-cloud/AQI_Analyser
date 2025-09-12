class City:
    """Represents a city with its geographical details."""
    def __init__(self, name, country=None, lat=None, lon=None):
        # Private attributes for encapsulation
        self._name = name
        self._country = country
        self._lat = lat
        self._lon = lon

    # Getters (Encapsulation)
    @property
    def name(self):
        return self._name
    
    @property
    def country(self):
        return self._country
    
    @property
    def lat(self):
        return self._lat
    
    @property
    def lon(self):
        return self._lon
    
    # Setters (Encapsulation)
    @name.setter
    def name(self, value):
        if value and isinstance(value, str):
            self._name = value.strip()
        else:
            raise ValueError("City name must be a non-empty string")
    
    @country.setter
    def country(self, value):
        if value is None or isinstance(value, str):
            self._country = value.strip() if value else None
        else:
            raise ValueError("Country must be a string or None")
    
    @lat.setter
    def lat(self, value):
        if value is None or (-90 <= float(value) <= 90):
            self._lat = float(value) if value is not None else None
        else:
            raise ValueError("Latitude must be between -90 and 90")
    
    @lon.setter
    def lon(self, value):
        if value is None or (-180 <= float(value) <= 180):
            self._lon = float(value) if value is not None else None
        else:
            raise ValueError("Longitude must be between -180 and 180")

    def __str__(self):
        if self._country:
            return f"{self._name}, {self._country}"
        return self._name
    
    def __repr__(self):
        return f"City(name='{self._name}', country='{self._country}', lat={self._lat}, lon={self._lon})"