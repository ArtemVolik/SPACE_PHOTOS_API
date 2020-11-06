import os
from PIL import Image
import instabot
from dotenv import load_dotenv
import time
import logging
from logging.handlers import RotatingFileHandler


def transform_image(picture):
    image = Image.open(picture)
    if image.mode != 'RGB':
        image = image.convert('RGB')
    image.thumbnail((1080, 1080))
    image.save(f'{picture}', format="JPEG")


def post_photo(photo):
    load_dotenv()
    insta_login = os.getenv('INSTA_LOGIN')
    insta_password = os.getenv('INSTA_PASSWORD')
    bot = instabot.Bot()
    bot.login(username=insta_login, password=insta_password)
    bot.upload_photo(f'{photo}')
    if bot.api.last_response.status_code != 200:
        logger.debug(bot.api.last_response)


def main():
    logging.basicConfig(level=logging.DEBUG)
    os.chdir('image')
    images_list = os.listdir()
    for image in images_list:
        transform_image(image)
    images_list = os.listdir()
    for image in images_list:
        print('Posting', image)
        post_photo(image)
        time.sleep(60)


if __name__ == '__main__':
    logger = logging.getLogger("Insta API Logger")
    logger.setLevel(logging.INFO)
    handler = RotatingFileHandler("app_insta_api.log", maxBytes=200, backupCount=2)
    logger.addHandler(handler)
    main()
