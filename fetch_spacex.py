import requests
import os
import argparse

urls = {
    'latest': 'https://api.spacexdata.com/v4/launches/latest',
    'all': 'https://api.spacexdata.com/v4/launches/'
}


def create_dir():
    parser = argparse.ArgumentParser('Get photos from spacex last launch')
    parser.add_argument('-f', '--folder', help='Enter folder name', default='image')
    args = parser.parse_args()
    os.makedirs(args.folder, exist_ok=True)
    return args.folder


def get_response(url):
    response = requests.get(url)
    response.raise_for_status()
    answer = response.json()
    return answer


def search_images_array_in_json(search, search_key='flickr', pictures_found=[]):
    for key, value in search.items():
        if key == search_key:
            pictures_found.append(value)
            return
        elif isinstance(value, dict):
            search_images_array_in_json(value, search_key, pictures_found)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    search_images_array_in_json(item, search_key, pictures_found)
    return pictures_found


def get_space_x_images_list():
    last_flight = get_response(urls['latest'])
    pictures_found = search_images_array_in_json(last_flight, search_key='flickr')[0]['original']
    if pictures_found:
        return pictures_found
    else:
        flights = get_response(urls['all'])
        for flight in flights:
            pictures_found_from_all = search_images_array_in_json(flight, search_key='flickr', pictures_found=[])[0][
                'original']
            if pictures_found_from_all:
                return pictures_found_from_all


def save_spacex_images(images, folder):
    os.chdir(folder)
    print(f'Saving {len(images)} photos from SpaceX')
    for image_order, image in enumerate(images):
        response = requests.get(image)
        response.raise_for_status()
        with open(f'spacex{image_order + 1}{os.path.splitext(image)[1]}', 'wb') as file:
            file.write(response.content)
            print(f'Photo {image_order} saved')


def fetch_spacex_last_launch():
    folder = create_dir()
    pictures = get_space_x_images_list()
    save_spacex_images(pictures, folder)


if __name__ == '__main__':
    fetch_spacex_last_launch()



