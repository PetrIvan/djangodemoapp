import cv2 as cv
import numpy as np

from django.core.files.uploadedfile import SimpleUploadedFile


def prepare_dummy_image(width=1920, height=1080) -> SimpleUploadedFile:
    """
    Creates a random test image with the specified dimensions.

    Returns:
        SimpleUploadedFile: File object that can be used in tests
    """
    img = np.random.randint(0, 256, (height, width, 3), dtype=np.uint8)
    _, img_encoded = cv.imencode(".jpg", img)
    image_bytes = img_encoded.tobytes()

    return SimpleUploadedFile("test.jpg", image_bytes, content_type="image/jpeg")


def validate_processed_image(image_path: str, max_dimension=800) -> tuple[bool, bool]:
    """
    Validates that an image has been properly processed.

    Args:
        image_path: Path to the image file
        max_dimension: Maximum allowed dimension (height or width)

    Returns:
        tuple: (is_valid_dimension, is_grayscale)
    """

    processed_img = cv.imread(image_path, cv.IMREAD_UNCHANGED)

    h, w = processed_img.shape[:2]
    is_valid_dimension = h <= max_dimension and w <= max_dimension
    is_grayscale = len(processed_img.shape) == 2

    return is_valid_dimension, is_grayscale
