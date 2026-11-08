import flet as ft
from database import obtener_inmuebles, obtener_resumen_metricas

class DashboardView(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.expand = True
        self.padding = 20
        self.bgcolor = "#0B0F19"
        self.load_ui()

    def _ir_a_escaneo(self, e):
        self.page.go("/scan")
        self.page.update()

    def load_ui(self):
        metricas = obtener_resumen_metricas()
        inmuebles = obtener_inmuebles()

        cards = []
        if not inmuebles:
            cards.append(
                ft.Container(
                    padding=25,
                    bgcolor="#1E293B",
                    border_radius=12,
                    alignment=ft.alignment.center,
                    content=ft.Column([
                        ft.Icon(ft.icons.FOLDER_OPEN, size=32, color=ft.colors.CYAN_ACCENT),
                        ft.Text("Base de datos limpia. Sin escaneos registrados.", color=ft.colors.GREY_400, size=13),
                        ft.Text("Inicia un nuevo escaneo AR para comenzar.", color=ft.colors.GREY_600, size=11)
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
                )
            )
        else:
            for nombre, tipo, lat, lon, area, vol in inmuebles:
                color_tag = ft.colors.GREEN_700 if tipo.lower() == "catastro" else (
                    ft.colors.BLUE_700 if tipo.lower() == "arquitectura" else ft.colors.ORANGE_700
                )
                cards.append(self._build_property_card(nombre, tipo.upper(), f"LAT: {lat} | LON: {lon}", f"Área: {area} m²", f"Volumen: {vol} m³", color_tag))

        self.content = ft.ListView(
            expand=True,
            spacing=15,
            controls=[
                ft.Row([
                    ft.Column([
                        ft.Text("Panel de Mapeo y Medición", size=14, color=ft.colors.CYAN_400),
                        ft.Text("RoomScan AR", size=24, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
                    ]),
                    ft.IconButton(icon=ft.icons.LOGOUT, icon_color=ft.colors.RED_ACCENT, tooltip="Cerrar Sesión", on_click=lambda _: self.page.go("/"))
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),

                ft.Container(
                    padding=15,
                    bgcolor="#1E293B",
                    border_radius=12,
                    content=ft.Column([
                        ft.Text("RESUMEN DEL SISTEMA", size=12, color=ft.colors.GREY_400, weight=ft.FontWeight.BOLD),
                        ft.Row([
                            ft.Column([ft.Text(str(metricas["totales"]), size=22, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE), ft.Text("Escaneos Totales", size=10, color=ft.colors.GREY_500)]),
                            ft.Column([ft.Text(f"{metricas['area_mapeada']} m²", size=22, weight=ft.FontWeight.BOLD, color=ft.colors.CYAN_ACCENT), ft.Text("Área Mapeada", size=10, color=ft.colors.GREY_500)]),
                            ft.Column([ft.Text(f"{metricas['volumen_3d']} m³", size=22, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE), ft.Text("Volumen 3D", size=10, color=ft.colors.GREY_500)]),
                        ], alignment=ft.MainAxisAlignment.SPACE_AROUND)
                    ])
                ),

                ft.Row([
                    ft.Text("INMUEBLES RECIENTES", size=12, color=ft.colors.GREY_400, weight=ft.FontWeight.BOLD),
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),

                *cards,

                ft.ElevatedButton(
                    text="+ Iniciar Nuevo Escaneo AR",
                    color=ft.colors.BLACK,
                    bgcolor=ft.colors.CYAN_ACCENT,
                    height=50,
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                    on_click=self._ir_a_escaneo
                ),

                ft.Row([
                    ft.TextButton("Inicio", icon=ft.icons.HOME, icon_color=ft.colors.CYAN_ACCENT),
                    ft.TextButton("Proyectos", icon=ft.icons.FOLDER, on_click=lambda _: self.page.go("/geo")),
                    ft.TextButton("Planos", icon=ft.icons.GRID_VIEW, on_click=lambda _: self.page.go("/export")),
                    ft.TextButton("Ajustes", icon=ft.icons.SETTINGS, on_click=lambda _: self.page.go("/settings")),
                ], alignment=ft.MainAxisAlignment.SPACE_AROUND)
            ]
        )

    def _build_property_card(self, title, tag, coords, area, vol, tag_color):
        return ft.Container(
            padding=15,
            bgcolor="#1E293B",
            border_radius=10,
            content=ft.Column([
                ft.Row([
                    ft.Text(title, size=16, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
                    ft.Container(
                        content=ft.Text(tag, size=10, color=ft.colors.WHITE, weight=ft.FontWeight.BOLD),
                        bgcolor=tag_color,
                        padding=ft.padding.symmetric(horizontal=8, vertical=4),
                        border_radius=6
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Text(coords, size=11, color=ft.colors.CYAN_400),
                ft.Row([
                    ft.Text(area, size=12, color=ft.colors.GREY_300),
                    ft.Text(vol, size=12, color=ft.colors.GREY_300),
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
            ])
        )