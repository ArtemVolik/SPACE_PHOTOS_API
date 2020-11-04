import requests
from fetch_spacex import get_image_extension, get_response, create_dir

def get_image_name(name):
    return ''.join(name.split('.')[:-1])


def fetch_habble(id):
    create_dir('image')
    links = get_response(f'http://hubblesite.org/api/v3/image/{id}')
    picture_link = links['image_files'][-1]['file_url']
    response = requests.get('http:'+picture_link)
    response.raise_for_status()
    with open(f'image/{id}.{get_image_extension(picture_link)}', 'wb') as file:
        file.write(response.content)


def fetch_habble_collection(habble_collection='holiday_cards'):
    collection = get_response(f'http://hubblesite.org/api/v3/images/{habble_collection}')
    collection_ids = []
    for photo in collection:
        collection_ids.append(photo['id'])
    print(f'Saving {len(collection_ids)} photos from Hubble')
    for number, id in enumerate(collection_ids):
        fetch_habble(id)
        print('Photo id:', id, 'saved.')


if __name__ == '__main__':
    fetch_habble_collection()