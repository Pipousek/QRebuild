from PIL import Image

def display_image(image_path):
    img = Image.open(image_path)
    img.show()