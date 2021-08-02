import requests
import os
from pathlib import Path
import json


folder_path = Path(f'{os.getcwd()}/images')

with open('access-token yandex.txt', 'r', encoding='utf-8') as file:
    Token = file.read()


class YandexDisk:

    def __init__(self, token):
        self.token = token

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token)
        }

    def create_folder(self, folder_name):       # Функция для создания папки на я.диске
        url = 'https://cloud-api.yandex.net/v1/disk/resources'
        headers = self.get_headers()
        params = {"path": folder_name}
        response = requests.put(url, headers=headers, params=params)
        return response.json()

    def _get_upload_link(self, disk_file_path):     # Функция для получения ссылки для загрузки файлов
        upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        headers = self.get_headers()
        params = {"path": disk_file_path, "overwrite": "true"}
        response = requests.get(upload_url, headers=headers, params=params)
        return response.json()

    def upload_file_to_disk(self, ya_disk_file_path, filename):     # Функция для загрузки файлов из указанной папки
        href = self._get_upload_link(disk_file_path=ya_disk_file_path).get("href", "")
        response = requests.put(href, data=open(filename, 'rb'))
        if response.status_code == 201:
            print("Success")


if __name__ == '__main__':
    ya = YandexDisk(token=Token)
    ya.create_folder(folder_name='images')
    for file in os.listdir(folder_path):
        ya.upload_file_to_disk(ya_disk_file_path=f'images/{file}',
                               filename=folder_path/file)
