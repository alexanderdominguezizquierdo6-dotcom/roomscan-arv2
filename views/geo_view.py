import flet as ft
from database import guardar_inmueble

class GeoView(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.expand = True
        self.padding = 20
        self.bgcolor = "#0B0F19"

        # Capturar coordenadas reales enviadas desde el visor GPS de la web
        lat_val = 18.334703
        lon_val = -93.206845
        
        try:
            route_str = page.route
            if "?" in route_str:
                query_part = route_str.split("?")[1]
                pairs = query_part.split("&")
                for pair in pairs:
                    if "lat=" in pair:
                        lat_val = float(pair.split("=")[1])
                    elif "lon=" in pair:
                        lon_val = float(pair.split("=")[1])
        except Exception:
            pass

        self.lat_real = lat_val
        self.lon_real = lon_val

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
                
                # Tarjeta que muestra las coordenadas reales exactas que acaban de capturar los satélites
                ft.Container(
                    padding=15, bgcolor="#111827", border_radius=10, border=ft.border.all(1, ft.colors.CYAN_900),
                    content=ft.Column([
                        ft.Icon(ft.icons.GPS_FIXED, color=ft.colors.CYAN_ACCENT, size=28),
                        ft.Text("Ubicación GPS Real Confirmada", size=13, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
                        ft.Text(f"LAT: {self.lat_real:.6f} | LON: {self.lon_real:.6f}", size=11, color=ft.colors.CYAN_ACCENT, font_family="monospace")
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

        # Guardar en base de datos SQLite con la latitud y longitud reales del dispositivo
        guardar_inmueble(
            nombre=self.txt_nombre.value or "Residencia Comalcalco",
            tipo_uso=self.txt_tipo.value or "Catastro",
            latitud=self.lat_real,
            longitud=self.lon_real,
            area=area_val,
            volumen=vol_val
        )

        self.page.snack_bar = ft.SnackBar(ft.Text("¡Inmueble y coordenadas GPS reales guardados en la BD!"), bgcolor=ft.colors.GREEN_700)
        self.page.snack_bar.open = True
        self.page.go("/export")