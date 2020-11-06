import os
from PIL import Image
import math
import instabot
from dotenv import load_dotenv
import time
from fetch_hubble import get_image_name


def transform_image(picture):
    image = Image.open(picture)
    # для PNG файлов которые содержат прозрачный слой и не могут быть сохранены как джпег
    if image.mode != 'RGB':
        image = image.convert('RGB')
    width, height = image.size
    # ресайз
    if width > height:
        box = ((width - height) // 2, 0, width - math.ceil((width - height) / 2), height)
        image = image.crop(box)
    elif width < height:
        box = (0, (height - width) // 2, width, height - math.ceil((height - width) / 2))
        image = image.crop(box)
    image.thumbnail((1080, 1080))
    name = get_image_name(picture)
    # для фоткам по которым не сработал ресайз
    width, height = image.size
    if width + height == 2160:
        image.save(f'{name}.jpg', format="JPEG")
    os.remove(f'{picture}')
# короче класс Image я проштудировал вдоль и поперек


def post_photo(photo):
    load_dotenv()
    insta_login = os.getenv('INSTA_LOGIN')
    insta_password = os.getenv('INSTA_PASSWORD')
    bot = instabot.Bot()
    bot.login(username=insta_login, password=insta_password)
    bot.upload_photo(f'{photo}')
    if bot.api.last_response.status_code != 200:
        print(bot.api.last_response)


def main():
    images_list = os.listdir('image')
    os.chdir('image')
    for image in images_list:
        transform_image(image)
    images_list = os.listdir()
    for image in images_list:
        print(image)
        post_photo(image)
        time.sleep(60)


if __name__ == '__main__':
    main()










