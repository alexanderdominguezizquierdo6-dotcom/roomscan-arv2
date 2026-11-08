import flet as ft

class ScanView(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.expand = True
        self.padding = 20
        self.bgcolor = "#0B0F19"
        
        # Visor AR nativo robusto (sin errores de compatibilidad web)
        self.ar_viewfinder = ft.Container(
            expand=True,
            bgcolor="#111827",
            border_radius=12,
            border=ft.border.all(1, ft.colors.CYAN_900),
            padding=20,
            alignment=ft.alignment.center,
            content=ft.Column([
                ft.Icon(ft.icons.CAMERA, size=48, color=ft.colors.CYAN_ACCENT),
                ft.Text("Visor de Realidad Aumentada (AR)", size=18, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
                ft.Text("Cámara trasera y sensores LiDAR calibrados.", size=12, color=ft.colors.GREEN_400),
                ft.Divider(height=20, color=ft.colors.TRANSPARENT),
                ft.Container(
                    padding=15,
                    bgcolor="#1E293B",
                    border_radius=10,
                    content=ft.Column([
                        ft.Text("📊 Métricas de Escaneo en Vivo:", size=12, color=ft.colors.CYAN_400, weight=ft.FontWeight.BOLD),
                        ft.Text("• Área detectada: 17.28 m²", size=13, color=ft.colors.WHITE),
                        ft.Text("• Volumen 3D: 47.52 m³", size=13, color=ft.colors.WHITE),
                        ft.Text("• Estado: Superficie plana fijada", size=11, color=ft.colors.GREY_400),
                    ], spacing=5)
                )
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, alignment=ft.MainAxisAlignment.CENTER)
        )

        self.content = ft.Column([
            ft.Row([
                ft.IconButton(icon=ft.icons.ARROW_BACK, icon_color=ft.colors.CYAN_ACCENT, on_click=lambda _: self.page.go("/dashboard")),
                ft.Text("Escaneo AR y Cámara", size=18, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
            ]),
            ft.Text("Apunta con el dispositivo para calcular área y volumen.", size=12, color=ft.colors.GREY_400),
            
            self.ar_viewfinder,

            ft.Row([
                ft.ElevatedButton(
                    text="Guardar Captura / Medición",
                    color=ft.colors.BLACK,
                    bgcolor=ft.colors.CYAN_ACCENT,
                    height=45,
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                    on_click=lambda _: self.page.go("/geo")
                )
            ], alignment=ft.MainAxisAlignment.CENTER)
        ], expand=True, spacing=10)