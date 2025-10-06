import flet as ft
from assets import styles as S

class NavBar(ft.Container):
    """Professional Navigation Bar"""
    def __init__(self, page: ft.Page, title: str = "AQI Monitor Pro"):
        self.page = page
        
        super().__init__(
            content=ft.Row([
                ft.Row([
                    ft.Icon(ft.Icons.AIR, color=S.PRIMARY, size=32),
                    ft.Text(title, style=S.H3),
                ], spacing=12),
                ft.Row([
                    self._nav_button("Home", "/", ft.Icons.HOME),
                    self._nav_button("Historical", "/historical", ft.Icons.ANALYTICS),
                    self._nav_button("Compare", "/compare", ft.Icons.COMPARE_ARROWS),
                ], spacing=8)
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            bgcolor=S.CARD,
            padding=ft.padding.symmetric(24, 16),
            border=ft.border.only(bottom=ft.BorderSide(1, ft.Colors.with_opacity(0.1, S.TEXT_PRIMARY)))
        )
    
    def _nav_button(self, text: str, route: str, icon: ft.Icons):
        is_active = self.page.route == route
        return ft.Container(
            content=ft.Row([
                ft.Icon(icon, color=S.TEXT_PRIMARY if is_active else S.TEXT_MUTED, size=18),
                ft.Text(text, style=ft.TextStyle(
                    size=14,
                    weight=ft.FontWeight.W_600 if is_active else ft.FontWeight.NORMAL,
                    color=S.TEXT_PRIMARY if is_active else S.TEXT_MUTED
                ))
            ], spacing=6),
            bgcolor=S.PRIMARY if is_active else None,
            padding=ft.padding.symmetric(12, 8),
            border_radius=S.RADIUS_SMALL,
            on_click=lambda _: self.page.go(route),
            ink=True
        )

class SearchBar(ft.Container):
    """Professional Search Component"""
    def __init__(self, on_search, placeholder: str = "Enter city name"):
        self.on_search = on_search
        
        self.input = ft.TextField(
            hint_text=placeholder,
            border_color=S.PRIMARY,
            focused_border_color=S.PRIMARY_LIGHT,
            text_style=ft.TextStyle(color=S.TEXT_PRIMARY, size=16),
            hint_style=ft.TextStyle(color=S.TEXT_MUTED),
            cursor_color=S.PRIMARY,
            prefix_icon=ft.Icons.SEARCH,
            border_radius=S.RADIUS_SMALL,
            bgcolor=S.CARD,
            height=56,
            on_submit=self.on_search
        )
        
        self.button = ft.Container(
            content=ft.Row([
                ft.Icon(ft.Icons.SEARCH, color=S.TEXT_PRIMARY, size=20),
                ft.Text("Search", style=ft.TextStyle(size=16, weight=ft.FontWeight.W_600, color=S.TEXT_PRIMARY))
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=8),
            bgcolor=S.PRIMARY,
            padding=ft.padding.symmetric(24, 16),
            border_radius=S.RADIUS_SMALL,
            on_click=self.on_search,
            ink=True,
            height=56
        )
        
        super().__init__(
            content=ft.Row([
                ft.Container(self.input, expand=True),
                self.button
            ], spacing=12),
            padding=ft.padding.symmetric(0, 0)
        )

class AQICard(ft.Container):
    """Large AQI Display Card"""
    def __init__(self):
        # Data controls (hidden initially)
        self.aqi_value = ft.Text("--", style=S.H1)
        self.aqi_level = ft.Text("Awaiting data...", style=S.H3)
        self.city_name = ft.Text("", style=S.CAPTION)
        self.badge = ft.Container()
        self.last_updated = ft.Text("", style=S.SMALL)

        # Data column (hidden until we have real data)
        self.data_column = ft.Column([
            ft.Row([
                ft.Column([
                    ft.Text("AIR QUALITY INDEX", style=S.CAPTION),
                    self.aqi_value,
                    self.aqi_level,
                    self.city_name,
                ], spacing=4),
                ft.Container(expand=True),
                ft.Column([
                    self.badge,
                    ft.Container(height=8),
                    self.last_updated
                ], horizontal_alignment=ft.CrossAxisAlignment.END)
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        ])

        # Placeholder shown initially
        placeholder_text = "Hi there! 😄 Type the city name and click the search button."
        # Keep placeholder text control so it can be updated (e.g., 'No data found')
        self.placeholder_text = ft.Text(placeholder_text, style=S.H3, text_align=ft.TextAlign.CENTER)
        self.placeholder = ft.Container(
            content=ft.Column([
                self.placeholder_text
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            alignment=ft.alignment.center,
        )

        # Start with placeholder visible and data hidden
        self.data_column.visible = False
        self.placeholder.visible = True

        super().__init__(
            content=ft.Column([
                self.placeholder,
                self.data_column
            ]),
            gradient=S.GRADIENT_DARK,
            padding=32,
            border_radius=S.RADIUS_LARGE,
            shadow=S.SHADOW_ELEVATED
        )

    def show_placeholder(self):
        """Show the centered placeholder and hide data view."""
        # Reset placeholder to greeting
        self.placeholder_text.value = "Hi there! 😄 Type the city name and click the search button."
        self.placeholder.visible = True
        self.data_column.visible = False
        # reset visual state
        self.aqi_value.value = "--"
        self.aqi_level.value = ""
        self.city_name.value = ""
        self.badge.content = ft.Container()
        self.last_updated.value = ""
        self.gradient = S.GRADIENT_DARK
        self.update()

    def show_not_found(self, city: str):
        """Show a centered 'no data' message for the given city."""
        print(f"AQICard.show_not_found() called for: {city}")
        self.placeholder_text.value = f"No data found for {city.title()}"
        self.placeholder.visible = True
        self.data_column.visible = False
        # reset any data controls
        self.aqi_value.value = "--"
        self.aqi_level.value = ""
        self.city_name.value = ""
        self.badge.content = ft.Container()
        self.last_updated.value = ""
        self.gradient = S.GRADIENT_DARK
        self.update()

    def update_data(self, aqi: int, level: str, city: str, timestamp: str = "Just now"):
        # Switch to data view
        self.placeholder.visible = False
        self.data_column.visible = True

        self.aqi_value.value = str(aqi)
        self.aqi_level.value = level
        self.city_name.value = city.title()
        self.badge.content = S.aqi_badge(level, aqi)
        self.last_updated.value = f"Updated: {timestamp}"
        self.gradient = S.get_aqi_gradient(aqi)
        self.update()

class MetricGrid(ft.Container):
    """Grid of metric cards"""
    def __init__(self):
        self.metrics = []
        super().__init__(
            content=ft.ResponsiveRow([], spacing=16),
            padding=0
        )
    
    def add_metric(self, title: str, value: str, icon: str, color: str = S.PRIMARY):
        metric = S.metric_card(title, value, icon, color)
        self.content.controls.append(
            ft.Container(metric, col={"sm": 12, "md": 6, "lg": 3})
        )
        self.metrics.append(metric)
        self.update()
    
    def clear(self):
        self.content.controls.clear()
        self.metrics.clear()
        self.update()

class PollutantCard(ft.Container):
    """Pollutant Information Card"""
    def __init__(self, name: str, value: float, unit: str = "µg/m³", is_dominant: bool = False):
        color = S.ERROR if is_dominant else S.PRIMARY
        bgcolor = S.CARD_ELEVATED if is_dominant else S.CARD
        
        super().__init__(
            content=ft.Row([
                ft.Container(
                    content=ft.Icon(ft.Icons.BUBBLE_CHART, color=color, size=24),
                    bgcolor=ft.Colors.with_opacity(0.1, color),
                    padding=8,
                    border_radius=S.RADIUS_SMALL
                ),
                ft.Column([
                    ft.Text(name, style=ft.TextStyle(size=16, weight=ft.FontWeight.W_600, color=S.TEXT_PRIMARY)),
                    ft.Text(f"{value:.1f} {unit}", style=S.CAPTION)
                ], spacing=2, expand=True),
                ft.Container(
                    content=ft.Text("⚠️" if is_dominant else "✓", size=20),
                    visible=is_dominant
                )
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            bgcolor=bgcolor,
            padding=16,
            border_radius=S.RADIUS_SMALL,
            border=ft.border.all(1, color) if is_dominant else None
        )

class StationCard(ft.Container):
    """Monitoring Station Card"""
    def __init__(self, name: str, aqi: int, location: str = ""):
        color = S.get_aqi_color(aqi)
        
        super().__init__(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.LOCATION_ON, color=color, size=20),
                    ft.Text(name, style=ft.TextStyle(size=15, weight=ft.FontWeight.W_600, color=S.TEXT_PRIMARY), expand=True)
                ], spacing=8),
                ft.Row([
                    ft.Text(f"AQI: {aqi}", style=S.BODY),
                    ft.Container(
                        content=ft.Text(str(aqi), style=ft.TextStyle(size=12, weight=ft.FontWeight.BOLD, color=S.TEXT_PRIMARY)),
                        bgcolor=color,
                        padding=ft.padding.symmetric(8, 6),
                        border_radius=S.RADIUS_SMALL
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Text(location, style=S.SMALL) if location else ft.Container()
            ], spacing=6),
            bgcolor=S.CARD,
            padding=16,
            border_radius=S.RADIUS_SMALL,
            border=ft.border.all(1, ft.Colors.with_opacity(0.1, color))
        )

class InfoSection(ft.Container):
    """Collapsible Information Section"""
    def __init__(self, title: str, icon: str, color: str = S.PRIMARY):
        self.title_text = ft.Text(title, style=S.H3)
        self.content_column = ft.Column([], spacing=12)
        self.is_expanded = True
        
        super().__init__(
            content=ft.Column([
                ft.Container(
                    content=ft.Row([
                        ft.Icon(icon, color=color, size=24),
                        self.title_text,
                        ft.Container(expand=True),
                        ft.IconButton(
                            icon=ft.Icons.EXPAND_LESS,
                            icon_color=S.TEXT_MUTED,
                            on_click=self._toggle
                        )
                    ], spacing=12),
                    on_click=self._toggle
                ),
                ft.Divider(height=1, color=S.TEXT_DISABLED),
                self.content_column
            ], spacing=12),
            bgcolor=S.CARD,
            padding=24,
            border_radius=S.RADIUS,
            shadow=S.SHADOW
        )
    
    def _toggle(self, e):
        self.is_expanded = not self.is_expanded
        self.content_column.visible = self.is_expanded
        self.update()
    
    def add_item(self, item: ft.Control):
        self.content_column.controls.append(item)
        self.update()
    
    def clear(self):
        self.content_column.controls.clear()
        self.update()

class LoadingOverlay(ft.Container):
    """Loading spinner overlay"""
    def __init__(self):
        super().__init__(
            content=ft.Column([
                ft.ProgressRing(color=S.PRIMARY, width=50, height=50),
                ft.Text("Loading data...", style=S.BODY)
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=16),
            alignment=ft.alignment.center,
            visible=False,
            bgcolor=ft.Colors.with_opacity(0.8, S.BG),
            expand=True
        )
    
    def show(self):
        self.visible = True
        self.update()
    
    def hide(self):
        self.visible = False
        self.update()
