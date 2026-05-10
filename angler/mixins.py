from PIL import Image, ImageOps
from io import BytesIO
import requests

class ImageRotateMixin:
    """
    Fixes image upload from ios mobile device auto rotation
    """
    image_field = None

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image_field:
            field = getattr(self, self.image_field)
            if field:
                response = requests.get(field.url)
                if response.status_code == 200:
                    image = Image.open(BytesIO(response.content))
                    image = ImageOps.exif_transpose(image)
                    image.info.pop('exif', None)
                    output = BytesIO()
                    image.save(output, format=image.format or 'JPEG')
                    output.seek(0)
                    field.save(field.name, output, save=False)
                    super().save(*args, **kwargs)