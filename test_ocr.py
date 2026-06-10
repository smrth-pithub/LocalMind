import pytesseract 
from PIL import ImageGrab
import pyautogui

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def capture_and_extract():
    print("Taking screenshot in 3 seconds... switch to any window with text")
    import time 
    time.sleep(3)

    screenshot = ImageGrab.grab()
    text = pytesseract.image_to_string(screenshot)
    print("---Extracted Text---")
    print(text)

capture_and_extract()
