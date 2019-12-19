from PIL import Image


def resize(image_path, max_size):
    img = Image.open(image_path)
    if img.height > max_size:
        h_percent = max_size / float(img.size[1])
        w_size = int(float(img.size[0]) * h_percent)
        img.thumbnail((w_size, max_size))
        img.save(image_path)
    if img.width > max_size:
        w_percent = max_size / float(img.size[0])
        h_size = int(float(img.size[1]) * w_percent)
        img.thumbnail((max_size, h_size))
        img.save(image_path)
