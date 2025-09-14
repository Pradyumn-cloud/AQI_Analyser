# historical_analyzer.py
"""
Contains the HistoricalAnalyzer class for processing and visualizing
historical AQI data. This version is adapted for GUI integration
by returning plot data instead of saving files.
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64
from typing import Dict, Optional

from datetime import datetime
from .models import AQIData

class HistoricalAnalyzer:
    """Analyzes historical AQI data and returns plots as base64 strings."""

    def __init__(self, csv_filepath: str):
        """Initializes the analyzer by loading and preprocessing the dataset."""
        try:
            self.__df = pd.read_csv(csv_filepath)
            self.__preprocess_data()
        except FileNotFoundError:
            self.__df = None

    def __preprocess_data(self):
        """Private method to perform initial data cleaning."""
        if self.__df is None: return
        self.__df['Datetime'] = pd.to_datetime(self.__df['Datetime'], errors='coerce')
        pollutant_cols = ['PM2.5', 'PM10', 'NO2', 'CO', 'SO2', 'O3', 'AQI']
        for col in pollutant_cols:
            if col in self.__df.columns:
                self.__df[col] = pd.to_numeric(self.__df[col], errors='coerce')

    def analyze_city(self, city_name: str) -> Optional[Dict[str, str]]:
        """
        Runs analysis for a city and returns a dictionary of base64-encoded plots.
        Returns None if the city or data is not found.
        """
        if self.__df is None: return None

        city_df = self.__df[self.__df['City'].str.lower() == city_name.lower()].copy()
        if city_df.empty: return None

        city_df.set_index('Datetime', inplace=True)
        city_df.fillna(method='ffill', inplace=True)

        plots = {
            "trend": self._plot_monthly_aqi_trends(city_df, city_name),
            "heatmap": self._plot_pollutant_heatmap(city_df, city_name),
            "distribution": self._plot_aqi_distribution(city_df, city_name)
        }
        return plots

    def _generate_plot_base64(self) -> str:
        """Helper method to convert a matplotlib plot to a base64 string."""
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight')
        buf.seek(0)
        img_str = base64.b64encode(buf.read()).decode('utf-8')
        plt.close()
        return img_str

    def _plot_monthly_aqi_trends(self, df: pd.DataFrame, city_name: str) -> str:
        """Plots monthly AQI trends and returns as base64 string."""
        monthly_avg_aqi = df['AQI'].resample('M').mean()
        plt.style.use('seaborn-v0_8-whitegrid')
        plt.figure(figsize=(10, 5))
        monthly_avg_aqi.plot(color='royalblue', lw=2)
        plt.title(f'Monthly Average AQI Trend in {city_name.title()}', fontsize=14)
        plt.xlabel('Year')
        plt.ylabel('Average AQI')
        return self._generate_plot_base64()

    def _plot_pollutant_heatmap(self, df: pd.DataFrame, city_name: str) -> str:
        """Creates a pollutant correlation heatmap and returns as base64 string."""
        pollutants = ['PM2.5', 'PM10', 'NO2', 'SO2', 'CO', 'O3', 'AQI']
        valid_pollutants = [p for p in pollutants if p in df.columns]
        correlation_matrix = df[valid_pollutants].corr()
        plt.figure(figsize=(8, 6))
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")
        plt.title(f'Pollutant Correlation for {city_name.title()}', fontsize=14)
        return self._generate_plot_base64()

    def _plot_aqi_distribution(self, df: pd.DataFrame, city_name: str) -> str:
        """Plots AQI distribution and returns as base64 string."""
        plt.figure(figsize=(10, 5))
        sns.histplot(df['AQI'].dropna(), kde=True, color='forestgreen', bins=50)
        plt.axvline(50, color='lime', linestyle='--', label='Good')
        plt.axvline(100, color='gold', linestyle='--', label='Satisfactory')
        plt.axvline(200, color='orange', linestyle='--', label='Moderate')
        plt.title(f'Distribution of AQI Values in {city_name.title()}', fontsize=14)
        plt.xlabel('AQI Value')
        plt.ylabel('Frequency')
        plt.legend()
        return self._generate_plot_base64()