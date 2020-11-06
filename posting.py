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
    image.save(picture, format="JPEG")


def post_photo(photo, insta_login, insta_password):
    bot = instabot.Bot()
    bot.login(username=insta_login, password=insta_password)
    bot.upload_photo(photo)
    if bot.api.last_response.status_code != 200:
        logger.info(bot.api.last_response)


def main():
    logger.basicConfig(level=logging.INFO)
    load_dotenv()
    insta_login = os.getenv('INSTA_LOGIN')
    insta_password = os.getenv('INSTA_PASSWORD')
    image_folder = os.getenv('IMAGE_FOLDER')
    os.chdir(image_folder)
    images = os.listdir()
    for image in images:
        transform_image(image)
        print('Posting', image)
        post_photo(image, insta_login, insta_password)
        time.sleep(30)


if __name__ == '__main__':
    logger = logging.getLogger("Insta API Logger")
    logger.setLevel(logging.INFO)
    handler = RotatingFileHandler("app_insta_api.log", maxBytes=200, backupCount=2)
    logger.addHandler(handler)
    main()
