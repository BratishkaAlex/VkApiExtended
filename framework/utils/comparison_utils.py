from PIL import ImageChops, Image

from framework.utils.logger import info
from resources import config


def compare_two_images(path_to_first_picture, path_to_second_picture):
    first_image = Image.open(path_to_first_picture)
    second_image = Image.open(path_to_second_picture)
    return ImageChops.difference(first_image, second_image).getbbox() is None


def compare_two_images_with_accuracy(path_to_first_picture, path_to_second_picture):
    info(f"Comparing two pictures, difference percentage must be no more than {config.PERCENT_OF_ACCURACY}")
    image_1 = Image.open(path_to_first_picture)
    image_2 = Image.open(path_to_second_picture)
    assert image_1.mode == image_2.mode, "Different kinds of images."
    assert image_1.size == image_2.size, "Different sizes."

    pairs = zip(image_1.getdata(), image_2.getdata())
    if len(image_1.getbands()) == 1:
        # for gray-scale jpegs
        dif = sum(abs(p1 - p2) for p1, p2 in pairs)
    else:
        dif = sum(abs(c1 - c2) for p1, p2 in pairs for c1, c2 in zip(p1, p2))

    components = image_1.size[0] * image_1.size[1] * 3
    difference_percentage = (dif / 255.0 * 100) / components
    return difference_percentage <= config.PERCENT_OF_ACCURACY
