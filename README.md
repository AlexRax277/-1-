##  Курсовой проект 
### Написание программы для резервного копирования фотографий с vk в облачное хранилище Яндекс.Диск.
## Задание:
### Нужно написать программу, которая будет:
1. Получать фотографии с профиля;
2. Сохранять фотографии максимального размера на Я.Диске;
3. Для имени фотографий использовать количество лайков;
4. Сохранять информацию по фотографиям в json-файл с результатами.
## Обязательные требования к программе:
1. Использовать REST API Я.Диска и ключ, полученный с полигона;
2. Для загруженных фотографий нужно создать свою папку;
3. Сохранять указанное количество фотографий(по умолчанию 5) наибольшего размера (ширина/высота в пикселях) на Я.Диске;
4. Сделать прогресс-бар или логирование для отслеживания процесса программы;
5. Код программы должен удовлетворять PEP8;
6. У программы должен быть свой отдельный репозиторий;
7. Все зависимости должны быть указаны в файле requiremеnts.txt.​
### Вермя на выполнение работы:
- плановое 336 ч;
- затраченное 72 ч.
### Рекомендации по запуску:
1. Получить token на сайте https://vk.com/dev и вписать его номер в файл с названием 'access-token vk'.
2. Вписать id аккаунта, с которого будут скачаны фото, в файл с названием 'user_id'.
3. Получить token на сайте https://yandex.ru/dev и вписать его номер в файл с названием 'access-token yandex'.
4. Запустить файл с названием 'first_part.py'.

*P.S.: Все номера token, id вписывать в том виде, в котором их предоставляет конкретный ресурс, в файлы с расширением .txt и соответствующими названиями.*