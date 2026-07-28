from http.server import BaseHTTPRequestHandler
import json
import requests

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        url = "https://moovitapp.com/api/lines/linearrival"
        
        headers = {
            "accept": "application/json, text/plain, */*",
            "content-type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Origin": "https://moovitapp.com",
            "Referer": "https://moovitapp.com/",
            "moovit_app_type": "WEB_TRIP_PLANNER",
            "moovit_client_version": "5.151.2/V567",
            "moovit_customer_id": "4908",
            "moovit_metro_id": "3738",
            "moovit_phone_type": "2"
        }

        payload = {
            "stopId": 384413826,
            "lineIds": "{\"ids\":[5931424]}"
        }

        try:
            res = requests.post(url, headers=headers, json=payload, timeout=8)
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            if res.status_code == 200 and res.content:
                self.wfile.write(res.content)
            else:
                fallback_data = json.dumps({"status": res.status_code, "respuesta": res.text})
                self.wfile.write(fallback_data.encode('utf-8'))
                
        except Exception as e:
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            error_data = json.dumps({"error": str(e)})
            self.wfile.write(error_data.encode('utf-8'))
