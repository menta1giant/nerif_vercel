from PIL import Image
import os
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.utils.crypto import get_random_string

def crop_center(pil_img, crop_width, crop_height):
    img_width, img_height = pil_img.size
    return pil_img.crop(((img_width - crop_width) // 2,
                         (img_height - crop_height) // 2,
                         (img_width + crop_width) // 2,
                         (img_height + crop_height) // 2))

def crop_max_square(pil_img):
    return crop_center(pil_img, min(pil_img.size), min(pil_img.size))

def rename_image(instance):
    new_filename = f"profile_image_{instance.user.pk}_{get_random_string(length=6)}.webp"
    
    return os.path.join('profile_images', new_filename)

def resize_image(instance, image):
    img = Image.open(image)
    
    desired_size = (320, 320)
    
    img = crop_max_square(img).resize(desired_size, resample=Image.Resampling.LANCZOS)
    
    buffer = BytesIO()
    
    img.save(buffer, format='WEBP')
    
    resized_image = InMemoryUploadedFile(
        buffer,
        None,
        rename_image(instance),
        'image/webp',
        buffer.tell(),
        None
    )
    
    return resized_image