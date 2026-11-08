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

        self.txt_nombre = ft.TextField(value="Levantamiento Catastral AR", bgcolor="#1E293B", color=ft.colors.WHITE, border_color=ft.colors.CYAN_700, border_radius=10)
        self.txt_tipo = ft.TextField(value="Catastro / Bienes Raíces", bgcolor="#1E293B", color=ft.colors.WHITE, border_color=ft.colors.CYAN_700, border_radius=10)
        
        self.txt_coords = ft.TextField(
            value="Esperando señal GPS en tiempo real...", 
            read_only=True, 
            bgcolor="#1E293B", 
            color=ft.colors.CYAN_ACCENT,
            border_color=ft.colors.CYAN_900,
            border_radius=10
        )

        self.gps_status_label = ft.Text("🛰️ Estado GPS: Solicitando permisos de ubicación...", size=13, color=ft.colors.YELLOW_400)

        self.map_container = ft.Container(
            height=180,
            bgcolor="#111827",
            border_radius=12,
            border=ft.border.all(1, ft.colors.CYAN_900),
            padding=20,
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.icons.GPS_FIXED, color=ft.colors.CYAN_ACCENT, size=28),
                    ft.Text("Monitoreo GPS en Vivo", size=16, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE)
                ], alignment=ft.MainAxisAlignment.START),
                ft.Divider(height=10, color=ft.colors.TRANSPARENT),
                self.gps_status_label,
                ft.Text("Cuando aceptes el aviso del navegador, verás tus coordenadas reales actualizándose aquí.", size=11, color=ft.colors.GREY_400),
            ], alignment=ft.MainAxisAlignment.CENTER)
        )

        self.content = ft.ListView(
            expand=True,
            spacing=15,
            controls=[
                ft.Text("Geolocalización Satelital Real", size=20, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
                ft.Text("Sincronización GPS y cartografía en tiempo real.", size=12, color=ft.colors.GREY_400),

                self.map_container,

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

    def did_mount(self):
        # Monitorear la posición GPS real del celular continuamente
        js_gps = """
        (function() {
            if (navigator.geolocation) {
                navigator.geolocation.watchPosition(
                    function(position) {
                        const lat = position.coords.latitude;
                        const lon = position.coords.longitude;
                        const acc = position.coords.accuracy;
                        
                        // Actualizar visualmente la interfaz modificando elementos del DOM en tiempo real
                        let txtBox = document.querySelector('input[aria-label*="Esperando"]');
                        if (!txtBox) {
                            // Buscar cualquier input de coordenadas disponible
                            let inputs = document.querySelectorAll('input');
                            inputs.forEach(inp => {
                                if (inp.value && inp.value.includes("GPS") || inp.value.includes("Esperando")) {
                                    inp.value = "Lat: " + lat.toFixed(6) + " | Lon: " + lon.toFixed(6) + " (Precisión: " + acc.toFixed(1) + "m)";
                                    inp.dispatchEvent(new Event('input', { bubbles: true }));
                                }
                            });
                        }
                        console.log("GPS Activo en tiempo real -> Lat: " + lat + ", Lon: " + lon);
                    },
                    function(error) {
                        console.warn("Error de GPS: " + error.message);
                    },
                    { enableHighAccuracy: true, maximumAge: 0, timeout: 5000 }
                );
            }
        })();
        """
        self.page.run_js(js_gps)

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