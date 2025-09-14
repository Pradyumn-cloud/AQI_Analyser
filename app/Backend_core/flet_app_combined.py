# flet_app_combined.py
"""
Combined Flet frontend for both Real-time AQI and Historical Analysis.
Features a tabbed layout to switch between functionalities.
"""
import flet as ft
from . import config
from .models import City
from .fetcher import DataFetcher
from .historical_analyzer import HistoricalAnalyzer # Import the modified analyzer
from threading import Thread

def main(page: ft.Page):
    page.title = "Universal AQI Monitor ☁️"
    page.window_width = 850
    page.window_height = 800
    page.theme_mode = ft.ThemeMode.DARK
    
    # --- REAL-TIME AQI TAB ---

    def search_realtime_clicked(e):
        city_name = rt_city_input.value.strip()
        if not city_name:
            rt_city_input.error_text = "City name cannot be empty"
            page.update()
        else:
            rt_city_input.error_text = None
            rt_progress.visible = True
            rt_search_button.disabled = True
            rt_results_view.controls.clear()
            page.update()
            # Run in a thread to keep UI responsive
            thread = Thread(target=fetch_realtime_data, args=(city_name,))
            thread.start()

    def fetch_realtime_data(city_name):
        data_fetcher = DataFetcher(api_url=config.API_URL, api_key=config.API_KEY)
        city = City(city_name)
        aqi_records = data_fetcher.fetch_data_for_city(city)
        
        if aqi_records:
            for record in aqi_records:
                rt_results_view.controls.append(ft.Text(record.display()))
        else:
            rt_results_view.controls.append(ft.Text(f"Could not fetch data for '{city_name}'."))
        
        # Update UI from the main thread
        rt_progress.visible = False
        rt_search_button.disabled = False
        page.update()

    rt_city_input = ft.TextField(label="Enter City for Real-time AQI", width=350, on_submit=search_realtime_clicked)
    rt_search_button = ft.ElevatedButton("Get AQI Data", icon=ft.icons.SEARCH, on_click=search_realtime_clicked)
    rt_progress = ft.ProgressRing(visible=False)
    rt_results_view = ft.ListView(expand=1, spacing=10, padding=20)

    real_time_tab = ft.Container(
        content=ft.Column([
            ft.Row([rt_city_input, rt_search_button], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([rt_progress], alignment=ft.MainAxisAlignment.CENTER),
            ft.Divider(),
            rt_results_view
        ]),
        padding=20
    )

    # --- HISTORICAL ANALYSIS TAB ---

    selected_csv_path = ft.Text("No CSV file selected.", italic=True)

    def on_file_picked(e: ft.FilePickerResultEvent):
        if e.files:
            selected_csv_path.value = e.files[0].path
        else:
            selected_csv_path.value = "File selection cancelled."
        page.update()

    file_picker = ft.FilePicker(on_result=on_file_picked)
    page.overlay.append(file_picker)

    def analyze_historical_clicked(e):
        if not selected_csv_path.value.endswith('.csv'):
            page.snack_bar = ft.SnackBar(ft.Text("Please select a valid CSV file first!"), bgcolor=ft.colors.ERROR)
            page.snack_bar.open = True
            page.update()
            return
            
        city_name = hist_city_input.value.strip()
        if not city_name:
            hist_city_input.error_text = "City name cannot be empty"
            page.update()
            return

        hist_city_input.error_text = None
        hist_progress.visible = True
        hist_analyze_button.disabled = True
        # Clear previous plots
        hist_plot_row.controls.clear()
        page.update()
        
        thread = Thread(target=run_analysis, args=(selected_csv_path.value, city_name,))
        thread.start()

    def run_analysis(csv_path, city_name):
        analyzer = HistoricalAnalyzer(csv_filepath=csv_path)
        plots = analyzer.analyze_city(city_name=city_name)
        
        if plots:
            trend_img = ft.Image(src_base64=plots["trend"], border_radius=ft.border_radius.all(10))
            heatmap_img = ft.Image(src_base64=plots["heatmap"], border_radius=ft.border_radius.all(10))
            dist_img = ft.Image(src_base64=plots["distribution"], border_radius=ft.border_radius.all(10))
            
            # Display images in a responsive grid
            hist_plot_row.controls.append(ft.Column([trend_img, dist_img], spacing=20))
            hist_plot_row.controls.append(heatmap_img)
        else:
            hist_plot_row.controls.append(ft.Text(f"Could not generate analysis for '{city_name}'. Check city name and CSV data."))
            
        hist_progress.visible = False
        hist_analyze_button.disabled = False
        page.update()

    hist_city_input = ft.TextField(label="Enter City for Historical Analysis", width=300)
    hist_analyze_button = ft.ElevatedButton("Analyze Data", icon=ft.icons.ANALYTICS, on_click=analyze_historical_clicked)
    hist_progress = ft.ProgressRing(visible=False)
    hist_plot_row = ft.Row(wrap=True, spacing=20, run_spacing=20, alignment=ft.MainAxisAlignment.CENTER)

    historical_tab = ft.Container(
        content=ft.Column([
            ft.Row([
                ft.ElevatedButton("Select CSV File", icon=ft.icons.UPLOAD_FILE, on_click=lambda _: file_picker.pick_files(allow_multiple=False, allowed_extensions=["csv"])),
                selected_csv_path
            ], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([hist_city_input, hist_analyze_button], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([hist_progress], alignment=ft.MainAxisAlignment.CENTER),
            ft.Divider(),
            ft.Container(hist_plot_row, expand=True)
        ]),
        padding=20
    )

    # --- MAIN LAYOUT WITH TABS ---
    tabs = ft.Tabs(
        selected_index=0,
        animation_duration=300,
        tabs=[
            ft.Tab(text="Real-time AQI", icon=ft.icons.WAVING_HAND, content=real_time_tab),
            ft.Tab(text="Historical Analysis", icon=ft.icons.INSIGHTS, content=historical_tab),
        ],
        expand=1,
    )
    
    page.add(tabs)

if __name__ == "__main__":
    ft.app(target=main)