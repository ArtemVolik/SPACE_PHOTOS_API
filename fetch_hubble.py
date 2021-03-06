import requests
import os
from space_api_func import get_response, create_dir


def fetch_habble(id, folder):
    links = get_response(f'http://hubblesite.org/api/v3/image/{id}')
    picture_link = links['image_files'][-1]['file_url']
    response = requests.get(f'http:{picture_link}')
    response.raise_for_status()
    with open(f'{folder}/{id}{os.path.splitext(picture_link)[1]}', 'wb') as file:
        file.write(response.content)


def fetch_habble_collection(folder, habble_collection='holiday_cards'):
    collection = get_response(f'http://hubblesite.org/api/v3/images/{habble_collection}')
    collection_ids = [photo['id'] for photo in collection]
    print(f'Saving {len(collection_ids)} photos from Hubble')
    for number, id in enumerate(collection_ids, 1):
        fetch_habble(id, folder)
        print('Photo id:', id, 'saved.')


if __name__ == '__main__':
    folder = create_dir()
    fetch_habble_collection(folder)
