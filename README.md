# Домашняя работа 2 по ВВОТ 
## Сделал Юсупов Марсель 11-002


### Для запуска необходимо 

1. `https://github.com/MarselYsup/vvot47-2.git`
2. `cd vvot47-2`
2. `pip install -r requirements.txt`
3. `python cloudphoto.py [-h] {upload,download,list,delete,mksite,init}`


### Важно!

1. Необходимо иметь конфиг файл в по пути - ***.config/cloudphoto/cloudphotorc***
2. В конфиг файле должно быть оформлено 
    ```
    bucket = INPUT_BUCKET_NAME 
    aws_access_key_id = INPUT_AWS_ACCESS_KEY_ID 
    aws_secret_access_key = INPUT_AWS_SECRET_ACCESS_KEY 
    region = ru-central1 
    endpoint_url = https://storage.yandexcloud.net
    ```    
### Структура проекта

1. `/resources` - Директория с файлами для создания веб-сайта
2. `/task` - Директория с файлами для взаимодействия с облаком 
3. `cloudphoto.py` - основной файл для запуска скрипта
4. `requirements.txt` - основные зависимости необходимые для работы