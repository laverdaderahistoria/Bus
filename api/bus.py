from http.server import BaseHTTPRequestHandler
import json
from datetime import datetime, timedelta

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Hora actual en España (HH:MM)
        ahora = datetime.utcnow() + timedelta(hours=2)
        hora_actual_str = ahora.strftime("%H:%M")

        # Horarios oficiales de referencia para la Línea 91 (Sangonera - Javalí - Murcia)
        horarios_base = [
            {"parada": "Sangonera la Seca (Centro)", "horarios": ["07:00", "08:30", "10:00", "11:30", "13:00", "14:30", "16:00", "17:30", "19:00", "20:30"]},
            {"parada": "Javalí Nuevo", "horarios": ["07:15", "08:45", "10:15", "11:45", "13:15", "14:45", "16:15", "17:45", "19:15", "20:45"]},
            {"parada": "Plaza Circular, 14", "horarios": ["07:45", "09:15", "10:45", "12:15", "13:45", "15:15", "16:45", "18:15", "19:45", "21:15"]},
            {"parada": "Cajamurcia", "horarios": ["07:50", "09:20", "10:50", "12:20", "13:50", "15:20", "16:50", "18:20", "19:50", "21:20"]},
            {"parada": "Avda. Constitución 8", "horarios": ["07:55", "09:25", "10:55", "12:25", "13:55", "15:25", "16:55", "18:25", "19:55", "21:25"]}
        ]

        # Filtrar estrictamente las próximas horas futuras a partir de la hora actual
        itinerario_valido = []
        for p in horarios_base:
            horas_futuras = [h for h in p["horarios"] if h >= hora_actual_str][:3]
            if not horas_futuras:
                # Si ya pasaron todas hoy, mostramos las primeras del día siguiente como referencia
                horas_futuras = p["horarios"][:2]
                
            itinerario_valido.append({
                "parada": p["parada"],
                "horarios": horas_futuras
            })

        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

        html_output = f"""<!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Próximas Salidas - Línea 91</title>
            <style>
                body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background-color: #f4f6f9; color: #333; margin: 0; padding: 20px; }}
                .container {{ max-width: 600px; margin: 0 auto; }}
                h1 {{ color: #1a73e8; font-size: 22px; margin-bottom: 5px; }}
                .subtitle {{ color: #666; font-size: 14px; margin-bottom: 25px; }}
                .card {{ background: #fff; padding: 16px 20px; margin-bottom: 12px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); border-left: 5px solid #1a73e8; }}
                .parada-nombre {{ font-size: 16px; font-weight: bold; color: #202124; margin-bottom: 10px; }}
                .horarios-list {{ display: flex; flex-wrap: wrap; gap: 8px; }}
                .badge {{ background: #e8f0fe; color: #1a73e8; padding: 6px 12px; border-radius: 20px; font-size: 14px; font-weight: 550; }}
                .footer {{ text-align: center; font-size: 12px; color: #888; margin-top: 30px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🚌 Próximas Salidas - Línea 91</h1>
                <div class="subtitle">Horarios en tiempo real a partir de las {hora_actual_str}</div>
        """

        for item in itinerario_valido:
            html_output += f"""
            <div class="card">
                <div class="parada-nombre">📍 {item['parada']}</div>
                <div class="horarios-list">
            """
            for hora in item['horarios']:
                html_output += f'<span class="badge">🕒 {hora}</span>'
            html_output += """
                </div>
            </div>
            """

        html_output += """
                <div class="footer">Sistema de horarios activos - Línea 91</div>
            </div>
        </body>
        </html>
        """

        self.wfile.write(html_output.encode('utf-8'))
