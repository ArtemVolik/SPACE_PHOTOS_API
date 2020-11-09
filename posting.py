import os
from PIL import Image
import instabot
from dotenv import load_dotenv
import time
import logging
from space_api_func import create_dir
logger = logging.getLogger(__file__)


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
    load_dotenv()
    logging.basicConfig(level=logging.ERROR)
    logger.setLevel(logging.DEBUG)
    image_folder = create_dir()
    insta_login = os.getenv('INSTA_LOGIN')
    insta_password = os.getenv('INSTA_PASSWORD')
    for image in os.listdir(image_folder):
        transform_image(f'{image_folder}/{image}')
        print('Posting', image)
        post_photo(f'{image_folder}/{image}', insta_login, insta_password)
        time.sleep(30)


if __name__ == '__main__':
    main()


