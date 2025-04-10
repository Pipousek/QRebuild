import cv2
from pyzbar.pyzbar import decode

def extract_qr(image_path):
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError("Image not found")
    decoded = decode(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY))
    if not decoded:
        raise ValueError("No QR code found")
    return decoded[0].data.decode("utf-8")