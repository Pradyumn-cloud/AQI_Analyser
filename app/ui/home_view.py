import flet as ft
from Backend_core.fetcher import AQIFetcher
from Backend_core.analysis import AQIAnalysis
from Backend_core.config import API_URL, API_KEY

class HomeView(ft.View):
    """Enhanced home view with comprehensive AQI display."""
    
    def __init__(self, page: ft.Page):
        super().__init__(
            route="/",
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            vertical_alignment=ft.MainAxisAlignment.START,
            scroll=ft.ScrollMode.AUTO,  # Enable scrolling
            padding=ft.padding.all(20)
        )
        self.page = page
        self.fetcher = AQIFetcher(API_URL, API_KEY)
        self.analyser = AQIAnalysis()
        
        # Initialize UI components
        self._init_search_components()
        self._init_display_components()
        self._init_layout()
    
    def _get_aqi_color_scheme(self, aqi_value: int) -> dict:
        """Get proper color scheme based on AQI value."""
        if aqi_value <= 50:
            return {
                'primary': ft.Colors.GREEN_700,
                'background': ft.Colors.GREEN_50,
                'accent': ft.Colors.GREEN_100
            }
        elif aqi_value <= 100:
            return {
                'primary': ft.Colors.YELLOW_700,
                'background': ft.Colors.YELLOW_50,
                'accent': ft.Colors.YELLOW_100
            }
        elif aqi_value <= 150:
            return {
                'primary': ft.Colors.ORANGE_700,
                'background': ft.Colors.ORANGE_50,
                'accent': ft.Colors.ORANGE_100
            }
        elif aqi_value <= 200:
            return {
                'primary': ft.Colors.RED_700,
                'background': ft.Colors.RED_50,
                'accent': ft.Colors.RED_100
            }
        elif aqi_value <= 300:
            return {
                'primary': ft.Colors.PURPLE_700,
                'background': ft.Colors.PURPLE_50,
                'accent': ft.Colors.PURPLE_100
            }
        else:
            return {
                'primary': ft.Colors.BROWN_700,
                'background': ft.Colors.BROWN_50,
                'accent': ft.Colors.BROWN_100
            }
    
    def _init_search_components(self):
        """Initialize search-related UI components."""
        self.city_input = ft.TextField(
            label="Enter City Name",
            width=300,
            border_radius=12,
            border_color=ft.Colors.BLUE_400,
            focused_border_color=ft.Colors.BLUE_600,
            text_align=ft.TextAlign.LEFT,
            prefix_icon=ft.Icons.LOCATION_CITY,
            bgcolor=ft.Colors.WHITE,
            color=ft.Colors.BLACK87,
            hint_text="e.g., Delhi, Mumbai, Bangalore"
        )
        
        self.search_button = ft.ElevatedButton(
            text="Analyze Air Quality",
            on_click=self.get_comprehensive_aqi_data,
            icon=ft.Icons.SEARCH,
            color=ft.Colors.WHITE,
            bgcolor=ft.Colors.BLUE_600,
            elevation=4,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=10),
                bgcolor={
                    ft.ControlState.HOVERED: ft.Colors.BLUE_700,
                    ft.ControlState.PRESSED: ft.Colors.BLUE_800,
                }
            )
        )
        
        # Add Home button
        self.home_button = ft.ElevatedButton(
            text="🏠 Home",
            on_click=self._go_to_home,
            icon=ft.Icons.HOME,
            color=ft.Colors.WHITE,
            bgcolor=ft.Colors.BLUE_500,
            elevation=2,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=8),
                bgcolor={
                    ft.ControlState.HOVERED: ft.Colors.BLUE_600,
                }
            )
        )
        
        self.progress_indicator = ft.ProgressRing(
            visible=False,
            width=40,
            height=40,
            color=ft.Colors.BLUE_600,
            stroke_width=4
        )
    
    def _go_to_home(self, e):
        """Navigate to home (refresh current view)."""
        # Clear all data and reset to initial state
        self._reset_view()
        self.page.update()
    
    def _reset_view(self):
        """Reset the view to initial state."""
        # Hide all result cards
        self.aqi_card.visible = False
        self.status_card.visible = False
        self.pollutant_container.visible = False
        self.stations_container.visible = False
        self.recommendations_container.visible = False
        self.error_display.visible = False
        
        # Clear input field
        self.city_input.value = ""
        
        # Reset card contents to initial state
        self.aqi_card.content.content.controls[1].value = "--"
        self.aqi_card.content.content.controls[1].color = ft.Colors.GREY_800
        self.aqi_card.content.content.controls[2].value = "Select a city to begin"
        self.aqi_card.content.bgcolor = ft.Colors.WHITE
        self.aqi_card.content.border = ft.border.all(1, ft.Colors.GREY_200)
        
        self.status_card.content.content.controls[1].value = "--"
        self.status_card.content.content.controls[1].color = ft.Colors.GREY_800
        self.status_card.content.content.controls[4].value = "--"
        self.status_card.content.bgcolor = ft.Colors.WHITE
        self.status_card.content.border = ft.border.all(1, ft.Colors.GREY_200)
    
    def _init_display_components(self):
        """Initialize data display components."""
        # Main AQI Display
        self.aqi_card = ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Text("AQI", size=18, weight=ft.FontWeight.W_600, color=ft.Colors.GREY_700),
                    ft.Text("--", size=52, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_800),
                    ft.Text("Select a city to begin", size=14, color=ft.Colors.GREY_600)
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=5),
                padding=25,
                border_radius=15,
                bgcolor=ft.Colors.WHITE,
                border=ft.border.all(1, ft.Colors.GREY_200)
            ),
            elevation=6,
            visible=False,
            margin=ft.margin.all(5)
        )
        
        # Status and Health Impact
        self.status_card = ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Text("Air Quality Level", size=16, weight=ft.FontWeight.W_600, color=ft.Colors.GREY_700),
                    ft.Text("--", size=22, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_800),
                    ft.Divider(height=10, color=ft.Colors.GREY_300),
                    ft.Text("Health Impact:", size=13, weight=ft.FontWeight.W_500, color=ft.Colors.GREY_600),
                    ft.Text("--", size=12, color=ft.Colors.GREY_700)
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=3),
                padding=20,
                border_radius=15,
                bgcolor=ft.Colors.WHITE,
                border=ft.border.all(1, ft.Colors.GREY_200)
            ),
            elevation=4,
            visible=False,
            margin=ft.margin.all(5)
        )
        
        # Pollutant Breakdown
        self.pollutant_container = ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Text("Pollutant Breakdown", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_700),
                    ft.Text("No data available", size=14, color=ft.Colors.GREY_600)
                ], spacing=10),
                padding=20,
                border_radius=12,
                bgcolor=ft.Colors.BLUE_50,
                border=ft.border.all(1, ft.Colors.BLUE_100)
            ),
            elevation=3,
            visible=False,
            margin=ft.margin.symmetric(vertical=5)
        )
        
        # Station Information
        self.stations_container = ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Text("Monitoring Stations", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN_700),
                    ft.Text("No stations found", size=14, color=ft.Colors.GREY_600)
                ], spacing=10),
                padding=20,
                border_radius=12,
                bgcolor=ft.Colors.GREEN_50,
                border=ft.border.all(1, ft.Colors.GREEN_100)
            ),
            elevation=3,
            visible=False,
            margin=ft.margin.symmetric(vertical=5)
        )
        
        # Recommendations
        self.recommendations_container = ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Text("Health Recommendations", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.ORANGE_700),
                    ft.Text("Enter a city to get recommendations", size=14, color=ft.Colors.GREY_600)
                ], spacing=10),
                padding=20,
                border_radius=12,
                bgcolor=ft.Colors.ORANGE_50,
                border=ft.border.all(1, ft.Colors.ORANGE_100)
            ),
            elevation=3,
            visible=False,
            margin=ft.margin.symmetric(vertical=5)
        )
        
        # Error display
        self.error_display = ft.Container(
            content=ft.Text(
                "", 
                color=ft.Colors.RED_700,
                size=14,
                weight=ft.FontWeight.W_500
            ),
            visible=False,
            padding=10,
            border_radius=8,
            bgcolor=ft.Colors.RED_50,
            border=ft.border.all(1, ft.Colors.RED_200),
            margin=ft.margin.symmetric(vertical=5)
        )
    
    def _init_layout(self):
        """Initialize the overall layout with proper scrolling."""
        self.controls = [
            ft.Column([
                # Header Section with Home Button
                ft.Container(
                    content=ft.Column([
                        # Home button in top right
                        ft.Row([
                            ft.Container(expand=True),  # Spacer
                            self.home_button
                        ], alignment=ft.MainAxisAlignment.END),
                        
                        ft.Container(height=10),
                        ft.Text(
                            "🌍 AQI Analyzer Pro", 
                            size=32, 
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.BLUE_800,
                            text_align=ft.TextAlign.CENTER
                        ),
                        ft.Text(
                            "Professional Air Quality Monitoring", 
                            size=16, 
                            color=ft.Colors.GREY_600,
                            text_align=ft.TextAlign.CENTER
                        ),
                        ft.Text(
                            "Powered by Data.gov.in", 
                            size=12, 
                            color=ft.Colors.GREY_500,
                            text_align=ft.TextAlign.CENTER,
                            style=ft.TextStyle(italic=True)
                        ),
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    padding=ft.padding.symmetric(vertical=20),
                ),
                
                # Search Section
                ft.Container(
                    content=ft.Column([
                        ft.Row([
                            self.city_input,
                            self.search_button
                        ], alignment=ft.MainAxisAlignment.CENTER, spacing=15),
                        ft.Container(height=15),
                        self.progress_indicator,
                        self.error_display,
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    padding=ft.padding.symmetric(vertical=10)
                ),
                
                # Main Display Section
                ft.Container(
                    content=ft.ResponsiveRow([
                        ft.Container(
                            content=self.aqi_card,
                            col={"sm": 12, "md": 6, "lg": 6}
                        ),
                        ft.Container(
                            content=self.status_card,
                            col={"sm": 12, "md": 6, "lg": 6}
                        )
                    ]),
                    padding=ft.padding.symmetric(vertical=15)
                ),
                
                # Detailed Information Section
                ft.Container(
                    content=ft.Column([
                        self.pollutant_container,
                        self.stations_container,
                        self.recommendations_container,
                    ], spacing=15),
                    padding=ft.padding.symmetric(vertical=10)
                ),
                
                # Navigation Section
                ft.Container(
                    content=ft.Row([
                        ft.ElevatedButton(
                            "📊 Historical Analysis", 
                            on_click=lambda _: self.page.go("/historical"),
                            bgcolor=ft.Colors.GREEN_600,
                            color=ft.Colors.WHITE,
                            elevation=3,
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=10),
                                bgcolor={
                                    ft.ControlState.HOVERED: ft.Colors.GREEN_700,
                                }
                            )
                        ),
                        ft.ElevatedButton(
                            "🔄 Compare Cities", 
                            on_click=lambda _: self.page.go("/compare"),
                            bgcolor=ft.Colors.PURPLE_600,
                            color=ft.Colors.WHITE,
                            elevation=3,
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=10),
                                bgcolor={
                                    ft.ControlState.HOVERED: ft.Colors.PURPLE_700,
                                }
                            )
                        ),
                    ], alignment=ft.MainAxisAlignment.CENTER, spacing=25),
                    padding=ft.padding.symmetric(vertical=30)
                ),
                
                # Bottom spacing
                ft.Container(height=30)
                
            ], spacing=0, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        ]
    
    def get_comprehensive_aqi_data(self, e):
        """Enhanced data fetching with comprehensive analysis."""
        city = self.city_input.value.strip()
        if not city:
            self._show_error("Please enter a city name")
            return
        
        self._show_loading(True)
        self._hide_error()
        
        try:
            # Get comprehensive data
            summary = self.fetcher.get_comprehensive_aqi_data(city)
            if summary:
                analysis = self.analyser.get_comprehensive_analysis(summary)
                self._display_comprehensive_results(analysis, summary)
            else:
                self._show_error(f"No data found for {city}. Try major Indian cities like Delhi, Mumbai, Bangalore.")
                
        except Exception as ex:
            self._show_error(f"Error: {str(ex)}")
        finally:
            self._show_loading(False)
    
    def _display_comprehensive_results(self, analysis, summary):
        """Display comprehensive analysis results with improved colors."""
        aqi_value = analysis['overall_aqi']
        color_scheme = self._get_aqi_color_scheme(aqi_value)
        
        # Update main AQI card
        self.aqi_card.content.content.controls[1].value = str(aqi_value)
        self.aqi_card.content.content.controls[1].color = color_scheme['primary']
        self.aqi_card.content.content.controls[2].value = analysis['level']
        self.aqi_card.content.bgcolor = color_scheme['background']
        self.aqi_card.content.border = ft.border.all(2, color_scheme['primary'])
        self.aqi_card.visible = True
        
        # Update status card
        self.status_card.content.content.controls[1].value = analysis['level']
        self.status_card.content.content.controls[1].color = color_scheme['primary']
        self.status_card.content.content.controls[4].value = analysis['health_impact']
        self.status_card.content.bgcolor = color_scheme['background']
        self.status_card.content.border = ft.border.all(2, color_scheme['accent'])
        self.status_card.visible = True
        
        # Update pollutant breakdown
        self._update_pollutant_breakdown(analysis['pollutant_breakdown'], analysis['dominant_pollutant'])
        
        # Update stations info
        self._update_stations_info(summary.stations, analysis['station_comparison'])
        
        # Update recommendations
        self._update_recommendations(analysis['recommendations'])
        
        self.page.update()
    
    def _update_pollutant_breakdown(self, breakdown, dominant):
        """Update pollutant breakdown display with better colors."""
        pollutant_controls = [
            ft.Text("Pollutant Breakdown", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_800),
            ft.Container(
                content=ft.Text(f"🎯 Dominant: {dominant}", size=16, weight=ft.FontWeight.W_600, color=ft.Colors.WHITE),
                bgcolor=ft.Colors.RED_600,
                padding=8,
                border_radius=6,
                margin=ft.margin.symmetric(vertical=5)
            )
        ]
        
        for pollutant, data in breakdown.items():
            is_dominant = pollutant == dominant
            bg_color = ft.Colors.RED_100 if is_dominant else ft.Colors.BLUE_50
            text_color = ft.Colors.RED_800 if is_dominant else ft.Colors.BLUE_800
            
            pollutant_controls.append(
                ft.Container(
                    content=ft.Row([
                        ft.Text(f"{pollutant}:", size=14, weight=ft.FontWeight.W_600, color=text_color),
                        ft.Text(f"{data['avg']:.1f} μg/m³", size=14, weight=ft.FontWeight.W_500, color=text_color)
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    bgcolor=bg_color,
                    padding=10,
                    border_radius=8,
                    border=ft.border.all(1, ft.Colors.RED_300 if is_dominant else ft.Colors.BLUE_200),
                    margin=ft.margin.symmetric(vertical=2)
                )
            )
        
        self.pollutant_container.content.content.controls = pollutant_controls
        self.pollutant_container.visible = True
    
    def _update_stations_info(self, stations, comparison):
        """Update monitoring stations information with better colors."""
        station_controls = [
            ft.Text("Monitoring Stations", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN_800),
            ft.Container(
                content=ft.Text(f"📍 {len(stations)} active stations", size=16, weight=ft.FontWeight.W_600, color=ft.Colors.WHITE),
                bgcolor=ft.Colors.GREEN_600,
                padding=8,
                border_radius=6,
                margin=ft.margin.symmetric(vertical=5)
            )
        ]
        
        for station_data in comparison[:3]:  # Show top 3 stations
            score = station_data['score']
            if score < 50:
                quality_text = "🟢 Clean"
                bg_color = ft.Colors.GREEN_100
                border_color = ft.Colors.GREEN_300
                text_color = ft.Colors.GREEN_800
            elif score < 100:
                quality_text = "🟡 Moderate"
                bg_color = ft.Colors.YELLOW_100
                border_color = ft.Colors.YELLOW_300
                text_color = ft.Colors.YELLOW_800
            else:
                quality_text = "🔴 Poor"
                bg_color = ft.Colors.RED_100
                border_color = ft.Colors.RED_300
                text_color = ft.Colors.RED_800
            
            station_controls.append(
                ft.Container(
                    content=ft.Text(f"{station_data['station']}: {quality_text}", size=13, weight=ft.FontWeight.W_500, color=text_color),
                    bgcolor=bg_color,
                    padding=8,
                    border_radius=6,
                    border=ft.border.all(1, border_color),
                    margin=ft.margin.symmetric(vertical=2)
                )
            )
        
        self.stations_container.content.content.controls = station_controls
        self.stations_container.visible = True
    
    def _update_recommendations(self, recommendations):
        """Update health recommendations with better colors."""
        rec_controls = [
            ft.Text("Health Recommendations", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.ORANGE_800)
        ]
        
        for i, rec in enumerate(recommendations[:4]):  # Show top 4 recommendations
            if i < 2:
                icon = "✅"
                bg_color = ft.Colors.GREEN_100
                border_color = ft.Colors.GREEN_300
                text_color = ft.Colors.GREEN_800
            else:
                icon = "⚠️"
                bg_color = ft.Colors.ORANGE_100
                border_color = ft.Colors.ORANGE_300
                text_color = ft.Colors.ORANGE_800
            
            rec_controls.append(
                ft.Container(
                    content=ft.Text(f"{icon} {rec}", size=13, weight=ft.FontWeight.W_500, color=text_color),
                    bgcolor=bg_color,
                    padding=10,
                    border_radius=6,
                    border=ft.border.all(1, border_color),
                    margin=ft.margin.symmetric(vertical=2)
                )
            )
        
        self.recommendations_container.content.content.controls = rec_controls
        self.recommendations_container.visible = True
    
    def _show_loading(self, show: bool):
        """Show/hide loading indicator."""
        self.progress_indicator.visible = show
        self.search_button.disabled = show
        self.page.update()
    
    def _show_error(self, message: str):
        """Display error message with better styling."""
        self.error_display.content.value = f"❌ {message}"
        self.error_display.visible = True
        self.page.update()
    
    def _hide_error(self):
        """Hide error message."""
        self.error_display.visible = False
        self.page.update()