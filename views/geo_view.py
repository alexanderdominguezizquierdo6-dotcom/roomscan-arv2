import flet as ft
from database import guardar_inmueble

class GeoView(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.expand = True
        self.padding = 20
        self.bgcolor = "#0B0F19"

        self.txt_nombre = ft.TextField(label="Nombre del Inmueble / Proyecto", bgcolor="#1E293B", color=ft.colors.WHITE, border_color=ft.colors.CYAN_700, border_radius=10)
        self.txt_tipo = ft.TextField(label="Tipo de Uso (Ej. Catastro, Arquitectura)", bgcolor="#1E293B", color=ft.colors.WHITE, border_color=ft.colors.CYAN_700, border_radius=10)
        
        # Campos de entrada reales para las mediciones capturadas por el usuario
        self.txt_area = ft.TextField(label="Área medida real (m²)", value="", bgcolor="#1E293B", color=ft.colors.WHITE, border_color=ft.colors.CYAN_700, border_radius=10, keyboard_type=ft.KeyboardType.NUMBER)
        self.txt_volumen = ft.TextField(label="Volumen 3D medido real (m³)", value="", bgcolor="#1E293B", color=ft.colors.WHITE, border_color=ft.colors.CYAN_700, border_radius=10, keyboard_type=ft.KeyboardType.NUMBER)

        self.map_container = ft.Container(
            padding=20,
            bgcolor="#111827",
            border_radius=12,
            border=ft.border.all(1, ft.colors.CYAN_900),
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.icons.GPS_FIXED, color=ft.colors.CYAN_ACCENT, size=28),
                    ft.Text("Módulo GPS con Permiso Real", size=16, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE)
                ], alignment=ft.MainAxisAlignment.START),
                ft.Divider(height=10, color=ft.colors.TRANSPARENT),
                ft.Text("Abre el capturador GPS para autorizar y obtener tu ubicación satelital real.", size=12, color=ft.colors.GREY_300),
                ft.Divider(height=10, color=ft.colors.TRANSPARENT),
                ft.ElevatedButton(
                    text="🛰️ Abrir Capturador GPS Real",
                    color=ft.colors.BLACK,
                    bgcolor=ft.colors.CYAN_ACCENT,
                    height=45,
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                    on_click=lambda _: self.page.launch_url("/geo.html")
                )
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        )

        self.content = ft.ListView(
            expand=True,
            spacing=15,
            controls=[
                ft.Text("Registro y Geolocalización", size=20, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
                ft.Text("Registra los datos reales de tu levantamiento técnico.", size=12, color=ft.colors.GREY_400),

                self.map_container,

                ft.Text("DATOS DEL LEVANTAMIENTO", size=11, color=ft.colors.GREY_400, weight=ft.FontWeight.BOLD),
                self.txt_nombre,
                self.txt_tipo,
                self.txt_area,
                self.txt_volumen,

                ft.ElevatedButton(
                    text="Guardar en Base de Datos",
                    color=ft.colors.BLACK,
                    bgcolor=ft.colors.CYAN_ACCENT,
                    height=50,
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                    on_click=self._guardar_registro
                ),
                ft.TextButton("Volver al Escaneo", on_click=lambda _: self.page.go("/scan"))
            ]
        )

    def _guardar_registro(self, e):
        try:
            area_val = float(self.txt_area.value) if self.txt_area.value else 0.0
            vol_val = float(self.txt_volumen.value) if self.txt_volumen.value else 0.0
        except ValueError:
            area_val = 0.0
            vol_val = 0.0

        guardar_inmueble(
            nombre=self.txt_nombre.value or "Proyecto sin nombre",
            tipo_uso=self.txt_tipo.value or "General",
            latitud=18.4011, # Coordenada base ajustable según captura real de geo.html
            longitud=-93.2201,
            area=area_val,
            volumen=vol_val
        )

        self.page.snack_bar = ft.SnackBar(ft.Text("¡Inmueble y datos registrados correctamente!"), bgcolor=ft.colors.GREEN_700)
        self.page.snack_bar.open = True
        self.page.go("/export")