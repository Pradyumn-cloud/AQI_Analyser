# app/ui/historical_view.py
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
import flet as ft
from pathlib import Path
from Backend_core.historical_analyzer import HistoricalAnalyzer

ASSETS_PLOTS_DIR = Path("assets") / "plots"

class HistoricalView(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__(route="/historical")
        self.page = page
        
        # Set assets directory for the page
        if not hasattr(page, 'assets_dir') or page.assets_dir is None:
            page.assets_dir = "assets"

        # Instantiate analyzer with the CSV path relative to app/
        # Adjust the csv path if your data lives elsewhere.
        self.analyzer = HistoricalAnalyzer(csv_filepath="data_analysis/Data/data.csv")

        # UI components
        self.city_input = ft.TextField(label="City", hint_text="Enter city name", expand=True)
        self.analyze_btn = ft.ElevatedButton("Analyze", on_click=self.run_analysis)
        self.results = ft.Column([], spacing=16, scroll=ft.ScrollMode.AUTO)
        self.snackbar = ft.SnackBar(content=ft.Text(""))

        self.build()

    def build(self):
        self.controls.clear()
        header = ft.Container(
            content=ft.Row([
                ft.Text("Historical Analysis (City-wise)", style=ft.TextStyle(size=20, weight=ft.FontWeight.BOLD)),
            ], alignment=ft.MainAxisAlignment.CENTER),
            padding=12
        )

        search_row = ft.Row([self.city_input, self.analyze_btn], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

        self.controls.append(
            ft.Column([
                header,
                search_row,
                ft.Divider(),
                self.results
            ], spacing=20, expand=True, scroll=ft.ScrollMode.AUTO)
        )

    def run_analysis(self, e):
        city = (self.city_input.value or "").strip()
        if not city:
            self.page.snack_bar = ft.SnackBar(ft.Text("Please enter a city name"))
            self.page.snack_bar.open = True
            self.page.update()
            return

        # Clear previous results
        self.results.controls.clear()
        self.page.update()

        try:
            analysis = self.analyzer.generate_city_analysis(city)
        except FileNotFoundError as ex:
            self.page.snack_bar = ft.SnackBar(ft.Text(str(ex)))
            self.page.snack_bar.open = True
            self.page.update()
            return
        except Exception as ex:
            self.page.snack_bar = ft.SnackBar(ft.Text(f"Error during analysis: {ex}"))
            self.page.snack_bar.open = True
            self.page.update()
            return

        if not analysis:
            self.page.snack_bar = ft.SnackBar(ft.Text(f"No data found for city: {city}"))
            self.page.snack_bar.open = True
            self.page.update()
            return

        # Summary info
        self.results.controls.append(
            ft.Column([
                ft.Text(f"Results for {analysis['city'].title()}", style=ft.TextStyle(size=18, weight=ft.FontWeight.BOLD)),
                ft.Row([
                    ft.Column([ft.Text("Best Month"), ft.Text(str(analysis.get('best_month')))]),
                    ft.Column([ft.Text("Worst Month"), ft.Text(str(analysis.get('worst_month')))]),
                    ft.Column([ft.Text("Most toxic pollutant"), ft.Text(str(analysis.get('most_toxic_overall')))]),
                ], alignment=ft.MainAxisAlignment.SPACE_AROUND)
            ], spacing=12)
        )

        # Show plots if present; the analyzer saved them under assets/plots and returned paths like 'plots/xxx.png'
        image_keys = [
            ('Yearly Trend', analysis.get('yearly_path')),
            ('Monthly Trend', analysis.get('monthly_path')),
            ('Hourly Pattern', analysis.get('hourly_path')),
            ('Most Toxic Pollutants', analysis.get('most_toxic_path')),
            ('Correlation Heatmap', analysis.get('heatmap_path')),
        ]
        
        # --- TABS FOR 5 PLOTS ---
        tabs = []
        for title, relpath in image_keys:
            if relpath:
                tab = ft.Tab(
                    text=title,
                    content=ft.Container(
                        content=ft.Image(
                            src=relpath,
                            width=800,
                            height=500,
                            fit=ft.ImageFit.CONTAIN,
                            error_content=ft.Text(f"Failed to load: {relpath}")
                        ),
                        padding=20,
                        alignment=ft.alignment.center
                    )
                )
                tabs.append(tab)

        if tabs:
            self.results.controls.append(
                ft.Container(
                    content=ft.Tabs(
                        tabs=tabs,
                        selected_index=0,
                        expand=False
                    ),
                    height=600
                )
            )

        # Show peak months table
        peak = analysis.get('peak_months', {})
        if peak:
            rows = []
            for p, m in peak.items():
                rows.append(ft.Row([ft.Text(p), ft.Text(str(m))], alignment=ft.MainAxisAlignment.SPACE_BETWEEN))
            self.results.controls.append(ft.Card(content=ft.Column([ft.Text("Peak month per pollutant"), ft.Divider()] + rows), elevation=1))

        # Show average pollutant values
        avg = analysis.get('avg_pollutants', {})
        if avg:
            avg_rows = [ft.Row([ft.Text(k), ft.Text(f"{v:.2f}")], alignment=ft.MainAxisAlignment.SPACE_BETWEEN) for k, v in avg.items()]
            self.results.controls.append(ft.Card(content=ft.Column([ft.Text("Average pollutant concentrations (city)"), ft.Divider()] + avg_rows), elevation=1))

        self.page.update()