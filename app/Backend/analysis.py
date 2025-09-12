from aqi_data import AQIData, RealTimeAQIData, HistoricalAQIData
from typing import List, Dict, Any
from datetime import datetime

class Analysis:
    """Performs comprehensive analysis on AQI data with proper OOP design."""
    
    def __init__(self):
        # Private attributes for encapsulation
        self._analysis_history = []
        self._threshold_settings = {
            'good': 50,
            'moderate': 100,
            'unhealthy_sensitive': 150,
            'unhealthy': 200,
            'very_unhealthy': 300
        }
    
    # Getters for encapsulation
    @property
    def analysis_history(self):
        return self._analysis_history.copy()
    
    @property
    def threshold_settings(self):
        return self._threshold_settings.copy()
    
    # Setter for threshold customization
    def update_threshold(self, category: str, value: float):
        """Update AQI threshold values"""
        if category in self._threshold_settings and 0 <= value <= 500:
            self._threshold_settings[category] = value
        else:
            raise ValueError(f"Invalid category '{category}' or value '{value}'")
    
    def get_health_recommendation(self, aqi_data: AQIData):
        """
        Provides health recommendation based on the AQI value.
        This method demonstrates Polymorphism - it can accept any object
        that is a subclass of AQIData (RealTime or Historical).
        """
        if not isinstance(aqi_data, AQIData):
            raise TypeError("Expected AQIData instance")
        
        aqi = aqi_data.aqi_value
        
        if aqi is None:
            return "No AQI data available - Unable to provide recommendation."
        
        # Store analysis in history
        analysis_record = {
            'timestamp': datetime.now(),
            'city': aqi_data.city,
            'aqi_value': aqi,
            'data_type': type(aqi_data).__name__
        }
        self._analysis_history.append(analysis_record)
        
        # Health recommendations based on AQI ranges
        if aqi <= self._threshold_settings['good']:
            return "Good: Air quality is satisfactory. Enjoy your usual outdoor activities."
        elif aqi <= self._threshold_settings['moderate']:
            return "Moderate: Air quality is acceptable. Unusually sensitive individuals should consider reducing prolonged or heavy exertion."
        elif aqi <= self._threshold_settings['unhealthy_sensitive']:
            return "Unhealthy for Sensitive Groups: Members of sensitive groups may experience health effects. The general public is not likely to be affected."
        elif aqi <= self._threshold_settings['unhealthy']:
            return "Unhealthy: Everyone may begin to experience health effects. Members of sensitive groups may experience more serious health effects."
        elif aqi <= self._threshold_settings['very_unhealthy']:
            return "Very Unhealthy: Health warnings of emergency conditions. The entire population is more likely to be affected."
        else:
            return "Hazardous: Health alert! Everyone may experience more serious health effects."
    
    def compare_aqi_data(self, aqi_data_list: List[AQIData]):
        """
        Compare multiple AQI data points and provide analysis.
        Demonstrates polymorphism by accepting any AQIData subclass.
        """
        if not aqi_data_list:
            return "No data provided for comparison."
        
        valid_data = [data for data in aqi_data_list if isinstance(data, AQIData) and data.aqi_value is not None]
        
        if not valid_data:
            return "No valid AQI data found for comparison."
        
        # Analysis results
        analysis = {
            'total_locations': len(valid_data),
            'average_aqi': sum(data.aqi_value for data in valid_data) / len(valid_data),
            'min_aqi': min(data.aqi_value for data in valid_data),
            'max_aqi': max(data.aqi_value for data in valid_data),
            'cities': [data.city for data in valid_data]
        }
        
        # Find best and worst locations
        best_location = min(valid_data, key=lambda x: x.aqi_value)
        worst_location = max(valid_data, key=lambda x: x.aqi_value)
        
        comparison_text = f"""
AQI Comparison Analysis:
- Total locations analyzed: {analysis['total_locations']}
- Average AQI: {analysis['average_aqi']:.1f}
- Best air quality: {best_location.city} (AQI: {best_location.aqi_value})
- Worst air quality: {worst_location.city} (AQI: {worst_location.aqi_value})
- AQI Range: {analysis['min_aqi']} - {analysis['max_aqi']}
        """
        
        return comparison_text.strip()
    
    def analyze_pollutant_levels(self, aqi_data: AQIData):
        """
        Analyze individual pollutant levels within AQI data.
        """
        if not isinstance(aqi_data, AQIData):
            raise TypeError("Expected AQIData instance")
        
        pollutants = aqi_data.pollutant_data
        
        if not pollutants:
            return "No pollutant data available for analysis."
        
        # Analyze each pollutant
        analysis = []
        analysis.append(f"Pollutant Analysis for {aqi_data.city}:")
        analysis.append("-" * 40)
        
        for pollutant, value in pollutants.items():
            if isinstance(value, (int, float)):
                level_desc = self._get_pollutant_level_description(pollutant, value)
                analysis.append(f"{pollutant}: {value} {level_desc}")
            else:
                analysis.append(f"{pollutant}: {value}")
        
        return "\n".join(analysis)
    
    def _get_pollutant_level_description(self, pollutant: str, value: float):
        """
        Private method to get pollutant level description.
        This demonstrates encapsulation by keeping internal logic private.
        """
        # Simplified pollutant level descriptions
        if pollutant == "PM2.5":
            if value <= 12:
                return "(Good)"
            elif value <= 35:
                return "(Moderate)"
            elif value <= 55:
                return "(Unhealthy for Sensitive Groups)"
            else:
                return "(Unhealthy)"
        elif pollutant == "PM10":
            if value <= 54:
                return "(Good)"
            elif value <= 154:
                return "(Moderate)"
            else:
                return "(Unhealthy)"
        else:
            return "(μg/m³)"
    
    def get_data_source_analysis(self, aqi_data: AQIData):
        """
        Analyze the data source and provide insights.
        Demonstrates polymorphism by handling different AQIData types differently.
        """
        if isinstance(aqi_data, RealTimeAQIData):
            freshness = "Fresh" if aqi_data.is_data_fresh() else "Stale"
            return f"Real-time data from {aqi_data.source_station} - Status: {freshness}"
        elif isinstance(aqi_data, HistoricalAQIData):
            age_days = aqi_data.get_age_in_days()
            recent = "Recent" if aqi_data.is_recent() else "Older"
            return f"Historical data from {age_days} days ago - Category: {recent}"
        else:
            return f"Data source: {aqi_data.get_data_source()}"
    
    def generate_comprehensive_report(self, aqi_data: AQIData):
        """
        Generate a comprehensive analysis report.
        Combines multiple analysis methods demonstrating composition.
        """
        if not isinstance(aqi_data, AQIData):
            raise TypeError("Expected AQIData instance")
        
        report = []
        report.append("=== COMPREHENSIVE AQI ANALYSIS REPORT ===")
        report.append(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        
        # Basic information
        report.append("BASIC INFORMATION:")
        report.append(f"Location: {aqi_data.city}")
        report.append(f"AQI Value: {aqi_data.aqi_value or 'N/A'}")
        report.append(f"Category: {aqi_data.get_aqi_category()}")
        report.append(f"Data Source: {self.get_data_source_analysis(aqi_data)}")
        report.append("")
        
        # Health recommendation
        report.append("HEALTH RECOMMENDATION:")
        report.append(self.get_health_recommendation(aqi_data))
        report.append("")
        
        # Pollutant analysis
        report.append("POLLUTANT ANALYSIS:")
        pollutant_analysis = self.analyze_pollutant_levels(aqi_data)
        report.append(pollutant_analysis)
        
        return "\n".join(report)