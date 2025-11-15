from typing import List, Dict
from .models import CityAQISummary, StationData, PollutantData
import flet as ft

class AQIAnalysis:
    
    @staticmethod
    def display_summary(city, aqi_records: List):
        print(f"AQI Summary for {city.get_name()}")
    
    def get_comprehensive_analysis(self, summary: CityAQISummary) -> Dict:
        basic_analysis = self.get_aqi_analysis(summary.overall_aqi)
        
        return {
            'overall_aqi': summary.overall_aqi,
            'level': basic_analysis['level'],
            'color': basic_analysis['color'],
            'description': basic_analysis['description'],
            'dominant_pollutant': summary.dominant_pollutant,
            'station_count': len(summary.stations),
            'health_impact': self._get_health_impact(summary.overall_aqi),
            'recommendations': self._get_recommendations(summary.overall_aqi),
            'pollutant_breakdown': self._get_pollutant_breakdown(summary.stations),
            'station_comparison': self._compare_stations(summary.stations)
        }
    
    def get_aqi_analysis(self, aqi_value: int) -> Dict:
        if aqi_value <= 50:
            return {
                'level': 'Good',
                'color': ft.Colors.GREEN_600,
                'description': 'Air quality is satisfactory for most people'
            }
        elif aqi_value <= 100:
            return {
                'level': 'Moderate',
                'color': ft.Colors.YELLOW_600,
                'description': 'Air quality is acceptable for most people'
            }
        elif aqi_value <= 150:
            return {
                'level': 'Unhealthy for Sensitive Groups',
                'color': ft.Colors.ORANGE_600,
                'description': 'Sensitive individuals may experience minor symptoms'
            }
        elif aqi_value <= 200:
            return {
                'level': 'Unhealthy',
                'color': ft.Colors.RED_600,
                'description': 'Everyone may begin to experience health effects'
            }
        elif aqi_value <= 300:
            return {
                'level': 'Very Unhealthy',
                'color': ft.Colors.PURPLE_600,
                'description': 'Health warnings of emergency conditions'
            }
        else:
            return {
                'level': 'Hazardous',
                'color': ft.Colors.BROWN_600,
                'description': 'Health alert: everyone may experience serious effects'
            }
    
    def _get_health_impact(self, aqi_value: int) -> str:
        """Get detailed health impact description based on AQI."""
        if aqi_value <= 50:
            return "Air quality poses little or no risk. Ideal for outdoor activities and exercise."
        elif aqi_value <= 100:
            return "Air quality is acceptable. Unusually sensitive people should consider limiting prolonged outdoor exertion."
        elif aqi_value <= 150:
            return "Members of sensitive groups may experience health effects. The general public is less likely to be affected."
        elif aqi_value <= 200:
            return "Some members of the general public may experience health effects; sensitive groups may experience more serious effects."
        elif aqi_value <= 300:
            return "Health alert: The risk of health effects is increased for everyone."
        else:
            return "Health warning of emergency conditions: everyone is more likely to be affected."
    
    def _get_recommendations(self, aqi_value: int) -> List[str]:
        """Get specific health recommendations based on AQI level."""
        if aqi_value <= 50:
            return [
                "Perfect day for outdoor activities",
                "Windows can be kept open for fresh air",
                "Great time for jogging or cycling",
                "No special precautions needed"
            ]
        elif aqi_value <= 100:
            return [
                "Good day for most outdoor activities",
                "Sensitive people should monitor symptoms",
                "Consider closing windows during peak hours",
                "Air purifiers not necessary for most people"
            ]
        elif aqi_value <= 150:
            return [
                "Limit prolonged outdoor activities",
                "Keep windows closed during daytime",
                "Use air purifier if available",
                "Sensitive groups should stay indoors"
            ]
        elif aqi_value <= 200:
            return [
                "Avoid outdoor exercise and activities",
                "Keep windows and doors closed",
                "Use N95 masks when going outside",
                "Run air purifiers continuously"
            ]
        elif aqi_value <= 300:
            return [
                "Stay indoors as much as possible",
                "Use high-quality air purifiers",
                "Wear N95 or better masks outdoors",
                "Avoid all outdoor physical activities"
            ]
        else:
            return [
                "Emergency conditions - minimize outdoor exposure",
                "Seal gaps around windows and doors",
                "Use multiple air purifiers",
                "Seek medical attention if experiencing symptoms"
            ]
    
    def _get_pollutant_breakdown(self, stations: List[StationData]) -> Dict[str, Dict]:
        """Analyze pollutant distribution across stations."""
        pollutant_data = {}
        
        for station in stations:
            for pollutant in station.pollutants:
                if pollutant.pollutant_id not in pollutant_data:
                    pollutant_data[pollutant.pollutant_id] = {
                        'values': [],
                        'min': float('inf'),
                        'max': float('-inf'),
                        'total': 0,
                        'count': 0
                    }
                
                data_entry = pollutant_data[pollutant.pollutant_id]
                data_entry['values'].append(pollutant.avg_value)
                data_entry['min'] = min(data_entry['min'], pollutant.min_value)
                data_entry['max'] = max(data_entry['max'], pollutant.max_value)
                data_entry['total'] += pollutant.avg_value
                data_entry['count'] += 1
        
        # Calculate averages and format data
        for pollutant in pollutant_data:
            data = pollutant_data[pollutant]
            data['avg'] = data['total'] / data['count'] if data['count'] > 0 else 0
            # Remove intermediate calculation fields
            del data['total'], data['count']
        
        return pollutant_data
    
    def _compare_stations(self, stations: List[StationData]) -> List[Dict]:
        """Compare pollution levels across different stations."""
        station_scores = []
        
        for station in stations:
            pm25_avg = 0
            pm10_avg = 0
            pollutant_sum = 0
            pollutant_count = 0
            
            for pollutant in station.pollutants:
                if pollutant.pollutant_id == "PM2.5":
                    pm25_avg = pollutant.avg_value
                elif pollutant.pollutant_id == "PM10":
                    pm10_avg = pollutant.avg_value
                
                # Weight different pollutants for overall score
                weight = self._get_pollutant_weight(pollutant.pollutant_id)
                pollutant_sum += pollutant.avg_value * weight
                pollutant_count += weight
            
            # Calculate overall station score
            overall_score = pollutant_sum / pollutant_count if pollutant_count > 0 else pm25_avg
            
            station_scores.append({
                'station': station.station,
                'score': overall_score,
                'pm25': pm25_avg,
                'pm10': pm10_avg,
                'pollutant_count': len(station.pollutants),
                'quality_rating': self._get_station_rating(overall_score)
            })
        
        return sorted(station_scores, key=lambda x: x['score'])
    
    def _get_pollutant_weight(self, pollutant_id: str) -> float:
        """Get weight for different pollutants in overall scoring."""
        weights = {
            'PM2.5': 1.0,    # Highest weight - most harmful
            'PM10': 0.8,
            'NO2': 0.6,
            'SO2': 0.5,
            'CO': 0.4,
            'OZONE': 0.7
        }
        return weights.get(pollutant_id, 0.3)
    
    def _get_station_rating(self, score: float) -> str:
        """Get quality rating for a station based on its score."""
        if score <= 50:
            return "Excellent"
        elif score <= 100:
            return "Good"
        elif score <= 150:
            return "Moderate"
        elif score <= 200:
            return "Poor"
        else:
            return "Very Poor"