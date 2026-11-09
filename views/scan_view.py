import flet as ft

class ScanView(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.expand = True
        self.padding = 20
        self.bgcolor = "#0B0F19"

        self.content = ft.ListView(
            expand=True,
            spacing=15,
            controls=[
                ft.Row([
                    ft.IconButton(icon=ft.icons.ARROW_BACK, icon_color=ft.colors.CYAN_ACCENT, on_click=lambda _: self.page.go("/dashboard")),
                    ft.Text("Escaneo AR y Sensores en Vivo", size=18, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
                ]),
                
                ft.Container(
                    padding=20,
                    bgcolor="#111827",
                    border_radius=12,
                    border=ft.border.all(1, ft.colors.CYAN_900),
                    content=ft.Column([
                        ft.Icon(ft.icons.CAMERA_ALT, size=50, color=ft.colors.CYAN_ACCENT),
                        ft.Text("Módulo de Hardware del Dispositivo", size=16, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
                        ft.Text("Activa los visores especializados para conceder permisos del sistema operativo y capturar video y coordenadas reales.", size=12, color=ft.colors.GREY_400, text_align=ft.TextAlign.CENTER),
                        ft.Divider(height=15, color=ft.colors.TRANSPARENT),
                        
                        ft.ElevatedButton(
                            text="📷 Activar Cámara Trasera Real",
                            color=ft.colors.BLACK,
                            bgcolor=ft.colors.CYAN_ACCENT,
                            height=48,
                            width=float("inf"),
                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                            on_click=lambda _: page.launch_url("/camera.html")
                        ),
                        
                        ft.ElevatedButton(
                            text="🛰️ Obtener Ubicación GPS Satelital",
                            color=ft.colors.BLACK,
                            bgcolor=ft.colors.CYAN_300,
                            height=48,
                            width=float("inf"),
                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                            on_click=lambda _: page.launch_url("/geo.html")
                        ),
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=12)
                ),

                ft.Container(
                    padding=15,
                    bgcolor="#1E293B",
                    border_radius=10,
                    content=ft.Column([
                        ft.Text("Métricas Estimadas del Espacio", size=13, weight=ft.FontWeight.BOLD, color=ft.colors.CYAN_ACCENT),
                        ft.Row([
                            ft.Text("Área Calculada: 15.24 m²", size=12, color=ft.colors.WHITE),
                            ft.Text("Volumen: 41.06 m³", size=12, color=ft.colors.WHITE),
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                    ])
                ),

                ft.ElevatedButton(
                    text="Continuar a Registro y Guardado ➔",
                    color=ft.colors.BLACK,
                    bgcolor=ft.colors.GREEN_400,
                    height=50,
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                    on_click=lambda _: self.page.go("/geo")
                ),
                ft.TextButton("Volver al Dashboard", on_click=lambda _: self.page.go("/dashboard"))
            ]
        )