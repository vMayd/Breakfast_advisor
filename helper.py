from PIL import Image


def save_image(image, save_to, *, size=None):
    if not size:
        size = (150, 150)
    im = Image.open(image)
    # _format = im.format.lower()
    resize = im.resize(size, Image.ANTIALIAS)
    resize.save(save_to)


class ValidationError(Exception):
    def __init__(self, key):
        self.key = key

    def __str__(self):
        return 'Validation error: field %s does not meet requirements' % self.key
