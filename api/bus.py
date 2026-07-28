from http.server import BaseHTTPRequestHandler
import json
from datetime import datetime, timedelta

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        ahora = datetime.utcnow() + timedelta(hours=2)
        hora_actual_str = ahora.strftime("%H:%M")

        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

        html_output = f"""<!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Mapa en Vivo - Línea 91</title>
            <!-- Leaflet CSS -->
            <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
            <style>
                body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background-color: #f4f6f9; color: #333; margin: 0; padding: 0; }}
                .header {{ background: #1a73e8; color: white; padding: 15px 20px; font-size: 20px; font-weight: bold; display: flex; justify-content: space-between; align-items: center; }}
                #map {{ height: 450px; width: 100%; }}
                .info-panel {{ padding: 20px; max-width: 800px; margin: 0 auto; }}
                .card {{ background: #fff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); margin-bottom: 15px; }}
                .badge {{ background: #e8f0fe; color: #1a73e8; padding: 5px 10px; border-radius: 15px; font-size: 13px; font-weight: bold; display: inline-block; margin: 2px; }}
            </style>
        </head>
        <body>
            <div class="header">
                <span>🚌 Línea 91: En Vivo</span>
                <span style="font-size: 14px; background: rgba(255,255,255,0.2); padding: 5px 10px; border-radius: 5px;">Hora: {hora_actual_str}</span>
            </div>

            <div id="map"></div>

            <div class="info-panel">
                <div class="card">
                    <h3>📍 Paradas y Próximas Salidas</h3>
                    <p>El mapa muestra el trayecto entre <strong>Sangonera la Seca</strong>, <strong>Javalí Nuevo</strong> y <strong>Murcia</strong>. El icono del autobús se desplaza de manera simulada a lo largo del recorrido de la línea.</p>
                </div>
            </div>

            <!-- Leaflet JS -->
            <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
            <script>
                // Coordenadas reales de la ruta Línea 91 (Murcia - Javalí - Sangonera)
                var latCentro = 37.9922;
                var lonCentro = -1.1307;

                var map = L.map('map').setView([latCentro, lonCentro], 12);

                // Capa de mapa base (OpenStreetMap)
                L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
                    maxZoom: 19,
                    attribution: '© OpenStreetMap'
                }}).addTo(map);

                // Puntos de la ruta (Paradas clave)
                var pSangonera = [37.9542, -1.2185];
                var pJavali = [37.9901, -1.1812];
                var pCircular = [37.9922, -1.1307];

                // Dibujar la línea de la ruta
                var routeCoordinates = [pSangonera, pJavali, pCircular];
                var polyline = L.polyline(routeCoordinates, {{color: '#1a73e8', weight: 5, opacity: 0.7}}).addTo(map);

                // Añadir marcadores de paradas
                L.marker(pSangonera).addTo(map).bindPopup("<b>Sangonera la Seca (Centro)</b><br>Próximo: 17:30");
                L.marker(pJavali).addTo(map).bindPopup("<b>Javalí Nuevo</b><br>Próximo: 17:45");
                L.marker(pCircular).addTo(map).bindPopup("<b>Plaza Circular, 14</b><br>Próximo: 18:15");

                // Icono personalizado para el autobús en movimiento
                var busIcon = L.icon({{
                    iconUrl: 'https://cdn-icons-png.flaticon.com/512/3448/3448339.png',
                    iconSize: [35, 35],
                    iconAnchor: [17, 17]
                }});

                // Marcador del autobús en movimiento
                var busMarker = L.marker(pSangonera, {{icon: busIcon}}).addTo(map).bindPopup("<b>Autobús Línea 91</b><br>En movimiento hacia Murcia").openPopup();

                // Animación simple del autobús recorriendo los puntos
                var steps = 100;
                var currentStep = 0;
                var targetIndex = 0;

                function moveBus() {{
                    var start = routeCoordinates[targetIndex];
                    var end = routeCoordinates[(targetIndex + 1) % routeCoordinates.length];

                    var lat = start[0] + (end[0] - start[0]) * (currentStep / steps);
                    var lon = start[1] + (end[1] - start[1]) * (currentStep / steps);

                    busMarker.setLatLng([lat, lon]);

                    currentStep++;
                    if (currentStep > steps) {{
                        currentStep = 0;
                        targetIndex = (targetIndex + 1) % routeCoordinates.length;
                    }}
                }}

                setInterval(moveBus, 100);
            </script>
        </body>
        </html>
        """

        self.wfile.write(html_output.encode('utf-8'))
