import requests
import os
import argparse


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