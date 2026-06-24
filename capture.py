import pytesseract
from PIL import ImageGrab
import tkinter as tk
import ctypes

ctypes.windll.shcore.SetProcessDpiAwareness(2)


pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

class RegionSelector:
    def __init__(self):
        self.start_x = 0
        self.start_y = 0
        self.end_x = 0
        self.end_y = 0
        self.rect = None

    def select_region(self):
        self.root = tk.Tk()
        self.root.attributes('-fullscreen', True)
        self.root.attributes('-alpha', 0.3)
        self.root.configure(bg='black')
        self.root.attributes('-topmost', True)

        self.canvas = tk.Canvas(self.root, cursor='cross', bg='black')
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.canvas.bind('<ButtonPress-1>', self.on_press)
        self.canvas.bind('<B1-Motion>', self.on_drag)
        self.canvas.bind('<ButtonRelease-1>', self.on_release)

        self.root.mainloop()

        return self.capture_region()

    def on_press(self, event):
        self.start_x = event.x_root
        self.start_y = event.y_root



    def on_drag(self, event):
        if self.rect:
            self.canvas.delete(self.rect)
            
        cur_x = self.root.winfo_pointerx()
        cur_y = self.root.winfo_pointery()
        self.rect = self.canvas.create_rectangle(
            self.start_x, self.start_y,
            cur_x, cur_y,
            outline='red', width=2)
        
        
        
    


    def on_release(self, event):
        self.end_x = event.x_root
        self.end_y = event.y_root
        self.root.destroy()

    def capture_region(self):
        x1 = min(self.start_x, self.end_x)
        y1 = min(self.start_y, self.end_y)
        x2 = max(self.start_x, self.end_x)
        y2 = max(self.start_y, self.end_y)

        screenshot = ImageGrab.grab(bbox=(x1, y1, x2, y2))
        
        
        screenshot = screenshot.convert('L')  
        screenshot = screenshot.point(lambda x: 0 if x < 140 else 255) 
        
        text = pytesseract.image_to_string(screenshot)
        return text

def scan_screen():
    selector = RegionSelector()
    text = selector.select_region()
    return text

if __name__ == "__main__":
    print("Draw a box around the area you want to scan...")
    text = scan_screen()
    print("--- EXTRACTED TEXT ---")
    print(text)