"""
Main module demonstrating the complete OOP implementation of AQI Analyzer.
This module showcases:
- Encapsulation: Private attributes with getters/setters
- Inheritance: AQIData -> RealTimeAQIData, HistoricalAQIData
- Polymorphism: Different data sources handled uniformly
- Abstraction: Abstract base classes for data fetchers
"""

from city import City
from aqi_data import AQIData, RealTimeAQIData, HistoricalAQIData
from data_fetcher import DataFetcher, APIDataFetcher, CSVDataFetcher
from analysis import Analysis
from datetime import datetime

class AQIAnalyzerApp:
    """
    Main application class demonstrating OOP design patterns.
    Encapsulates the entire application logic.
    """
    
    def __init__(self):
        # Private attributes (Encapsulation)
        self._csv_fetcher = CSVDataFetcher()
        self._api_fetcher = APIDataFetcher()
        self._analyzer = Analysis()
        self._session_data = []
    
    # Getters (Encapsulation)
    @property
    def available_cities(self):
        return self._csv_fetcher.get_available_cities()
    
    @property
    def session_data(self):
        return self._session_data.copy()
    
    def demonstrate_encapsulation(self):
        """Demonstrate encapsulation with City class"""
        print("=== DEMONSTRATING ENCAPSULATION ===")
        
        # Create a city with private attributes
        city = City("Mumbai", "India", 19.0760, 72.8777)
        
        print(f"City created: {city}")
        print(f"Accessing city name via property: {city.name}")
        print(f"Accessing coordinates: ({city.lat}, {city.lon})")
        
        # Demonstrate setter validation
        try:
            city.name = "New Mumbai"  # Valid
            print(f"City name updated: {city.name}")
            
            city.lat = 91  # Invalid - should raise error
        except ValueError as e:
            print(f"Encapsulation working - Validation error: {e}")
        
        print()
    
    def demonstrate_inheritance_and_polymorphism(self):
        """Demonstrate inheritance and polymorphism"""
        print("=== DEMONSTRATING INHERITANCE & POLYMORPHISM ===")
        
        # Get data using different fetchers (Polymorphism)
        city_name = "Delhi"
        
        # Fetch historical data (inheritance from AQIData)
        historical_data = self._csv_fetcher.fetch_historical_data(city_name)
        
        if historical_data:
            print(f"Historical Data: {historical_data}")
            print(f"Data source: {historical_data.get_data_source()}")
            print(f"Age in days: {historical_data.get_age_in_days()}")
            
            # Polymorphism - same method works for different subclasses
            recommendation = self._analyzer.get_health_recommendation(historical_data)
            print(f"Health Recommendation: {recommendation}")
            
            self._session_data.append(historical_data)
        
        # Try to fetch real-time data (different subclass)
        print("\nAttempting to fetch real-time data...")
        try:
            realtime_data = self._api_fetcher.fetch_realtime_data(city_name)
            if realtime_data:
                print(f"Real-time Data: {realtime_data}")
                print(f"Data source: {realtime_data.get_data_source()}")
                
                # Same analyzer method works with different data types (Polymorphism)
                recommendation = self._analyzer.get_health_recommendation(realtime_data)
                print(f"Health Recommendation: {recommendation}")
                
                self._session_data.append(realtime_data)
            else:
                print("Real-time data not available (API might be down)")
        except Exception as e:
            print(f"Real-time data fetch failed: {e}")
        
        print()
    
    def demonstrate_data_analysis(self):
        """Demonstrate comprehensive data analysis"""
        print("=== DEMONSTRATING DATA ANALYSIS ===")
        
        if not self._session_data:
            print("No data available for analysis")
            return
        
        # Analyze individual data points
        for data in self._session_data:
            print(f"\nAnalyzing data for {data.city}:")
            
            # Generate comprehensive report
            report = self._analyzer.generate_comprehensive_report(data)
            print(report)
            print("-" * 50)
        
        # Compare multiple data points if available
        if len(self._session_data) > 1:
            print("\nCOMPARATIVE ANALYSIS:")
            comparison = self._analyzer.compare_aqi_data(self._session_data)
            print(comparison)
    
    def demonstrate_csv_data_operations(self):
        """Demonstrate working with CSV data"""
        print("=== DEMONSTRATING CSV DATA OPERATIONS ===")
        
        available_cities = self.available_cities
        print(f"Available cities in dataset: {len(available_cities)}")
        print(f"Sample cities: {available_cities[:10]}")  # Show first 10
        
        # Get data for multiple cities
        sample_cities = available_cities[:3] if len(available_cities) >= 3 else available_cities
        multi_city_data = []
        
        for city in sample_cities:
            data = self._csv_fetcher.fetch_historical_data(city)
            if data:
                multi_city_data.append(data)
                print(f"Data loaded for {city}: AQI = {data.aqi_value}")
                
                # Get date range for this city
                start_date, end_date = self._csv_fetcher.get_date_range_for_city(city)
                print(f"  Date range: {start_date} to {end_date}")
        
        # Perform comparative analysis
        if multi_city_data:
            print("\nMulti-city comparison:")
            comparison = self._analyzer.compare_aqi_data(multi_city_data)
            print(comparison)
        
        print()
    
    def run_complete_demo(self):
        """Run the complete OOP demonstration"""
        print("AQI ANALYZER - COMPLETE OOP DEMONSTRATION")
        print("=" * 60)
        print(f"Demo started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # 1. Demonstrate Encapsulation
        self.demonstrate_encapsulation()
        
        # 2. Demonstrate Inheritance and Polymorphism
        self.demonstrate_inheritance_and_polymorphism()
        
        # 3. Demonstrate CSV operations
        self.demonstrate_csv_data_operations()
        
        # 4. Demonstrate Analysis
        self.demonstrate_data_analysis()
        
        print("\n" + "=" * 60)
        print("DEMO COMPLETED SUCCESSFULLY!")
        print(f"Total data points processed: {len(self._session_data)}")
        print(f"Analysis history entries: {len(self._analyzer.analysis_history)}")

def main():
    """Main function to run the OOP demonstration"""
    try:
        app = AQIAnalyzerApp()
        app.run_complete_demo()
    except Exception as e:
        print(f"Application error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()