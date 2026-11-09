import flet as ft

class ScanView(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.expand = True
        self.padding = 15
        self.bgcolor = "#0B0F19"

        # Visor de hardware integrado directamente en Flet
        html_visor = ft.Html(
            html="""
            <div style="background: #111827; border: 1px solid #0e7490; border-radius: 12px; padding: 10px; text-align: center; color: white; height: 100%; box-sizing: border-box; display: flex; flex-direction: column; justify-content: space-between;">
                <div>
                    <div style="display: flex; justify-content: space-between; font-size: 10px; color: #38bdf8; font-family: monospace; margin-bottom: 4px;">
                        <span>● ESCANEO ACTIVO (LIDAR/AR)</span>
                        <span>90° Muro</span>
                    </div>
                    <video id="webcam" autoplay playsinline muted style="width: 100%; height: 160px; background: #000; border-radius: 8px; object-fit: cover;"></video>
                </div>

                <div style="display: flex; gap: 6px; margin: 6px 0;">
                    <button onclick="activarCamara()" style="flex: 1; background: #00f2fe; color: #000; border: none; padding: 8px; font-weight: bold; border-radius: 6px; cursor: pointer; font-size: 11px;">
                        📷 Encender Cámara
                    </button>
                    <button onclick="obtenerGPS()" style="flex: 1; background: #38bdf8; color: #000; border: none; padding: 8px; font-weight: bold; border-radius: 6px; cursor: pointer; font-size: 11px;">
                        🛰️ Capturar GPS
                    </button>
                </div>

                <div id="status-log" style="font-family: monospace; font-size: 10px; color: #facc15; background: #1E293B; padding: 6px; border-radius: 6px; text-align: left; word-break: break-all;">
                    Estado: Listo para escanear espacio.
                </div>
            </div>

            <script>
                async function activarCamara() {
                    const video = document.getElementById('webcam');
                    const log = document.getElementById('status-log');
                    try {
                        const stream = await navigator.mediaDevices.getUserMedia({
                            video: { facingMode: { ideal: "environment" } },
                            audio: false
                        });
                        video.srcObject = stream;
                        await video.play();
                        log.innerHTML = "¡Cámara trasera activa en tiempo real!";
                        log.style.color = "#4ade80";
                    } catch (err) {
                        log.innerHTML = "Error cámara: " + err.message;
                        log.style.color = "#f87171";
                    }
                }

                function obtenerGPS() {
                    const log = document.getElementById('status-log');
                    if (!navigator.geolocation) {
                        log.innerHTML = "GPS no soportado.";
                        log.style.color = "#f87171";
                        return;
                    }
                    navigator.geolocation.getCurrentPosition(
                        (pos) => {
                            const lat = pos.coords.latitude.toFixed(6);
                            const lon = pos.coords.longitude.toFixed(6);
                            log.innerHTML = `GPS OK -> Lat: ${lat} | Lon: ${lon}`;
                            log.style.color = "#4ade80";
                        },
                        (err) => {
                            log.innerHTML = "Error GPS: " + err.message;
                            log.style.color = "#f87171";
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
                ft.Text("Escaneo AR y Medición", size=16, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
            ]),
            
            ft.Container(expand=True, content=html_visor),

            ft.Row([
                ft.Container(
                    expand=True, bgcolor="#111827", padding=8, border_radius=8, border=ft.border.all(1, ft.colors.CYAN_900),
                    content=ft.Column([
                        ft.Text("15.24 m²", size=14, weight=ft.FontWeight.BOLD, color=ft.colors.CYAN_ACCENT),
                        ft.Text("ÁREA CALCULADA", size=9, color=ft.colors.GREY_400)
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
                ),
                ft.Container(
                    expand=True, bgcolor="#111827", padding=8, border_radius=8, border=ft.border.all(1, ft.colors.CYAN_900),
                    content=ft.Column([
                        ft.Text("41.06 m³", size=14, weight=ft.FontWeight.BOLD, color=ft.colors.CYAN_ACCENT),
                        ft.Text("VOLUMEN ESTIMADO", size=9, color=ft.colors.GREY_400)
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
                ),
            ], spacing=8),

            ft.ElevatedButton(
                text="Capturar y Geolocalizar Inmueble ➔",
                color=ft.colors.BLACK,
                bgcolor=ft.colors.CYAN_ACCENT,
                height=42,
                width=float("inf"),
                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
                on_click=lambda _: self.page.go("/geo")
            )
        ], expand=True, spacing=8)