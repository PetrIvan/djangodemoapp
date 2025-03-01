import cv2 as cv
from .models import Task


def process_task_image(task: Task) -> None:
    """Process task photo: convert to grayscale and resize if needed"""
    if not task.photo:
        return

    img = cv.imread(task.photo.path)
    img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    # Limit to 800x800 px without distortion
    max_size = max(img.shape[0], img.shape[1])
    if max_size > 800:
        compression_factor = max_size / 800
        img = cv.resize(
            img,
            (
                int(img.shape[1] / compression_factor),
                int(img.shape[0] / compression_factor),
            ),
        )

    cv.imwrite(task.photo.path, img)
