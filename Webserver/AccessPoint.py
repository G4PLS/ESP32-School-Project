import network

class AccessPoint:
    def __init__(self, ssid, password, authmode=0):
        self._ssid = ssid
        self._password = password
        self._authmode = authmode
        
        self._ap = None
        
    def start(self):
        print("SETTING UP ACCESS POINT")
        if self._ap is not None:
            return
        
        self._ap = network.WLAN(network.AP_IF)
        
        self._ap.config(
            ssid=self._ssid,
            password=self._password,
            authmode=self._authmode
            )
        
        self._ap.active(True)
        
        print(f"Access Point {self._ssid} is {"active" if self._ap.active() else 'not active'}")
        print(f"IP: {self._ap.ifconfig()[0]}")
