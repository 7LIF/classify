# pip install pillow

# this file have been inside the images folder

from PIL import Image
import os, glob

folder_path = 'static/assets/images/districts'
desired_width = 425
desired_height = 290


def get_all_images(folder_path):
    image_paths = []
    search_pattern = os.path.join(folder_path, "*.jpg")  # Altere a extensão do arquivo conforme necessário
    for image_path in glob.glob(search_pattern):
        image_paths.append(image_path)
    return image_paths

image_paths = get_all_images(folder_path)



# The 'Image.LANCZOS' method provides a good balance between quality and performance when resizing. 
# It prevents distortion and preserves overall image quality.
def resize_images(image_paths, desired_width, desired_height):
    for image_path in image_paths:
        img = Image.open(image_path)
        current_width, current_height = img.size
        if current_width != desired_width or current_height != desired_height:
            img = img.resize((desired_width, desired_height), Image.LANCZOS)
            base_path, filename = os.path.split(image_path)
            resized_filename = filename
            resized_image_path = os.path.join(base_path, resized_filename)
            img.save(resized_image_path)



resize_images(image_paths, desired_width, desired_height)
print('run successfully')