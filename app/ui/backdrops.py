# ui/backdrops.py
import asyncio
import random
import flet as ft
from assets import styles as S

class Backdrop:
    def __init__(self, page: ft.Page):
        self.page = page
        self.stack = ft.Stack(expand=False, height=180)
        self._running = False

    def build(self) -> ft.Control:
        return self.stack

    async def animate(self):
        """Override to animate shapes."""
        pass

    def start(self):
        if not self._running:
            self._running = True
            self.page.run_task(self.animate)

    def stop(self):
        self._running = False

class ClearSkyBackdrop(Backdrop):
    def __init__(self, page: ft.Page):
        super().__init__(page)
        # gradient sky
        self.sky = ft.Container(
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_center,
                end=ft.alignment.bottom_center,
                colors=["#1E3A8A", "#0D1117"],
            ),
            border_radius=S.RADIUS,
            expand=True,
        )
        # soft sun
        self.sun = ft.Container(
            width=140, height=140, border_radius=200,
            bgcolor=ft.Colors.with_opacity(0.15, "#FFD166"),
            top=20, right=20,
        )
        # few clouds
        self.clouds = []
        for i in range(3):
            c = ft.Container(
                width=random.randint(120, 160),
                height=random.randint(55, 75),
                border_radius=999,
                bgcolor=ft.Colors.with_opacity(0.12, ft.Colors.WHITE),
                left=20 + i*110,
                top=60 + random.randint(-10,10),
            )
            self.clouds.append(c)

        self.stack.controls = [self.sky, self.sun, *self.clouds]

    async def animate(self):
        dx = 1
        while self._running:
            for c in self.clouds:
                c.left = (c.left + dx) % 360
                c.update()
            await asyncio.sleep(0.03)

class DustyBackdrop(Backdrop):
    def __init__(self, page: ft.Page):
        super().__init__(page)
        self.sky = ft.Container(
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_center,
                end=ft.alignment.bottom_center,
                colors=["#3A2E1F", "#0D1117"],
            ),
            border_radius=S.RADIUS,
            expand=True,
        )
        # drifting dust particles (tiny dots)
        self.particles: list[ft.Container] = []
        for i in range(30):
            p = ft.Container(
                width=6, height=6, border_radius=99,
                bgcolor=ft.Colors.with_opacity(0.25, "#E3B261"),
                left=random.randint(0, 340),
                top=random.randint(20, 150),
            )
            self.particles.append(p)

        # dusty gust ribbons
        self.ribbons = []
        for i in range(3):
            r = ft.Container(
                width=240, height=22, border_radius=22,
                bgcolor=ft.Colors.with_opacity(0.08, "#E3B261"),
                left=i*90, top=40 + i*35,
            )
            self.ribbons.append(r)

        self.stack.controls = [self.sky, *self.ribbons, *self.particles]

    async def animate(self):
        while self._running:
            for p in self.particles:
                p.left += random.uniform(0.8, 2.2)
                if p.left > 360:
                    p.left = -10
                    p.top = random.randint(20, 150)
                p.update()
            for i, r in enumerate(self.ribbons):
                r.left += 1.2 + 0.2*i
                if r.left > 360:
                    r.left = -240
                r.update()
            await asyncio.sleep(0.03)

# ---------- Hazy sunny day (okayish) ----------
class HazySunnyBackdrop(Backdrop):
    def __init__(self, page: ft.Page):
        super().__init__(page)
        self.sky = ft.Container(
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_center,
                end=ft.alignment.bottom_center,
                colors=["#2C3E50", "#0D1117"],
            ),
            border_radius=S.RADIUS,
            expand=True,
        )
        self.sun = ft.Container(
            width=110, height=110, border_radius=200,
            bgcolor=ft.Colors.with_opacity(0.18, "#FFC857"),
            left=18, top=18,
        )
        # light haze bands
        self.haze = []
        for i in range(4):
            h = ft.Container(
                width=360, height=18, border_radius=999,
                bgcolor=ft.Colors.with_opacity(0.06, ft.Colors.WHITE),
                left=-20, top=40 + i*28,
            )
            self.haze.append(h)

        # tiny few dust specks
        self.specks = []
        for i in range(10):
            s = ft.Container(
                width=4, height=4, border_radius=99,
                bgcolor=ft.Colors.with_opacity(0.2, "#D6B26F"),
                left=random.randint(0, 340), top=random.randint(40, 160),
            )
            self.specks.append(s)

        self.stack.controls = [self.sky, self.sun, *self.haze, *self.specks]

    async def animate(self):
        t = 0.0
        while self._running:
            t += 0.03
            for i, h in enumerate(self.haze):
                h.left = -20 + 10 * (1 if i % 2 == 0 else -1)
                h.opacity = 0.06 + 0.02 * (1 if i % 2 == 0 else 0)
                h.update()
            for s in self.specks:
                s.left += 0.5
                if s.left > 360:
                    s.left = -5
                s.update()
            await asyncio.sleep(0.03)

# ---------- Factory ----------
def backdrop_for_status(page: ft.Page, status: str) -> Backdrop:
    s = status.lower()
    if "good" in s:
        return ClearSkyBackdrop(page)
    if "poor" in s or "unhealthy" in s:
        return DustyBackdrop(page)
    return HazySunnyBackdrop(page)
