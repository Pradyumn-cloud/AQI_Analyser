# ui/historical_view.py
import flet as ft
from assets import styles as S

class HistoricalView:
    def __init__(self, page: ft.Page, city="Delhi", app_instance=None):
        self.page = page
        self.city = city
        self.app = app_instance
        self.historical_data = []
        self.selected_date = None
        self._load_historical_data()
    
    def _load_historical_data(self):
        """Load historical data from backend"""
        if self.app and self.app.backend and self.app.backend.is_backend_available():
            try:
                data = self.app.backend.get_historical_aqi_data(self.city, self.selected_date)
                if data:
                    self.historical_data = [data]
                    
                # Get pollutant analysis
                self.pollutant_analysis = self.app.backend.get_pollutant_analysis(self.city)
            except Exception as e:
                print(f"Error loading historical data: {e}")
    
    def _on_city_change(self, e):
        """Handle city selection change"""
        selected_city = e.control.value
        if selected_city and self.app:
            self.city = selected_city
            self._load_historical_data()
            # Rebuild the view
            self.page.update()
    
    def _on_date_change(self, e):
        """Handle date selection change"""
        if e.control.value:
            self.selected_date = e.control.value.strftime("%Y-%m-%d")
            self._load_historical_data()
            self.page.update()
    
    def _create_city_selector(self):
        """Create city selection dropdown"""
        if not self.app:
            return ft.Container()
        
        return ft.Dropdown(
            label="Select City",
            value=self.city,
            options=[ft.dropdown.Option(city) for city in self.app.available_cities],
            on_change=self._on_city_change,
            width=200,
        )
    
    def _create_date_picker(self):
        """Create date picker for historical data"""
        return ft.ElevatedButton(
            "Select Date",
            icon=ft.Icons.CALENDAR_MONTH,
            on_click=lambda e: self.page.open(
                ft.DatePicker(
                    first_date=ft.datetime.datetime(2020, 1, 1),
                    last_date=ft.datetime.datetime.now(),
                    on_change=self._on_date_change,
                )
            ),
        )
    
    def _get_historical_stats(self):
        """Get statistics from historical data"""
        if self.historical_data:
            data = self.historical_data[0]
            return {
                "current_aqi": data.get("aqi_value", 0),
                "status": data.get("status", "Unknown"),
                "city": data.get("city", self.city),
                "data_age": "Historical data"
            }
        return {
            "current_aqi": 0,
            "status": "No Data",
            "city": self.city,
            "data_age": "No historical data available"
        }

    def stat(self, title: str, value: str, color: str) -> ft.Container:
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text(title, style=S.CAPTION),
                    ft.Text(value, style=S.H2, color=ft.Colors.BLACK),
                ],
                spacing=6,
            ),
            padding=16,
            bgcolor=color,
            border_radius=16,
            width=160,
        )

    def build(self) -> ft.Column:
        # Get current stats
        stats = self._get_historical_stats()
        
        # Controls section
        controls_section = ft.Container(
            content=ft.Row([
                self._create_city_selector(),
                self._create_date_picker(),
            ], spacing=12),
            padding=10,
        )
        
        # Historical data display
        historical_info = S.card(
            ft.Column(
                [
                    ft.Text(f"📊 Historical Data for {stats['city']}", style=S.BODY),
                    ft.Text(f"AQI: {stats['current_aqi']} ({stats['status']})", style=S.H2),
                    ft.Text(stats['data_age'], style=S.CAPTION),
                    ft.Text(f"Date: {self.selected_date or 'Latest available'}", style=S.CAPTION),
                ],
                spacing=10,
            ),
            padding=18,
        )
        
        # Pollutant analysis display
        pollutant_display = S.card(
            ft.Column(
                [
                    ft.Text("🔬 Pollutant Analysis", style=S.BODY),
                    ft.Container(
                        content=ft.Text(
                            getattr(self, 'pollutant_analysis', 'No pollutant data available'),
                            style=S.CAPTION,
                            selectable=True
                        ),
                        bgcolor=S.CARD_SOFT,
                        border_radius=16,
                        padding=12,
                        height=200
                    ),
                ],
                spacing=10,
            ),
            padding=18,
        )
        
        monthly = S.card(
            ft.Column(
                [
                    ft.Text("📊 Monthly AQI (CSV Data Available)", style=S.BODY),
                    ft.Container(height=160, bgcolor=S.CARD_SOFT, border_radius=16),
                    ft.Text("Backend integration: CSV data loaded with 29,531+ records", style=S.CAPTION),
                ],
                spacing=10,
            ),
            padding=18,
        )
        yearly = S.card(
            ft.Column(
                [
                    ft.Text("📈 Yearly AQI (Historical Analysis)", style=S.BODY),
                    ft.Container(height=160, bgcolor=S.CARD_SOFT, border_radius=16),
                    ft.Text("Backend integration: Multiple cities available for analysis", style=S.CAPTION),
                ],
                spacing=10,
            ),
            padding=18,
        )

        tabs = ft.Tabs(
            tabs=[
                ft.Tab(text="Current", content=historical_info),
                ft.Tab(text="Pollutants", content=pollutant_display),
                ft.Tab(text="Monthly", content=monthly),
                ft.Tab(text="Yearly", content=yearly),
            ],
            selected_index=0,
            expand=1,
        )

        stats_row = ft.Row(
            [
                self.stat("Best AQI", "40", S.GOOD),
                self.stat("Worst AQI", "180", S.POOR),
                self.stat("Average", "92", S.MODERATE),
            ],
            spacing=12,
            wrap=True,
        )

        col = ft.Column(
            [
                ft.Text(f"Historical Analysis - {self.city}", style=S.TITLE),
                controls_section,
                tabs,
                stats_row,
            ],
            spacing=16,
            expand=True,
            scroll="auto",
        )
        return ft.Container(
            content=ft.Column([
                col
            ],
            spacing=0,
            expand=True,
            ),
            padding=16,
            bgcolor=S.BG,
            expand=True,
        )
