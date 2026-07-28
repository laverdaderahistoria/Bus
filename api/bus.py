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
            "moovit_phone_type": "2",
            "moovit_user_key": "F42722",
            "x-aws-waf-token": "9c2c9c9e-85d0-43ac-82d8-ddeee4309353:HQoAeGlJhLI/AAAA:B2IqhjBW1QLvpARnKcyCQMmKOFuxW7ybIeHOh9M66syg4k79II1exdtO0s6DGqPyj9EqQk2SyAFQay4isELTMlLN3v+Gc437Vz73aL/2jfz/HazxuW4fE+dsctrA111J3xYHipAhhOGAUPNQv8pqYh329RiChNSA/jUx5N52XpsZgU09NzYSIoQBzDk2+3b3L17DyRN/i6dK3S1wX+U2WqMSxsbja4GMNfTLrC8dThQYESkgnJ1zkUbr+eZkzIgzc1sF"
        }

        payload = {
            "stopId": 384413826,
            "lineIds": "{\"ids\":[5931424]}"
        }

        try:
            res = requests.post(url, headers=headers, json=payload, timeout=8)
            
            self.send_response(res.status_code)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            # Forzar el envío del contenido devuelto por Moovit
            self.wfile.write(res.content)
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))
