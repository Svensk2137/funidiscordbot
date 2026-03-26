from wand.image import Image

with Image(filename='image.jpg') as img:
    print(img.size)
    with img.clone() as i:
        i.resize(int(i.width * 0.25), int(i.height * 0.25))
        i.save(filename='image-poop.jpg')