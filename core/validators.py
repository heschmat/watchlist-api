from django.conf import settings
from django.core.exceptions import ValidationError
from PIL import Image


def validate_image_file(file):
    # Size check
    if file.size > settings.MAX_IMAGE_SIZE_BYTES:
        raise ValidationError(
            f"Image too large. Max size is {settings.MAX_IMAGE_SIZE_MB}MB."
        )

    # Content-type check
    content_type = getattr(file, "content_type", None)
    if content_type not in settings.ALLOWED_IMAGE_TYPES:
        raise ValidationError("Unsupported image format.")

    # Image integrity + dimensions
    try:
        image = Image.open(file)
        image.verify()  # checks corruption
        image = Image.open(file)
        width, height = image.size
    except Exception:
        raise ValidationError("Invalid or corrupted image file.")

    if width > settings.MAX_IMAGE_WIDTH or height > settings.MAX_IMAGE_HEIGHT:
        raise ValidationError(
            f"Image dimensions too large. Max is "
            f"{settings.MAX_IMAGE_WIDTH}x{settings.MAX_IMAGE_HEIGHT}px."
        )
