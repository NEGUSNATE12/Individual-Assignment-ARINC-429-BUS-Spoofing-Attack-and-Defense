# Terminal 1

import socket, json, hmac, hashlib

class ARINC429Bus:
    def __init__(self):
        self.host = 'localhost'
        self.port = 8888
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.host, self.port))
        print(" Monitor Started")
        print(" Listening on localhost:8888")
        print("=" * 50)

    def check_hmac(self, msg):
        if 'hmac' not in msg: return False
        data = f"{msg['sender']}:{msg['airspeed']}:{msg['label']}"
        good_hmac = hmac.new(self.key, data.encode(), hashlib.sha256).hexdigest()
        return hmac.compare_digest(good_hmac, msg['hmac'])
        
#monitor incoming messages
    def start_monitor(self):
        while True:
            data, addr = self.sock.recvfrom(1024)
            message = json.loads(data.decode())

            valid = self.check_hmac(message)
            
            if message['type'] == 'data':
                if valid:  
                 print(f" [BUS] {message['sender']} -> "
                      f"Airspeed: {message['airspeed']} knots "
                      f"(Label: 0x{message['label']:02X})")
            
            elif message['type'] == 'attack':
                print(f" [ATTACK] {message['sender']} -> "
                      f"FAKE Airspeed: {message['airspeed']} knots "
                      f" SPOOFED DATA!")
            
            elif message['type'] == 'warning':
                print(f" [WARNING] {message['message']}")

if __name__ == "__main__":
    bus = ARINC429Bus()
    bus.start_monitor()
