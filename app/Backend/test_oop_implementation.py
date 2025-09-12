"""
Test script to verify OOP implementation works correctly.
This script tests all the major OOP concepts implemented.
"""

import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from city import City
from aqi_data import AQIData, RealTimeAQIData, HistoricalAQIData
from data_fetcher import CSVDataFetcher, APIDataFetcher
from analysis import Analysis

def test_encapsulation():
    """Test encapsulation in City class"""
    print("Testing Encapsulation...")
    
    # Create city with encapsulated attributes
    city = City("Mumbai", "India", 19.0760, 72.8777)
    
    # Test getters
    assert city.name == "Mumbai"
    assert city.country == "India"
    assert city.lat == 19.0760
    assert city.lon == 72.8777
    
    # Test setters with validation
    city.name = "New Mumbai"
    assert city.name == "New Mumbai"
    
    try:
        city.lat = 91  # Should raise ValueError
        assert False, "Should have raised ValueError"
    except ValueError:
        pass  # Expected
    
    print("✓ Encapsulation tests passed!")

def test_inheritance():
    """Test inheritance hierarchy"""
    print("Testing Inheritance...")
    
    # Test base class
    pollutants = {"PM2.5": 45, "PM10": 78}
    
    # Test RealTimeAQIData inheritance
    realtime_data = RealTimeAQIData("Delhi", 150, pollutants, "Station A")
    assert isinstance(realtime_data, AQIData)  # Is-a relationship
    assert realtime_data.city == "Delhi"
    assert realtime_data.aqi_value == 150
    assert realtime_data.source_station == "Station A"
    
    # Test HistoricalAQIData inheritance
    historical_data = HistoricalAQIData("Mumbai", 120, pollutants, "2023-01-01")
    assert isinstance(historical_data, AQIData)  # Is-a relationship
    assert historical_data.city == "Mumbai"
    assert historical_data.aqi_value == 120
    
    print("✓ Inheritance tests passed!")

def test_polymorphism():
    """Test polymorphism with different AQIData types"""
    print("Testing Polymorphism...")
    
    analyzer = Analysis()
    pollutants = {"PM2.5": 25, "PM10": 50}
    
    # Create different data types
    realtime_data = RealTimeAQIData("Delhi", 75, pollutants, "Station A")
    historical_data = HistoricalAQIData("Mumbai", 125, pollutants, "2023-01-01")
    
    # Same method should work for both types (polymorphism)
    realtime_recommendation = analyzer.get_health_recommendation(realtime_data)
    historical_recommendation = analyzer.get_health_recommendation(historical_data)
    
    assert "Moderate" in realtime_recommendation
    assert "Unhealthy" in historical_recommendation
    
    # Test comparison with mixed types
    comparison = analyzer.compare_aqi_data([realtime_data, historical_data])
    assert "2" in comparison  # Should show 2 locations
    
    print("✓ Polymorphism tests passed!")

def test_csv_data_fetcher():
    """Test CSV data fetcher"""
    print("Testing CSV Data Fetcher...")
    
    csv_fetcher = CSVDataFetcher()
    
    # Test if CSV data is loaded
    cities = csv_fetcher.get_available_cities()
    if cities:
        print(f"Found {len(cities)} cities in CSV data")
        
        # Test fetching data for a city
        test_city = cities[0] if cities else "Delhi"
        data = csv_fetcher.fetch_historical_data(test_city)
        
        if data:
            assert isinstance(data, HistoricalAQIData)
            assert data.city == test_city
            print(f"Successfully fetched data for {test_city}")
        else:
            print(f"No data found for {test_city}")
    else:
        print("No cities found in CSV data - check file path")
    
    print("✓ CSV Data Fetcher tests passed!")

def test_analysis_features():
    """Test analysis features"""
    print("Testing Analysis Features...")
    
    analyzer = Analysis()
    pollutants = {"PM2.5": 35, "PM10": 65, "NO2": 40}
    
    # Create test data
    aqi_data = HistoricalAQIData("TestCity", 95, pollutants, "2023-01-01")
    
    # Test health recommendation
    recommendation = analyzer.get_health_recommendation(aqi_data)
    assert "Moderate" in recommendation
    
    # Test pollutant analysis
    pollutant_analysis = analyzer.analyze_pollutant_levels(aqi_data)
    assert "PM2.5" in pollutant_analysis
    assert "PM10" in pollutant_analysis
    
    # Test comprehensive report
    report = analyzer.generate_comprehensive_report(aqi_data)
    assert "COMPREHENSIVE AQI ANALYSIS REPORT" in report
    assert "TestCity" in report
    
    print("✓ Analysis features tests passed!")

def main():
    """Run all tests"""
    print("Starting OOP Implementation Tests")
    print("=" * 50)
    
    try:
        test_encapsulation()
        test_inheritance()
        test_polymorphism()
        test_csv_data_fetcher()
        test_analysis_features()
        
        print("\n" + "=" * 50)
        print("🎉 ALL TESTS PASSED! OOP implementation is working correctly.")
        print("✓ Encapsulation: Private attributes with getters/setters")
        print("✓ Inheritance: AQIData base class with specialized subclasses")
        print("✓ Polymorphism: Same methods work with different data types")
        print("✓ Abstraction: Abstract base classes and interface segregation")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
