import pathlib 
import pytesseract
from PIL import Image


BASE_DIR = pathlib.Path(__file__).parent
IMAGE_DIR = BASE_DIR / "images"
image_path = IMAGE_DIR / "img1.PNG"
pytesseract.pytesseract.tesseract_cmd = 'C:\Program Files\Tesseract-OCR\\tesseract.exe'


def img_to_text(image_path):
    img = Image.open(image_path)

    preds = pytesseract.image_to_string(img)

    return preds