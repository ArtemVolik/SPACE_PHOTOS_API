import requests
import os

urls = {
    'latest': 'https://api.spacexdata.com/v4/launches/latest',
    'all': 'https://api.spacexdata.com/v4/launches/'
}


def create_dir():
    if not os.path.exists('image'):
        os.mkdir('image')
    return


def get_api_data(url):
    response = requests.get(url)
    response.raise_for_status()
    answer = response.json()
    return answer


def search_pictures(search_dict, search_key='flickr', pictures_found=[]):
    for key, value in search_dict.items():
        if key == search_key:
            pictures_found.append(value)
            return
        elif isinstance(value, dict):
            search_pictures(value, search_key, pictures_found)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    search_pictures(item, search_key, pictures_found)
    return pictures_found


def pictures_links():
    last_flight = get_api_data(urls['latest'])
    pictures_found = search_pictures(last_flight, search_key='flickr')[0]['original']
    if pictures_found:
        return pictures_found
    else:
        flights = get_api_data(urls['all'])
        for flight in flights:
            pictures_found_from_all = search_pictures(flight, search_key='flickr', pictures_found=[])[0]['original']
            if pictures_found_from_all:
                return pictures_found_from_all


def save_pictures(pictures_list):
    for picture_order, picture in enumerate(pictures_list):
        response = requests.get(picture)
        response.raise_for_status()
        with open(f'image/spacex{picture_order+1}.{extension(picture)}', 'wb') as file:
            file.write(response.content)


def extension(url):
    return url.split('/')[-1].split('.')[-1]


def fetch_spacex_last_launch():
    create_dir()
    pictures = pictures_links()
    save_pictures(pictures)


def fetch_habble(id):
    create_dir()
    links = get_api_data(f'http://hubblesite.org/api/v3/image/{id}')
    picture_link = links['image_files'][-1]['file_url']
    response = requests.get('http:'+picture_link)
    response.raise_for_status()
    with open(f'image/{id}.{extension(picture_link)}', 'wb') as file:
        file.write(response.content)



if __name__ == '__main__':
    fetch_habble(1)
    fetch_spacex_last_launch()

