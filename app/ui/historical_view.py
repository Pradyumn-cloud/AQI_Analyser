import flet as ft
from Backend_core.historical_analyzer import HistoricalAnalyzer
from Backend_core.config import API_URL, API_KEY
from assets import styles as S
from ui.components import NavBar, LoadingOverlay

class HistoricalView(ft.View):
    """Professional Historical Data View"""
    
    def __init__(self, page: ft.Page):
        super().__init__(
            route="/historical",
            padding=0,
            scroll=ft.ScrollMode.AUTO,
            bgcolor=S.BG
        )
        self.page = page
        self.analyzer = HistoricalAnalyzer(API_URL, API_KEY)
        
        self._init_components()
        self._build_layout()
    
    def _init_components(self):
        """Initialize components"""
        self.navbar = NavBar(self.page, "Historical Analysis")
        self.loading = LoadingOverlay()
        
        # Search inputs
        self.city_input = ft.TextField(
            hint_text="City name",
            border_color=S.PRIMARY,
            text_style=ft.TextStyle(color=S.TEXT_PRIMARY),
            bgcolor=S.CARD,
            border_radius=S.RADIUS_SMALL,
            prefix_icon=ft.Icons.LOCATION_CITY,
            height=56
        )
        
        self.days_dropdown = ft.Dropdown(
            hint_text="Select period",
            options=[
                ft.dropdown.Option("7", "Last 7 days"),
                ft.dropdown.Option("14", "Last 14 days"),
                ft.dropdown.Option("30", "Last 30 days"),
            ],
            value="7",
            border_color=S.PRIMARY,
            text_style=ft.TextStyle(color=S.TEXT_PRIMARY),
            bgcolor=S.CARD,
            border_radius=S.RADIUS_SMALL,
            height=56
        )
        
        self.analyze_btn = ft.Container(
            content=ft.Row([
                ft.Icon(ft.Icons.ANALYTICS, color=S.TEXT_PRIMARY, size=20),
                ft.Text("Analyze", style=ft.TextStyle(size=16, weight=ft.FontWeight.W_600, color=S.TEXT_PRIMARY))
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=8),
            gradient=S.GRADIENT_PRIMARY,
            padding=ft.padding.symmetric(24, 16),
            border_radius=S.RADIUS_SMALL,
            on_click=self._analyze_historical,
            ink=True,
            height=56
        )
        
        # Results display
        self.results_container = ft.Column([], spacing=24)
    
    def _build_layout(self):
        """Build layout"""
        self.controls = [
            ft.Stack([
                ft.Column([
                    self.navbar,
                    
                    ft.Container(
                        content=ft.Column([
                            # Header
                            ft.Container(
                                content=ft.Column([
                                    ft.Text("Historical Trends", style=S.TITLE, text_align=ft.TextAlign.CENTER),
                                    ft.Text("Analyze air quality trends over time", style=S.BODY, text_align=ft.TextAlign.CENTER, color=S.TEXT_MUTED),
                                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                                padding=ft.padding.symmetric(32, 40)
                            ),
                            
                            # Search Section
                            ft.Container(
                                content=ft.ResponsiveRow([
                                    ft.Container(self.city_input, col={"sm": 12, "md": 5}),
                                    ft.Container(self.days_dropdown, col={"sm": 12, "md": 4}),
                                    ft.Container(self.analyze_btn, col={"sm": 12, "md": 3}),
                                ], spacing=16),
                                padding=ft.padding.symmetric(32, 0)
                            ),
                            
                            # Results
                            ft.Container(
                                content=self.results_container,
                                padding=32
                            ),
                        ], spacing=0),
                        expand=True
                    )
                ], spacing=0),
                self.loading
            ], expand=True)
        ]
    
    def _analyze_historical(self, e):
        """Analyze historical data"""
        city = self.city_input.value.strip()
        days = int(self.days_dropdown.value)
        
        if not city:
            self._show_snackbar("Please enter a city name", S.ERROR)
            return
        
        self.loading.show()
        
        try:
            analysis = self.analyzer.get_trend_analysis(city, days)
            if analysis:
                self._display_results(analysis, city, days)
            else:
                self._show_snackbar(f"No historical data found for {city}", S.ERROR)
        except Exception as ex:
            self._show_snackbar(f"Error: {str(ex)}", S.ERROR)
        finally:
            self.loading.hide()
    
    def _display_results(self, analysis, city: str, days: int):
        """Display historical analysis results"""
        self.results_container.controls.clear()
        
        # Summary Card
        trend_icon = ft.Icons.TRENDING_UP if analysis['trend'] == 'improving' else ft.Icons.TRENDING_DOWN
        trend_color = S.SUCCESS if analysis['trend'] == 'improving' else S.ERROR
        
        self.results_container.controls.append(
            S.gradient_card(
                ft.Column([
                    ft.Text(f"{city.title()} - {days} Day Analysis", style=S.H2, text_align=ft.TextAlign.CENTER),
                    ft.Container(height=16),
                    ft.Row([
                        ft.Column([
                            ft.Text("Average AQI", style=S.CAPTION),
                            ft.Text(str(analysis['avg_aqi']), style=S.H1, color=S.get_aqi_color(analysis['avg_aqi'])),
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, expand=True),
                        ft.Column([
                            ft.Text("Trend", style=S.CAPTION),
                            ft.Row([
                                ft.Icon(trend_icon, color=trend_color, size=32),
                                ft.Text(analysis['trend'].title(), style=S.H3, color=trend_color),
                            ], spacing=8),
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, expand=True),
                    ]),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=8),
                gradient=S.GRADIENT_DARK,
                padding=32
            )
        )
        
        # Statistics Grid
        stats_row = ft.ResponsiveRow([
            ft.Container(
                S.card(
                    ft.Column([
                        ft.Icon(ft.Icons.ARROW_UPWARD, color=S.ERROR, size=32),
                        ft.Text("Maximum AQI", style=S.CAPTION),
                        ft.Text(str(analysis['max_aqi']), style=S.H2),
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=8),
                    padding=24
                ),
                col={"sm": 12, "md": 4}
            ),
            ft.Container(
                S.card(
                    ft.Column([
                        ft.Icon(ft.Icons.ARROW_DOWNWARD, color=S.SUCCESS, size=32),
                        ft.Text("Minimum AQI", style=S.CAPTION),
                        ft.Text(str(analysis['min_aqi']), style=S.H2),
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=8),
                    padding=24
                ),
                col={"sm": 12, "md": 4}
            ),
            ft.Container(
                S.card(
                    ft.Column([
                        ft.Icon(ft.Icons.TRENDING_FLAT, color=S.INFO, size=32),
                        ft.Text("Data Points", style=S.CAPTION),
                        ft.Text(str(len(analysis.get('daily_data', []))), style=S.H2),
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=8),
                    padding=24
                ),
                col={"sm": 12, "md": 4}
            ),
        ], spacing=16)
        
        self.results_container.controls.append(stats_row)
        
        # Daily Breakdown
        if 'daily_data' in analysis and analysis['daily_data']:
            daily_card = S.card(
                ft.Column([
                    ft.Text("Daily Breakdown", style=S.H3),
                    ft.Divider(color=S.TEXT_DISABLED),
                    ft.Column([
                        self._daily_row(day['date'], day['aqi'])
                        for day in analysis['daily_data'][:10]  # Show last 10 days
                    ], spacing=8)
                ], spacing=16),
                padding=24,
                elevated=True
            )
            self.results_container.controls.append(daily_card)
        
        # Dominant Pollutants
        if 'pollutant_trends' in analysis:
            pollutant_card = S.card(
                ft.Column([
                    ft.Text("Pollutant Trends", style=S.H3),
                    ft.Divider(color=S.TEXT_DISABLED),
                    ft.Column([
                        self._pollutant_row(name, data)
                        for name, data in analysis['pollutant_trends'].items()
                    ], spacing=12)
                ], spacing=16),
                padding=24,
                elevated=True
            )
            self.results_container.controls.append(pollutant_card)
        
        self.page.update()
    
    def _daily_row(self, date: str, aqi: int):
        """Create daily data row"""
        return ft.Container(
            content=ft.Row([
                ft.Text(date, style=S.BODY, expand=True),
                ft.Container(
                    content=ft.Text(str(aqi), style=ft.TextStyle(size=14, weight=ft.FontWeight.BOLD, color=S.TEXT_PRIMARY)),
                    bgcolor=S.get_aqi_color(aqi),
                    padding=ft.padding.symmetric(12, 8),
                    border_radius=S.RADIUS_SMALL
                )
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            bgcolor=S.CARD_SOFT,
            padding=12,
            border_radius=S.RADIUS_SMALL
        )
    
    def _pollutant_row(self, name: str, data: dict):
        """Create pollutant trend row"""
        avg = data.get('avg', 0)
        trend = data.get('trend', 'stable')
        trend_icon = ft.Icons.TRENDING_UP if trend == 'increasing' else ft.Icons.TRENDING_DOWN if trend == 'decreasing' else ft.Icons.TRENDING_FLAT
        trend_color = S.ERROR if trend == 'increasing' else S.SUCCESS if trend == 'decreasing' else S.INFO
        
        return ft.Container(
            content=ft.Row([
                ft.Text(name, style=S.BODY, expand=True),
                ft.Text(f"{avg:.1f} µg/m³", style=S.CAPTION),
                ft.Icon(trend_icon, color=trend_color, size=20)
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            bgcolor=S.CARD_SOFT,
            padding=16,
            border_radius=S.RADIUS_SMALL
        )
    
    def _show_snackbar(self, message: str, color: str):
        """Show snackbar"""
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text(message, color=S.TEXT_PRIMARY),
            bgcolor=color
        )
        self.page.snack_bar.open = True
        self.page.update()