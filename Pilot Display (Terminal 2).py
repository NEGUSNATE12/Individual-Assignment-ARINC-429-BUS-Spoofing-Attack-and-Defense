#Terminal 2

import socket, json, hmac, hashlib

class PilotDisplay:
    def __init__(self):
        self.host = 'localhost'
        self.port = 8889
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.host, self.port))
        self.current_speed = 0
        print("Pilot Display Started")
        print(" Waiting for airspeed data...")
        print("=" * 50)

    def check_hmac(self, msg):
        if 'hmac' not in msg: return False
        data = f"{msg['sender']}:{msg['airspeed']}:{msg['label']}"
        good_hmac = hmac.new(self.key, data.encode(), hashlib.sha256).hexdigest()
        return hmac.compare_digest(good_hmac, msg['hmac'])   
    
#monitor incoming messages and update display
    def update_display(self):
        while True:
            data, addr = self.sock.recvfrom(1024)
            message = json.loads(data.decode())
            
            valid = self.check_hmac(message)
            self.current_speed = message['airspeed']
            
            if message['type'] == 'normal':
                if valid:
                 print(f" [DISPLAY] Current Airspeed: {self.current_speed} knots  NORMAL")

                else:
                 print(f" [DISPLAY] Current Airspeed: {self.current_speed} knots  INVALID HMAC!")
            
            elif message['type'] == 'attack':
                print(f" [DISPLAY] Current Airspeed: {self.current_speed} knots  SPOOFED!")
                
                # Warning for dangerous values
                if self.current_speed < 450:
                    print(" LOW AIRSPEED WARNING!")
                elif self.current_speed >520:
                    print("  OVERSPEED WARNING!")

if __name__ == "__main__":
    display = PilotDisplay()
    display.update_display()
