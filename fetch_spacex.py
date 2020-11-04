import requests
import os

urls = {
    'latest': 'https://api.spacexdata.com/v4/launches/latest',
    'all': 'https://api.spacexdata.com/v4/launches/'
}


def create_dir(dir_name):
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)
    return


def get_response(url):
    response = requests.get(url)
    response.raise_for_status()
    answer = response.json()
    return answer


def search_images_array_in_json(search_dict, search_key='flickr', pictures_found=[]):
    for key, value in search_dict.items():
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


def save_spacex_images(pictures_list):
    os.chdir('image')
    print(f'Saving {len(pictures_list)} photos from SpaceX')
    for picture_order, picture in enumerate(pictures_list):
        response = requests.get(picture)
        response.raise_for_status()
        with open(f'spacex{picture_order + 1}.{get_image_extension(picture)}', 'wb') as file:
            file.write(response.content)
            print(f'Photo {picture_order} saved')


def get_image_extension(url):
    return url.split('/')[-1].split('.')[-1]


def fetch_spacex_last_launch():
    create_dir('image')
    pictures = get_space_x_images_list()
    save_spacex_images(pictures)


if __name__ == '__main__':
    fetch_spacex_last_launch()
