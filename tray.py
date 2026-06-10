import pystray
from PIL import Image, ImageDraw
import threading

def create_icon():
    img = Image.new('RGB', (64, 64), color=(30, 30, 30))
    draw = ImageDraw.Draw(img)
    draw.ellipse([8, 8, 56, 56], fill=(0, 120, 212))
    return img

def on_quit(icon, item):
    icon.stop()

def run_tray():
    icon = pystray.Icon(
        "LocalMind",
        create_icon(),
        "LocalMind",
        menu=pystray.Menu(
            pystray.MenuItem("LocalMind", lambda: None, enabled=False),
            pystray.MenuItem("Quit", on_quit)
        )
    )
    icon.run()

if __name__ == "__main__":
    print("LocalMind starting...")
    run_tray()