from pythonosc import udp_client
import keyboard
import random
import io
from infi.systray import SysTrayIcon
import json
import mouse
import screeninfo

AVATAR_PARAMS_KEYCODE = "/avatar/parameters/KeyCode"
AVATAR_PARAMS_MOUSE_X = "/avatar/parameters/mouse_x"
AVATAR_PARAMS_MOUSE_Y = "/avatar/parameters/mouse_y"
DEFAULT_ADDRESS = "127.0.0.1"
DEFAULT_SEND_PORT = 9000
DEFAULT_JSON = {"address": DEFAULT_ADDRESS,"port": DEFAULT_SEND_PORT,"keycode_path": AVATAR_PARAMS_KEYCODE, "mouse_x_path": AVATAR_PARAMS_MOUSE_X, "mouse_y_path": AVATAR_PARAMS_MOUSE_Y, "randomized": False, "use_keycode": True, "use_mouse": True}
SETTING_FILE_PATH = "./setting.json"

class KeyCodeSender(object):
    __slots__ = (
        "_client",
        "_randomized",
        "_address",
        "_port",
        "_keycode_path",
        "_mouse_x_path",
        "_mouse_y_path",
        "_monitor_x",
        "_monitor_y",
        "_use_keycode",
        "_use_mouse",
    )
    
    def __init__(self, randomized: bool = False, use_keycode: bool = True, use_mouse: bool = True):
        self._randomized: bool = randomized
        self._use_keycode: bool = use_keycode
        self._use_mouse: bool = use_mouse
        self._monitor_x: int = 0
        self._monitor_y: int = 0
        monitors = screeninfo.get_monitors()
        for monitor in monitors:
            self._monitor_x += monitor.width
            self._monitor_y += monitor.height
            
        try:
            with open(SETTING_FILE_PATH) as setting_file:
                setting_json: dict = json.load(setting_file)
                self._address: str = setting_json.get("address", DEFAULT_ADDRESS)
                self._port: int = setting_json.get("port", DEFAULT_SEND_PORT)
                self._keycode_path: str = setting_json.get("keycode_path", AVATAR_PARAMS_KEYCODE)
                self._mouse_x_path: str = setting_json.get("mouse_x_path", AVATAR_PARAMS_MOUSE_X)
                self._mouse_y_path: str = setting_json.get("mouse_y_path", AVATAR_PARAMS_MOUSE_Y)
                self._randomized: bool = setting_json.get("randomized", False)
                self._use_keycode: bool = setting_json.get("use_keycode", True)
                self._use_mouse: bool = setting_json.get("use_mouse", True)
                # print(f"address: {self._address}, port: {self._port}, path: {self._keycode_path}")
        except FileNotFoundError :
            with open(SETTING_FILE_PATH, "w") as setting_file:
                self.create_new_json(setting_file=setting_file)
        self.create_new_client(self._address, self._port)
        
    def create_new_client(self, address: str = DEFAULT_ADDRESS, port: int = DEFAULT_SEND_PORT) -> None:
        try:
            self._client: udp_client.SimpleUDPClient = udp_client.SimpleUDPClient(address=address, port=port)
        except OSError:
            print(f"IP Address \"{address}\" is not valid.\nDefault Address is used instead.\n")
            self._client: udp_client.SimpleUDPClient = udp_client.SimpleUDPClient(address=DEFAULT_ADDRESS, port=port)
            with open(SETTING_FILE_PATH, "w") as setting_file:
                self.create_new_json(setting_file=setting_file, port=self._port, keycode_path=self._keycode_path, mouse_x_path=self._mouse_x_path, mouse_y_path=self._mouse_y_path, randomized=self._randomized, use_keycode=self._use_keycode, use_mouse=self._use_mouse)
        try:
            self._client.send_message(self._keycode_path, 0)
        except OverflowError:
            print(f"Port number \"{port}\" is not valid.\nDefault port is used instead.\n")
            self.create_new_client(address)
            with open(SETTING_FILE_PATH, "w") as setting_file:
                self.create_new_json(setting_file=setting_file, address=self._address, keycode_path=self._keycode_path, mouse_x_path=self._mouse_x_path, mouse_y_path=self._mouse_y_path, randomized=self._randomized, use_keycode=self._use_keycode, use_mouse=self._use_mouse)
        
    def on_keyDown(self, event: keyboard.KeyboardEvent) -> None:
        if self._use_keycode:
            code: int = event.scan_code
            if self._randomized:
                code = random.randrange(255)
            try:
                self._client.send_message(self._keycode_path, code)
            except OverflowError:
                print(f"Port number \"{self._client._port}\" is not valid.\nDefault port is used instead.\n")
                self.create_new_client(address=self._client._address, randomized=self._randomized)
            
    def on_mouse_move(self, event: mouse.MoveEvent):
        if self._use_mouse and isinstance(event, mouse.MoveEvent):
            x: float = 2.0 * float(event.x)/float(self._monitor_x) - 1.0
            y: float = 2.0 * float(event.y)/float(self._monitor_y) - 1.0
            x = max(min(x, 1.0), -1.0)
            y = max(min(y, 1.0), -1.0)
            try:
                self._client.send_message(self._mouse_x_path, x)
                self._client.send_message(self._mouse_y_path, y)
            except OverflowError:
                print(f"Port number \"{self._client._port}\" is not valid.\nDefault port is used instead.\n")
                self.create_new_client(address=self._client._address, randomized=self._randomized)
        
    def start_send(self) -> None:
        keyboard.on_press(self.on_keyDown)
        mouse.hook(self.on_mouse_move)
        
    def create_new_json(self, setting_file: io.TextIOWrapper, address: str = DEFAULT_ADDRESS, port: int = DEFAULT_SEND_PORT, keycode_path: str = AVATAR_PARAMS_KEYCODE, mouse_x_path: str = AVATAR_PARAMS_MOUSE_X, mouse_y_path: str = AVATAR_PARAMS_MOUSE_Y, randomized: bool = False, use_keycode: bool = True, use_mouse: bool = True):
        setting_dict: dict = {"address": address, "port": port, "keycode_path": keycode_path, "mouse_x_path": mouse_x_path, "mouse_y_path": mouse_y_path, "randomized": randomized, "use_keycode": use_keycode, "use_mouse": use_mouse}
        json.dump(setting_dict, setting_file, indent=4)
        self._address = address
        self._port = port
        self._keycode_path = keycode_path
        self._mouse_x_path = mouse_x_path
        self._mouse_y_path = mouse_y_path
        self._randomized = randomized
        self._use_keycode = use_keycode
        self._use_mouse = use_mouse
        
    def save_current_setting_json(self, setting_file: io.TextIOWrapper) -> None:
        self.create_new_json(setting_file=setting_file, address=self._address, port=self._port, keycode_path=self._keycode_path, mouse_x_path=self._mouse_x_path, mouse_y_path=self._mouse_y_path, randomized=self._randomized, use_keycode=self._use_keycode, use_mouse=self._use_mouse)
        
        
        
class Systray(object):
    __slots__ = (
        "_sender",
        "_menu_options",
        "_randomize_texts",
        "_keycode_texts",
        "_mouse_texts",
    )
    
    def __init__(self, sender: KeyCodeSender = KeyCodeSender()):
        self._sender = sender
        self._randomize_texts = ["Randomize: [ ]", "Randomize:  [x]"]
        self._keycode_texts = ["KeyCode: [ ]", "KeyCode: [x]"]
        self._mouse_texts = ["Mouse: [ ]", "Mouse: [x]"]
        self._menu_options = (("Toggle Randomize", None, self.toggle_randomize),
                            ("Toggle KeyCode", None, self.toggle_keycode),
                            ("Toggle Mouse", None, self.toggle_mouse),
                            ("Save Setting", None, self.save_setting),)
        
    def create_systray(self) -> None:
        hover = self.create_hover_text()
        systray = SysTrayIcon("icon.ico", hover_text=hover, menu_options=self._menu_options)
        systray.start()
        
    def create_hover_text(self) -> str:
        randomize_text = self._randomize_texts[1] if self._sender._randomized else self._randomize_texts[0]
        keycode_text = self._keycode_texts[1] if self._sender._use_keycode else self._keycode_texts[0]
        mouse_text = self._mouse_texts[1] if self._sender._use_mouse else self._mouse_texts[0]
        return f"VRChat-KeyCode-OSC\n {randomize_text}\n {keycode_text}\n {mouse_text}"
        
    def execute_keycode_sender(self) -> None:
        self._sender.start_send()
    
    def toggle_randomize(self, systray: SysTrayIcon) -> None:
        self._sender._randomized = not self._sender._randomized
        hover = self.create_hover_text()
        systray.update(hover_text=hover)
        
        
    def toggle_keycode(self, systray) -> None:
        self._sender._use_keycode = not self._sender._use_keycode
        hover = self.create_hover_text()
        systray.update(hover_text=hover)

        
    def toggle_mouse(self, systray) -> None:
        self._sender._use_mouse = not self._sender._use_mouse
        hover = self.create_hover_text()
        systray.update(hover_text=hover)
        
    def save_setting(self, systray) -> None:
        with open(SETTING_FILE_PATH, "w") as setting_file:
                self._sender.save_current_setting_json(setting_file=setting_file)
        
        
def main():
    kecode_sender = KeyCodeSender()
    systray = Systray(kecode_sender)
    systray.create_systray()
    systray.execute_keycode_sender()
    
if __name__ == "__main__":
    main()