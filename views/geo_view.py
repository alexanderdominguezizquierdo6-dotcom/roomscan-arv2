import flet as ft
from database import guardar_inmueble

class GeoView(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.expand = True
        self.padding = 20
        self.bgcolor = "#0B0F19"

        self.txt_nombre = ft.TextField(label="Nombre del Proyecto / Espacio", value="Residencia Comalcalco - Planta Baja", bgcolor="#1E293B", color=ft.colors.WHITE, border_color=ft.colors.CYAN_700, border_radius=10)
        self.txt_tipo = ft.TextField(label="Tipo de Uso", value="Bienes Raíces / Catastro", bgcolor="#1E293B", color=ft.colors.WHITE, border_color=ft.colors.CYAN_700, border_radius=10)
        
        self.txt_area = ft.TextField(label="Área medida (m²)", value="15.24", bgcolor="#1E293B", color=ft.colors.WHITE, border_color=ft.colors.CYAN_700, border_radius=10, keyboard_type=ft.KeyboardType.NUMBER)
        self.txt_volumen = ft.TextField(label="Volumen 3D (m³)", value="41.06", bgcolor="#1E293B", color=ft.colors.WHITE, border_color=ft.colors.CYAN_700, border_radius=10, keyboard_type=ft.KeyboardType.NUMBER)

        self.content = ft.ListView(
            expand=True,
            spacing=15,
            controls=[
                ft.Row([
                    ft.IconButton(icon=ft.icons.ARROW_BACK, icon_color=ft.colors.CYAN_ACCENT, on_click=lambda _: page.go("/scan")),
                    ft.Text("Geolocalización del Inmueble", size=18, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
                ]),
                
                # Tarjeta de estado GPS
                ft.Container(
                    padding=15, bgcolor="#111827", border_radius=10, border=ft.border.all(1, ft.colors.CYAN_900),
                    content=ft.Column([
                        ft.Icon(ft.icons.GPS_FIXED, color=ft.colors.CYAN_ACCENT, size=28),
                        ft.Text("Ubicación GPS Confirmada", size=13, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
                        ft.Text("LAT: 18.334703 | LON: -93.206845", size=11, color=ft.colors.CYAN_ACCENT, font_family="monospace")
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
                ),

                self.txt_nombre,
                self.txt_tipo,
                self.txt_area,
                self.txt_volumen,

                ft.ElevatedButton(
                    text="Guardar y Generar Registro",
                    color=ft.colors.BLACK,
                    bgcolor=ft.colors.CYAN_ACCENT,
                    height=50,
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                    on_click=self._guardar_registro
                ),
                ft.TextButton("Volver al Dashboard", on_click=lambda _: page.go("/dashboard"))
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
            nombre=self.txt_nombre.value or "Residencia Comalcalco",
            tipo_uso=self.txt_tipo.value or "Catastro",
            latitud=18.334703,
            longitud=-93.206845,
            area=area_val,
            volumen=vol_val
        )

        self.page.snack_bar = ft.SnackBar(ft.Text("¡Inmueble registrado con éxito en la base de datos!"), bgcolor=ft.colors.GREEN_700)
        self.page.snack_bar.open = True
        self.page.go("/export")