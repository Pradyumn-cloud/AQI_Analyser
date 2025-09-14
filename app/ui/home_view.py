import flet as ft
from Backend_core.fetcher import AQIFetcher
from Backend_core.analysis import AQIAnalysis
from Backend_core.config import API_URL, API_KEY

class HomeView(ft.View):
    """
    The main view of the application, showing real-time AQI data.
    It inherits from ft.View and defines the UI controls for the home screen.
    """
    def __init__(self, page: ft.Page):
        # Call the constructor of the parent class (ft.View)
        super().__init__(
            route="/",
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            vertical_alignment=ft.MainAxisAlignment.START
        )
        self.page = page
        self.fetcher = AQIFetcher(API_URL, API_KEY)
        self.analyser = AQIAnalysis()

        # Define UI Controls
        self.city_input = ft.TextField(
            label="Enter City Name",
            width=280,
            border_radius=10,
            border_color=ft.Colors.GREY_700,
            text_align=ft.TextAlign.CENTER
        )
        self.search_button = ft.ElevatedButton(
            text="Search",
            on_click=self.get_aqi_data,
            icon=ft.Icons.SEARCH
        )
        self.aqi_display = ft.Text("AQI: -", size=30, weight=ft.FontWeight.BOLD)
        self.status_display = ft.Text("Enter a city to begin", size=20)
        self.progress_ring = ft.ProgressRing(visible=False)
        self.error_display = ft.Text("", color=ft.Colors.RED_500)

        # The 'controls' attribute is required by ft.View to render its content.
        self.controls = [
            ft.Container(height=50),
            ft.Text("Real-time AQI", size=32, weight=ft.FontWeight.BOLD),
            ft.Row(
                controls=[self.city_input],
                alignment=ft.MainAxisAlignment.CENTER
            ),
            ft.Container(height=10),
            self.search_button,
            ft.Container(height=20),
            self.progress_ring,
            self.error_display,
            ft.Column(
                [self.aqi_display, self.status_display],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10
            ),
            ft.Container(height=50),
            ft.Row(
                [
                    ft.ElevatedButton("Historical Data", on_click=lambda _: self.page.go("/historical")),
                    ft.ElevatedButton("Compare Cities", on_click=lambda _: self.page.go("/compare")),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20
            )
        ]

    def get_aqi_data(self, e):
        """
        Event handler for the search button. Fetches and displays AQI data.
        """
        city = self.city_input.value.strip()
        if not city:
            self.error_display.value = "City name cannot be empty."
            self.page.update()
            return

        self.progress_ring.visible = True
        self.error_display.value = ""
        self.aqi_display.value = "AQI: -"
        self.status_display.value = "Fetching data..."
        self.page.update()

        try:
            data = self.fetcher.get_realtime_aqi(city)
            if data and data.get('status') == 'ok':
                aqi_value = data['data']['aqi']
                analysis = self.analyser.get_aqi_analysis(aqi_value)
                
                self.aqi_display.value = f"AQI: {aqi_value}"
                self.status_display.value = analysis['level']
                self.status_display.color = analysis['color']
            else:
                error_message = data.get('data', 'Unknown error')
                self.error_display.value = f"Error: {error_message}"
                self.status_display.value = "Could not fetch data."
                self.status_display.color = ft.Colors.WHITE

        except Exception as ex:
            self.error_display.value = f"An unexpected error occurred: {ex}"
            self.status_display.value = "Failed to connect."
            self.status_display.color = ft.Colors.WHITE
        
        finally:
            self.progress_ring.visible = False
            self.page.update()