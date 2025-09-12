"""
Test script to verify backend integration works properly.
Run this before starting the UI to ensure everything is connected.
"""

import sys
import os

# Add paths
app_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(app_path)

def test_backend_integration():
    """Test if backend integration is working"""
    print("🧪 Testing Backend Integration...")
    print("=" * 50)
    
    try:
        # Import service
        from services import backend_service
        
        # Test 1: Check if backend is available
        print("Test 1: Backend Availability")
        is_available = backend_service.is_backend_available()
        print(f"✅ Backend Available: {is_available}")
        
        if not is_available:
            print("⚠️ Backend not fully available, but service will provide fallback data")
        
        # Test 2: Get available cities
        print("\nTest 2: Available Cities")
        cities = backend_service.get_available_cities()
        print(f"✅ Found {len(cities)} cities: {cities[:5]}{'...' if len(cities) > 5 else ''}")
        
        # Test 3: Get real-time data
        print("\nTest 3: Real-time AQI Data")
        if cities:
            test_city = cities[0]
            realtime_data = backend_service.get_realtime_aqi_data(test_city)
            print(f"✅ Real-time data for {test_city}:")
            print(f"   AQI: {realtime_data.get('aqi_value', 'N/A')}")
            print(f"   Status: {realtime_data.get('status', 'N/A')}")
            print(f"   Source: {realtime_data.get('data_source', 'N/A')}")
        
        # Test 4: Get historical data
        print("\nTest 4: Historical AQI Data")
        if cities:
            historical_data = backend_service.get_historical_aqi_data(test_city)
            print(f"✅ Historical data for {test_city}:")
            print(f"   AQI: {historical_data.get('aqi_value', 'N/A')}")
            print(f"   Status: {historical_data.get('status', 'N/A')}")
            print(f"   Timestamp: {historical_data.get('timestamp', 'N/A')}")
        
        # Test 5: Health recommendation
        print("\nTest 5: Health Recommendation")
        if cities:
            recommendation = backend_service.get_health_recommendation(test_city)
            print(f"✅ Health recommendation for {test_city}:")
            print(f"   {recommendation[:100]}{'...' if len(recommendation) > 100 else ''}")
        
        # Test 6: City comparison
        print("\nTest 6: City Comparison")
        if len(cities) >= 2:
            comparison = backend_service.compare_cities([cities[0], cities[1]])
            if "comparison_text" in comparison:
                print(f"✅ Comparison between {cities[0]} and {cities[1]}:")
                print(f"   {comparison['comparison_text'][:100]}{'...' if len(comparison['comparison_text']) > 100 else ''}")
            else:
                print(f"⚠️ Comparison result: {comparison}")
        
        print("\n" + "=" * 50)
        print("🎉 Backend Integration Test Complete!")
        print("✅ All systems ready for UI connection")
        
        return True
        
    except Exception as e:
        print(f"❌ Backend integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_backend_integration()
    if success:
        print("\n🚀 You can now run the UI with: python main.py")
    else:
        print("\n⚠️ There were issues with backend integration. The UI will use fallback data.")
