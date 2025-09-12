# AQI Analyzer - OOP Implementation

## Overview
This project demonstrates comprehensive Object-Oriented Programming (OOP) concepts in Python through an Air Quality Index (AQI) analyzer application.

## OOP Concepts Implemented

### 1. Encapsulation
- **City Class**: Private attributes (`_name`, `_country`, `_lat`, `_lon`) with property-based getters and setters
- **AQIData Class**: Private attributes with validation and controlled access
- **Analysis Class**: Private analysis history and threshold settings

**Example:**
```python
city = City("Mumbai", "India", 19.0760, 72.8777)
city.name = "New Mumbai"  # Uses setter with validation
print(city.name)  # Uses getter
```

### 2. Inheritance
- **Base Class**: `AQIData` (abstract base class)
- **Subclasses**: 
  - `RealTimeAQIData`: Extends AQIData for real-time data
  - `HistoricalAQIData`: Extends AQIData for historical data
- **DataFetcher Hierarchy**: Abstract `DataFetcher` with `APIDataFetcher` and `CSVDataFetcher` subclasses

**Example:**
```python
# Both classes inherit from AQIData
realtime_data = RealTimeAQIData("Delhi", 150, pollutants, "Station A")
historical_data = HistoricalAQIData("Mumbai", 120, pollutants, "2023-01-01")
```

### 3. Polymorphism
- **Method Overriding**: Each subclass implements `__str__()` and `get_data_source()` differently
- **Duck Typing**: Analysis methods work with any AQIData subclass
- **Interface Consistency**: Same methods work differently based on object type

**Example:**
```python
analyzer = Analysis()
# Same method works with different data types
analyzer.get_health_recommendation(realtime_data)  # Works with RealTimeAQIData
analyzer.get_health_recommendation(historical_data)  # Works with HistoricalAQIData
```

### 4. Abstraction
- **Abstract Base Classes**: `AQIData` and `DataFetcher` define interfaces
- **Private Methods**: Internal implementation details hidden from users
- **High-level Interface**: Complex operations exposed through simple methods

## Class Structure

```
AQIData (Abstract Base Class)
├── RealTimeAQIData
└── HistoricalAQIData

DataFetcher (Abstract Base Class)
├── APIDataFetcher
└── CSVDataFetcher

City (Standalone Class)
Analysis (Standalone Class)
AQIAnalyzerApp (Main Application Class)
```

## Key Features

### City Class
- Encapsulated geographical data
- Validation for coordinates
- Property-based access control

### AQIData Hierarchy
- Base class with common functionality
- Specialized subclasses for different data sources
- Abstract methods enforcing implementation

### DataFetcher Hierarchy
- Abstract interface for data fetching
- API and CSV implementations
- Caching and error handling

### Analysis Class
- Comprehensive AQI analysis
- Health recommendations
- Comparative analysis
- Report generation

## Usage

### Running the Complete Demo
```bash
cd app/Backend
python main.py
```

### Running Tests
```bash
cd app/Backend
python test_oop_implementation.py
```

### Using Individual Classes
```python
from city import City
from data_fetcher import CSVDataFetcher
from analysis import Analysis

# Create city
city = City("Delhi")

# Fetch data
fetcher = CSVDataFetcher()
data = fetcher.fetch_historical_data("Delhi")

# Analyze data
analyzer = Analysis()
recommendation = analyzer.get_health_recommendation(data)
```

## Data Source
- **CSV Data**: Uses `city_day.csv` from the Data folder
- **API Data**: Configured for real-time data (requires internet)

## OOP Benefits Demonstrated

1. **Code Reusability**: Base classes provide common functionality
2. **Maintainability**: Changes to base classes affect all subclasses
3. **Extensibility**: Easy to add new data sources or analysis methods
4. **Data Protection**: Private attributes prevent unauthorized access
5. **Interface Consistency**: Same methods work across different implementations

## File Structure
```
Backend/
├── city.py                      # City class with encapsulation
├── aqi_data.py                  # AQIData hierarchy (inheritance)
├── data_fetcher.py              # DataFetcher hierarchy (abstraction)
├── analysis.py                  # Analysis class with polymorphism
├── main.py                      # Main application demonstrating all concepts
├── test_oop_implementation.py   # Unit tests for OOP concepts
└── README.md                    # This file
```

## Requirements
- Python 3.7+
- requests library (for API data fetching)
- CSV data files in ../Data/ directory

## Testing
The implementation includes comprehensive tests that verify:
- Encapsulation with property validation
- Inheritance relationships
- Polymorphic behavior
- Data fetching operations
- Analysis functionality

All tests must pass to ensure proper OOP implementation.
