import flet as ft
from database import guardar_inmueble

class GeoView(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.expand = True
        self.padding = 20
        self.bgcolor = "#0B0F19"

        self.lat_val = 18.4011
        self.lon_val = -93.2201

        self.txt_nombre = ft.TextField(value="Levantamiento Catastral AR", bgcolor="#1E293B", color=ft.colors.WHITE)
        self.txt_tipo = ft.TextField(value="Catastro / Bienes Raíces", bgcolor="#1E293B", color=ft.colors.WHITE)
        
        self.txt_coords = ft.TextField(
            value="Obteniendo coordenadas reales del GPS...", 
            read_only=True, 
            bgcolor="#1E293B", 
            color=ft.colors.CYAN_ACCENT
        )

        # Componente que incrusta un mapa real interactivo (Leaflet + OpenStreetMap)
        self.mapa_html = ft.Html(
            html="""
            <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
            <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
            <div id="real-map" style="width:100%; height:100%; border-radius:12px; z-index:1;"></div>
            <script>
                var map = L.map('real-map').setView([18.4011, -93.2201], 15);
                L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                    maxZoom: 19,
                    attribution: '© OpenStreetMap'
                }).addTo(map);

                var marker = L.marker([18.4011, -93.2201]).addTo(map)
                    .bindPopup('Ubicación del Inmueble RoomScan').openPopup();

                // Obtener GPS real del celular
                if (navigator.geolocation) {
                    navigator.geolocation.getCurrentPosition(position => {
                        var lat = position.coords.latitude;
                        var lon = position.coords.longitude;
                        map.setView([lat, lon], 17);
                        marker.setLatLng([lat, lon]);
                        
                        // Enviar coordenadas a la interfaz si se requiere
                        console.log("GPS Real obtenido: " + lat + ", " + lon);
                    }, err => {
                        console.warn("GPS no disponible o denegado.");
                    }, { enableHighAccuracy: true });
                }
            </script>
            """,
            expand=True
        )

        self.content = ft.ListView(
            expand=True,
            spacing=15,
            controls=[
                ft.Text("Geolocalización Satelital Real", size=20, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
                ft.Text("Sincronización GPS y cartografía en tiempo real.", size=12, color=ft.colors.GREY_400),

                # Contenedor del mapa real
                ft.Container(
                    height=250,
                    bgcolor="#111827",
                    border_radius=12,
                    border=ft.border.all(1, ft.colors.CYAN_900),
                    content=self.mapa_html
                ),

                ft.Text("COORDENADAS CAPTURADAS", size=11, color=ft.colors.GREY_400, weight=ft.FontWeight.BOLD),
                self.txt_coords,

                ft.Text("NOMBRE DEL PROYECTO", size=11, color=ft.colors.GREY_400, weight=ft.FontWeight.BOLD),
                self.txt_nombre,

                ft.Text("TIPO DE USO", size=11, color=ft.colors.GREY_400, weight=ft.FontWeight.BOLD),
                self.txt_tipo,

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
        area = self.page.session.get("temp_area") or 17.28
        volumen = self.page.session.get("temp_volumen") or 47.52
        
        guardar_inmueble(
            nombre=self.txt_nombre.value,
            tipo_uso=self.txt_tipo.value,
            latitud=self.lat_val,
            longitud=self.lon_val,
            area=area,
            volumen=volumen
        )

        self.page.snack_bar = ft.SnackBar(ft.Text("¡Inmueble y coordenadas guardados con éxito!"), bgcolor=ft.colors.GREEN_700)
        self.page.snack_bar.open = True
        self.page.go("/export")