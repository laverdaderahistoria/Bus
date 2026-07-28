from http.server import BaseHTTPRequestHandler
import json
import re
import requests

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        url = "https://moovitapp.com/tripplan/murcia-3738/lines/91/65629805/5931424/en?customerId=4908"
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Cookie": "euconsent-v2=CPXx...; __cmpcc={%22consent%22:true}"
        }

        try:
            res = requests.get(url, headers=headers, timeout=8)
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            if res.status_code == 200:
                html_content = res.text
                matches = re.findall(r'>([^<>\n]{2,50})<', html_content)
                
                exclusiones = [
                    "Moovit", "Cookie", "Privacy", "About", "Terms", "Ads", "Press", 
                    "Sign", "Log", "EN", "Get the App", "Community", "App Support", 
                    "Contact Us", "Change direction", "Today", "assets_", "cls-1", 
                    "Back", "Change day", "Select a stop", "TMP - Monbus"
                ]
                
                paradas_dict = []
                parada_actual = None
                
                for t in matches:
                    t_limpio = t.strip()
                    if not t_limpio or "{" in t_limpio or "}" in t_limpio or any(exc.lower() in t_limpio.lower() for exc in exclusiones):
                        continue
                    
                    if re.search(r'\d{1,2}:\d{2}', t_limpio) or "Additional Times" in t_limpio:
                        if parada_actual and t_limpio != "Additional Times":
                            for hora in t_limpio.split(","):
                                hora_limpia = hora.strip()
                                if hora_limpia and hora_limpia != "Additional Times:" and hora_limpia not in parada_actual["horarios"]:
                                    parada_actual["horarios"].append(hora_limpia)
                    else:
                        if len(t_limpio) > 2 and not t_limpio.isdigit():
                            parada_actual = {"parada": t_limpio, "horarios": []}
                            paradas_dict.append(parada_actual)

                resultado = {
                    "linea": "TMP - Monbus 91",
                    "itinerario": [p for p in paradas_dict if len(p["horarios"]) > 0]
                }
                
                self.wfile.write(json.dumps(resultado, ensure_ascii=False, indent=2).encode('utf-8'))
            else:
                error_data = json.dumps({"status": res.status_code, "error": "No se pudo conectar"})
                self.wfile.write(error_data.encode('utf-8'))
                
        except Exception as e:
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            error_data = json.dumps({"error": str(e)})
            self.wfile.write(error_data.encode('utf-8'))
