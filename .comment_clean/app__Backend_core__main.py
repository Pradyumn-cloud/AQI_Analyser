
"""
The main entry point for the AQI monitoring application.
It orchestrates the creation of objects and the flow of data.
"""
from .import config 
from .models import City 
from .fetcher import DataFetcher 
from .analysis import Analysis 

def run_application ():
    """Main function to run the application logic."""
    print ("🚀 Welcome to the Real-time AQI Monitoring App!")


    city_name =input ("Please enter a city name (e.g., Delhi, Mumbai): ").strip ()
    if not city_name :
        print ("City name cannot be empty. Exiting.")
        return 


    target_city =City (city_name )
    data_fetcher =DataFetcher (api_url =config .API_URL ,api_key =config .API_KEY )


    print (f"\n🔍 Fetching data for {target_city .get_name ().title ()}...")

    aqi_data =data_fetcher .fetch_data_for_city (target_city )


    if aqi_data is not None :
        Analysis .display_summary (target_city ,aqi_data )
    else :
        print ("Could not retrieve data. Please check your connection or the city name.")

if __name__ =="__main__":
    run_application ()