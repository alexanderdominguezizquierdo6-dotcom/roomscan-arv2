import flet as ft

class ScanView(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.expand = True
        self.padding = 15
        self.bgcolor = "#0B0F19"

        self.content = ft.Column([
            # Cabecera de la vista
            ft.Row([
                ft.IconButton(icon=ft.icons.ARROW_BACK, icon_color=ft.colors.CYAN_ACCENT, on_click=lambda _: self.page.go("/dashboard")),
                ft.Text("Escaneo AR y Medición en Vivo", size=16, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
            ]),
            
            # Tarjeta visual estilo HUD (Simulando la Pantalla 2 de tu propuesta)
            ft.Container(
                expand=True,
                bgcolor="#111827",
                border_radius=12,
                border=ft.border.all(1, ft.colors.CYAN_900),
                padding=20,
                alignment=ft.alignment.center,
                content=ft.Column([
                    ft.Row([
                        ft.Text("● ESCANEO ACTIVO (LIDAR)", size=11, color=ft.colors.CYAN_ACCENT, weight=ft.FontWeight.BOLD),
                        ft.Text("90° Muro", size=11, color=ft.colors.GREY_400),
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    
                    ft.Divider(height=10, color=ft.colors.TRANSPARENT),
                    
                    ft.Icon(ft.icons.VIEW_IN_AR, size=72, color=ft.colors.CYAN_ACCENT),
                    ft.Text("[ DETECTANDO PLANO Y ESPACIO ]", size=13, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
                    ft.Text("Sensores de profundidad y movimiento listos.", size=11, color=ft.colors.GREY_400, text_align=ft.TextAlign.CENTER),
                    
                    ft.Divider(height=10, color=ft.colors.TRANSPARENT),
                    
                    ft.Row([
                        ft.Container(
                            padding=10, bgcolor="#1E293B", border_radius=8, expand=True,
                            content=ft.Column([
                                ft.Text("2.75 m", size=14, weight=ft.FontWeight.BOLD, color=ft.colors.CYAN_ACCENT),
                                ft.Text("ALTO", size=9, color=ft.colors.GREY_400)
                            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
                        ),
                        ft.Container(
                            padding=10, bgcolor="#1E293B", border_radius=8, expand=True,
                            content=ft.Column([
                                ft.Text("4.80 m", size=14, weight=ft.FontWeight.BOLD, color=ft.colors.CYAN_ACCENT),
                                ft.Text("ANCHO", size=9, color=ft.colors.GREY_400)
                            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
                        ),
                    ], spacing=10)
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, alignment=ft.MainAxisAlignment.CENTER)
            ),

            # Métricas en tiempo real según el PDF
            ft.Row([
                ft.Container(
                    expand=True, bgcolor="#111827", padding=10, border_radius=8, border=ft.border.all(1, ft.colors.CYAN_900),
                    content=ft.Column([
                        ft.Text("15.24 m²", size=15, weight=ft.FontWeight.BOLD, color=ft.colors.CYAN_ACCENT),
                        ft.Text("ÁREA CALCULADA", size=10, color=ft.colors.GREY_400)
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
                ),
                ft.Container(
                    expand=True, bgcolor="#111827", padding=10, border_radius=8, border=ft.border.all(1, ft.colors.CYAN_900),
                    content=ft.Column([
                        ft.Text("41.06 m³", size=15, weight=ft.FontWeight.BOLD, color=ft.colors.CYAN_ACCENT),
                        ft.Text("VOLUMEN ESTIMADO", size=10, color=ft.colors.GREY_400)
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
                ),
            ], spacing=10),

            ft.ElevatedButton(
                text="Capturar y Geolocalizar Inmueble ➔",
                color=ft.colors.BLACK,
                bgcolor=ft.colors.CYAN_ACCENT,
                height=45,
                width=float("inf"),
                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
                on_click=lambda _: self.page.go("/geo")
            )
        ], expand=True, spacing=10)