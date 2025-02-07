from io import BytesIO
from PIL import Image

def save_graph_image(bytes_image, filename):
    buffer = BytesIO(bytes_image)
    
    with Image.open(buffer) as img:
        img.save(filename)