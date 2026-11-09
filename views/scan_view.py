import flet as ft

class ScanView(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.expand = True
        self.padding = 15
        self.bgcolor = "#0B0F19"

        # Componente HTML embebido directamente en la interfaz de Flet para mostrar la cámara y el GPS en vivo
        visor_ar_html = ft.Html(
            html="""
            <div style="background: #111827; border: 1px solid #0e7490; border-radius: 12px; padding: 12px; text-align: center; color: white; height: 100%; box-sizing: border-box; display: flex; flex-direction: column; justify-content: space-between;">
                <div>
                    <div style="display: flex; justify-content: space-between; font-size: 11px; color: #38bdf8; font-family: monospace; margin-bottom: 6px;">
                        <span>● ESCANEO ACTIVO (AR)</span>
                        <span>90° Muro Detección</span>
                    </div>
                    <video id="webcam" autoplay playsinline muted style="width: 100%; height: 180px; background: #000; border-radius: 8px; object-fit: cover;"></video>
                </div>

                <div style="display: flex; gap: 8px; margin: 8px 0;">
                    <button onclick="activarCamaraReal()" style="flex: 1; background: #00f2fe; color: #000; border: none; padding: 10px; font-weight: bold; border-radius: 6px; cursor: pointer; font-size: 12px;">
                        📷 Encender Cámara
                    </button>
                    <button onclick="obtenerGPSReal()" style="flex: 1; background: #38bdf8; color: #000; border: none; padding: 10px; font-weight: bold; border-radius: 6px; cursor: pointer; font-size: 12px;">
                        🛰️ Obtener GPS
                    </button>
                </div>

                <div id="status-box" style="font-family: monospace; font-size: 11px; color: #facc15; background: #1E293B; padding: 6px; border-radius: 6px; text-align: left; word-break: break-all;">
                    Estado: Listo para activar sensores.
                </div>
            </div>

            <script>
                let gpsData = { lat: 18.334703, lon: -93.206845 };

                async function activarCamaraReal() {
                    const video = document.getElementById('webcam');
                    const statusBox = document.getElementById('status-box');
                    try {
                        const stream = await navigator.mediaDevices.getUserMedia({
                            video: { facingMode: { ideal: "environment" } },
                            audio: false
                        });
                        video.srcObject = stream;
                        await video.play();
                        statusBox.innerHTML = "¡Cámara trasera activa en tiempo real!";
                        statusBox.style.color = "#4ade80";
                    } catch (err) {
                        statusBox.innerHTML = "Error de cámara: " + err.message;
                        statusBox.style.color = "#f87171";
                    }
                }

                function obtenerGPSReal() {
                    const statusBox = document.getElementById('status-box');
                    if (!navigator.geolocation) {
                        statusBox.innerHTML = "GPS no soportado.";
                        statusBox.style.color = "#f87171";
                        return;
                    }
                    navigator.geolocation.getCurrentPosition(
                        (pos) => {
                            gpsData.lat = pos.coords.latitude;
                            gpsData.lon = pos.coords.longitude;
                            const acc = pos.coords.accuracy.toFixed(1);
                            statusBox.innerHTML = `GPS OK -> Lat: ${gpsData.lat.toFixed(4)} | Lon: ${gpsData.lon.toFixed(4)} (±${acc}m)`;
                            statusBox.style.color = "#4ade80";
                        },
                        (err) => {
                            statusBox.innerHTML = "Error GPS: " + err.message;
                            statusBox.style.color = "#f87171";
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
                ft.Text("Escaneo AR y Medición en Vivo", size=16, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
            ]),
            
            # Contenedor principal que aloja el visor web en la app
            ft.Container(expand=True, content=visor_ar_html),

            # Métricas estimadas según la propuesta
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