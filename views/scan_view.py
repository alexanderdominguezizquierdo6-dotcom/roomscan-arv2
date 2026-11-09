import flet as ft

class ScanView(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.expand = True
        self.padding = 20
        self.bgcolor = "#0B0F19"
        
        # HTML y JS embebido directamente en la vista web para evitar el aislamiento de pestañas
        html_component = ft.Html(
            html="""
            <div style="background: #111827; padding: 15px; border-radius: 12px; text-align: center; color: white; border: 1px solid #0e7490;">
                <h3 style="color: #00f2fe; margin-top: 0;">Visor de Cámara y GPS en Vivo</h3>
                <video id="webcam" autoplay playsinline muted style="width: 100%; max-height: 280px; background: #000; border-radius: 8px; object-fit: cover;"></video>
                <div style="margin-top: 15px;">
                    <button onclick="startCamera()" style="background: #00f2fe; color: #000; border: none; padding: 12px 20px; font-weight: bold; border-radius: 8px; cursor: pointer; width: 100%; margin-bottom: 8px;">
                        📷 Activar Cámara Trasera
                    </button>
                    <button onclick="getGPS()" style="background: #38bdf8; color: #000; border: none; padding: 12px 20px; font-weight: bold; border-radius: 8px; cursor: pointer; width: 100%;">
                        🛰️ Obtener Coordenadas GPS
                    </button>
                </div>
                <p id="gps-status" style="font-family: monospace; font-size: 12px; color: #facc15; margin-top: 10px;">GPS: En espera...</p>
            </div>

            <script>
                async function startCamera() {
                    const video = document.getElementById('webcam');
                    try {
                        const stream = await navigator.mediaDevices.getUserMedia({
                            video: { facingMode: { ideal: "environment" } },
                            audio: false
                        });
                        video.srcObject = stream;
                    } catch (err) {
                        alert("No se pudo acceder a la cámara: " + err.message);
                    }
                }

                function getGPS() {
                    const status = document.getElementById('gps-status');
                    if (!navigator.geolocation) {
                        status.innerText = "GPS no soportado en este navegador.";
                        return;
                    }
                    status.innerText = "Buscando satélites...";
                    navigator.geolocation.getCurrentPosition(
                        (pos) => {
                            const lat = pos.coords.latitude.toFixed(6);
                            const lon = pos.coords.longitude.toFixed(6);
                            status.innerHTML = `¡GPS Activo! <br>Lat: ${lat} | Lon: ${lon}`;
                        },
                        (err) => {
                            status.innerText = "Error GPS: " + err.message;
                        },
                        { enableHighAccuracy: true, timeout: 10000 }
                    );
                }
            </script>
            """,
            expand=True
        )

        self.content = ft.Column([
            ft.Row([
                ft.IconButton(icon=ft.icons.ARROW_BACK, icon_color=ft.colors.CYAN_ACCENT, on_click=lambda _: self.page.go("/dashboard")),
                ft.Text("RoomScan AR - Web en Vivo", size=18, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
            ]),
            ft.Text("Acceso directo al hardware desde el navegador para cualquier dispositivo.", size=12, color=ft.colors.GREY_400),
            html_component,
            ft.ElevatedButton(
                text="Ir a Registro y Guardar",
                color=ft.colors.BLACK,
                bgcolor=ft.colors.CYAN_ACCENT,
                height=45,
                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                on_click=lambda _: self.page.go("/geo")
            )
        ], expand=True, spacing=15)