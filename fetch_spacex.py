import requests
import os
from space_api_func import create_dir, get_response

urls = {
    'latest': 'https://api.spacexdata.com/v4/launches/latest',
    'all': 'https://api.spacexdata.com/v4/launches/'
}


def get_space_x_images_list():
    last_flight = get_response(urls['latest'])
    if last_flight['links']['flickr']['original']:
        return last_flight['links']['flickr']['original']
    else:
        flights = get_response(urls['all'])
        flight_images = [flight['links']['flickr']['original'] for flight in flights if flight['links']['flickr']['original']]
        return flight_images[1]


def save_spacex_images(images, folder):
    print(f'Saving {len(images)} photos from SpaceX')
    for image_order, image in enumerate(images, 1):
        response = requests.get(image)
        response.raise_for_status()
        with open(f'{folder}/spacex{image_order}{os.path.splitext(image)[1]}', 'wb') as file:
            file.write(response.content)
            print(f'Photo {image_order} saved')


def fetch_spacex_last_launch():
    folder = create_dir()
    pictures = get_space_x_images_list()
    save_spacex_images(pictures, folder)


if __name__ == '__main__':
    fetch_spacex_last_launch()



