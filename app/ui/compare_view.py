import flet as ft
from typing import Any
from Backend_core.fetcher import AQIFetcher
from Backend_core.analysis import AQIAnalysis
from Backend_core.config import API_URL, API_KEY
from assets import styles as S
from ui.components import NavBar, SearchBar, LoadingOverlay, StationCard

class CompareView(ft.View):
    """Professional City Comparison View"""
    
    def __init__(self, page: ft.Page):
        super().__init__(
            route="/compare",
            padding=0,
            scroll=ft.ScrollMode.AUTO,
            bgcolor=S.BG
        )
        self.page = page
        self.fetcher = AQIFetcher(API_URL, API_KEY)
        self.analyser = AQIAnalysis()
        
        self._init_components()
        self._build_layout()
    
    def _init_components(self):
        """Initialize components"""
        self.navbar = NavBar(self.page, "Compare Cities")
        self.loading = LoadingOverlay()
        
        # City inputs
        self.city1_input = ft.TextField(
            hint_text="First city",
            border_color=S.PRIMARY,
            text_style=ft.TextStyle(color=S.TEXT_PRIMARY),
            hint_style=ft.TextStyle(color=S.TEXT_MUTED),
            bgcolor=S.CARD,
            border_radius=S.RADIUS_SMALL,
            prefix_icon=ft.Icons.LOCATION_CITY,
            height=56
        )
        
        self.city2_input = ft.TextField(
            hint_text="Second city",
            border_color=S.ACCENT,
            text_style=ft.TextStyle(color=S.TEXT_PRIMARY),
            hint_style=ft.TextStyle(color=S.TEXT_MUTED),
            bgcolor=S.CARD,
            border_radius=S.RADIUS_SMALL,
            prefix_icon=ft.Icons.LOCATION_CITY,
            height=56
        )
        
        self.compare_btn = ft.Container(
            content=ft.Row([
                ft.Icon(ft.Icons.COMPARE_ARROWS, color=S.TEXT_PRIMARY, size=20),
                ft.Text("Compare", style=ft.TextStyle(size=16, weight=ft.FontWeight.W_600, color=S.TEXT_PRIMARY))
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=8),
            gradient=S.GRADIENT_PRIMARY,
            padding=ft.padding.symmetric(32, 16),
            border_radius=S.RADIUS_SMALL,
            on_click=self._compare_cities,
            ink=True,
            height=56
        )
        
        # Comparison display
        self.city1_column = ft.Column([], spacing=16)
        self.city2_column = ft.Column([], spacing=16)
        self.comparison_result = ft.Container()
    
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
                                    ft.Text("Compare Air Quality", style=S.TITLE, text_align=ft.TextAlign.CENTER),
                                    ft.Text("Compare AQI between two Indian cities", style=S.BODY, text_align=ft.TextAlign.CENTER, color=S.TEXT_MUTED),
                                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                                padding=ft.padding.symmetric(32, 40)
                            ),
                            
                            # Input Section
                            ft.Container(
                                content=ft.ResponsiveRow([
                                    ft.Container(self.city1_input, col={"sm": 12, "md": 5}),
                                    ft.Container(
                                        content=ft.Icon(ft.Icons.COMPARE_ARROWS, color=S.PRIMARY, size=32),
                                        col={"sm": 12, "md": 2},
                                        alignment=ft.alignment.center
                                    ),
                                    ft.Container(self.city2_input, col={"sm": 12, "md": 5}),
                                ], spacing=16),
                                padding=ft.padding.symmetric(32, 0)
                            ),
                            
                            ft.Container(
                                content=self.compare_btn,
                                padding=ft.padding.symmetric(32, 16),
                                alignment=ft.alignment.center
                            ),
                            
                            # Results
                            ft.Container(
                                content=self.comparison_result,
                                padding=32
                            ),
                            
                            # Side by side comparison
                            ft.Container(
                                content=ft.ResponsiveRow([
                                    ft.Container(
                                        content=S.card(self.city1_column, padding=24, elevated=True),
                                        col={"sm": 12, "md": 6}
                                    ),
                                    ft.Container(
                                        content=S.card(self.city2_column, padding=24, elevated=True),
                                        col={"sm": 12, "md": 6}
                                    ),
                                ], spacing=24),
                                padding=32
                            ),
                        ], spacing=0),
                        expand=True
                    )
                ], spacing=0),
                self.loading
            ], expand=True)
        ]
    
    def _compare_cities(self, e):
        """Compare two cities"""
        city1 = self.city1_input.value.strip()
        city2 = self.city2_input.value.strip()
        
        if not city1 or not city2:
            self._show_snackbar("Please enter both city names", S.ERROR)
            return
        
        self.loading.show()
        
        try:
            # Fetch data for both cities
            summary1 = self.fetcher.get_comprehensive_aqi_data(city1)
            summary2 = self.fetcher.get_comprehensive_aqi_data(city2)
            
            if summary1 and summary2:
                analysis1 = self.analyser.get_comprehensive_analysis(summary1)
                analysis2 = self.analyser.get_comprehensive_analysis(summary2)
                self._display_comparison(analysis1, analysis2, summary1, summary2)
            else:
                self._show_snackbar("Data not found for one or both cities", S.ERROR)
        except Exception as ex:
            self._show_snackbar(f"Error: {str(ex)}", S.ERROR)
        finally:
            self.loading.hide()
    
    def _display_comparison(self, analysis1, analysis2, summary1, summary2):
        """Display comparison results"""
        aqi1 = analysis1['overall_aqi']
        aqi2 = analysis2['overall_aqi']
        
        # Winner card
        if aqi1 < aqi2:
            winner_name = summary1.city.get_name().title()
            winner_aqi = aqi1
            winner_color = S.get_aqi_color(aqi1)
            winner_text = f"{winner_name} has better air quality"
        else:
            winner_name = summary2.city.get_name().title()
            winner_aqi = aqi2
            winner_color = S.get_aqi_color(aqi2)
            winner_text = f"{winner_name} has better air quality"
        
        self.comparison_result.content = S.gradient_card(
            ft.Column([
                ft.Icon(ft.Icons.EMOJI_EVENTS, color=S.TEXT_PRIMARY, size=48),
                ft.Text(winner_text, style=S.H2, text_align=ft.TextAlign.CENTER),
                ft.Text(f"AQI: {winner_aqi}", style=S.BODY, text_align=ft.TextAlign.CENTER),
                ft.Text(f"Difference: {abs(aqi1 - aqi2)} points", style=S.CAPTION, text_align=ft.TextAlign.CENTER),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=12),
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=[winner_color, ft.Colors.with_opacity(0.6, winner_color)]
            ),
            padding=32
        )
        
        # City 1 details
        self._populate_city_column(self.city1_column, analysis1, summary1, S.PRIMARY)
        
        # City 2 details
        self._populate_city_column(self.city2_column, analysis2, summary2, S.ACCENT)
        
        self.page.update()
    
    def _populate_city_column(self, column: ft.Column, analysis, summary, color: str):
        """Populate city comparison column"""
        column.controls.clear()
        
        aqi = analysis['overall_aqi']
        
        # Header
        column.controls.append(
            ft.Container(
                content=ft.Column([
                    ft.Text(summary.city.get_name().title(), style=S.H2, text_align=ft.TextAlign.CENTER),
                    ft.Text(str(aqi), style=S.H1, text_align=ft.TextAlign.CENTER, color=S.get_aqi_color(aqi)),
                    ft.Text(analysis['level'], style=S.BODY, text_align=ft.TextAlign.CENTER),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=8),
                padding=16,
                bgcolor=S.CARD_ELEVATED,
                border_radius=S.RADIUS,
                border=ft.border.all(2, color)
            )
        )
        
        # Metrics
        column.controls.append(
            S.card(
                ft.Column([
                    ft.Text("Key Metrics", style=S.H3),
                    ft.Divider(color=S.TEXT_DISABLED),
                    self._metric_row("Dominant Pollutant", analysis['dominant_pollutant']),
                    self._metric_row("Active Stations", str(len(summary.stations))),
                    self._metric_row("Health Impact", analysis['health_impact'][:30]),
                ], spacing=12),
                padding=20
            )
        )
        
        # Top pollutants
        column.controls.append(
            S.card(
                ft.Column([
                    ft.Text("Top Pollutants", style=S.H3),
                    ft.Divider(color=S.TEXT_DISABLED),
                    *[self._metric_row(name, f"{data['avg']:.1f} µg/m³") 
                      for name, data in list(analysis['pollutant_breakdown'].items())[:3]]
                ], spacing=12),
                padding=20
            )
        )
    
    def _metric_row(self, label: str, value: str):
        """Create metric row"""
        return ft.Row([
            ft.Text(label, style=S.CAPTION, expand=True),
            ft.Text(value, style=ft.TextStyle(size=14, weight=ft.FontWeight.W_600, color=S.TEXT_PRIMARY))
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
    
    def _show_snackbar(self, message: str, color: str):
        """Show snackbar"""
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text(message, color=S.TEXT_PRIMARY),
            bgcolor=color
        )
        self.page.snack_bar.open = True
        self.page.update()