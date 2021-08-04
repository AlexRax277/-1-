import requests
import time
import os
import json
import logging
from pathlib import Path
from tqdm import tqdm


logging.basicConfig(filename='log.log', filemode='w', level=logging.INFO)
with open('access-token vk.txt', 'r', encoding='utf-8') as file:
    Token_Vk = file.read()
with open('user_id.txt', 'r', encoding='utf-8') as file:
    User_id = file.read()
with open('access-token yandex.txt', 'r', encoding='utf-8') as file:
    Token_Ya = file.read()


class VkUser:
    url = 'https://api.vk.com/method/'

    def __init__(self, token, version):
        self.params = {
            'access_token': token,
            'v': version
        }

    def photos_get(self, user_id, count_photo):      # Функция для получения всех фото профиля в формате .json
        photos_get_url = self.url + 'photos.get'
        photos_get_params = {
            'user_id': user_id,
            'album_id': 'profile',
            'extended': 1,
            'photo_sizes': 1,
            'count': count_photo
        }
        res = requests.get(photos_get_url, params={**self.params, **photos_get_params})
        return res.json()


Alexander = VkUser(Token_Vk, '5.131')
json_photos = (Alexander.photos_get(User_id, 5))


def create_json_file():     # Функция для созданя файла .json с отсортированной информацией
    list_photos = []
    for recording in json_photos['response']['items']:
        dict_recording = {}
        dict_recording['file_name'] = f'{recording["likes"]["count"]}.jpg'
        dict_recording['size'] = f'{recording["sizes"][-1]["type"]}'
        list_photos.append(dict_recording)
    with open('list_photos.json', 'w') as file_write:
        json.dump(list_photos, file_write)
    return f'Файл list_photos.json создан.'


def upload_photos():        # функция для скачивания всех фото профиля на жесткий диск
    dict_photos = {}
    for photos in json_photos['response']['items']:
        dict_photos[photos['likes']['count']] = photos['sizes'][-1]
        time.sleep(1)
    if not os.path.exists('images'):        # Создаем папку с названием 'images', если такой нет
        os.mkdir('images')
    for photo in list(dict_photos.items()):
        file_name = str(f'{photo[0]}.jpg')
        file_url = photo[1]['url']
        r = requests.get(file_url)
        open('images/%s' % file_name, 'wb').write(r.content)
    return f'Фотографии добавлены в директорию images/.'


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
        return f'Папка с именем {folder_name} создана на я.диске!'

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
            pass
        else:
            print('Ошибка! Что-то пошло не так')
            logging.error('Error!')


if __name__ == '__main__':
    print(create_json_file())
    logging.info('Success - .json-file was added!')
    print(upload_photos())
    logging.info('Success - photos uploaded!')
    folder_path = Path(f'{os.getcwd()}/images')
    ya = YandexDisk(token=Token_Ya)
    print(ya.create_folder(folder_name='images'))
    logging.info('Success - folder on ya.disk was created!')
    with tqdm(total=100) as progress_bar:
        for file in os.listdir(folder_path):
            ya.upload_file_to_disk(ya_disk_file_path=f'images/{file}',
                                   filename=folder_path / file)
            progress_bar.update(20)
    print('Все фото загружены на я.диск!')
    logging.info('Success - photos uploaded on ya.disk!')
