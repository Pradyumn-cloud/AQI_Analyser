import flet as ft
from typing import Any
from Backend_core.fetcher import AQIFetcher
from Backend_core.analysis import AQIAnalysis
from Backend_core.config import API_URL, API_KEY
from assets import styles as S
from ui.components import NavBar, SearchBar, AQICard, MetricGrid, PollutantCard, StationCard, InfoSection, LoadingOverlay

class HomeView(ft.View):
    """Professional Home Dashboard"""
    
    def __init__(self, page: ft.Page):
        super().__init__(
            route="/",
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
        """Initialize all components"""
        self.navbar = NavBar(self.page)
        self.search_bar = SearchBar(self._search_aqi)
        self.loading = LoadingOverlay()
        
        # Main display components
        self.aqi_card = AQICard()
        self.metrics = MetricGrid()
        
        # Sections
        self.pollutants_section = InfoSection("Pollutant Analysis", ft.Icons.SCIENCE, S.PRIMARY)
        self.stations_section = InfoSection("Monitoring Stations", ft.Icons.LOCATION_ON, S.ACCENT)
        self.recommendations_section = InfoSection("Health Recommendations", ft.Icons.HEALTH_AND_SAFETY, S.SUCCESS)

    def _build_layout(self):
        """Build the complete layout"""
        self.controls = [
            ft.Stack([
                ft.Column([
                    # Navigation
                    self.navbar,
                    
                    # Main Content
                    ft.Container(
                        content=ft.Column([
                            # Hero Section
                            ft.Container(
                                content=ft.Column([
                                    ft.Text("Air Quality Monitoring", style=S.TITLE, text_align=ft.TextAlign.CENTER),
                                    ft.Text("Real-time AQI data for Indian cities", style=S.BODY, text_align=ft.TextAlign.CENTER, color=S.TEXT_MUTED),
                                    ft.Container(height=24),
                                    self.search_bar,
                                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                                padding=ft.padding.symmetric(32, 40)
                            ),
                            
                            # AQI Display
                            ft.Container(
                                content=self.aqi_card,
                                padding=ft.padding.symmetric(32, 0)
                            ),
                            
                            # Metrics Grid
                            ft.Container(
                                content=self.metrics,
                                padding=ft.padding.symmetric(32, 16)
                            ),
                            
                            # Detailed Sections
                            # Detailed sections are not rendered in the main layout by default.
                            # They will be inserted into the AQI card after a successful search.
                            
                            # Quick Actions
                            ft.Container(
                                content=ft.Column([
                                    ft.Text("Quick Actions", style=S.H3, text_align=ft.TextAlign.CENTER),
                                    ft.Container(height=16),
                                    ft.ResponsiveRow([
                                        ft.Container(
                                            self._action_card("Historical Trends", "View past AQI data", ft.Icons.TIMELINE, S.GRADIENT_PRIMARY, "/historical"),
                                            col={"sm": 12, "md": 6}
                                        ),
                                        ft.Container(
                                            self._action_card("Compare Cities", "Compare air quality", ft.Icons.COMPARE_ARROWS, S.GRADIENT_ACCENT, "/compare"),
                                            col={"sm": 12, "md": 6}
                                        ),
                                    ], spacing=16)
                                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                                padding=ft.padding.symmetric(32, 32)
                            )
                        ], spacing=0),
                        expand=True
                    )
                ], spacing=0),
                self.loading
            ], expand=True)
        ]
    
    def _action_card(self, title: str, description: str, icon: str, gradient: Any, route: str):
        """Create action card"""
        return ft.Container(
            content=ft.Column([
                ft.Icon(icon, color=S.TEXT_PRIMARY, size=40),
                ft.Container(height=12),
                ft.Text(title, style=S.H3, text_align=ft.TextAlign.CENTER),
                ft.Text(description, style=S.CAPTION, text_align=ft.TextAlign.CENTER),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=8),
            gradient=gradient,
            padding=32,
            border_radius=S.RADIUS,
            on_click=lambda _: self.page.go(route),
            ink=True,
            shadow=S.SHADOW_GLOW
        )
    
    def _search_aqi(self, e):
        """Search for city AQI"""
        city = self.search_bar.input.value.strip()
        if not city:
            self._show_snackbar("Please enter a city name", S.ERROR)
            return
        
        self.loading.show()
        
        try:
            summary = self.fetcher.get_comprehensive_aqi_data(city)
            if summary:
                analysis = self.analyser.get_comprehensive_analysis(summary)
                self._display_results(analysis, summary)
            else:
                # Show user-facing message
                print(f"HomeView: No data found for {city}; invoking show_not_found()")
                self._show_snackbar(f"No data found for {city}", S.ERROR)

                # Show AQI card 'no data' placeholder and clear other UI lists
                try:
                    self.aqi_card.show_not_found(city)
                    print("HomeView: called aqi_card.show_not_found")
                    self.metrics.clear()
                    self.pollutants_section.clear()
                    self.stations_section.clear()
                    self.recommendations_section.clear()
                    self.page.update()
                    print("HomeView: page.update() called after no-data handling")
                except Exception as ex:
                    print(f"HomeView: exception while showing not-found: {ex}")
                    self.page.update()
        except Exception as ex:
            self._show_snackbar(f"Error: {str(ex)}", S.ERROR)
        finally:
            self.loading.hide()
    
    def _display_results(self, analysis, summary):
        msg = "HomeView._display_results: entering"
        print(msg)
        try:
            with open(r".\app\debug_ui.log", "a", encoding="utf-8") as fh:
                fh.write(msg + "\n")
        except Exception:
            pass
        try:
            aqi = analysis['overall_aqi']
            
            # Update main AQI display
            self.aqi_card.update_data(
                aqi,
                analysis['level'],
                summary.city.get_name(),
                "Just now"
            )
        except Exception as ex:
            print(f"HomeView._display_results: ERROR while updating AQI card: {ex}")
            # still attempt to show a minimal summary and bail out
            try:
                self.aqi_card.set_summary(f"AQI: {analysis.get('overall_aqi', 'N/A')}")
            except Exception:
                pass
            raise
        
        # Update metrics
        self.metrics.clear()
        self.metrics.add_metric("Dominant Pollutant", analysis['dominant_pollutant'], ft.Icons.WARNING, S.ERROR)
        self.metrics.add_metric("Active Stations", str(len(summary.stations)), ft.Icons.SENSORS, S.INFO)
        self.metrics.add_metric("Air Quality", analysis['level'], ft.Icons.AIR, S.get_aqi_color(aqi))
        
        # Update pollutants
        self.pollutants_section.clear()
        dominant = analysis['dominant_pollutant']
        for pollutant, data in analysis['pollutant_breakdown'].items():
            self.pollutants_section.add_item(
                PollutantCard(pollutant, data['avg'], is_dominant=(pollutant == dominant))
            )
        
        # Update stations
        self.stations_section.clear()
        for station_data in analysis['station_comparison'][:5]:
            self.stations_section.add_item(
                StationCard(station_data['station'], station_data['score'])
            )
        
        # Update recommendations
        self.recommendations_section.clear()
        for rec in analysis['recommendations']:
            self.recommendations_section.add_item(
                ft.Row([
                    ft.Icon(ft.Icons.CHECK_CIRCLE, color=S.SUCCESS, size=20),
                    ft.Text(rec, style=S.BODY, expand=True)
                ], spacing=12)
            )

        # debug: print counts of items prepared for each section
        try:
            p_count = len(self.pollutants_section.content_column.controls)
            s_count = len(self.stations_section.content_column.controls)
            r_count = len(self.recommendations_section.content_column.controls)
            print(f"HomeView._display_results: prepared items -> pollutants={p_count}, stations={s_count}, recs={r_count}")
        except Exception as ex:
            print(f"HomeView._display_results: debug error counting items: {ex}")

        # Place the three sections into the AQI card details area so they appear
        # inside the rounded AQI card together.
        # Build compact, fresh containers for the in-card display. Using
        # simple containers avoids control reuse/mounting issues and keeps the
        # AQI card layout predictable.
        p_items = [
            ft.Text("Pollutant Analysis", style=S.H3),
            ft.Container(height=8)
        ]
        for c in list(self.pollutants_section.content_column.controls):
            p_items.append(c)

        p_container = ft.Container(
            content=ft.Column(p_items, spacing=8),
            bgcolor=S.CARD,
            padding=16,
            border_radius=S.RADIUS
        )

        s_items = [
            ft.Text("Monitoring Stations", style=S.H3),
            ft.Container(height=8)
        ]
        for c in list(self.stations_section.content_column.controls):
            s_items.append(c)

        s_container = ft.Container(
            content=ft.Column(s_items, spacing=8),
            bgcolor=S.CARD,
            padding=16,
            border_radius=S.RADIUS
        )

        r_items = [
            ft.Text("Health Recommendations", style=S.H3),
            ft.Container(height=8)
        ]
        for c in list(self.recommendations_section.content_column.controls):
            r_items.append(c)

        r_container = ft.Container(
            content=ft.Column(r_items, spacing=8),
            bgcolor=S.CARD,
            padding=16,
            border_radius=S.RADIUS
        )

        # set a short summary text as an immediate visual cue
        try:
            summary_line = f"Dominant: {analysis.get('dominant_pollutant', 'N/A')} · Stations: {len(summary.stations)} · AQI: {analysis.get('overall_aqi', '')}"
            self.aqi_card.set_summary(summary_line)
        except Exception:
            pass

        self.aqi_card.set_details([p_container, s_container, r_container])

        self.page.update()
    
    def _show_snackbar(self, message: str, color: str):
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text(message, color=S.TEXT_PRIMARY),
            bgcolor=color
        )
        self.page.snack_bar.open = True
        self.page.update()