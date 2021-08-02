import requests
import time
import os
import json


with open('access-token vk.txt', 'r', encoding='utf-8') as file:
    Token = file.read()
with open('user_id.txt', 'r', encoding='utf-8') as file:
    User_id = file.read()


class VkUser:
    url = 'https://api.vk.com/method/'

    def __init__(self, token, version):
        self.params = {
            'access_token': token,
            'v': version
        }

    def photos_get(self, user_id):      # Функция для получения всех фото профиля в формате .json
        photos_get_url = self.url + 'photos.get'
        photos_get_params = {
            'user_id': user_id,
            'album_id': 'profile',
            'extended': 1,
            'photo_sizes': 1,
        }
        res = requests.get(photos_get_url, params={**self.params, **photos_get_params})
        return res.json()


Alexander = VkUser(Token, '5.131')
json_photos = (Alexander.photos_get(User_id))


def create_json_file():     # Функция для созданя файла .json с отсортированной информацией
    list_photos = []
    for recording in json_photos['response']['items']:
        dict_recording = {}
        dict_recording['file_name'] = f'{recording["likes"]["count"]}.jpg'
        dict_recording['size'] = f'{recording["sizes"][-1]["type"]}'
        list_photos.append(dict_recording)
    with open('list_photos.json', 'w') as file_write:
        json.dump(list_photos, file_write)
    return


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
    return 'Success'


if __name__ == '__main__':
    create_json_file()
    print(upload_photos())
